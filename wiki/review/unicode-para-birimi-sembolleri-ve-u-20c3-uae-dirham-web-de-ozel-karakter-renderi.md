# Unicode Para Birimi Sembolleri ve U+20C3 UAE Dirham: Web'de Özel Karakter Renderı

## Meta
- status: draft-review
- category: frontend
- confidence: 85
- novelty: 78
- model: minimax/minimax-m2.7
- source: https://dev.to/pooyagolchian/the-uae-dirham-currency-symbol-u20c3-why-it-took-18-years-and-how-to-use-it-today-2aap
- source_name: devto
- generated_at: 2026-04-08T02:54:19+00:00

## Ozet
UAE Dirham sembolü (U+20C3) Unicode standardına 18 yıl sonra dahil edildi. Bu konsept, Unicode standardizasyon sürecini, web'de özel para birimi sembollerinin render edilmesini ve farklı framework'lerde (React, Web Components, vanilla JS) sembol desteği için npm paketlerinin nasıl kullanılacağını açıklar. Operating system desteği gelene kadar zero-migration stratejisi ile sembolün nasıl gösterileceğini gösterir.

## Ana Noktalar
- Unicode standardı yeni karakterlerin kabulü için 18 yıl gibi uzun bir süreç gerektirebilir
- U+20C3 UAE Dirham sembolü resmi olarak Unicode'a dahil edildi
- dirham npm paketi (v1.3.0) ile React, Web Components ve vanilla JS'de sembol render edilebilir
- Operating system seviyesinde destek gelene kadar fallback stratejisi gereklidir
- Para birimi sembolleri için i18n (internationalization) yaklaşımları önemlidir
- Zero-migration stratejisi ile mevcut kodbase'de breaking change olmadan sembol desteği eklenebilir
- Farklı platformlarda tutarlı sembol gösterimi için font ve encoding yönetimi gereklidir
- Para birimi sembolleri UX ve localization açısından kritik öneme sahiptir

## Iliskili Sayfalar
- [[Web Performansı ve PWA (Service Worker)]]
- [[Renk Teorisi ve Tipografi]]
- [[Modern React Desenleri]]
- [[Erişilebilirlik: WCAG ve ARIA]]

## Kaynak Basligi
The UAE Dirham Currency Symbol (U+20C3): Why It Took 18 Years and How to Use It Today
