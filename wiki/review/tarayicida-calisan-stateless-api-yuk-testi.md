# Tarayıcıda Çalışan Stateless API Yük Testi

## Meta
- status: draft-review
- category: frontend
- confidence: 78
- novelty: 72
- model: minimax/minimax-m2.7
- source: https://dev.to/taranbir_singh_6199c3c9bb/how-i-built-a-stateless-api-load-tester-that-runs-in-your-browser-no-setup-required-33i1
- source_name: devto
- generated_at: 2026-04-08T02:56:55+00:00

## Ozet
Modern tarayıcıların Web Worker ve parallel fetch API'lerini kullanarak sunucuya bağımlılık olmadan stateless API yük testi gerçekleştirmeyi sağlayan istemci taraflı bir test aracı geliştirme sürecini anlatır.

## Ana Noktalar
- Web Worker'lar ile ana thread'i bloke etmeden arka planda eşzamanlı istekler gönderme
- BroadcastChannel API ile stateless durum yönetimi
- Tarayıcının native fetch API'si ile parallel connection limitlerini test etme
- Sonuçların real-time toplanması ve istatistiklerin hesaplanması
- CORS politikalarının tarayıcı taraflı test üzerindeki etkisi ve preflight davranışları
- Heap memory kontrolü ile büyük payload'ların yönetimi
- Worklet ve SharedArrayBuffer kullanımı ile performans optimizasyonu

## Iliskili Sayfalar
- [[Web Performansı ve PWA (Service Worker)]]
- [[CORS ve Güvenlik Headerları]]
- [[Rate Limiting ve Token Bucket Algoritması]]

## Kaynak Basligi
How I Built a Stateless API Load Tester That Runs in Your Browser (No Setup Required)
