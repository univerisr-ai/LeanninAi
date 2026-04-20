# Sicak Bellek (Hot Cache)

Bu bolum en son uretilen draft bilgisinin hizli ozetidir.

## Web Audio ile Hassas Zamanlama: setTimeout Yerine Lookahead Scheduler Kullanımı
→ [[review/web-audio-ile-hassas-zamanlama-settimeout-yerine-lookahead-scheduler-kullanimi]]

Bu makalede, web tabanlı bir metronom uygulamasında doğru zamanlama için neden setTimeout veya setInterval kullanılmaması gerektiği açıklanıyor. Bunun yerine Web Audio API'nin yüksek hassasiyetli zamanlamasını kullanan 'lookahead scheduling' yöntemi detaylandırılıyor. Bu yaklaşım, ses sentezleme işlemlerinde ana iş parçacığındaki gecikmelerden bağımsız olarak kesin zamanlamayı garanti altına alır.
- setTimeout/setInterval ana iş parçacığına bağlı olduğu için ses zamanlamasında sapmalara neden olur.
- Web Audio API, donanım saatinden bağımsız ve örnek bazında ilerleyen bir zamanlayıcı sunar.
- Lookahead scheduler, gelecekteki olayları önceden planlayarak ses senkronizasyonunu sağlar.

## StadiumSync: Canlı Stadyum Deneyimini Dönüştüren Gerçek Zamanlı Web Uygulaması
→ [[review/stadiumsync-canli-stadyum-deneyimini-donusturen-gercek-zamanli-web-uygulamasi]]

Stadyum etkinliklerinde gerçek zamanlı koordinasyon ve kullanıcı deneyimi sunan bir platform olan StadiumSync'in teknik yapısı ve tasarım yaklaşımı. React, Firebase ve glassmorphism tasarımın entegrasyonuyla büyük ölçekli etkinliklerde bilgi akışını optimize ediyor.
- Gerçek zamanlı veri senkronizasyonu için Firebase Firestore `onSnapshot` kullanımı
- Kod tabanlı giriş sistemi ile hesapsız, anında erişim imkanı
- Glassmorphism ve koyu tema ile stadyum ortamına uygun mobil-first arayüz tasarımı

## Next.js ile GitHub Pages Üzerinde Statik Portföy Sitesi Barındırma
→ [[review/next-js-ile-github-pages-uzerinde-statik-portfoy-sitesi-barindirma]]

Bu makalede, bir geliştiricinin Next.js kullanarak kişisel portföy sitesini nasıl oluşturduğunu ve GitHub Pages üzerinde statik dışa aktarım ile nasıl yayınladığını inceliyoruz. JSON tabanlı içerik yönetimi, alt dizin dağıtımları ve GitHub Actions entegrasyonu gibi pratik çözümler ele alınıyor.
- Next.js projeleri `output: 'export'` ayarı ile tamamen statik hale getirilebilir.
- GitHub Pages üzerinde barındırılan projelerde alt dizin yolları için `basePath` ve `assetPrefix` yapılandırmaları kritik öneme sahiptir.
- İçeriklerin JSX dışında JSON dosyalarında tutulması bakım süreçlerini kolaylaştırır.

## TanStack Query v5 ile Ölçeklenebilir Sunucu Durumu Yönetimi
→ [[review/tanstack-query-v5-ile-olceklenebilir-sunucu-durumu-yonetimi]]

TanStack Query v5'in sunduğu yeni API ve desenler sayesinde sunucu durumu yönetimi daha ölçeklenebilir hale geliyor. Bu içerikte, sürümdeki kritik değişiklikler, sorgu anahtarı fabrikaları, iyimser güncelleme stratejileri ve Suspense entegrasyonu ele alınıyor.
- Sunucu durumunu client durumu gibi işlemek uygunsuzdur; bu, veri tutarsızlıklarına ve yarış koşullarına neden olur.
- v5 sürümünde `isLoading` yerine `isPending`, tekil seçenek objesi ve daha iyi TypeScript desteği geldi.
- Sorgu anahtarlarını merkezileştirmek için key factory deseni öneriliyor; böylece önbellek geçersizleme işlemleri daha tutarlı oluyor.

## Klinik Asistanlarda Bellek Tabanlı Tasarım
→ [[review/klinik-asistanlarda-bellek-tabanli-tasarim]]

Bu makalede, klinik asistan sistemlerinde etkili bilgi yönetimi için bellek tabanlı bir mimari yaklaşım ele alınmaktadır. Geleneksel durumsuz sistemlerin zaman içinde bilgi kaybetme sorununa odaklanarak, yapılandırılmış olay tabanlı veri saklama ve geri çağırma ile doktorların hasta özetlerine daha etkili erişmesi sağlanmaktadır.
- Durumsuz sistemlerin uzun vadeli klinik akışlarda yetersiz kaldığı gözlemlenmiştir.
- Ziyaret notları yerine yapılandırılmış olaylar (medikasyon, taahhüt, kişisel detay vb.) saklanarak kalıcı bellek oluşturulmuştur.
- Hasta bazlı iş parçacıkları (thread) kullanılarak her hastanın kendi tarihçesi izole edilmiştir.

