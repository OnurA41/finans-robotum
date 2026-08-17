# ARCHITECTURE — Hedef Mimari (FAZ 1.1 + FAZ 2.1)

Aşağıda hedef mimarinin sadeleştirilmiş ve uygulanabilir ilk-sürüm yapısı sunulmuştur. FAZ 2.1 kapsamında merkezi logging ve konfigürasyon katmanları eklendi.

## Temel mimari akış (ilk sürüm)
1. Streamlit UI
2. Application / Services
3. Analysis / Portfolio
4. Data Providers / Validation
5. Database

## FAZ 2.1 değişiklikleri
- Merkezi logging katmanı eklendi (src/logging_config.py). Loglar masking/redaction ile korunur.
- Merkezi configuration katmanı eklendi (src/config.py) — zorunlu env varların fail-fast doğrulaması.

(Devamı: Mimari detaylar önceki sürümle aynıdır.)
