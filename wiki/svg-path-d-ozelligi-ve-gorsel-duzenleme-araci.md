# SVG Path d Özelliği ve Görsel Düzenleme Aracı

## Meta
- status: published
- category: ui-ux
- confidence: 95
- novelty: 75
- model: qwen/qwen3-coder:free
- source: https://dev.to/sendotltd/i-finally-understand-the-svg-d-attribute-because-i-built-an-editor-for-it-5b74
- source_name: devto
- generated_at: 2026-04-22T03:25:10+00:00

## Ozet
Bu makalede SVG path öğesinin d özelliği detaylı olarak açıklanmakta ve bu özelliği anlamayı kolaylaştıran interaktif bir düzenleyici tanıtılıyor. Yazar, SVG yol komutlarını öğrenmek için küçük bir görsel editör geliştirerek karmaşık d dizgesini anlaşılır hale getirmiş ve bu süreçte SVG yol dilbilgisinin kritik yönlerini keşfetmiştir.

## Ana Noktalar
- SVG path d özelliği, sanal bir kalemin çizim talimatlarından oluşan bir dizgesidir.
- Komutlar büyük/küçük harfe duyarlıdır; büyük harfler mutlak, küçük harfler göreli koordinatlardır.
- H, V, S, T gibi kısa komutlar daha temel komutların kısaltmalarıdır.
- M komutu ardışık koordinat çiftleri aldığında yalnızca ilki hareket (moveto), diğerleri çizgi (lineto) komutudur.
- Yazar tarafından geliştirilen düzenleyici sayesinde SVG yolları görsel olarak manipüle edilebilir ve gerçek zamanlı d çıktısı alınabilir.
- Editör Svelte 5, TypeScript ve Vite kullanılarak sıfır bağımlılıkla yazılmıştır.

## Iliskili Sayfalar
- [[Renk-Teorisi-ve-Tipografi]]
- [[index]]
- [[review/index]]
- [[Tasarim-Psikolojisi-Gestalt-Hick]]
- [[Renk-Teorisi-ve-Tipografi]]

## Kaynak Basligi
I Finally Understand the SVG d Attribute — Because I Built an Editor for It
