# Vercel Güvenlik İhlali: Üçüncü Taraf AI Entegrasyonundan Kaynaklı Sızıntı

## Meta
- status: published
- category: security
- confidence: 95
- novelty: 75
- model: qwen/qwen3-coder:free
- source: https://dev.to/om_shree_0709/vercel-just-confirmed-a-security-breach-heres-what-actually-got-exposed-and-why-its-bigger-pon
- source_name: devto
- generated_at: 2026-04-20T03:41:48+00:00

## Ozet
Vercel'in Nisan 2026'da açıkladığı güvenlik ihlali, üçüncü taraf bir AI aracının Google Workspace OAuth uygulamasından kaynaklanmıştır. Bu durum, modern SaaS mimarilerinde güvenliğin yalnızca dış perdeyi değil, aynı zamanda entegre araçları da kapsaması gerektiğini göstermektedir. İhmal edilen bu saldırı vektörü özellikle geliştiriciler ve DevOps ekipleri için önemli dersler barındırmaktadır.

## Ana Noktalar
- İhlal doğrudan Vercel altyapısına yönelik değildi; üçüncü parti bir AI aracı üzerinden gerçekleşti.
- Google Workspace OAuth entegrasyonu saldırıya açık hale gelmişti.
- ShinyHunters adlı gruptan 580 çalışan kaydı ele geçirildiği iddia edildi.
- API anahtarları ve NPM token’larının tehlikeye girdiği bildirildi.
- Linear ve GitHub entegrasyonlarının saldırıya uğradığı belirtildi.

## Iliskili Sayfalar
- [[XSS-ve-CSRF-Açiklari]]
- [[JWT-ve-Kimlik-Dogrulama]]
- [[Rate-Limiting-Token-Bucket]]
- [[Bot-Tespiti-ve-Honeypot]]
- [[index]]
- [[review/index]]
- [[XSS-ve-CSRF-Açiklari]]
- [[CORS-ve-Guvenlik-Headerlari]]

## Kaynak Basligi
Vercel Just Confirmed a Security Breach. Here's What Actually Got Exposed — and Why It's Bigger Than One Company.
