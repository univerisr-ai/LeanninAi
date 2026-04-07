# CORS ve Güvenlik Headerları

Tarayıcının domain (Alan Adı) güvenliği prensiplerini yöneten Sunucu (Server) yanıt başlıklarıdır.

## CORS (Cross-Origin Resource Sharing)
Tarayıcıların, "A" sitesindeki JavaScript'in "B" sitesine istek (fetch/ajax) atmasını güvenli şekilde engellemesi (veya kabul etmesi) standardıdır. 
Eğer `www.benimsitem.com` üzerinden `api.seninsiten.com`'a istek geliyorsa, ve API tarafında origin (köken) kısıtlaması yoksa veri sızdırılmaz. Backend daima bir "Whitelist" (İzin verilen domainler listesi) tutmalı ve `Access-Control-Allow-Origin: www.benimsitem.com` olarak yanıt dönmelidir.

> Note: CORS bir backend önlemi değil, Tarayıcı (Browser) kısıtlamasıdır. Postman veya bir cURL botu CORS takmaz, çünkü tarayıcı değillerdir.

## Helmet.js Header Korumaları
Express uygulamalarında Helmet.js ile otomatik eklenen veya elle yazılması zorunlu header'lar:
1. **Content-Security-Policy (CSP):** Sitede hangi dış kaynaklardan script/resim okunabileceğini kısıtlar (Örn: Sadece kendi domainim ve google analytics JS'i çalışsın diyerek [[XSS-ve-CSRF-Açiklari]]'nı önler).
2. **Strict-Transport-Security (HSTS):** SSL Strip (Http'ye düşürme) saldırısını önler. Tarayıcıya "Artık beni sonsuza dek HTTPS ile aç" emrini verir.
3. **X-Frame-Options (DENY):** Clickjacking saldırısını önler. Sizin sitenizin başka bir sitede İframe `<iframe src="benimsitem">` içinde gizlice açılıp üzerine tıklatılmasını (Örn: banka havale butonu) imkansız hale getirir.

**İlgili Bağlantılar:**
- [[XSS-ve-CSRF-Açiklari]]
- [[JWT-ve-Kimlik-Dogrulama]]
