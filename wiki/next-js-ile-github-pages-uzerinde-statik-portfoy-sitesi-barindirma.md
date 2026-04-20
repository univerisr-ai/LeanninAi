# Next.js ile GitHub Pages Üzerinde Statik Portföy Sitesi Barındırma

## Meta
- status: published
- category: frontend
- confidence: 95
- novelty: 72
- model: qwen/qwen3-coder:free
- source: https://dev.to/mehtab_riaz_bdb7e6c61115f/i-shipped-my-developer-portfolio-on-github-pages-with-nextjs-static-export-1e74
- source_name: devto
- generated_at: 2026-04-20T03:35:17+00:00

## Ozet
Bu makalede, bir geliştiricinin Next.js kullanarak kişisel portföy sitesini nasıl oluşturduğunu ve GitHub Pages üzerinde statik dışa aktarım ile nasıl yayınladığını inceliyoruz. JSON tabanlı içerik yönetimi, alt dizin dağıtımları ve GitHub Actions entegrasyonu gibi pratik çözümler ele alınıyor.

## Ana Noktalar
- Next.js projeleri `output: 'export'` ayarı ile tamamen statik hale getirilebilir.
- GitHub Pages üzerinde barındırılan projelerde alt dizin yolları için `basePath` ve `assetPrefix` yapılandırmaları kritik öneme sahiptir.
- İçeriklerin JSX dışında JSON dosyalarında tutulması bakım süreçlerini kolaylaştırır.
- Dinamik veriler derleme zamanında `getStaticProps` ile çekilerek statik siteye entegre edilmelidir.
- SVG favicon kullanımında Chromium uyumsuzlukları yaşanabilir; bitmap veri URI’leri tercih edilmelidir.

## Iliskili Sayfalar
- [[Next.js]]
- [[Web-Performansi-PWA]]
- [[React Formlarında Performans Optimizasyonu: Schepta Örneği]]
- [[index]]
- [[review/index]]
- [[Modern-React-Desenleri]]
- [[Web-Performansi-PWA]]

## Kaynak Basligi
I shipped my developer portfolio on GitHub Pages with Next.js static export
