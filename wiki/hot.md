# Sicak Bellek (Hot Cache)

Bu bolum en son uretilen draft bilgisinin hizli ozetidir.

## Turbo 8 Morphing ile Rails Frontend Geliştirme
→ [[review/turbo-8-morphing-ile-rails-frontend-gelistirme]]

Turbo 8'in yeni morfolojik güncelleme özelliği sayesinde, Rails uygulamalarında dinamik arayüz güncellemeleri artık daha kolay hale geldi. Bu teknik, geleneksel Turbo Stream yöntemlerine alternatif olarak, tam sayfa yenilemesi yapmadan yalnızca değişen HTML bölümlerini akıllıca güncelleyerek kullanıcı deneyimini artırıyor.
- Turbo 8 ile birlikte gelen 'Page Morphing', DOM üzerinde sadece değişen kısımları güncelliyor.
- Bu yöntem, scroll pozisyonunu koruyarak ve form içeriklerini silmeden akıcı geçişler sağlıyor.
- Geliştiricilerin manuel olarak yazdığı birçok `.turbo_stream.erb` dosyasını ortadan kaldırabiliyor.

## Prompt Mühendisliği: Takımlar İçin Prompt Kütüphanesi Oluşturma ve Yönetme
→ [[review/prompt-muhendisligi-takimlar-icin-prompt-kutuphanesi-olusturma-ve-yonetme]]

Yazılım ekiplerinin yapay zeka prompt'larını etkili biçimde organize etme, sürüm kontrolüne alma ve işbirlikçi bir şekilde yönetme stratejilerini açıklar. Prompt dosya formatları, kategorizasyon yöntemleri ve sürüm kontrolü gibi konuları kapsar.
- Prompt kütüphaneleri, tekrarlamayı azaltır, tutarlılığı artırır ve bilgi kaybını önler.
- Prompt’lar model bazında değil, işlevsel kategorilere göre düzenlenmelidir (örn. /code-review/, /content/).
- Her prompt standartlaştırılmış bir formatta (YAML + Markdown) saklanmalı ve sürüm bilgilerini içermelidir.

## AI Destekli Kod İnceleme İş Akışları: Güvenlik ve Kalite Odaklı Prompt Mühendisliği
→ [[review/ai-destekli-kod-inceleme-is-akislari-guvenlik-ve-kalite-odakli-prompt-muhendisligi]]

Bu makale, GPT-4 ve Claude gibi büyük dil modellerini kullanarak otomatik kod inceleme iş akışları oluşturma yöntemlerini açıklar. Özellikle güvenlik zaafları, kod kalitesi ve stil tutarlılığı olmak üzere üç katmanlı bir inceleme mimarisi önerilir. Her katman için özel olarak hazırlanmış prompt tasarımları sunularak, AI destekli statik analiz süreçlerinin nasıl daha etkili hale getirileceği detaylandırılır.
- Manuel kod incelemelerinin verimliliğini artırmak için AI kullanımı, %50 oranında gözden kaçan hataları yakalayabilir.
- AI kod incelemelerinin etkinliği tamamen kullanılan prompt kalitesine bağlıdır.
- Üç katmanlı inceleme mimarisi: Güvenlik, Kalite ve Stil kontrolü için ayrı prompt’lar önerilmiştir.

## Eco-Web Auditor
→ [[review/eco-web-auditor]]

Eco-Web Auditor, web sitelerinin dijital sürdürülebilirliğini ölçmek için geliştirilmiş bir araçtır. 20 farklı ekolojik metriği değerlendirerek, geleneksel performans araçlarının göz ardı ettiği 'yeşil tasarım' kriterlerine odaklanır. Araç, kullanıcıya hem skor hem de uygulanabilir teknik öneriler sunarak web'in karbon ayak izini azaltmayı hedefler.
- 20 farklı dijital sürdürülebilirlik metriğini analiz eder.
- Lighthouse ve PageSpeed Insights gibi araçların eksik bıraktığı yönleri ele alır.
- Zombie kod, yeşil hosting ve enerji verimli tasarım gibi kriterleri içerir.

## Auth Migrations: Oturum Stratejisi ile Kimlik Doğrulama Geçişi
→ [[review/auth-migrations-oturum-stratejisi-ile-kimlik-dogrulama-gecisi]]

Bu makale, kimlik doğrulama geçişlerinin genellikle sağlayıcı seçiminden ziyade oturum davranışlarıyla ilgili sorunlar nedeniyle başarısız olduğunu açıklar. Gerçek kullanıcı deneyimini etkileyen oturum yaşam döngüsünü planlamanın önemine değinir.
- Kimlik doğrulama geçişlerinin başarısı, sağlayıcıdan çok oturum davranışına bağlıdır.
- Kullanıcılar, giriş ekranındaki değişiklikleri değil, oturum sürekliliğini hisseder.
- Oturum yaşam döngüsü: oluşturma, yenileme, düşürme, iptal etme ve sonlandırma süreçleri önceden tanımlanmalıdır.

