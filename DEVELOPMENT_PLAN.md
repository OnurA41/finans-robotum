# DEVELOPMENT_PLAN (FAZ 1.1)

Güncellenmiş FAZ bazlı geliştirme planı. Her faz için amaç, ön koşullar, yapılacaklar, çıktı, test kriterleri ve tamamlanma kriterleri belirtilir. Veritabanı seçenekleri ve mimari tercihler sadeleştirilmiştir; PostgreSQL/TimescaleDB ileri ölçekleme aşamaları için önerilmiştir.

---

## FAZ 0 — Mevcut proje analizi
- Amaç: Repo durumunun belgelenmesi (mevcut analiz).
- Ön koşullar: Repo incelenmiş.
- Yapılacaklar: FAZ0 raporu.
- Çıktılar: FAZ0 raporu.
- Test kriterleri: Analiz doğruluğu.
- Tamamlanma: Rapor onayı.

## FAZ 1 — Proje anayasası ve mimari (bu faz)
- Amaç: Proje dokümantasyonu ve hedef mimari.
- Ön koşullar: FAZ0.
- Yapılacaklar: PROJECT_SPECIFICATION.md, ARCHITECTURE.md, DEVELOPMENT_PLAN.md, DATA_SOURCES.md, SECURITY.md, TESTING.md.
- Çıktılar: Doküman seti.
- Test kriterleri: Doküman onayı.
- Tamamlanma: Doküman onayı.

## FAZ 2 — Güvenlik, logging ve hata yönetimi
- Amaç: Temel güvenlik & işletim hazır hale getirme.
- Ön koşullar: FAZ1 onayı.
- Yapılacaklar:
  - Centralized logging, structured logs.
  - Error handling conventions; except:pass kaldırılması.
  - Secrets handling (env var check + fail fast).
- Çıktılar: Güvenlik ve Logging modülleri.
- Test: Security lint, secret-scan.

## FAZ 3 — Veritabanı (başlangıç önerisi)
- Amaç: JSON dosyaları yerine kalıcı depolama.
- Ön koşullar: FAZ2.
- Yapılacaklar:
  - İlk kişisel kullanım sürümünde önerilen basit seçenek: SQLite + SQLAlchemy.
  - Migration scriptleri ve veri transfer planı.
- Çıktılar: DB modelleri ve migration planı.
- Not: PostgreSQL + TimescaleDB yüksek veri hacmi veya çok kullanıcılı sistem aşamasında değerlendirilecektir; ancak ilk başta zorunlu değildir.

## FAZ 4 — Veri toplama, normalizasyon ve doğrulama
- Amaç: Güvenilir, normalized data layer.
- Ön koşullar: FAZ3.
- Yapılacaklar: Adapter pattern implementasyonu, validation pipeline, cache.

## FAZ 5 — Katılım hisse sistemi
- Amaç: Hisse veri modeli, analiz ve UI entegrasyonu.
- Ön koşullar: FAZ4.

## FAZ 6 — Katılım fon sistemi
- Amaç: Fon verileri & analiz.
- Ön koşullar: FAZ4.

## FAZ 7 — Temel analiz
- Amaç: Finansal tablo parsing ve oran hesaplayıcı.
- Ön koşullar: FAZ5/6, KAP adapter( plan ).

## FAZ 8 — Teknik analiz
- Amaç: İndikatörler, signal engine.
- Ön koşullar: FAZ4.

## FAZ 9 — Değerleme
- Amaç: DCF/relativ multiples modelleri.
- Ön koşullar: FAZ7.

## FAZ 10 — Risk motoru
- Amaç: Portföy risk hesapları.
- Ön koşullar: FAZ3, FAZ5.

## FAZ 11 — Portföy analitiği
- Amaç: Zengin portföy raporları, tarihselleştirme.
- Ön koşullar: FAZ3, FAZ10.

## FAZ 12 — AI analiz motoru
- Amaç: AI'yı analiz-asistanı olarak güvenli kullanmak.
- Ön koşullar: FAZ7-FAZ11, SECURITY.
- Not: AI yalnızca doğrulanmış veri ile beslenir ve raporlarda veri kaynak metadata'sı görünür olmalıdır.

## FAZ 13 — Raporlama
- Amaç: Export (PDF/HTML), scheduled reports.
- Ön koşullar: FAZ11.

## FAZ 14 — Alarm ve sinyal
- Amaç: Robust alerting framework.
- Ön koşullar: FAZ4, FAZ11.

## FAZ 15 — Backtesting
- Amaç: Deterministic backtest engine.
- Ön koşullar: FAZ3, FAZ11, FAZ14.

## FAZ 16 — Paper trading
- Amaç: Simülasyon ile kullanıcı onaylı emir denemesi.
- Ön koşullar: FAZ15.

## FAZ 17 — Broker/emir altyapısı
- Amaç: Gerçek broker entegrasyonuna hazırlık.
- Ön koşullar: FAZ16, SECURITY.

## FAZ 18 — Güvenlik ve üretim hazırlığı
- Amaç: Production hardening.
- Ön koşullar: FAZ2, FAZ3, FAZ17.

## FAZ 19 — Kontrollü otomatik işlem (sıralı kısıtlama)
- Amaç: Kademeli, güvenlik onaylı otomatik emir yeteneği.
- Zorunlu zincir (otomatik işlem devreye alma sırası):
  1. Veri doğrulama
  2. Analiz
  3. Backtest
  4. Paper trading
  5. Kullanıcı onaylı emir
  6. Güvenlik doğrulaması
  7. Kontrollü otomatik işlem
- Not: Bu zincire uyulmadan otomatik işlem aktif edilmeyecektir.

---

Her faz sonunda PR ile kod review ve rollback planı zorunludur.
