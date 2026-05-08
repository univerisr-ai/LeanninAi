# Shadow DOM ile Tooltip Renderlama: Iframe Alternatifi

## Meta
- status: published
- category: ui-ux
- confidence: 90
- novelty: 75
- model: qwen/qwen3-coder:free
- source: https://dev.to/palo_alto_ai/why-i-used-shadow-dom-instead-of-iframes-for-inline-tooltips-5d0m
- source_name: devto
- generated_at: 2026-05-08T03:45:38+00:00

## Ozet
Chrome eklentilerinde tooltip'ler için iframeler yerine Shadow DOM kullanılmasının avantajları. Stil izolasyonu, font uyumu ve senkron etkileşim gibi pratik uygulamalar.

## Ana Noktalar
- Shadow DOM, host sayfanın CSS'inin tooltip üzerine etki etmesini engeller.
- Tooltip içinde host sayfanın font bilgileri okunarak native görünüm sağlanır.
- Iframe'lerdeki FOUC (Flash of Unstyled Content) problemi yaşanmaz.
- Click ve drag gibi etkileşimler senkron çalışır, postMessage gecikmesi olmaz.
- JavaScript izolasyonu yoktur; güvenlik açısından dikkatli kullanılmalı.
- API istekleri doğrudan browser ile yapılır, ara sunucu kullanılmaz.

## Iliskili Sayfalar
- [[Erisilebilirlik-WCAG-ve-ARIA]]
- [[UI/UX Design: Gestalt, color theory, typography, micro-interactions, responsive design]]
- [[index]]
- [[review/index]]
- [[Tasarim-Psikolojisi-Gestalt-Hick]]
- [[Renk-Teorisi-ve-Tipografi]]

## Kaynak Basligi
Why I used shadow DOM instead of iframes for inline tooltips
