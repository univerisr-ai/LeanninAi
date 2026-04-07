# Tasarım Psikolojisi: Gestalt ve Hick

Arayüz (UI) tasarımı dekorasyon değil, insan beyninin bilgiyi algılama sisteminin manipülasyonudur.

## Gestalt Algı Yasaları

Kullanıcılar tekil elemanları değil, deseni (pattern) algılarlar:
1. **Yakınlık (Proximity):** Birbirine yakın elemanlar aynı grubun parçası kabul edilir. Form etiketleri (label) kendi input'una çok yakın (4px), diğer gruba uzak (32px) olmalıdır. Boşluk (Whitespace) en büyük gruplama aracıdır.
2. **Benzerlik (Similarity):** Aynı renk, şekil ve tipografiye sahip öğeler işlevsel olarak bağlı zannedilir.
3. **Süreklilik (Continuity):** Göz, belirli bir diyagram veya hiyerarşi hattını takip eder.

## Karar Vermenin Matematiği
- **Hick Yasası:** Ekranda gösterilen seçenek sayısı arttıkça kullanıcının karar verme süresi **logaritmik** olarak uzar. Bu yüzden arayüzde nadir kullanılan toollar "Üç nokta" dropdown'ı arkasına saklanmalı, sadece birincil (Primary Button) ve ikincil eylemler açıkta bırakılmalıdır.
- **Fitts Yasası:** Hedef (Buton) ne kadar küçük ve fare imlecine/parmağa ne kadar uzaksa, Oraya tıklamak o kadar yavaşlar. Mobilde minimum tıklama/dokunma hedefi **44x44px** / **48x48px** arasında olmalıdır. Tehlikeli eylemler (Örn: Hesabı Sil) kazara tıkı önlemek için özellikle küçük ve menü içinde uzak köşelere konulur.

**İlgili Bağlantılar:**
- [[Renk-Teorisi-ve-Tipografi]]
- [[Erisilebilirlik-WCAG-ve-ARIA]]
