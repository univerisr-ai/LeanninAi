# Klavye Navigasyon ve Focus (A11y)

## Meta
- category: a11y
- status: published


Bir web uygulamasının faresi olmayan veya görme engelli birisi tarafından sadece klavye (`Tab`, `Space`, `Enter`, `Yön Tusları`) kullanılarak %100 yönetilebilmesidir.

## Outline Yönetimi: `focus-visible`
- Fareyle herhangi bir menüye tıklayan kullanıcı, tıkladığı butonun etrafında mavi/siyah kalın bir çerçeve (`outline`) görmek **İSTEMEZ**.
- Ancak siteyi tamamen klavye ile kullanan `Tab`cı kullanıcı, o an hangi elemanın üzerinde olduğunu seçili görebilmek için o kutuya **MECBURDUR**.
Bu uyumsuzluğu, modern web tarayıcılarında sadece klavye dokunuşlarına tepki veren css `:focus-visible` seçicisi ile çözeriz. Global olarak eski `:focus` ile çerçeveler temizlenir ve görünür focus tanımlanır.

## Skip Link (İçeriğe Atla)
Ekran okuyucu kullanıcıları, sayfa her açıldığında sitenizin Header'ındaki 25 tane menü elemanını ve logoyu dinlemek istemezler.
Body başlar başlamaz `position: absolute; left: -9999px` ile ekrandan kaçırılmış ancak `Tab` tuşuna bir kere basılınca üstten ortaya fırlayan "Ana İçeriğe Atla" (`<a href="#main-content">`) bağlantısı konmalıdır.

## Tabindex Mantığı
- `<button>`, `<a href>`, `<input>` varsayılan olarak zaten `tabindex=0` (klavye tab sırasına kendi doğal DOM sırası ile girer) değerindedir.
- Asla `<div tabindex="3">` şeklinde pozitif rakamlar verip doğal akışı çökertmeyin. Sadece div'i js ile (arka plandan) odakta tutmak istiyorsanız gizli indeks `-1` (`tabindex="-1"`) kullanın.

**İlgili Bağlantılar:**
- [[Erisilebilirlik-WCAG-ve-ARIA]]
- [[Tasarim-Psikolojisi-Gestalt-Hick]]