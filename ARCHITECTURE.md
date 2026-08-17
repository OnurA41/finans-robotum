# ARCHITECTURE — Hedef Mimari (FAZ 1.1)

Aşağıda hedef mimarinin sadeleştirilmiş ve uygulanabilir ilk-sürüm yapısı sunulmuştur. REST/gRPC katmanları ilk sürüm için zorunlu değildir; ihtiyaç halinde sonraki sürümlerde eklenebilir.

## Temel mimari akış (ilk sürüm)
1. Streamlit UI
2. Application / Services
3. Analysis / Portfolio
4. Data Providers / Validation
5. Database

Streamlit UI doğrudan Application/Services katmanına istek yapar. Bu, küçük/tek-kullanıcı kişisel sürümlerde sadeliği korumak içindir. REST API veya RPC katmanı ayrı bir gereklilik değildir; gelecekte çok kullanıcılı veya geniş erişim gereksimi doğduğunda eklenebilir.

## Katmanlar ve sorumlulukları (kısa)
- Presentation / UI (Streamlit)
  - Kullanıcı etkileşimi, görselleştirme.
  - UI sadece Services ile konuşur; business logic UI içinde dağınık olmamalıdır.

- Application / Services
  - İş kuralları, P&L, pozisyon yönetimi, stop/tp logic, raporlama orchestration.
  - Services, Data Providers aracılığıyla veri alır.

- Analysis / Portfolio
  - Portföy modelleri, temel/teknik/valuasyon hesaplayıcıları.
  - Deterministik hesaplama fonksiyonları burada yer alır.

- Data Providers / Validation
  - Adapter pattern ile dış kaynaklardan veri çekimi.
  - Validation ve normalization burada yapılır; her veri parçası metadata ile birlikte saklanır (kaynak, timestamp, güvenilirlik).

- Database
  - Başlangıç için hafif veritabanı (ör. SQLite + SQLAlchemy) önerilir.
  - Yük ve çoklu kullanıcı gereksinimi arttıkça PostgreSQL/TimescaleDB düşünülebilir; ancak bu henüz zorunlu değildir.

## Önerilen klasör yapısı (dokümante edilmiş, henüz oluşturmayın)
- /src
  - /ui (Streamlit uygulaması)
  - /services (business logic)
  - /analysis (fundamental, technical, valuation)
  - /adapters (tefas_adapter.py, yfinance_adapter.py, kap_adapter.py (plan))
  - /data (ORM modelleri veya repository pattern)
  - /db (migration scriptleri — opsiyonel başlangıçta)
  - /tasks (background jobs)
  - /ai (prompt templates, wrappers, validators)
  - /tests
  - /configs

## Bağımlılık sınırları
- UI ➜ yalnızca Services katmanına çağrı yapar.
- Services ➜ yalnızca Adapters aracılığıyla dış veri alır.
- Adapters ➜ ham veri sağlar; validation & normalization ayrı katmanda yapılır.
- AI ➜ yalnızca normalized/verifed veri alır; herhangi bir veri mutasyonu yapmaz.

## Diğer öneriler
- Adapter interface contract'ları olmalı ve mock'lanabilir olması zorunlu.
- Zaman serisi verileri UTC timestamp ile saklanmalı.
- İlk sürümde mimari sadeliği koruyun; ölçeklendirme gerektikçe katmanlar ayrıştırılsın.
