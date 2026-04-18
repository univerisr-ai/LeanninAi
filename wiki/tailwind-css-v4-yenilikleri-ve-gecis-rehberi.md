# Tailwind CSS v4 Yenilikleri ve Geçiş Rehberi

## Meta
- status: published
- category: ui-ux
- confidence: 95
- novelty: 75
- model: qwen/qwen3-coder:free
- source: https://dev.to/whoffagents/tailwind-css-v4-what-actually-changed-and-how-to-migrate-without-breaking-everything-4f6h
- source_name: devto
- generated_at: 2026-04-13T03:29:24+00:00

## Ozet
Tailwind CSS v4, mimari olarak tamamen yeniden yazılmıştır. JS tabanlı yapılandırmayı bırakarak CSS-first bir yaklaşım benimsemiştir. Bu rehberde v4'teki kilit değişiklikler, yeni yapılandırma yöntemi, PostCSS entegrasyonu, içerik tespiti ve mevcut projeye geçiş adımları açıklanmaktadır.

## Ana Noktalar
- Yapılandırma artık CSS dosyasında `@theme` bloğu ile tanımlanır.
- `tailwind.config.js` dosyası kaldırılmıştır.
- Lightning CSS motoru ile derleme süreleri kısalır.
- Tüm tasarım token’ları otomatik olarak CSS değişkenlerine çevrilir.
- PostCSS eklentisi güncellenmeli ve autoprefixer artık gerekli değildir.
- İçerik dosyaları otomatik olarak algılanır; manuel içerik yolu belirtmeye gerek yoktur.
- Özel eklentiler artık `@plugin` direktifi ile CSS içinde tanımlanır.
- Mevcut JS tabanlı eklentilerin güncellenmesi gerekebilir.

## Iliskili Sayfalar
- [[review/index]]
- [[review/index]]
- [[Tasarim-Psikolojisi-Gestalt-Hick]]
- [[Renk-Teorisi-ve-Tipografi]]

## Kaynak Basligi
Tailwind CSS v4: What Actually Changed and How to Migrate Without Breaking Everything
