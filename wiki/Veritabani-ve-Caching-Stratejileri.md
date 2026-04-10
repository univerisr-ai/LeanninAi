# Veritabanı ve Caching Stratejileri

Yüksek trafikli sistemlerde veritabanının yorulmamasını sağlamak en kritik mimari konudur. Okuma ve yazma stratejileri ayrı tasarlanır.

## N+1 Problemi ve Prisma ORM
İlişkisel verilerde (Örn: "Tüm Yazıları" çekerken her yazının "Yazarını" bulmak için tek tek veritabanına yeniden gidilmesi) yaşanan devasa performans sorunudur. Prisma'da bu `include` ile Eager Loading (tek sorguda join yapma) olarak çözülür. GraphQL'de ise Dataloader kalıbı kullanılır.

## Redis Cache-Aside Stratejisi
1. Uygulama veriyi önce Redis'ten okumaya çalışır (Cache Hit).
2. Veri yoksa (Cache Miss), gidip asıl veritabanından (PostgreSQL/MySQL) okur.
3. Alınan data, bir sonraki sefere hızlı olsun diye Redis'e yazılır (TTL - geçerlilik süresi ile birlikte).
*Not: Veri değiştiğinde (Update/Delete), Cache in-validate (geçersiz) edilmelidir ki kullanıcıya eski veri (stale data) gösterilmesin.*

## Queue Stratejisi (BullMQ)
E-posta gönderme, video işleme, PDF oluşturma gibi HTTP isteğini kilitleyecek ve yavaş yanıt döndürecek "ağır" işlemler ana API akışından çıkartılır. BullMQ (Redis tabanlı) kullanılarak "Kuyruğa" atılır (Asenkron İş). Kullanıcıya anında HTTP 202 (Accepted) dönülür.

**İlgili Bağlantılar:**
- [[Clean-Architecture]]

## 📚 İlgili Draftlar
- [[review/api-response-yapilari-flat-vs-nested-duzlestirilmis-vs-ic-ice]]
