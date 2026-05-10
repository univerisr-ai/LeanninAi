# Sicak Bellek (Hot Cache)

Bu bolum en son uretilen draft bilgisinin hizli ozetidir.

## Apple Pencil ile Tarayıcıda Basınç Hassasiyeti Yakalama: PointerEvent ve getCoalescedEvents() Kullanımı
→ [[review/apple-pencil-ile-tarayicida-basinc-hassasiyeti-yakalama-pointerevent-ve-getcoalescedevents-kullanimi]]

Bu makale, tarayıcıda Apple Pencil gibi stilus cihazlardan gerçek zamanlı basınç verisi almak için PointerEvent API'sinin nasıl kullanılacağını açıklar. Özellikle e.pressure kullanımı, cihaz farklılıklarına dikkat edilerek optimize edilmiş bir yaklaşım sunar. Ayrıca, yüksek frekanslı girdilerde çizgi kalitesini artırmak için getCoalescedEvents() yöntemi ele alınır.
- PointerEvent, mouse, touch ve pen girdilerini tek bir API üzerinden yönetmeyi sağlar.
- e.pressure değeri cihazlara göre farklılık gösterir; mouse sabit 0.5, Apple Pencil ise 0-1 arası sürekli değer verir.
- Basınç değerine göre çizgi kalınlığı ayarlanırken fallback stratejileri kullanılmalıdır.

