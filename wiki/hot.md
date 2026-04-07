# 🔥 Sıcak Bellek (Hot Cache)
*En son eklenen bilgilerin 500 kelimelik yoğun özeti. Claude bu sayfayı genel bağlam için sık sık okur.*

---

## 🚀 Son Öğrenimler: Modern Web Stack & Güvenlik

AiBeyin sistemime yeni eklenen dökümanlar; Frontend/Backend Mimarisi, UI/UX tasarımı, Web Güvenliği, Bot Koruması ve Erişilebilirlik (a11y) temellerini oluşturdu. İşte en güncel bilgilerin kristallize edilmiş hali:

### 1. Mimari Mükemmellik
Projeler artık **Clean Architecture** prensibiyle yapılandırılmalı. Backend tarafında (Örn: Node.js/Express) katmanlı yapı (Domain, Application, Infrastructure, Presentation) şarttır. Veritabanı yönetiminde **Prisma ORM**, N+1 probleminden kaçınmak için `include` ile Eager Loading yaparken, sorgu optimizasyonu için **Redis Cache-Aside** stratejisi uygulanmalıdır. Frontend'de (React) **Compound Components** (Bileşik Bileşenler) ile modüler esneklik sağlanmalı, state yönetimi ise ikiye ayrılmalıdır: UI durumu için **Zustand**, Sunucu senkronizasyonu için **TanStack Query**.

### 2. Güvenlik Zırhı
Modern web uygulamasının güvenliği taviz vermez. **XSS** saldırılarını DomPurify ile sanitize ederek ve `textContent` kullanarak engelleyin. **CSRF** koruması için Double Submit Cookie Pattern kullanılmalı; API'ler HTTP başlığındaki token'i çerezdeki token'la eşleştirmelidir. Yetkilendirme için **JWT** kullanılacaksa: Kısa ömürlü (15 dk) *Access Token* bellek (memory) üzerinde, uzun ömürlü *Refresh Token* ise **HttpOnly, Secure ve SameSite=Strict** bayraklarına sahip bir cookie olarak taşınmalıdır. Scraper botlara karşı Express'te **express-rate-limit** ile Token Bucket algoritmasına dayalı limitleme yapılmalı, bal küpü (honeypot) görünmez form alanlarıyla botlar otomatik yakalanmalıdır.

### 3. Kullanıcı Deneyimi ve Kapsayıcılık (UI/UX + a11y)
Tasarım sadece boya değil, bir matematik sorunudur. Seçenek bolluğunu azaltarak karar süresini düşüren **Hick's Law** ile buton boyutlarını artırarak etkileşimi kolaylaştıran **Fitts's Law** uygulanmalıdır. Tasarım sisteminde HEX yerine **HSL** kullanılmalıdır (Hue, Saturation, Lightness manipülasyonu dark mode adaptasyonunu inanılmaz kolaylaştırır). Tipografi **Modüler Ölçek** (1.25 base oran) kullanılarak matematiksel bir orantı içinde büyütülmelidir (örn: var(--text-2xl)). 

Arayüz tamamen **Erişilebilir (a11y - WCAG 2.2 AA standardı)** olmalıdır. Sayfanın mutlaka anlamlı div'ler yerine `nav`, `main`, `header` gibi semantik veya en azından landmark **ARIA** (role="navigation") etiketleri içermesi gerekir. Görsel olmayan etkileşimler (`aria-live="polite"`) canlı bölgeler üzerinden ekran okuyuculara sesli duyurulur. Asla sadece `outline: none` kullanılmamalı, klavye gezintisi için `:focus-visible` ile kalın ve kontrastı yüksek (min 4.5:1) sınırlar çizilmelidir.

Tüm modern frontend, son aşamada **Vite** üzerinden SWC ile derlenmeli ve çevrimdışı önbellekleme (Offline cache stratejisi: Cache First / Network First) için **PWA Service Worker'ları** kullanılmalıdır.
