# SECURITY (FAZ 1.1)

Güncellenmiş güvenlik ilkeleri ve uygulama önerileri. Devcontainer yapılandırmasındaki CORS/XSRF kapatma gibi riskler üretim ortamında kabul edilemez olarak vurgulanmıştır.

## API key yönetimi
- Tüm API anahtarları environment variables veya secrets manager (Vault) ile saklanmalı.
- Anahtarlar kodda veya Git geçmişinde ASLA tutulmamalı.

## Environment variables
- Uygulama başında gerekli env var'lar doğrulanmalı; eksikse fail-fast davranışı uygulanmalı.
- Geliştirme için example.env tutulabilir ama gerçek .env veya secrets commit edilmemelidir.

## Secret rotation
- Secrets düzenli olarak rotasyona tabi tutulmalı (ör. 90 gün).

## GitHub'a secret commit edilmemesi
- pre-commit hooks ve secret scanning zorunlu.

## Input validation
- Tüm dış veri ve kullanıcı girdileri schema validation (pydantic) ile doğrulanmalı.

## Logging sırasında secret masking
- Loglarda hassas alanlar maskelenmeli; structured logging tercih edilmeli.

## Kullanıcı verilerinin korunması
- PII mevcutsa şifreleme ve erişim kontrolü uygulanmalı.

## Broker kimlik bilgilerinin korunması
- Broker credential'ları Vault'ta saklanmalı; runtime'da transient olarak çekilmeli.

## Otomatik işlem için ayrı güvenlik katmanı
- Otomatik işlem sadece FAZ19 zincirindeki tüm adımlar tamamlandığında devreye alınır.

## Least privilege
- Servis hesapları ve DB kullanıcıları en az yetki ilkesine göre konfigüre edilmeli.

## Audit log
- Kritik eylemler immutable audit log'a yazılmalı.

## Güvenli HTTP istekleri
- Tüm dış çağrılar TLS/HTTPS ile yapılmalı; sertifika doğrulama zorunlu.

## Rate limiting
- Dış servisler için rate-limiter & retry/backoff politikası hazırlanmalı.

## Dependency güvenliği
- Dependabot veya benzeri vulnerability scanning aktif olmalı; SBOM oluşturulmalı.

## Prod ortam riskleri ve devcontainer uyarısı
- .devcontainer içinde streamlit'in CORS/XSRF korumasını devre dışı bırakmak geliştirici kolaylığıdır; üretimde kabul edilemez.

## İhlal yönetimi
- Incident response plan oluşturulmalı (contain → eradicate → notify → post-mortem).
