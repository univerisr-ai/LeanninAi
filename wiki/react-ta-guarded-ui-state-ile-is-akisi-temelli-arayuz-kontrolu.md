# React'ta Guarded UI State ile İş Akışı Temelli Arayüz Kontrolü

## Meta
- status: published
- category: ui-ux
- confidence: 90
- novelty: 75
- model: qwen/qwen3-coder:free
- source: https://dev.to/alexey79/when-disabled-is-not-enough-building-guarded-ui-state-in-react-cge
- source_name: devto
- generated_at: 2026-05-09T03:37:29+00:00

## Ozet
Karmaşık React uygulamalarında isLoading durumunun yetersiz kaldığı senaryolarda, iş akışlarını temsilen adlandırılmış kapsamlar oluşturarak UI kontrollerinin davranışlarını merkezi şekilde yönetmek için 'guarded UI state' yaklaşımı. Bu yöntem, disabled veya loading gibi durumların yalnızca yüzeysel kalmasının ötesine geçerek, her kontrolün bağlamına özel tepkiler tanımlamayı sağlar.

## Ana Noktalar
- isLoading yalnızca yerel bileşenler için yeterlidir; iş akışları genişledikçe anlam ifade etmez.
- react-action-guard ile iş akışlarına isimlendirilmiş kapsamlar atanır ve bu kapsamların blokaj durumu takip edilir.
- react-action-guard-ui ile bu blokaj durumu farklı UI kontrollerine bağlamsal olarak çevrilir (buton disable, input readonly, link navigation engelleme vs.).
- Core state (iş akışı gerçekliği) ile UI state (kontrol gösterimi) ayrımı yapılarak daha sürdürülebilir ve açıklayıcı UI mimarisi oluşturulur.
- Erişilebilirlik açısından da faydalıdır: screen reader kullanıcılarına neden engellendiği bildirilebilir.

## Iliskili Sayfalar
- [[Modern-React-Desenleri]]
- [[Erisilebilirlik-WCAG-ve-ARIA]]
- [[index]]
- [[review/index]]
- [[Tasarim-Psikolojisi-Gestalt-Hick]]
- [[Renk-Teorisi-ve-Tipografi]]

## Kaynak Basligi
When disabled is not enough: Building guarded UI state in React
