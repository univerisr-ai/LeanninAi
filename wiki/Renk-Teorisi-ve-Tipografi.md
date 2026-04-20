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
- [[review/tailwind-css-v4-yenilikleri-ve-gecis-rehberi]]
- [[review/tasarim-becerisi-olmadan-minimalist-ui-olusturmak-flickle-ornegi]]
- [[review/ai-ile-oyun-ve-uygulama-icin-telifsiz-muzik-uretimi]]
- [[review/angular-icin-gercekci-ui-bileseni-destegi]]
- [[review/tek-json-dan-coklu-cikti-uretimi-design-token-pipeline]]
- [[review/html-den-markdown-a-donusturerek-llm-maliyetlerini-azaltmak]]
- [[review/html-in-canvas-interaktif-web-deneyimlerini-donusturebilecek-deneysel-api]]
- [[review/3d-portfolyo-tasarimi-react-three-fiber-ve-next-js-ile-interaktif-gunes-sistemi]]
- [[review/ai-destekli-erisilebilirlik-uyumlulugu-icin-saas-gelistirme-axle-ornegi]]
- [[review/ai-powered-blogging-platform-tam-otomatik-icerik-uretimi-ve-yayin-akisi]]
- [[review/coklu-web-sitesi-yonetimi-40-ozelligi-merkezi-veri-ve-otomasyonla-yonetmek]]
- [[review/roastttp-http-durum-kodlarini-eglenceli-terminal-bildirimleriyle-goruntuleme]]
- [[review/smoothui-animasyonlu-react-bilesenleri-ve-hareket-tasarimi]]
- [[review/tarayici-tabanli-gelistirici-araclari-dev-toolbox-mimarisi]]
- [[review/woocommerce-sabit-ceviri-glosarisi-ile-etiket-tutarliligi]]
- [[review/oyun-motoru-secimi-web-ve-mobil-uyumlu-gelistirme-stratejileri]]
- [[review/stadiumsync-canli-stadyum-deneyimini-donusturen-gercek-zamanli-web-uygulamasi]]
- [[review/web-audio-ile-hassas-zamanlama-settimeout-yerine-lookahead-scheduler-kullanimi]]