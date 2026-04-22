# Sicak Bellek (Hot Cache)

Bu bolum en son uretilen draft bilgisinin hizli ozetidir.

## 2026'da Modern Web Tasarımı: Grid ve Container Query ile Performanslı Layout
→ [[review/2026-da-modern-web-tasarimi-grid-ve-container-query-ile-performansli-layout]]

Bu rehber, 2026 yılına uygun modern web tasarımında Flexbox'un sınırlarını aşarak CSS Grid ve container query kullanımını merkeze alıyor. Gerçek performans metrikleri (Core Web Vitals) doğrultusunda layout ve optimizasyon stratejilerini uygulamalı olarak ele alıyor.
- Flexbox yerine CSS Grid ile iki boyutlu sayfa düzenlemeleri yapılmalı
- Container query kullanarak bileşenler viewport değil, gerçek yerleşim alanına göre uyarlanmalı
- Core Web Vitals (LCP, INP, CLS) doğrultusunda HTML/CSS/JS optimizasyonları yapılmalı

## SVG Path d Özelliği ve Görsel Düzenleme Aracı
→ [[review/svg-path-d-ozelligi-ve-gorsel-duzenleme-araci]]

Bu makalede SVG path öğesinin d özelliği detaylı olarak açıklanmakta ve bu özelliği anlamayı kolaylaştıran interaktif bir düzenleyici tanıtılıyor. Yazar, SVG yol komutlarını öğrenmek için küçük bir görsel editör geliştirerek karmaşık d dizgesini anlaşılır hale getirmiş ve bu süreçte SVG yol dilbilgisinin kritik yönlerini keşfetmiştir.
- SVG path d özelliği, sanal bir kalemin çizim talimatlarından oluşan bir dizgesidir.
- Komutlar büyük/küçük harfe duyarlıdır; büyük harfler mutlak, küçük harfler göreli koordinatlardır.
- H, V, S, T gibi kısa komutlar daha temel komutların kısaltmalarıdır.

## Auth Secret Yönetimi: Vercel Breach Sonrası Yeni Stratejiler
→ [[review/auth-secret-yonetimi-vercel-breach-sonrasi-yeni-stratejiler]]

Vercel'in güvenlik ihlali sonrası, auth secret'ların deployment platformundan bağımsız yönetilmesi gerektiği gündeme geldi. Bu konsept, Clerk, Auth0 ve Authon gibi sağlayıcılar üzerinden auth mimarilerinin tekrar değerlendirilmesini ve secret yönetiminin stratejik olarak yeniden tasarlanmasını özetliyor.
- Auth secret’lar, genel environment variable'lardan farklıdır ve sızması durumunda sistem bütünüyle ele geçirilebilir.
- Clerk, Vercel ile sıkı entegre olduğu için vendor lock-in ve güvenlik riski taşır.
- Auth0 gibi platformdan bağımsız çözümler, auth katmanının izole edilmesini sağlar.

## Client-Side SEO: Araç Bazlı Web Uygulamalarında Arama Motoru Optimizasyonu
→ [[review/client-side-seo-arac-bazli-web-uygulamalarinda-arama-motoru-optimizasyonu]]

Tamamen istemci tarafında çalışan araç tabanlı web uygulamalarında SEO stratejileri. Google Search Console verileriyle desteklenmiş gerçek performans analizi ve SEO odaklı içerik mimarisi.
- İstemci taraflı render edilen statik sayfaların hızlı indekslenmesi
- Her bir araca özel sayfa yapıları ile long-tail anahtar kelimelerde organik trafik kazanımı
- Ana sayfa yerine bireysel araç sayfalarına odaklanan SEO yaklaşımı

