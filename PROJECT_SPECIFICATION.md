# PROJECT_SPECIFICATION

## Projenin amacı
Kişisel Katılım Finans Terminali: yalnızca BIST Katılım Endeksi kapsamındaki hisseler ve Katılım uyumlu fonlar için yatırımcıya kapsamlı, doğrulanmış veri tabanlı analiz, portföy yönetimi, raporlama ve uyarı desteği sağlamak. Bu ürünün ilk sürümü kişisel kullanım amaçlı, tek kullanıcıya yöneliktir.

## Uygulamanın kapsamı (ölçülebilir)
- Yalnızca Katılım endeksi kapsamındaki hisselerin ve Katılım uyumlu fonların takibi.
- Kullanıcıların sınırsız sayıda portföy oluşturabilmesi ve yönetebilmesi (tek kullanıcı odaklı başlangıçta).
- Portföy performans raporları: günlük, haftalık, aylık, 3/6/9/12 aylık periyotlarda.
- Temel analiz: finansal tablolardan türetilen oranlar ve özetler (planlanan veri kaynakları ile).
- Teknik analiz: standart indikatörler, periyot-temelli görselleştirme.
- Değerleme: F/K, PD/DD, benzeri metrikler.
- Risk analizi: volatilite, Sharpe, max drawdown, pozisyon bazlı risk.
- Fon analizi: TEFAS verileri ve uyumluluk kontrolü.
- Şirket / sektör karşılaştırması: normalize edilmiş metriklerle.
- KAP analizi: KAP bildirimlerinin çekilip özetlenmesi (planlanan).
- Haber analizi: haber akışından özet ve sentiment (planlanan).
- AI destekli analiz: yalnızca yapılandırılmış ve doğrulanmış verilerin yorumlanması.
- Uyarılar: stop-loss, take-profit, veri-tutarsızlık, API hatası durumu.
- Backtest & Paper trading: kullanıcı onaylı simülasyon (planlanan).
- Kullanıcı onaylı emir ve gelecekte kontrollü otomatik emir entegrasyonu (kesin ayrı güvenlik katmanıyla, çok son aşamada).

## Kullanıcı profili
- Bireysel yatırımcılar ve küçük portföy yöneticileri, Katılım prensiplerine önem veren yatırımcılar.
- Teknik/finans bilgisi orta seviyede; arayüz açıklayıcı ve rehberli olacak.

## Veri doğrulama ilkesi (kesin kural)
- Birincil resmi kaynak varsa önceliklidir.
- İkinci bağımsız kaynak mümkün olduğunda çapraz doğrulama amacıyla kullanılır.
- Birincil kaynak tek başına mevcutsa bu durum veri metadata'sında açıkça belirtilir.
- Tek kaynaklı veri AI tarafından kesinlik seviyesi yüksekmiş gibi sunulamaz.
- Veri kaynağı güvenilirlik seviyesi analiz sonuçlarında görünür olmalıdır.

## AI kullanımı (kesin)
- AI hiçbir zaman veri kaynağı değildir.
- AI, yalnızca doğrulanmış ve yapılandırılmış verileri yorumlayan bir analiz katmanıdır.
- AI, ham veya doğrulanmamış veriyi gerçek veri gibi sunamaz.
- AI çıktıları deterministik hesaplama motorlarının yerine geçemez.
- Hiçbir yatırım kararı yalnızca tek bir veri noktasına veya yalnızca AI çıktısına dayanamaz.
- Raporlarda kullanılan verilerin kaynak ve zaman bilgisinin (metadata) görünür olması zorunludur.

## Kapsamda olmayanlar (ilk sürüm)
- Multi-user / RBAC / authentication: İlk sürüm için zorunlu değildir; gelecekte genişletme olarak planlanmıştır.
- Otomatik emir/otomatik işlem: Sadece çok son aşamada ve özel güvenlik zincirinden sonra devreye alınacaktır (bkz. DEVELOPMENT_PLAN).

## Ölçülebilir hedefler (KPI)
- Veri tutarlılığı: kaynaklar arası uyuşmazlık oranı < %2 (ilk 6 ay için hedef).
- Tarihsel veri kayıt tamlığı: günlük portföy değeri kaydı %99.
- Test kapsamı: finansal hesaplama modüllerinde %95 deterministik test geçişi.
- Güvenlik: gizli anahtarların hiçbirinin Git geçmişinde bulunmaması (%100).

## Notlar
- Bu belge FAZ 1.1 çıktısıdır; mevcut repository durumuna (FAZ 0) göre güncellenmiştir. Mevcut kodda olmayan hiçbir özellik "mevcut" olarak gösterilmemiştir.
