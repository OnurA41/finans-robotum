import os
import json
import requests
import yfinance as yf
import google.generativeai as genai

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def mesaj_gonder(metin):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    bilgi = {"chat_id": CHAT_ID, "text": metin, "parse_mode": "Markdown"}
    requests.post(url, data=bilgi)

genai.configure(api_key=GEMINI_API_KEY)
ai_model = genai.GenerativeModel("gemini-1.5-flash")

# DİNAMİK PORTFÖY VERİSİNİ DOSYADAN OKU
def portfoyleri_yukle():
    if os.path.exists("portfoyler.json"):
        with open("portfoyler.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

sanal_portfoyler = portfoyleri_yukle()

if not sanal_portfoyler or all(len(v) == 0 for v in sanal_portfoyler.values()):
    mesaj_gonder("ℹ️ *Finans Nöbetçisi:* Şu an takip edilecek dinamik bir portföy bulunamadı. Web arayüzünden hisse/fon ekleyebilirsiniz.")
else:
    analiz_verisi = "Aşağıda yatırımcının oluşturduğu dinamik portföyler ve güncel veriler yer almaktadır:\n\n"

    for portfoy_adi, varliklar in sanal_portfoyler.items():
        if not varliklar:
            continue
        analiz_verisi += f"--- {portfoy_adi} ---\n"
        for v in varliklar:
            try:
                ticker = yf.Ticker(v["kod"])
                hist = ticker.history(period="5d")
                if not hist.empty:
                    fiyat = float(hist["Close"].iloc[-1])
                    maliyet = v["maliyet"]
                    getiri = ((fiyat - maliyet) / maliyet) * 100
                    
                    # Stop / TP Kontrolleri
                    stop_limit = v.get("stop_loss", -0.10)
                    tp_limit = v.get("tp1", 0.30)
                    
                    if (getiri / 100) <= stop_limit:
                        mesaj_gonder(f"🚨 *STOP-LOSS UYARISI [{portfoy_adi}]*\n{v['isim']} fiyatı {fiyat:.2f} TL'ye düştü! (Getiri: %{getiri:.1f})")
                    elif (getiri / 100) >= tp_limit:
                        mesaj_gonder(f"🎯 *KÂR ALMA UYARISI [{portfoy_adi}]*\n{v['isim']} fiyatı {fiyat:.2f} TL'ye yükseldi! (Getiri: +%{getiri:.1f})")

                    analiz_verisi += f"• {v['isim']} ({v.get('tip','Hisse')}): Fiyat: {fiyat:.2f} TL | Maliyet: {maliyet} TL | Getiri: %{getiri:.1f}\n"
            except Exception as e:
                analiz_verisi += f"• {v['isim']}: Veri okunamadı.\n"

    istem = f"""
    Sen BIST Katılım Endeksi ve TEFAS Katılım Fonları konusunda uzman kıdemli bir Finansal Analist ve Yatırım Uzmanısın.
    Aşağıdaki dinamik portföy verilerini incele:

    {analiz_verisi}

    Lütfen yatırımcıya şu 3 başlıkta kısa, net ve profesyonel bir analiz raporu sun (Telegram formatında, bol emojili):
    1. **Genel Portföy Değerlendirmesi:** Portföylerin genel durumu ve kârlılık seyri?
    2. **Risk & Fırsat Analizi:** Öne çıkan veya risk teşkil eden varlıklar?
    3. **Stratejik Tavsiye:** Portföy dengelenmesi veya Katılım prensiplerine uygun rotasyon önerileri?
    """

    response = ai_model.generate_content(istem)
    mesaj_gonder(f"🤖 *DİNAMİK KATILIM PORTFÖY ANALİZ RAPORU*\n\n{response.text}")
