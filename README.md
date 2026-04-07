# 🧠 AiBeyin — İkinci Beyin Bilgi Tabanı

**Son Güncelleme:** 2026-04-07  
**Toplam Rehber:** 7  
**Toplam Boyut:** ~187 KB | ~4,500+ satır profesyonel içerik

---

## 📚 Rehber Haritası

```
AiBeyin/
└── raw/
    ├── 🏗️ frontend-mimarisi-rehberi.md       28 KB — Temel mimari desenler
    ├── ⚛️ frontend-gelistirme-rehberi.md      32 KB — İleri frontend teknikleri
    ├── 🔧 backend-gelistirme-rehberi.md       35 KB — Backend mimarisi ve API
    ├── 🎨 modern-ui-ux-prensipleri.md         30 KB — Tasarım prensipleri
    ├── ♿ erisilebilik-rehberi.md              22 KB — WCAG 2.2, ARIA, a11y
    ├── 🛡️ web-guvenlik-rehberi.md             26 KB — XSS, CSRF, JWT, CORS
    └── 🤖 anti-bot-guvenligi-ve-rate-limit.md 15 KB — Bot koruması
```

---

## 📖 Rehberler

### 1. [Frontend Mimarisi](./raw/frontend-mimarisi-rehberi.md) — 🏗️
> Feature-based yapı, Compound Components, Custom Hooks, Zustand, TanStack Query, CSS Design Tokens, Container Query, Test piramidi

### 2. [Frontend Geliştirme](./raw/frontend-gelistirme-rehberi.md) — ⚛️
> İleri TypeScript (branded types, generics), Polymorphic Components, Optimistic Updates, WebSocket/SSE, PWA Service Worker, Core Web Vitals, Vite

### 3. [Backend Geliştirme](./raw/backend-gelistirme-rehberi.md) — 🔧
> Clean Architecture, Domain/Application/Infrastructure katmanları, REST API tasarımı, Prisma DB, Redis Cache, BullMQ, JWT+RBAC, Pino Logging, Dependency Injection

### 4. [Modern UI/UX Prensipleri](./raw/modern-ui-ux-prensipleri.md) — 🎨
> Gestalt yasaları, Hick's/Fitts's Law, HSL renk sistemi, kontrast kuralları, dark mode, tipografi, 8px grid, mikro-etkileşimler, skeleton loading, form tasarımı

### 5. [Erişilebilirlik (a11y)](./raw/erisilebilik-rehberi.md) — ♿
> WCAG 2.2, semantik HTML, landmark roller, klavye navigasyonu, ARIA desenleri (tabs, combobox, live regions), görsel erişilebilirlik, ekran okuyucu testi

### 6. [Web Güvenliği](./raw/web-guvenlik-rehberi.md) — 🛡️
> XSS koruması (CSP, DOMPurify), CSRF token, JWT (Access+Refresh), Cookie bayrakları, CORS whitelist, SQL Injection, SRI, güvenli dosya yükleme, Zod validation

### 7. [Anti-Bot Güvenliği](./raw/anti-bot-guvenligi-ve-rate-limit.md) — 🤖
> Rate limiting, Token Bucket, IP engelleme, User-Agent analizi, CAPTCHA, Honeypot, JS challenge, proxy rotasyonu

---

## 🔗 Çapraz Referans Diyagramı

```
                    ┌──────────────┐
                    │   UI/UX      │
                    │  Prensipleri │
                    └──────┬───────┘
                           │ Renk, tipografi
                           │ spacing, animasyon
                    ┌──────▼───────┐
           ┌────────┤  Erişile-    ├────────┐
           │        │  bilirlik    │        │
           │        └──────┬───────┘        │
           │               │ ARIA, WCAG     │
     ┌─────▼──────┐  ┌─────▼──────┐  ┌─────▼──────┐
     │  Frontend   │  │  Frontend  │  │  Backend   │
     │  Mimari     │◄─┤  Geliştirme├─►│  Geliştirme│
     │  (Yapı)     │  │  (İleri)   │  │  (API+DB)  │
     └─────┬───────┘  └─────┬──────┘  └─────┬──────┘
           │               │                │
           │     CSRF Token + JWT + CSP     │
           │               │                │
           │         ┌─────▼──────┐         │
           └────────►│    Web     │◄────────┘
                     │  Güvenlik  │
                     └─────┬──────┘
                           │ Rate Limit
                     ┌─────▼──────┐
                     │  Anti-Bot  │
                     │  Güvenlik  │
                     └────────────┘
```

---

## 📋 Öğrenme Yolu

| Adım | Rehber | Odak |
|---|---|---|
| 1 | UI/UX Prensipleri | Tasarım temellerini öğren |
| 2 | Frontend Mimarisi | Proje yapısı ve component desenleri |
| 3 | Erişilebilirlik | A11y ile kaliteli UI geliştir |
| 4 | Backend Geliştirme | API ve sunucu mimarisi |
| 5 | Web Güvenliği | Frontend-backend güvenlik katmanı |
| 6 | Frontend Geliştirme | TypeScript, PWA, real-time |
| 7 | Anti-Bot Güvenliği | Savunma teknikleri |

---

## 🏷️ Konu Etiketleri ile Hızlı Erişim

| Aradığın Konu | Rehber | Bölüm |
|---|---|---|
| Renk paleti / dark mode | UI/UX §2 | HSL renk sistemi |
| Tipografi / font yükleme | UI/UX §3 | Type scale + font-display |
| Buton hover/active/focus | UI/UX §5 | Mikro-etkileşimler |
| Skeleton loading | UI/UX §6 | Yükleme durumu tasarımı |
| ARIA rolleri | Erişilebilirlik §4 | Tabs, combobox, live region |
| Klavye navigasyonu | Erişilebilirlik §3 | Focus trap, tab sırası |
| WCAG kontrastı | Erişilebilirlik §1, UI/UX §2.2 | Kontrast oranı |
| `fetch` / API çağrısı | Frontend Mimari §4.3, Güvenlik §3.2 | TanStack Query + CSRF |
| Form doğrulama | Güvenlik §6, UI/UX §8 | Zod + form tasarımı |
| JWT token yönetimi | Güvenlik §4.2, Backend §8 | Access/Refresh + RBAC |
| Veritabanı tasarımı | Backend §3 | Prisma + Index stratejisi |
| WebSocket | Frontend Geliştirme §4 | useWebSocket hook |
| Cache | Backend §4 | Redis cache-aside |
| Hata yönetimi | Backend §5, Frontend Gel. §2.3 | AppError + ErrorBoundary |
| Service Worker / PWA | Frontend Geliştirme §5 | Cache stratejileri |
| Rate limit | Anti-Bot §2.1, §5 | Token Bucket |
| CORS ayarları | Güvenlik §9 | Whitelist + credentials |
| CSS animasyon | Frontend Gel. §3, UI/UX §5 | Keyframes + View Transitions |

---

## 🤖 Gunluk AI Otomasyonu (MVP Basladi)

Bu repo artik gunluk calisan bir otomasyon iskeletine sahip.

### Eklenen Bilesenler

- `config/pipeline.json`: kaynaklar, kalite esikleri, model ve kota ayarlari
- `scripts/run_pipeline.py`: pipeline calistirma giris noktasi
- `src/aibeyin/`: envanter, dedup, kaynak toplama, OpenRouter, draft yazimi
- `.github/workflows/daily-aibeyin.yml`: her gun 03:00 Europe/Istanbul (UTC 00:00) scheduler
- `storage/inventory.json`: ogrenilmis bilgi envanteri ve fingerprint kayitlari

### Tekrar Ogrenmeme Mekanizmasi

Sistem ayni bilgiyi tekrar islememek icin iki seviyeli kontrol uygular:

1. Kaynak hash kontrolu
      - Her dis kaynak icerigi SHA-256 ile fingerprintlenir.
      - Hash degismediyse kaynak otomatik skip edilir.

2. Wiki benzerlik kontrolu
      - Yeni icerik mevcut wiki sayfalari ile benzerlik testinden gecer.
      - Esik ustu benzerlikte yeni draft olusturulmaz.

Ek olarak envanter, repo dosya yapisi snapshotini (raw/wiki) tutar ve degisim takibi yapar.

### Calistirma

Dry-run (dosya yazmadan test):

```
python scripts/run_pipeline.py --config config/pipeline.json --dry-run
```

Normal calisma (OpenRouter key gerekli):

```
python scripts/run_pipeline.py --config config/pipeline.json
```

Strict calisma (partial durumda da fail etsin):

```
python scripts/run_pipeline.py --config config/pipeline.json --fail-on-partial
```

Gerekli ortam degiskeni:

```
OPENROUTER_API_KEY=...
```

### Uretim Ciktilari

- Draft ciktilar: `wiki/review/`
- Son envanter durumu: `storage/inventory.json`
- Son calisma raporu: `storage/last_run_report.json`
- Calisma gecmisi: `storage/run_history.jsonl`
- Haftalik otomatik derleme: `wiki/reports/weekly-YYYY-wWW.md`

Bu asamada yayin politikasi Draft-Review olarak uygulanir; otomatik dogrudan publish yoktur.

Haftalik derleme mekanizmasi pazar gunu otomatik devreye girer ve son 7 gunun toplu metriklerini tek markdown dosyasina yazar.
Pipeline raporu icinde `error_samples` alani tutulur; boylece hatali kaynagin URL ve hata nedeni gorulebilir.
