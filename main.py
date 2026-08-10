import os
import requests
import yfinance as yf
import google.generativeai as genai

# Şifreleri GitHub Kasasından Otomatik Çekiyoruz
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def mesaj_gonder(metin):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    bilgi = {"chat_id": CHAT_ID, "text": metin, "parse_mode": "Markdown"}
    requests.post(url, data=bilgi)

genai.configure(api_key=GEMINI_API_KEY)
ai_model = genai.GenerativeModel("gemini-1.5-flash")

sanal_portfoyler = {
    "1. Sanal Portföy (Hızlı Büyüme)": [
        {"kod": "ATATP.IS", "isim": "ATATP", "maliyet": 80.0},
        {"kod": "YEOTK.IS", "isim": "YEOTK", "maliyet": 200.0},
        {"kod": "ARDYZ.IS", "isim": "ARDYZ", "maliyet": 45.0},
        {"kod": "SDTTR.IS", "isim": "SDTTR", "maliyet": 280.0},
        {"kod": "CWENE.IS", "isim": "CWENE", "maliyet": 190.0}
    ],
    "2. Sanal Portföy (Çekirdek Devler)": [
        {"kod": "ASELS.IS", "isim": "ASELSN", "maliyet": 65.0},
        {"kod": "BIMAS.IS", "isim": "BİMAS",  "maliyet": 480.0},
        {"kod": "MPARK.IS", "isim": "MPARK",  "maliyet": 300.0},
        {"kod": "LOGO.IS",  "isim": "LOGO",   "maliyet": 100.0},
        {"kod": "TUPRS.IS", "isim": "TUPRS",  "maliyet": 160.0}
    ]
}

analiz_verisi = "Aşağıda yatırımcının sanal portföyündeki hisselerin güncel fiyat ve temel rasyo verileri yer almaktadır:\n\n"

for portfoy_adi, hisseler in sanal_portfoyler.items():
    analiz_verisi += f"--- {portfoy_adi} ---\n"
    for h in hisseler:
        try:
            ticker = yf.Ticker(h["kod"])
            fiyat = ticker.history(period="1d")["Close"].iloc[-1]
            fk = ticker.info.get('trailingPE', 'N/A')
            pddd = ticker.info.get('priceToBook', 'N/A')
            getiri = ((fiyat - h["maliyet"]) / h["maliyet"]) * 100
            analiz_verisi += f"• {h['isim']}: Fiyat: {fiyat:.2f} TL | Maliyet: {h['maliyet']} TL | Getiri: %{getiri:.1f} | F/K: {fk} | PD/DD: {pddd}\n"
        except:
            analiz_verisi += f"• {h['isim']}: Veri çekilemedi.\n"

istem = f"""
Sen BIST Katılım Endeksi ve hisse senetleri konusunda uzman kıdemli bir Finansal Analist ve Yatırım Uzmanısın.
Aşağıdaki portföy verilerini incele:

{analiz_verisi}

Lütfen yatırımcıya şu 3 başlıkta kısa, net ve profesyonel bir analiz raporu sun:
1. **Genel Portföy Değerlendirmesi:** Hangi portföy güçlü duruyor?
2. **Değerleme/Çarpan Yorumu:** F/K ve PD/DD açısından ucuz veya primli hisseler?
3. **Stratejik Öneri:** Portföyler arası rotasyon veya kâr realizasyonu tavsiyesi?
"""

response = ai_model.generate_content(istem)
mesaj_gonder(f"🤖 *GÜNLÜK OTOMATİK FİNANSAL ANALİST RAPORU*\n\n{response.text}")

import xml.etree.ElementTree as ET

def kap_bilanco_kontrol():
    # KAP'ın genel RSS bildirim akışını kontrol eder
    kap_rss_url = "https://www.kap.org.tr/tr/rss"
    try:
        response = requests.get(kap_rss_url, timeout=10)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            
            # Portföyümüzdeki hisse kodları
            takipteki_hisseler = ["ATATP", "YEOTK", "ARDYZ", "SDTTR", "CWENE", "ASELS", "BIMAS", "MPARK", "LOGO", "TUPRS"]
            
            for item in root.findall('.//item'):
                baslik = item.find('title').text if item.find('title') is not None else ""
                link = item.find('link').text if item.find('link') is not None else ""
                
                # Eğer bildirim takip ettiğimiz hisselerden biriyle ilgiliyse ve Finansal Rapor içeriyorsa
                for hisse in takipteki_hisseler:
                    if hisse in baslik and ("Finansal Rapor" in baslik or "Bilanço" in baslik):
                        
                        # Gemini AI'a Bilanço Yorumlatma
                        kap_istem = f"""
                        Aşağıdaki KAP haber başlığı takip ettiğimiz bir şirkete aittir:
                        Başlık: {baslik}
                        Link: {link}
                        
                        Bu bildirim için yatırımcıya Telegram formatında kısa, heyecan verici bir Bilanço Açıklandı Uyarısı hazırla.
                        """
                        ai_kap_yaniti = ai_model.generate_content(kap_istem)
                        mesaj_gonder(f"🚨 *YENİ KAP BİLANÇO BİLDİRİMİ*\n\n{ai_kap_yaniti.text}\n\n🔗 [KAP Bildirimi Detayı]({link})")
    except Exception as e:
        print(f"KAP kontrolü sırasında hata: {e}")

# Kodun en sonuna KAP kontrol fonksiyonunu çağırıyoruz:
kap_bilanco_kontrol()
