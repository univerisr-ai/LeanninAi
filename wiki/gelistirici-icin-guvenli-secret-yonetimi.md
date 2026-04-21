# Geliştirici İçin Güvenli Secret Yönetimi

## Meta
- status: published
- category: security
- confidence: 95
- novelty: 75
- model: qwen/qwen3-coder:free
- source: https://dev.to/21ideas/secret-management-for-vibe-coders-the-system-i-wish-i-had-a-year-ago-531o
- source_name: devto
- generated_at: 2026-04-21T03:35:17+00:00

## Ozet
Bu kavram, geliştiricilerin çevresel değişkenlerdeki gizli bilgileri doğru şekilde yönetmeleri, sınıflandırmaları ve döndürmeleri için pratik bir sistem sunar. Gerçek gizli anahtarlar, yapılandırma değerleri ve genel değişkenler arasında ayrım yaparak, şifre yöneticisinden üretim ortamına kadar üç katmanlı bir yaklaşım önerir.

## Ana Noktalar
- .env dosyasındaki tüm değerler gizli değildir; gerçek sırlar, konfigürasyonlar ve genel değişkenler şeklinde üçe ayrılmalıdır.
- Şifre yöneticiniz (Bitwarden, 1Password vb.) tek doğruluk kaynağı olmalı ve her projeye özel klasörler içermelidir.
- Üretim ortamındaki çevre değişkenleri yalnızca barındırma platformundan sağlanmalı ve uygulama tarafından doğrudan erişilmemelidir.
- Yerel geliştirme için .env.local dosyası kullanılmalı ve bu dosya git tarafından göz ardı edilmelidir.
- .env.example dosyası, gerçek değerler olmadan örnek yapılandırmayı paylaşmak için kullanılmalı ve versiyon kontrolüne dahil edilmelidir.

## Iliskili Sayfalar
- [[XSS-ve-CSRF-Açiklari]]
- [[JWT-ve-Kimlik-Dogrulama]]
- [[Rate-Limiting-Token-Bucket]]
- [[index]]
- [[review/index]]
- [[XSS-ve-CSRF-Açiklari]]
- [[CORS-ve-Guvenlik-Headerlari]]

## Kaynak Basligi
Secret Management for Vibe Coders: The System I Wish I Had a Year Ago
