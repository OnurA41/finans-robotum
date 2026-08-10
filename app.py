import streamlit as st
import yfinance as yf
import pandas as pd

# Sayfa Tasarımı
st.set_page_config(page_title="Kişisel Finans Merkezim", page_icon="📈", layout="wide")
st.title("📈 Kişisel Finans ve Portföy Takip Paneli")

# Sanal Portföy Tanımları
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

# Yahoo Engeline Takılmamak İçin Veri Önbellekleme (5 Dakikada Bir Yenilenir)
@st.cache_data(ttl=300)
def hisse_fiyati_getir(hisse_kodu):
    try:
        t = yf.Ticker(hisse_kodu)
        hist = t.history(period="5d")
        if not hist.empty and 'Close' in hist.columns:
            return float(hist['Close'].iloc[-1])
    except Exception:
        pass
    return None

sekmeler = st.tabs(list(sanal_portfoyler.keys()))

for i, (portfoy_adi, hisseler) in enumerate(sanal_portfoyler.items()):
    with sekmeler[i]:
        st.subheader(f"📊 {portfoy_adi}")
        
        veri_listesi = []
        for h in hisseler:
            fiyat = hisse_fiyati_getir(h["kod"])
            
            if fiyat is not None:
                maliyet = h["maliyet"]
                kar_zarar_yuzde = ((fiyat - maliyet) / maliyet) * 100
                
                veri_listesi.append({
                    "Hisse": h["isim"],
                    "Güncel Fiyat (TL)": round(fiyat, 2),
                    "Maliyet (TL)": maliyet,
                    "Kar/Zarar (%)": round(kar_zarar_yuzde, 2)
                })
            else:
                st.warning(f"⚠️ {h['isim']} verisi şu an alınamıyor (Yahoo geçici sınır koydu).")
                
        df = pd.DataFrame(veri_listesi)
        
        if not df.empty:
            col1, col2 = st.columns(2)
            toplam_getiri = df["Kar/Zarar (%)"].mean()
            col1.metric("Portföy Ortalama Getirisi", f"%{toplam_getiri:.2f}")
            col2.metric("Takip Edilen Hisse Sayısı", len(df))
            
            # Tablo
            st.dataframe(df, use_container_width=True)
            
            # Kar/Zarar Grafiği
            st.bar_chart(df.set_index("Hisse")["Kar/Zarar (%)"])
