# Minimal Bağımlılıklarla Beyaz Tahta Uygulaması Geliştirme

## Meta
- status: published
- category: ui-ux
- confidence: 95
- novelty: 75
- model: qwen/qwen3-coder:free
- source: https://dev.to/11suixing11/how-i-built-a-whiteboard-app-with-3-dependencies-bj3
- source_name: devto
- generated_at: 2026-05-08T03:46:26+00:00

## Ozet
Bu konsept, sadece 3 bağımlılık kullanarak geliştirilen performans odaklı bir beyaz tahta uygulamasının mimarisini ve teknik kararlarını açıklar. Canvas API, Zustand tabanlı durum yönetimi ve minimal bundle yaklaşımı ele alınır.

## Ana Noktalar
- Canvas API kullanılarak donanım hızlandırmalı çizim motoru geliştirildi
- Zustand ile 3 küçük depo (drawing, view, theme) ile durum yönetimi sağlandı
- SVG yerine Canvas tercih edilerek DOM ek yükü önlenildi
- Tailwind CSS ve React ile 160KB'lık gzipped bundle oluşturuldu
- Dokunmatik cihazlar ve masaüstü için responsive tasarım uygulandı
- LocalStorage ile otomatik kaydetme ve 50 adımlık geri alma/ileri alma özelliği eklendi

## Iliskili Sayfalar
- [[State-Yonetimi-Zustand-TanStack]]
- [[Renk-Teorisi-ve-Tipografi]]
- [[Web-Performansi-PWA]]
- [[index]]
- [[review/index]]
- [[Tasarim-Psikolojisi-Gestalt-Hick]]
- [[Renk-Teorisi-ve-Tipografi]]

## Kaynak Basligi
How I Built a Whiteboard App with 3 Dependencies
