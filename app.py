import streamlit as st
import yfinance as yf
import pandas as pd
import json
import os

st.set_page_config(page_title="Katılım Finans Yönetimi", page_icon="🕌", layout="wide")
st.title("🕌 Katılım Portföy & Analiz Merkezi")

JSON_DOSYASI = "portfoyler.json"

# Portföy Verilerini Yükle
def portfoyleri_yukle():
    if os.path.exists(JSON_DOSYASI):
        with open(JSON_DOSYASI, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"Varsayılan Portföy": []}

# Portföy Verilerini Kaydet
def portfoyleri_kaydet(veri):
    with open(JSON_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)

portfoyler = portfoyleri_yukle()

@st.cache_data(ttl=300)
def hisse_fiyati_getir(hisse_kodu):
    try:
        kod = hisse_kodu.upper().strip()
        if not kod.endswith(".IS") and not kod.isalpha() and len(kod) <= 5:
            kod = f"{kod}.IS"
        elif not kod.endswith(".IS") and len(kod) == 5:
            kod = f"{kod}.IS"
            
        t = yf.Ticker(kod)
        hist = t.history(period="5d")
        if not hist.empty and 'Close' in hist.columns:
            return float(hist['Close'].iloc[-1])
    except Exception:
        pass
    return None

# YAN MENÜ: DİNAMİK PORTFÖY YÖNETİMİ
st.sidebar.header("⚙️ Portföy Yönetim Paneli")

# 1. Yeni Portföy Oluşturma
yeni_portfoy_adi = st.sidebar.text_input("Yeni Portföy Adı Girin:")
if st.sidebar.button("➕ Yeni Portföy Ekle"):
    if yeni_portfoy_adi and yeni_portfoy_adi not in portfoyler:
        portfoyler[yeni_portfoy_adi] = []
        portfoyleri_kaydet(portfoyler)
        st.sidebar.success(f"'{yeni_portfoy_adi}' oluşturuldu!")
        st.rerun()

st.sidebar.markdown("---")

# 2. Portföye Varlık (Hisse/Fon) Ekleme
st.sidebar.subheader("📌 Portföye Varlık Ekle")
secilen_portfoy = st.sidebar.selectbox("Portföy Seçin:", list(portfoyler.keys()))

varlik_tipi = st.sidebar.radio("Varlık Tipi:", ["Hisse (BIST)", "Katılım Fonu (TEFAS)"])
varlik_kodu = st.sidebar.text_input("Hisse/Fon Kodu (Örn: THYAO, KFA, ZKP):").upper()
maliyet_fiyati = st.sidebar.number_input("Alış Maliyeti (TL):", min_value=0.0, value=10.0, step=0.1)
stop_loss_orani = st.sidebar.number_input("Stop-Loss Limiti (%):", min_value=-50.0, max_value=0.0, value=-10.0)
tp_orani = st.sidebar.number_input("Kâr Alma Limiti (%):", min_value=0.0, max_value=500.0, value=30.0)

if st.sidebar.button("💾 Varlığı Portföye Kaydet"):
    if varlik_kodu:
        yeni_varlik = {
            "kod": f"{varlik_kodu}.IS" if varlik_tipi == "Hisse (BIST)" and not varlik_kodu.endswith(".IS") else varlik_kodu,
            "isim": varlik_kodu,
            "maliyet": maliyet_fiyati,
            "stop_loss": stop_loss_orani / 100,
            "tp1": tp_orani / 100,
            "tip": varlik_tipi
        }
        portfoyler[secilen_portfoy].append(yeni_varlik)
        portfoyleri_kaydet(portfoyler)
        st.sidebar.success(f"{varlik_kodu} -> {secilen_portfoy} portföyüne eklendi!")
        st.rerun()

# ANA EKRAN: PORTFÖYLERİN CANLI YÖNETİMİ
if portfoyler:
    sekmeler = st.tabs(list(portfoyler.keys()))
    
    for i, (p_adi, varliklar) in enumerate(portfoyler.items()):
        with sekmeler[i]:
            col_baslik, col_sil = st.columns([4, 1])
            col_baslik.subheader(f"📂 {p_adi}")
            
            if col_sil.button("🗑️ Portföyü Sil", key=f"sil_{p_adi}"):
                del portfoyler[p_adi]
                portfoyleri_kaydet(portfoyler)
                st.rerun()
                
            if not varliklar:
                st.info("Bu portföyde henüz eklenmiş bir hisse veya fon bulunmuyor. Sol menüden ekleyebilirsiniz.")
            else:
                tablo_verisi = []
                for idx, v in enumerate(varliklar):
                    fiyat = hisse_fiyati_getir(v["kod"])
                    if fiyat:
                        maliyet = v["maliyet"]
                        getiri = ((fiyat - maliyet) / maliyet) * 100
                        tablo_verisi.append({
                            "Tip": v.get("tip", "Hisse"),
                            "Kod": v["isim"],
                            "Maliyet (TL)": maliyet,
                            "Güncel Fiyat (TL)": round(fiyat, 2),
                            "Kâr/Zarar (%)": round(getiri, 2),
                            "Stop Limit (%)": v["stop_loss"] * 100,
                            "Kâr Alma (%)": v["tp1"] * 100
                        })
                    else:
                        tablo_verisi.append({
                            "Tip": v.get("tip", "Hisse"),
                            "Kod": v["isim"],
                            "Maliyet (TL)": v["maliyet"],
                            "Güncel Fiyat (TL)": "Veri Bekleniyor",
                            "Kâr/Zarar (%)": 0,
                            "Stop Limit (%)": v["stop_loss"] * 100,
                            "Kâr Alma (%)": v["tp1"] * 100
                        })
                
                df = pd.DataFrame(tablo_verisi)
                st.dataframe(df, use_container_width=True)
                
                # Performans Grafiği
                if not df.empty and "Kâr/Zarar (%)" in df.columns:
                    st.bar_chart(df.set_index("Kod")["Kâr/Zarar (%)"])
