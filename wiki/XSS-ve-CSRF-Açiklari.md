# XSS ve CSRF Açıkları

Web güvenliğinin en yaygın ve tehlikeli iki cephesidir. Biri tarayıcı tarafındaki güveni kötüye kullanırken diğeri sunucunun kimlik bağlamını yanıltır.

## XSS (Cross-Site Scripting)
Saldırganın uygulamanıza zararlı JavaScript kodu enjekte edip, o kodu diğer kullanıcıların tarayıcısında çalıştırmasıdır.
- **Stored XSS:** Zararlı kod DB'ye kalıcı kaydedilir (örn. yorum kısmına `<script>`). Çok tehlikelidir.
- **Savunma:** 
  1. Sunucu Tarafı: `DOMPurify` gibi kütüphaneler ile gelen HTML sanitizasyonu (temizleme).
  2. Frontend Tarafı: Veriyi React gibi otomatik escape eden framework'lerle veya Native'de `element.innerHTML` yerine `element.textContent` ile basmak.
  3. Header Koruması: CSP (Content-Security-Policy) ayarlanarak dış kaynaklı JS çalıştırmak engellenmelidir ([[CORS-ve-Guvenlik-Headerlari]]).

## CSRF (Cross-Site Request Forgery)
Kullanıcının başka bir sitedeyken (evil.com) kendi haberi olmadan bankası.com hesabına arka planda POST isteği attırılmasıdır (Tarayıcı HttpOnly cookie'leri otomatik yollar).

- **Savunma:**
  - **Double Submit Cookie Pattern:** Sunucu bir CSRF Token üretir. Bunu hem cookie (js ile okunabilir) hem de değişkende yollar. Frontend formu POST ederken bu token'ı `X-CSRF-Token` header'ı ile gönderir. Sunucu, header'daki değer ile cookie'dekini karşılaştırır. Saldırgan cookie'yi okuyamayacağı için (evil.com üzerinden okuma yapılamaz) header'ı doğru set edemez ve istek reddedilir.
  - Veya Cookie özelliğinizi `SameSite=Strict` yaparak çözebilirsiniz.

**İlgili Bağlantılar:**
- [[JWT-ve-Kimlik-Dogrulama]]
- [[CORS-ve-Guvenlik-Headerlari]]

## 📚 İlgili Draftlar
- [[review/guvenligi-ogrenmek-icin-zafiyetli-web-uygulamasi-gelistirme-go-vue-js]]
