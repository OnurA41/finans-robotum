# SECURITY (FAZ 1.1 + FAZ 2.1)

Güncellenmiş güvenlik ilkeleri ve uygulama önerileri. Devcontainer yapılandırmasındaki CORS/XSRF kapatma gibi riskler üretim ortamında kabul edilemez olarak vurgulanmıştır.

## FAZ 2.1 - Completed
Aşağıdaki altyapı FAZ 2.1 kapsamında uygulandı:
- Merkezi konfigürasyon (src/config.py) ile zorunlu environment variable'ların doğrulanması.
- Merkezi logging yapılandırması (src/logging_config.py) ve mesaj maskleme (sensitivity redaction).
- Özel uygulama hata sınıfları (src/exceptions.py).
- .gitignore güncellemesi ile .env ve credential dosyalarının korunması.
- app.py ve main.py içerisindeki sessiz hata yutmalar (except: pass) minimal şekilde logger ile raporlanacak şekilde düzeltildi.

## Sonraki adımlar
- Central log collector entegrasyonu (ELK/Grafana Loki) — FAZ 2.x
- Secrets vault (Vault/Cloud K/V) entegrasyonu — FAZ 2.x
- Daha gelişmiş retry/backoff ve izleme kuralları — FAZ 4.

Diğer güvenlik maddeler (önceden tanımlı):
- Tüm API anahtarları environment variables veya secrets manager (Vault) ile saklanmalı.
- Anahtarlar kodda veya Git geçmişinde ASLA tutulmamalı.
