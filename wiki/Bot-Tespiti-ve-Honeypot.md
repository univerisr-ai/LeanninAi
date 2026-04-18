# Bot Tespiti ve Honeypot (Bal Küpü)

## Meta
- category: security
- status: published


Scraping (veri kazıma) ve Spam form doldurma botlarına karşı savunma mekanizmalarıdır.

## Honeypot (Görünmez Form)
CAPTCHA'yı sevmeyen gerçek kullanıcılara (UX dostu) rahatsızlık vermemek için arka planda konulan tuzak.
- E-posta veya iletişim formuna "telefon_numarasi" adında bir input koyulur.
- CSS ile insan gözünden gizlenir (`display: none`, `opacity: 0` veya `absolute left: -9999px`).
- Normal bir insan bunu görmediği için boş bırakır. Ancak otomatik okuma ve doldurma yapan spambotlar, kodu okudukları için bu alanı da "doldurur".
- Backend bu alanı `if (req.body.telefon_numarasi) return Error;` olarak kontrol edip botları engeller. 

## Headless Browser Tespiti
Puppeteer, Playwright gibi otomasyon botları genellikle tespit edilebilir imzalara sahiptir (`navigator.webdriver == true`). Ancak modern botlar bunları gizler. Gelişmiş koruma sistemleri (Cloudflare Turnstile, reCAPTCHA v3) IP'nin geçmişini (reputation), fare hareketlerinin hızını, ekran çözünürlüğünün tutarlılığını ölçerek bot tespiti yapar.

**İlgili Bağlantılar:**
- [[Rate-Limiting-Token-Bucket]]

## 📚 İlgili Draftlar
- [[review/ai-tehdit-modelleme-stride-ai-ve-mitre-atlas-ile-guvenlik-analizi]]
- [[review/mcp-sunuculari-gelistiriciler-icin-yeni-bir-backend-paradigmasi]]
- [[review/cve-2026-34197-13-yildir-gizli-kalan-activemq-rce-acigi-ve-acil-patch-zorunlulugu]]
