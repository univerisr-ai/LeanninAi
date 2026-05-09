# Sicak Bellek (Hot Cache)

Bu bolum en son uretilen draft bilgisinin hizli ozetidir.

## React'ta Guarded UI State ile İş Akışı Temelli Arayüz Kontrolü
→ [[review/react-ta-guarded-ui-state-ile-is-akisi-temelli-arayuz-kontrolu]]

Karmaşık React uygulamalarında isLoading durumunun yetersiz kaldığı senaryolarda, iş akışlarını temsilen adlandırılmış kapsamlar oluşturarak UI kontrollerinin davranışlarını merkezi şekilde yönetmek için 'guarded UI state' yaklaşımı. Bu yöntem, disabled veya loading gibi durumların yalnızca yüzeysel kalmasının ötesine geçerek, her kontrolün bağlamına özel tepkiler tanımlamayı sağlar.
- isLoading yalnızca yerel bileşenler için yeterlidir; iş akışları genişledikçe anlam ifade etmez.
- react-action-guard ile iş akışlarına isimlendirilmiş kapsamlar atanır ve bu kapsamların blokaj durumu takip edilir.
- react-action-guard-ui ile bu blokaj durumu farklı UI kontrollerine bağlamsal olarak çevrilir (buton disable, input readonly, link navigation engelleme vs.).

## React ile Sekme Bildirimleri: Dikkat Çekici Sekme Tasarımı
→ [[review/react-ile-sekme-bildirimleri-dikkat-cekici-sekme-tasarimi]]

Bu konsept, React uygulamalarında kullanıcı dikkatini çekmek için tarayıcı sekmesi başlığını, favicon'u ve bildirimleri etkili şekilde nasıl kullanacağınızı öğretir. ReactUse kütüphanesinden useTitle gibi özel hook'lar sayesinde sekme bazlı kullanıcı deneyimi stratejileri geliştirilir.
- Tarayıcı sekmesi başlığı, favicon ve bildirimler kullanıcıyı geri çekmek için kritik yüzeylerdir.
- React bileşenlerinde document.title kullanımında dikkatli olunmalı, aksi halde başlık çakışmaları yaşanabilir.
- ReactUse kütüphanesindeki useTitle gibi hook’lar, sekme başlığını güvenli ve verimli yönetir.

## Çoklu Rol Yönetimi ile Güvenli Admin Paneli: React ve Express Üzerine Katmanlı Yetkilendirme
→ [[review/coklu-rol-yonetimi-ile-guvenli-admin-paneli-react-ve-express-uzerine-katmanli-yetkilendirme]]

Bu konsept, React ve Express kullanılarak geliştirilen çoklu rol tabanlı bir admin panelinde güvenliği nasıl üst düzeye çıkaracağınızı açıklar. JWT tabanlı kimlik doğrulama, hibrit API mimarisi ve çift katmanlı yetkilendirme stratejileri ele alınır.
- JWT ile kullanıcı rolü ve hostelId bilgilerinin şifreli şekilde iletilmesi
- Frontend'de rota bazlı koruma ile kullanıcı deneyimi güvenliği
- Backend'de doğrudan API erişimini engellemek için katmanlı yetkilendirme

## Tesseract-8D/128: Deneysel TypeScript Şifreleme Algoritması
→ [[review/tesseract-8d-128-deneysel-typescript-sifreleme-algoritmasi]]

Tesseract-8D/128, 8 boyutlu durum uzayında bayt dönüşümleri yapan deneysel bir şifreleme algoritmasıdır. Bu proje, kriptografik kavramları öğretmek ve görsel yapıların şifreleme süreçlerine nasıl entegre edilebileceğini araştırmak amacıyla geliştirilmiştir. Güvenlik sağlamayı hedeflememektedir ancak kriptografi eğitimi açısından değerli bir araçtır.
- 8 boyutlu durum uzayında her bayt bir koordinatla temsil edilir.
- Şifreleme süreci boyunca koordinatlar dönüşümler, permütasyonlar ve difüzyon ile işlenir.
- Algoritma, simetrik şifreleme, S-Box, nonce, avalanche etkisi gibi kavramları öğretmeyi amaçlar.

## AI Agent Varlıklarını Seçmeli Olarak Yönetmek: agent-harness
→ [[review/ai-agent-varliklarini-secmeli-olarak-yonetmek-agent-harness]]

agent-harness, farklı AI destekli geliştirme ortamlarında (VS Code, Cursor, Claude vb.) yeniden kullanılabilir AI agent varlıklarını seçmeli ve kontrollü şekilde entegre etmeye yardımcı olan Node.js/TypeScript tabanlı bir CLI aracıdır. Bu araç, büyük ve genel amaçlı AI beceri paketlerinden ziyade, daha dar kapsamlı ve kontrollü içerik yönetimi sunar.
- AI agent varlıklarının keşfi, hazırlanması, kurulumu ve etkinleştirilmesi için yaşam döngüsü yönetimi sağlar.
- VS Code, GitHub Copilot, Cursor, Claude Code gibi araçlarla uyumlu çalışır.
- Büyük AI beceri paketlerinin yol açtığı bağlama karmaşasını önler.

