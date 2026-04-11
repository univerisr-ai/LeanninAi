# JWT ve Kimlik Doğrulama

## Meta
- category: security
- status: published


JSON Web Token (JWT), durumsuz (stateless) kimlik doğrulama için endüstri standardıdır, ancak frontend'de güvenli şekilde saklanması her zaman büyük bir tartışma konusudur.

## Güvenli JWT Mimarisi (İkili Sistem)
Asla tek bir uzun ömürlü token kullanmayın. Mimari ikiye ayrılır:

1. **Access Token (Erişim Token'ı):**
   - **Ömrü:** Çok kısa (Örn: 10-15 dakika).
   - **Kullanımı:** API'lere yapılan her istekte `Authorization: Bearer <token>` başlığında gönderilir.
   - **Saklama Yeri (Frontend):** SADECE Javascript belleğinde (memory, örn. Zustand state içinde). Asla `localStorage` veya `sessionStorage` içine yazmayın, XSS anında çalınır! (Bkz: [[XSS-ve-CSRF-Açiklari]])

2. **Refresh Token (Yenileme Token'ı):**
   - **Ömrü:** Uzun (Örn: 7 gün veya 1 ay).
   - **Kullanımı:** Sadece Access token'ın süresi dolduğunda, yeni bir Access Token almak için (örn. `/api/refresh`) kullanılır.
   - **Saklama Yeri:** **HttpOnly, Secure, ve SameSite=Strict** bayraklarıyla işaretlenmiş bir çerez (cookie) içinde saklanmalıdır. Böylece Javascript kodları kesinlikle bu cookie'yi okuyamaz (çalınmaz) ve sadece yenileme endpoint'i ile sunucuya taşınır.

## Şifreleme (Argon2id)
Kullanıcıların şifreleri veritabanında ASLA düz metin veya MD5/SHA-256 ile tutulmamalıdır.
Brute-force ve GPU saldırılarına karşı piyasadaki modern algoritma **Argon2id** olmalıdır. Çünkü Argon2 sadece işlemci zamanı değil, RAM (bellek tüketimi) parametresi de isteyerek otomatik saldırı maliyetlerini tavana vurdurur.

**İlgili Bağlantılar:**
- [[CORS-ve-Guvenlik-Headerlari]]
- [[State-Yonetimi-Zustand-TanStack]]

## 📚 İlgili Draftlar
- [[review/ai-saas-baslangic-kiti-mimarisi-tekrarlanan-kurulum-sureclerini-otomatiklestirme]]
- [[review/guvenligi-ogrenmek-icin-zafiyetli-web-uygulamasi-gelistirme-go-vue-js]]