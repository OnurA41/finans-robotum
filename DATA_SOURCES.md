# DATA_SOURCES (FAZ 1.1)

Bu doküman mevcut ve planlanan veri kaynaklarını, her biri için beklenen veri türünü, güvenilirlik ve önceliklendirme kurallarını açıklar. "Mevcut entegrasyon" ve "Planlanan entegrasyon" başlıkları ayrı tutulmuştur.

## Genel kurallar
- Tüm ham veri UTC timestamp ile saklanır.
- Her veri satırı için: kaynak_id, çekilme_zamani, orijinal_payload ve normalized_payload saklanır.
- Veri kaynakları yalnızca aynı enstrüman, aynı veri tipi ve aynı dönem/zaman damgası üzerinden karşılaştırılmalıdır. Örneğin: hisse fiyatı sadece hisse fiyatı ile; fon birim fiyatı sadece fon birim fiyatı ile; ve aynı timestamp/period için karşılaştırma yapılmalıdır.

---

## Mevcut entegrasyonlar (kodda doğrulanmış)

### TEFAS (mevcut, fon verisi)
- Sağlayacağı veri: Fon birim fiyatları (BİRİM FİYAT), fon meta verileri.
- Güvenilirlik: Yüksek (resmi kaynak).
- Rol: Birincil kaynak — fon fiyatları için öncelikli olarak kullanılacaktır.
- Güncelleme sıklığı: Günlük (fon tipine göre değişebilir).
- API erişimi: Kodda mevcut bir POST çağrısı örneği vardır (app.py içinde). Teknik erişim detayları ve rate limit doğrulamaları uygulama tarafından kontrol edilmelidir.
- Veri uyuşmazlığı: TEFAS birincildir; eş zamanlı karşılaştırma ancak aynı enstrüman/aynı veri tipi/aynı timestamp ihtiyacını sağladığında yapılır.
- Rate limit / ulaşılamama: Cache ve backoff politikası uygulanmalıdır; eğer API yanıtı yoksa veri "gecikmeli" veya "eksik" olarak işaretlenmelidir.

### yfinance / Yahoo Finance (mevcut, hisse verisi)
- Sağlayacağı veri: Hisse anlık fiyat, geçmiş fiyatlar.
- Güvenilirlik: Orta.
- Rol: İkincil/yardımcı kaynak — hisse fiyatları için destek ve çapraz kontrol amacıyla kullanılabilir.
- Güncelleme sıklığı: İstek bazlı; cache önerilir (örn. 1 dakika).
- API erişimi: SDK (yfinance) ile yapılır (kodda kullanılmıştır).
- Veri uyuşmazlığı: yfinance ile TEFAS doğrudan karşılaştırılmaz; karşılaştırma yalnızca "aynı enstrüman/yazım/sınıf ve aynı timestamp" sağlandığında yapılır.
- Rate limit / ulaşılamama: Error/exception loglanmalı ve retry/backoff uygulanmalı.

---

## Planlanan entegrasyonlar (NOT: henüz kodda yok)
Aşağıdaki kaynaklar planlanmıştır. "Planlanan entegrasyon" başlığı, bu kaynakların henüz teknik olarak doğrulanmadığını belirtir; aşağıdaki koşullar doğrulanmalıdır:
- API erişimi gerekliliği (API key gerekliliği dahil) doğrulanmalıdır.
- Kesin veri kapsamı ve lisans koşulları doğrulanmalıdır.
- Teknik endpointlerin stabilitesi ve rate limit bilgileri doğrulanmalıdır.

### KAP (planlanan)
- Sağlayacağı veri: Şirket bildirileri (finansal tablolar, kar/zarar, özel durum açıklamaları).
- Güvenilirlik: Çok yüksek (resmi kurumsal bildirim).
- Rol: Birincil — temel analiz ve kurumsal haberler için hedeflenmiştir.
- Güncelleme sıklığı: Bildirim anında (near real-time).
- Entegrasyon koşulu: KAP API erişimi ve veri formatı doğrulanmalıdır.

### Fintables (planlanan)
- Sağlayacağı veri: Derin finansal tablolar, ek metrikler.
- Güvenilirlik: Yüksek (lisanslı)
- Entegrasyon koşulu: API erişimi, lisans şartları ve veri kapsamı doğrulanmalıdır.

### Investing.com (planlanan)
- Sağlayacağı veri: Haber, alternatif fiyat veri, market özetleri.
- Güvenilirlik: Orta.
- Entegrasyon koşulu: Erişim yöntemleri ve veri kapsamı doğrulanmalıdır.

### Fonaly / FVT (planlanan)
- Sağlayacağı veri: Fon spesifik analiz, ek metrikler.
- Entegrasyon koşulu: API erişimi ve lisans durumu doğrulanmalıdır.

### Gelecekte eklenebilecek resmi/lisanslı sağlayıcılar
- Sağlayacağı veri: Yüksek kaliteli tarihsel/tick-level veriler.
- Entegrasyon koşulu: Lisans ve teknik erişim doğrulanmalıdır.

---

## Veri önceliklendirme kuralı (özet)
1. Resmi kaynaklar (TEFAS, KAP) birincildir — ancak karşılaştırma sadece uygun koşullarda yapılır (aynı enstrüman, veri tipi, dönem/timestamp).
2. Lisanslı sağlayıcılar ikincil/öncelikli olabilir.
3. yfinance / Investing / üçüncü taraflar yalnızca destek amacıyla kullanılır.

Uyuşmazlık davranışı:
- Fon fiyatı uyuşmazlığında TEFAS önceliklidir (aynı enstrüman/aynı timestamp koşulu sağlandığında).
- Şirket tablo uyuşmazlığında KAP ana referanstır (kondisyonel).
- Farklılık belirlenen eşik değerinin (örn. %2) üzerinde ise veri flag'lenir ve alert üretilir.

---

## Zaman etiketleme
- Her veri satırı UTC timestamp ile saklanır ve kaynak tarafından sağlanan timestamp kullanılır; yoksa çekilme zamanı ile birlikte "inferred_timestamp" olarak işaretlenir.
