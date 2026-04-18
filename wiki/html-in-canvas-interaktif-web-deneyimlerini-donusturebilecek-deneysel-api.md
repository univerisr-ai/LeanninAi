# HTML-in-Canvas: İnteraktif Web Deneyimlerini Dönüştürebilecek Deneysel API

## Meta
- status: published
- category: ui-ux
- confidence: 90
- novelty: 75
- model: qwen/qwen3-coder:free
- source: https://dev.to/andresclua/html-in-canvas-the-api-that-could-change-how-we-build-interactive-experiences-on-the-web-1435
- source_name: devto
- generated_at: 2026-04-18T02:54:41+00:00

## Ozet
Bu konsept, henüz deneysel aşamada olan HTML-in-Canvas API'sini tanıtıyor. Bu yeni yaklaşım, HTML elementlerinin doğrudan <canvas> içerisine yerleştirilerek hem görsel performansın korunmasını hem de erişilebilirlik, form elemanları ve metin seçimi gibi native tarayıcı özelliklerinden vazgeçilmeden zengin interaktif deneyimler oluşturulmasını sağlıyor.

## Ana Noktalar
- HTML-in-Canvas, WICG tarafından önerilen ve şu anda yalnızca Chrome Canary'de aktif edilebilen deneysel bir özelliktir.
- Temel amaç, canvas üzerinde çizilen içeriklerde erişilebilirlik, form elemanları ve metin işlemleri gibi HTML'in sunduğu avantajlardan faydalanabilmektir.
- Üç temel yapı taşından oluşur: `layoutsubtree` özelliği, `drawElementImage()` metodu ve `paint` olayı.
- `layoutsubtree` özelliği sayesinde canvas altındaki HTML elementleri gerçek layout sürecine dahil olur ancak doğrudan ekrana çizilmez.
- `drawElementImage()` ile bu elementler canvas üzerine koordinat bazında çizilirken, aynı zamanda erişilebilirlik ağacı ve hit-testing senkronize tutulur.
- `paint` olayı, requestAnimationFrame yerine daha verimli ve doğru zamanlamada yeniden çizim yapılabilmesini sağlar.

## Iliskili Sayfalar
- [[Erisilebilirlik-WCAG-ve-ARIA]]
- [[Web-Performansi-PWA]]
- [[Tasarim-Psikolojisi-Gestalt-Hick]]
- [[index]]
- [[review/index]]
- [[Tasarim-Psikolojisi-Gestalt-Hick]]
- [[Renk-Teorisi-ve-Tipografi]]

## Kaynak Basligi
HTML in Canvas: The API That Could Change How We Build Interactive Experiences on the Web
