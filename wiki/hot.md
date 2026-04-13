# Sicak Bellek (Hot Cache)

Bu bolum en son uretilen draft bilgisinin hizli ozetidir.

## Tailwind CSS v4 Yenilikleri ve Geçiş Rehberi
→ [[review/tailwind-css-v4-yenilikleri-ve-gecis-rehberi]]

Tailwind CSS v4, mimari olarak tamamen yeniden yazılmıştır. JS tabanlı yapılandırmayı bırakarak CSS-first bir yaklaşım benimsemiştir. Bu rehberde v4'teki kilit değişiklikler, yeni yapılandırma yöntemi, PostCSS entegrasyonu, içerik tespiti ve mevcut projeye geçiş adımları açıklanmaktadır.
- Yapılandırma artık CSS dosyasında `@theme` bloğu ile tanımlanır.
- `tailwind.config.js` dosyası kaldırılmıştır.
- Lightning CSS motoru ile derleme süreleri kısalır.

## Reaktif Durum Yönetiminde Cebirsel Veri Türleri
→ [[review/reaktif-durum-yonetiminde-cebirsel-veri-turleri]]

Bu makale, reaktif programlamada durum makinelerini cebirsel veri türleri (ADT) kullanarak nasıl açık ve güvenli hale getireceğinizi açıklar. Özellikle signal lifecycle (hayat döngüsü) kavramını Unset | Active<T> | Disposed üçlüsüyle modelliyor ve bu yaklaşımın tip güvenliği ve eksiksiz durum kontrolü sağladığını gösteriyor.
- Reaktif durumlar genellikle gizli sonlu durum makineleridir; bunları açıkça modellemek hataları azaltır.
- Cebirsel veri türleri sayesinde her mümkün durum adlandırılır, tiplenir ve derleme zamanında kontrol edilir.
- `signal` yaşam döngüsünü temsil eden üçlü bir ADT örneği: Unset, Active<T>, Disposed.

