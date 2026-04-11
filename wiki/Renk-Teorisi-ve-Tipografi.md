# Renk Teorisi ve Tipografi

## Meta
- category: ui-ux
- status: published


Uygulamalı tasarım sisteminin arkasındaki temel matematik kuralları.

## HSL (Hue, Saturation, Lightness)
Geleneksel HEX (Örn: `#FF0000`) okuması zor ve manipülasyonu (matematiksel olarak rengini açma/koyultma) zordur. Modern tasarım sistemleri HSL kullanır.
`hsl(0, 100%, 50%) == Kırmızı`
- Rengi 10 birim açmak isterseniz L değerini `%60` yapmanız yeterlidir. CSS Custom Properties (Değişkenler) ve Dark Mode adaptasyonu için rakipsizdir.

## Modüler Tipografi (Type Scale)
Font boyutları "göze hoş gelen" rastgele px değerleri değil, Altın Oran veya Majör Üçlü gibi matematiksel dizilerle orantılı olarak büyütülmelidir (Tıpkı Müzikteki nota aralıkları gibi).
Genellikle `1.250` (Kök Oranı) kullanılır.
- 16px * 1.25 = 20px
- 20px * 1.25 = 25px
Bu sistem okunabilir ritim yaratır. Değerler CSS `clamp()` ile responsive (ekrana göre akışkan büyüyen) hale getirilmelidir.

**İlgili Bağlantılar:**
- [[Tasarim-Psikolojisi-Gestalt-Hick]]
- [[Erisilebilirlik-WCAG-ve-ARIA]]

## 📚 İlgili Draftlar
- [[review/unicode-para-birimi-sembolleri-ve-u-20c3-uae-dirham-web-de-ozel-karakter-renderi]]