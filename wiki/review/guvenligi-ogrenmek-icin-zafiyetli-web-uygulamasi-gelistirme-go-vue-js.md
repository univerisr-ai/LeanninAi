# Güvenliği Öğrenmek için Zafiyetli Web Uygulaması Geliştirme (Go + Vue.js)

## Meta
- status: draft-review
- category: frontend
- confidence: 90
- novelty: 85
- model: stepfun/step-3.5-flash:free
- source: https://dev.to/manuelarte/practicing-basic-concepts-on-web-security-5a9m
- source_name: devto
- generated_at: 2026-04-08T18:00:09+00:00

## Ozet
Bu makale, geliştiricilerin web güvenlik açıklarını (XSS, CSRF, SQL Enjeksiyonu vb.) pratik yoluyla öğrenmek için bilinçli olarak zafiyetli bir uygulama nasıl inşa edeceğini ve test edeceğini adım adım açıklar. Go (backend) ve Vue.js (frontend) kullanılarak yapılan bu 'build-and-break' yaklaşımı, teorik bilgiyi somut deneyimle pekiştirmeyi amaçlar.

## Ana Noktalar
- Güvenlik açıklarını anlamak için bilinçli olarak zafiyetli bir uygulama geliştirme felsefesi.
- Go (Gin) backend ve Vue.js frontend ile basit bir uygulama mimarisi oluşturma.
- Yaygın web açıkları (XSS, CSRF, SQL Enjeksiyonu, Dizin Gezintisi) uygulamada nasıl tetiklenir ve test edilir?
- Zafiyetleri 'break' aşamasında keşfetmek ve ardından 'fix' aşamasında düzeltmek.
- Güvenli kodlama alışkanlıkları geliştirmek için pratik, el yapımı bir laboratuvar ortamı oluşturma.
- Araçlar: Go (Gin), Vue.js, Postman (veya benzeri) API test aracı, tarayıcı geliştirici araçları.

## Iliskili Sayfalar
- [[index]]
- [[XSS-ve-CSRF-Açiklari]]
- [[CORS-ve-Guvenlik-Headerlari]]
- [[JWT-ve-Kimlik-Dogrulama]]
- [[Rate-Limiting-Token-Bucket]]

## Kaynak Basligi
Practicing Basic Concepts On Web Security
