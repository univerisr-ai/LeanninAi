# 🧠 AiBeyin — İkinci Beyin (LLM Wiki)

Bu sayfa, Frontend Mimarisi ve Web Site Güvenliği üzerine kişisel bilgi tabanımın ana navigasyon merkezidir. Tüm notlar atomik, birbiriyle bağlantılı ve Claude Code tarafından `raw/` verilerinden sentezlenmiştir.

## 🧭 Navigasyon

* İşlem geçmişi ve sistem güncellemeleri için: [[log]]
* En son sentezlenen 500 kelimelik taze bilgi için: [[hot]]

---

## 🏗️ Yazılım Mimarisi (Frontend & Backend)
* [[Clean-Architecture]]: Katmanlı mimari desenleri ve bağımlılıkların yönetimi.
* [[Modern-React-Desenleri]]: Compound Components, Polymorphic yapılar ve Optimistic Updates.
* [[State-Yonetimi-Zustand-TanStack]]: UI ve Sunucu state'lerinin ayrılması.
* [[Veritabani-ve-Caching-Stratejileri]]: N+1 problemi, Redis Cache-Aside, Prisma modelleme.

## 🛡️ Web Güvenliği ve Bot Koruması
* [[XSS-ve-CSRF-Açiklari]]: Temel web saldırıları ve DOMPurify / Token önlemleri.
* [[JWT-ve-Kimlik-Dogrulama]]: Access/Refresh token stratejileri ve RBAC (Rol Tabanlı Erişim).
* [[Rate-Limiting-Token-Bucket]]: API limitleri ve Token Bucket algoritması.
* [[Bot-Tespiti-ve-Honeypot]]: Web scraping botlarını yakalama ve CAPTCHA entegrasyonu.
* [[CORS-ve-Guvenlik-Headerlari]]: Helmets, SameSite, HttpOnly tanımlamaları.

## 🎨 UI/UX ve Performans
* [[Tasarim-Psikolojisi-Gestalt-Hick]]: Kullanıcı algısı, Hick's Law ve Gestalt yasaları.
* [[Renk-Teorisi-ve-Tipografi]]: HSL renk paletleri, Dark mode, modüler Type Scale (1.25 oran).
* [[Web-Performansi-PWA]]: Service Worker stratejileri, Core Web Vitals ölçümleri, Vite Optimizasyonu.

## ♿ Erişilebilirlik (a11y)
* [[Erisilebilirlik-WCAG-ve-ARIA]]: Engelli kullanıcılar için kapsayıcı ARIA kuralları ve Landmark roller.
* [[Klavye-Navigasyon-Focus]]: Tab sırası, tabindex, Skip Link, outline yönetimi.
