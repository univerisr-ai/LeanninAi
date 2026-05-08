# Sicak Bellek (Hot Cache)

Bu bolum en son uretilen draft bilgisinin hizli ozetidir.

## CSS Counters ile Otomatik Liste Numaralandırma
→ [[review/css-counters-ile-otomatik-liste-numaralandirma]]

CSS counter-reset, counter-increment ve counter() fonksiyonları kullanılarak HTML içeriklerinde otomatik ve özelleştirilebilir numaralandırma yapılması yöntemini açıklar. Bu teknik ile manuel numaralandırma ihtiyacını ortadan kaldırarak performanslı ve dinamik listeler oluşturulabilir.
- CSS sayaçları, JavaScript'e gerek kalmadan otomatik numaralandırma sağlar.
- counter-reset ile sayaç başlatılır, counter-increment ile her elemanda artırılır.
- counter() fonksiyonu content özelliği içinde kullanılarak görüntülenir.

## Bileşen Tabanlı Email Şablonları ve Composable Email Mimarisi
→ [[review/bilesen-tabanli-email-sablonlari-ve-composable-email-mimarisi]]

Bu konsept, email şablonlarının bileşen tabanlı olarak nasıl yönetileceğini ve composable (birleştirilebilir) bir yapıyla nasıl sürdürülebilir hale getirileceğini açıklar. UI bileşenlerine benzer şekilde email içerikleri de yeniden kullanılabilir, sürdürülebilir ve test edilebilir bileşenlerden oluşur. Böylece büyük ve karmaşık email sistemlerinde tutarlılık, değişiklik yönetimi ve ekip içi sorumluluk dağılımı kolaylaşır.
- Email şablonları, modern UI bileşenleri gibi bağımsız ve yeniden kullanılabilir bileşenlerden oluşmalıdır.
- Her email bileşeni (başlık, paragraf, buton, kart) kendi stilini ve davranışını barındıran bağımsız HTML parçalarıdır.
- Template'ler bu küçük bileşenleri birleştirerek oluşturulur; bu da değişikliklerin tek bir yerden yönetilmesini sağlar.

## Shadow DOM ile Tooltip Renderlama: Iframe Alternatifi
→ [[review/shadow-dom-ile-tooltip-renderlama-iframe-alternatifi]]

Chrome eklentilerinde tooltip'ler için iframeler yerine Shadow DOM kullanılmasının avantajları. Stil izolasyonu, font uyumu ve senkron etkileşim gibi pratik uygulamalar.
- Shadow DOM, host sayfanın CSS'inin tooltip üzerine etki etmesini engeller.
- Tooltip içinde host sayfanın font bilgileri okunarak native görünüm sağlanır.
- Iframe'lerdeki FOUC (Flash of Unstyled Content) problemi yaşanmaz.

## Minimal Bağımlılıklarla Beyaz Tahta Uygulaması Geliştirme
→ [[review/minimal-bagimliliklarla-beyaz-tahta-uygulamasi-gelistirme]]

Bu konsept, sadece 3 bağımlılık kullanarak geliştirilen performans odaklı bir beyaz tahta uygulamasının mimarisini ve teknik kararlarını açıklar. Canvas API, Zustand tabanlı durum yönetimi ve minimal bundle yaklaşımı ele alınır.
- Canvas API kullanılarak donanım hızlandırmalı çizim motoru geliştirildi
- Zustand ile 3 küçük depo (drawing, view, theme) ile durum yönetimi sağlandı
- SVG yerine Canvas tercih edilerek DOM ek yükü önlenildi

## React Formlarında Gecikmeli Doğrulama ve Otomatik Taslak Kaydetme
→ [[review/react-formlarinda-gecikmeli-dogrulama-ve-otomatik-taslak-kaydetme]]

Bu makale, React form işlemlerinde kullanıcı deneyimini artırmak için debounced (gecikmeli) doğrulama, otomatik taslak kaydetme ve kontrollü input yönetimi gibi gelişmiş teknikleri anlatmaktadır. Her bir teknik adım adım manuel olarak uygulanmış, ardından daha temiz bir çözüm için ReactUse kütüphanesinden özel hook’lar önerilmiştir.
- Debounced doğrulama ile her tuşa basıldığında API çağrısı yapmaktan kaçınılması sağlanır.
- Kontrollü ve kontrolsüz input bileşenlerinin nasıl sarmalanacağı gösterilmiştir.
- localStorage kullanılarak form verilerinin otomatik olarak taslak olarak kaydedilmesi sağlanmıştır.

