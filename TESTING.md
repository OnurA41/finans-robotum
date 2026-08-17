# TESTING (FAZ 1.1)

Güncellenmiş test stratejisi. Finansal hesaplama hatalarının deterministik testlerle doğrulanması önceliklidir.

## Test stratejisi — genel
- Test pyramid uygulanır: Unit tests (çok), Integration tests (orta), End-to-end tests (az).
- External API çağrıları integration testlerinde mock/record (VCR) ile kontrollü hale getirilir.

## Kritik test türleri
- Unit test: hesaplama fonksiyonları, P&L, risk hesapları.
- Integration test: adapter + validation + normalization akışları.
- API/data-provider test: adapterların mock endpoint ile testi.
- Data validation test: kusurlu veri örnekleri ile validation kuralları testi.
- Financial calculation test: deterministik test datasetleri (pre-recorded price series).
- Portfolio calculation test: portföy değerleme, getiri hesaplama, time-weighted/ money-weighted return doğrulamaları.
- AI output validation test: AI çıktılarının beklenen şablonu sağlaması ve metadata içermesi.
- Regression test: her düzeltme için regression case.
- Security test: secret scanning, dependency scan, static code analysis.
- End-to-end test: data ingestion → analysis → report generation (sınırlı kapsam).
- Backtest validation: reproducibility ve seed kontrollü sonuçlar.
- Paper trading validation: ledger consistency.

## Deterministic finansal test yaklaşımı
- Finansal hesaplamalar için pre-recorded veri setleri kullanılmalı.
- Rastgelelik varsa seed sabitlenmeli.
- Numerik toleranslar açıkça belirtilmeli.

## Test harness & tooling
- pytest, coverage, tox/nox
- Mocks: responses / requests-mock / vcrpy
- CI: GitHub Actions (PR-level unit tests, nightly full suite)

## Acceptance metrics
- Unit test coverage hedefi: %85+ (öncelikli finans modüllerinde %95 deterministik hedef).

## Notlar
- Mevcut repository'de henüz test dosyası bulunmamaktadır; bu belge testlerin nasıl inşa edileceğini tarif eder.
