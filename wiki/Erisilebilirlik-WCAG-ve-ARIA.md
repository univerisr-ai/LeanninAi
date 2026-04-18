# Erişilebilirlik: WCAG ve ARIA

## Meta
- category: a11y
- status: published


Web'in kapsayıcı olması (engelliler, klavye kullanıcıları vb.) için gözetilen yasal zorunluluğa giren standartlar bütünüdür.

## 4 Temel WCAG İlkesi (POUR)
1. Perceptible (Algılanabilir): Renk körü / görme engelliler dahi bilgiyi alabilmeli (Yüksek kontrast, img `alt` etiketleri).
2. Operable (Kullanılabilir): Fare bozukken sadece `Tab` tuşu ile sitede tüm işler bitirilebilmeli.
3. Understandable (Anlaşılabilir): Dil tanımlı olmalı (`<html lang="tr">`), hatalar betimleyici olmalı.
4. Robust (Sağlam): Modern ekran okuyucular DOM'u rahat okuyabilmeli.

## Klavye Navigasyonu ve Focus Yönetimi
Asla `*:focus { outline: none; }` yazıp odak göstergesini tamamen silmeyin! Engelliler nerede olduklarını göremezler. Doğru yöntem Modern CSS olan `:focus-visible` sözdizimini kullanmaktır (sadece klavye tıklamalarında devreye girer, fareyi etkilemez). Başka bir kural ise `tabindex` değerinin pozitif rakam (`1`, `2` vs.) atandığında tüm tarayıcı sekmelerini kilitlediği ve karmaşaya neden olduğu kuralıdır; sadece `0` (sıraya dahil et) ve `-1` (js target focus'u) kullanın.

## ARIA'nın Altın Kuralları
1. **Yerel HTML yeterliyse ARIA kullanma!** `<div role="button">` yerine doğal `<button>` kullanmalısın, çünkü enter, space tıklaması otomatik desteklenir.
2. **ARIA Görünmez Bir Dünyadır:** `aria-live="polite"` dinamik değişiklik durumlarını (örn, toast mesajını, sepet miktarını) okuyucuya fısıldarken; `aria-hidden="true"` (örn. sadece dekor ikonları) okuyucunun o HTML elementini tamamen görmezden gelmesini sağlar.
3. Dropdown, TabMenu, Dialog Modallarında standart WAI-ARIA kod kalıplarına harfi harfine uyulmalıdır.

**İlgili Bağlantılar:**
- [[Tasarim-Psikolojisi-Gestalt-Hick]]
- [[Klavye-Navigasyon-Focus]]

## 📚 İlgili Draftlar
- [[review/react-projelerinde-biraktigim-aliskanliklar-ve-kod-kalitem-neden-daha-iyi-oldu]]
- [[unicode-para-birimi-sembolleri-ve-u-20c3-uae-dirham-web-de-ozel-karakter-renderi]]