import streamlit as st
import yfinance as yf
import pandas as pd
import json
import os
import requests

st.set_page_config(page_title="Katılım Finans Yönetimi", page_icon="🕌", layout="wide")
st.title("🕌 Katılım Portföy & Canlı Fiyat Takip Merkezi")

JSON_DOSYASI = "portfoyler.json"

# BIST Katılım Endeksi Örnek Hisse Havuzu
KATILIM_HISSE_HAVUZU = sorted([
    "AGROT", "ALARK", "ARDYZ", "ASELS", "ASTOR", "ATATP", "BIMAS", "BRSAN", 
    "BUCIM", "CIMSA", "CWENE", "DOAS", "EGEEN", "EKGYO", "ENJSA", "EREGL", 
    "ESCOM", "FONET", "FROTO", "GENIL", "GESAN", "GLRMK", "HEKTS", "KCAER", 
    "KONTR", "KORDS", "KOZAL", "KRDMD", "KTLEV", "LOGO", "MAVI", "MPARK", 
    "OTKAR", "OYAKC", "PASEU", "PETKM", "PGSUS", "RGYAS", "SDTTR", "SISE", 
    "SMRTG", "SOKM", "TAVHL", "TCELL", "THYAO", "TKFEN", "TOASO", "TTKOM", 
    "TUPRS", "ULKER", "VESBE", "YEOTK", "YYLGD"
])

# TEFAS Katılım Fonları Havuzu
KATILIM_FON_HAVUZU = ["KFA", "MPS", "ZKP", "RBK", "HKH", "KCS", "TKL"]

def portfoyleri_yukle():
    if os.path.exists(JSON_DOSYASI):
        try:
            with open(JSON_DOSYASI, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data:
                    return data
        except Exception:
            pass
    return {"Ana Katılım Portföyü": []}

def portfoyleri_kaydet(veri):
    with open(JSON_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)

portfoyler = portfoyleri_yukle()

# BIST HISSELERI İÇİN CANLI / SON AN FİYATI ÇEKME
@st.cache_data(ttl=60)  # 1 dakikada bir canlı günceller
def bist_fiyati_getir(hisse_kodu):
    try:
        kod = hisse_kodu.upper().strip()
        if not kod.endswith(".IS"):
            kod = f"{kod}.IS"
        t = yf.Ticker(kod)
        
        # Önce anlık hızlı fiyatı dene
        anlik_fiyat = t.fast_info.get('lastPrice', None)
        if anlik_fiyat and not pd.isna(anlik_fiyat):
            return float(anlik_fiyat)
            
        # Başarısız olursa son 1 günlük son mum fiyatını çek
        hist = t.history(period="1d", interval="1m")
        if not hist.empty and 'Close' in hist.columns:
            return float(hist['Close'].iloc[-1])
            
        # O da olmazsa 5 günlük kapanışı al
        hist5 = t.history(period="5d")
        if not hist5.empty and 'Close' in hist5.columns:
            return float(hist5['Close'].iloc[-1])
    except Exception:
        pass
    return None

# TEFAS FONLARI İÇİN SON EN GÜNCEL FİYATI ÇEKME
@st.cache_data(ttl=300)  # 5 dakikada bir önbellekler
def tefas_fon_fiyati_getir(fon_kodu):
    try:
        url = "https://www.tefas.gov.tr/api/DB/BindHistoryInfo"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "X-Requested-With": "XMLHttpRequest"
        }
        payload = {"FONTIP": "YAT", "FONKODU": fon_kodu.upper()}
        res = requests.post(url, data=payload, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if "data" in data and len(data["data"]) > 0:
                son_fiyat = data["data"][0]["BİRİM FİYAT"]
                return float(str(son_fiyat).replace(",", "."))
    except Exception:
        pass
    return None

def genel_fiyat_getir(v_kodu, v_tipi):
    if "Fon" in v_tipi or v_kodu in KATILIM_FON_HAVUZU:
        fiyat = tefas_fon_fiyati_getir(v_kodu)
        if fiyat is not None:
            return fiyat, "TEFAS Resmi Fiyatı"
    
    # Hisse veya Genel Sorgu
    fiyat = bist_fiyati_getir(v_kodu)
    if fiyat is not None:
        return fiyat, "BIST Anlık/Son Kapanış"
    
    return None, "Veri Alınamadı"

# YAN MENÜ
st.sidebar.header("⚙️ Portföy Yönetim Paneli")

if st.sidebar.button("🚀 Örnek Katılım Portföyünü Yükle"):
    ornek_portfoy = [
        {"kod": "ASELS.IS", "isim": "ASELS", "maliyet": 65.0, "stop_loss": -0.10, "tp1": 0.30, "tip": "Katılım Hissesi"},
        {"kod": "BIMAS.IS", "isim": "BIMAS", "maliyet": 480.0, "stop_loss": -0.08, "tp1": 0.25, "tip": "Katılım Hissesi"},
        {"kod": "ATATP.IS", "isim": "ATATP", "maliyet": 80.0, "stop_loss": -0.12, "tp1": 0.40, "tip": "Katılım Hissesi"},
        {"kod": "KFA",      "isim": "KFA",   "maliyet": 2.50, "stop_loss": -0.05, "tp1": 0.20, "tip": "Katılım Fonu"},
        {"kod": "ZKP",      "isim": "ZKP",   "maliyet": 1.80, "stop_loss": -0.05, "tp1": 0.20, "tip": "Katılım Fonu"}
    ]
    portfoyler["Ana Katılım Portföyü"] = ornek_portfoy
    portfoyleri_kaydet(portfoyler)
    st.sidebar.success("Örnek portföy başarıyla yüklendi!")
    st.rerun()

st.sidebar.markdown("---")

# Yeni Portföy Ekleme
yeni_p = st.sidebar.text_input("Yeni Portföy Adı:")
if st.sidebar.button("➕ Portföy Oluştur"):
    if yeni_p and yeni_p not in portfoyler:
        portfoyler[yeni_p] = []
        portfoyleri_kaydet(portfoyler)
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("📌 Varlık Ekle")
secilen_p = st.sidebar.selectbox("Hedef Portföy:", list(portfoyler.keys()))
v_tipi = st.sidebar.radio("Varlık Tipi:", ["Katılım Hissesi", "Katılım Fonu", "Manuel Kod Gir"])

if v_tipi == "Katılım Hissesi":
    varlik_kodu = st.sidebar.selectbox("Hisse Seçin:", KATILIM_HISSE_HAVUZU)
elif v_tipi == "Katılım Fonu":
    varlik_kodu = st.sidebar.selectbox("Fon Seçin:", KATILIM_FON_HAVUZU)
else:
    varlik_kodu = st.sidebar.text_input("Hisse/Fon Kodu Girin:").upper()

maliyet = st.sidebar.number_input("Alış Maliyeti (TL):", min_value=0.001, value=100.0, step=1.0, format="%.3f")
stop_l = st.sidebar.number_input("Stop-Loss Limiti (%):", min_value=-50.0, max_value=0.0, value=-10.0)
tp_l = st.sidebar.number_input("Kâr Alma Limiti (%):", min_value=0.0, max_value=500.0, value=30.0)

if st.sidebar.button("💾 Portföye Ekle"):
    if varlik_kodu:
        kod_format = f"{varlik_kodu}.IS" if v_tipi == "Katılım Hissesi" else varlik_kodu
        yeni_v = {
            "kod": kod_format,
            "isim": varlik_kodu,
            "maliyet": maliyet,
            "stop_loss": stop_l / 100,
            "tp1": tp_l / 100,
            "tip": v_tipi
        }
        if secilen_p in portfoyler:
            portfoyler[secilen_p].append(yeni_v)
            portfoyleri_kaydet(portfoyler)
            st.sidebar.success(f"{varlik_kodu} eklendi!")
            st.rerun()

# ANA EKRAN
if portfoyler:
    sekmeler = st.tabs(list(portfoyler.keys()))
    for i, (p_adi, varliklar) in enumerate(portfoyler.items()):
        with sekmeler[i]:
            c1, c2 = st.columns([4, 1])
            c1.subheader(f"📂 {p_adi}")
            if c2.button("🗑️ Portföyü Sil", key=f"del_{p_adi}"):
                del portfoyler[p_adi]
                portfoyleri_kaydet(portfoyler)
                st.rerun()

            if not varliklar:
                st.warning("⚠️ Bu portföy şu an boş. Sol menüden hisse veya fon ekleyebilirsiniz.")
            else:
                tablo = []
                for v in varliklar:
                    fiyat, veri_durumu = genel_fiyat_getir(v["isim"], v.get("tip", "Hisse"))
                    if fiyat:
                        m = v["maliyet"]
                        g = ((fiyat - m) / m) * 100
                        tablo.append({
                            "Tip": v.get("tip", "Hisse"),
                            "Kod": v["isim"],
                            "Maliyet (TL)": m,
                            "Son Fiyat (TL)": round(fiyat, 3 if "Fon" in v.get("tip","") else 2),
                            "Kâr/Zarar (%)": round(g, 2),
                            "Stop Limit (%)": v["stop_loss"] * 100,
                            "Kâr Alma (%)": v["tp1"] * 100,
                            "Veri Kaynağı": veri_durumu
                        })
                    else:
                        tablo.append({
                            "Tip": v.get("tip", "Hisse"),
                            "Kod": v["isim"],
                            "Maliyet (TL)": v["maliyet"],
                            "Son Fiyat (TL)": "Veri Bekleniyor",
                            "Kâr/Zarar (%)": 0,
                            "Stop Limit (%)": v["stop_loss"] * 100,
                            "Kâr Alma (%)": v["tp1"] * 100,
                            "Veri Kaynağı": "Alınamadı"
                        })
                df = pd.DataFrame(tablo)
                st.dataframe(df, use_container_width=True)
                if not df.empty and "Kâr/Zarar (%)" in df.columns:
                    st.bar_chart(df.set_index("Kod")["Kâr/Zarar (%)"])
