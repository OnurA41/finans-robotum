import os
import json
import datetime
import requests
import yfinance as yf
import google.generativeai as genai
import logging
import sys

from src.logging_config import configure_logging
from src.config import Config, ConfigError
from src.exceptions import APITimeoutError, DataUnavailableError

configure_logging()
logger = logging.getLogger(__name__)

try:
    config = Config()
except ConfigError as e:
    logger.error("Configuration error: %s", e)
    sys.exit(1)

TELEGRAM_TOKEN = config.TELEGRAM_TOKEN
CHAT_ID = config.CHAT_ID
GEMINI_API_KEY = config.GEMINI_API_KEY

PORTFOY_DOSYASI = "portfoyler.json"
GECMIS_DOSYASI = "gecmis.json"


def mesaj_gonder(metin):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    bilgi = {"chat_id": CHAT_ID, "text": metin, "parse_mode": "Markdown"}
    try:
        res = requests.post(url, data=bilgi, timeout=5)
        if res.status_code != 200:
            logger.warning("Telegram API returned status %s for message", res.status_code)
    except requests.exceptions.Timeout:
        logger.warning("Timeout while sending Telegram message")
    except Exception as e:
        logger.exception("Failed to send Telegram message: %s", e)


genai.configure(api_key=GEMINI_API_KEY)
ai_model = genai.GenerativeModel("gemini-1.5-flash")


def portfoyleri_yukle():
    if os.path.exists(PORTFOY_DOSYASI):
        with open(PORTFOY_DOSYASI, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Eski format (liste) ile kaydedilmiş portföyleri yeni formata taşı
        donusmus = {}
        for ad, icerik in data.items():
            if isinstance(icerik, list):
                for v in icerik:
                    v.setdefault("miktar", 1)
                donusmus[ad] = {"nakit": 100000.0, "varliklar": icerik}
            else:
                icerik.setdefault("nakit", 100000.0)
                icerik.setdefault("varliklar", [])
                donusmus[ad] = icerik
        return donusmus
    return {}


def gecmisi_yukle():
    if os.path.exists(GECMIS_DOSYASI):
        try:
            with open(GECMIS_DOSYASI, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.exception("Failed to load history %s: %s", GECMIS_DOSYASI, e)
    return {}


def gecmisi_kaydet(veri):
    with open(GECMIS_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)


sanal_portfoyler = portfoyleri_yukle()
gecmis = gecmisi_yukle()
bugun = datetime.date.today().isoformat()

if not sanal_portfoyler or all(len(v.get("varliklar", [])) == 0 for v in sanal_portfoyler.values()):
    mesaj_gonder("ℹ️ *Finans Nöbetçisi:* Şu an takip edilecek dinamik bir portföy bulunamadı. Web arayüzünden hisse/fon ekleyebilirsiniz.")
else:
    analiz_verisi = "Aşağıda yatırımcının oluşturduğu dinamik portföyler ve güncel veriler yer almaktadır:\n\n"

    for portfoy_adi, icerik in sanal_portfoyler.items():
        varliklar = icerik.get("varliklar", [])
        if not varliklar:
            continue

        toplam_deger = icerik.get("nakit", 0)
        analiz_verisi += f"--- {portfoy_adi} (Sanal nakit: {icerik.get('nakit', 0):.2f} TL) ---\n"

        for v in varliklar:
            try:
                ticker = yf.Ticker(v["kod"])
                hist = ticker.history(period="5d")
                if not hist.empty:
                    fiyat = float(hist["Close"].iloc[-1])
                    maliyet = v["maliyet"]
                    miktar_v = v.get("miktar", 1)
                    getiri = ((fiyat - maliyet) / maliyet) * 100
                    toplam_deger += fiyat * miktar_v

                    stop_limit = v.get("stop_loss", -0.10)
                    tp_limit = v.get("tp1", 0.30)
                    if (getiri / 100) <= stop_limit:
                        mesaj_gonder(f"🚨 *STOP-LOSS UYARISI [{portfoy_adi}]*\n{v['isim']} fiyatı {fiyat:.2f} TL'ye düştü! (Getiri: %{getiri:.1f})")
                    elif (getiri / 100) >= tp_limit:
                        mesaj_gonder(f"🎯 *KÂR ALMA UYARISI [{portfoy_adi}]*\n{v['isim']} fiyatı {fiyat:.2f} TL'ye yükseldi! (Getiri: +%{getiri:.1f})")

                    analiz_verisi += f"• {v['isim']} ({v.get('tip','Hisse')}) x{miktar_v}: Fiyat: {fiyat:.2f} TL | Maliyet: {maliyet} TL | Getiri: %{getiri:.1f}\n"
            except requests.exceptions.Timeout:
                logger.warning("Timeout while fetching data for %s", v.get('isim'))
                analiz_verisi += f"• {v['isim']}: Veri okunamadı (timeout).\n"
            except Exception as e:
                logger.exception("Error fetching data for %s: %s", v.get('isim', 'unknown'), e)
                analiz_verisi += f"• {v['isim']}: Veri okunamadı.\n"

        # Bugünün toplam portföy değerini geçmişe kaydet (raporlama için gerekli)
        gecmis.setdefault(portfoy_adi, [])
        gecmis[portfoy_adi] = [g for g in gecmis[portfoy_adi] if g["tarih"] != bugun]
        gecmis[portfoy_adi].append({"tarih": bugun, "deger": round(toplam_deger, 2)})

    gecmisi_kaydet(gecmis)

    istem = f"""
Sen BIST Katılım Endeksi ve TEFAS Katılım Fonları konusunda uzman kıdemli bir Finansal Analist ve Yatırım Uzmanısın.
Aşağıdaki dinamik portföy verilerini incele:

{analiz_verisi}

Lütfen yatırımcıya şu 3 başlıkta kısa, net ve profesyonel bir analiz raporu sun (Telegram formatında, bol emojili):
1. **Genel Portföy Değerlendirmesi:** Portföylerin genel durumu ve kârlılık seyri?
2. **Risk & Fırsat Analizi:** Öne çıkan veya risk teşkil eden varlıklar?
3. **Stratejik Tavsiye:** Portföy dengelenmesi veya Katılım prensiplerine uygun rotasyon önerileri?

Not: Bu sanal bir portföydür, gerçek para ile işlem yapılmamaktadır. Önerilerini bu bağlamda, kesin talimat değil değerlendirme olarak sun.
"""
    try:
        response = ai_model.generate_content(istem)
        mesaj_gonder(f"🤖 *DİNAMİK KATILIM PORTFÖY ANALİZ RAPORU*\n\n{response.text}")
    except Exception as e:
        logger.exception("AI generation failed: %s", e)
        mesaj_gonder("🤖 *DİNAMİK KATILIM PORTFÖY ANALİZ RAPORU*")
