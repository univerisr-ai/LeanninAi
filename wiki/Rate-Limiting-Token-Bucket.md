# Rate Limiting ve Token Bucket Algoritması

API'nizin (Sunucunuzun) kötü niyetli veya kontrolden çıkmış isteklerle boğulmaması (DDoS / Brute Force) için konulan hız sınırlarıdır.

## Token Bucket (Jeton Kovası) Algoritması
Express.js ekosisteminde `express-rate-limit` veya Nginx gibi araçların arka planda kullandığı temel matematiksek mantık.
- Sistemin bir kovası var ve içinde X tane jeton bulunur (Örneğin 10 jeton).
- Her gelen API isteği bir jeton tüketir.
- Kova saniyede/dakikada sabit bir hızla yeniden dolar (Örneğin dakikada 5 jeton eklenir).
- Kova boşsa (Token bittiyse), sunucu 429 Too Many Requests (Çok Fazla İstek) hatası döner.
> Spiky (anlık patlama) trafiğe izin verirken ortalama kullanım hızını sabit tutar.

## Diğer Stratejiler
- **Coğrafi / IP Kısıtlaması (Geo-Blocking):** Spamin yoğun olduğu spesifik ülkelerin IP bloklarını reddetmek.
- **Fail2Ban:** Belirli bir hatayı art arda tekrar eden IP adresini (Örn: 5 kere yanlış şifre) Firewall seviyesinde kalıcı banlamak (`iptables` vasıtasıyla).

**İlgili Bağlantılar:**
- [[Bot-Tespiti-ve-Honeypot]]
- [[CORS-ve-Guvenlik-Headerlari]]
