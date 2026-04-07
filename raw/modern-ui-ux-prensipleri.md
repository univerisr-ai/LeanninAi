# Modern UI/UX Prensipleri — Kapsamlı Profesyonel Rehber

**Tarih:** 2026-04-07  
**Kategori:** UI/UX Tasarım, Design System, Tipografi, Renk Teorisi, Mikro-etkileşim  
**Seviye:** Orta-İleri  
**İlişkili Konular:** [Frontend Mimarisi](./frontend-mimarisi-rehberi.md), [Frontend Geliştirme](./frontend-gelistirme-rehberi.md), [Erişilebilirlik](./erisilebilik-rehberi.md)

---

## 1. Tasarım Psikolojisi ve Temel Kurallar

### 1.1 Gestalt İlkeleri (Algı Kuralları)

```
┌────────────────────────────────────────────────────────┐
│                    GESTALT YASALARI                     │
├──────────────┬─────────────────────────────────────────┤
│  Yakınlık    │  Birbirine yakın elemanlar grup olarak  │
│  (Proximity) │  algılanır. Boşluk = gruplama aracı.   │
│              │                                         │
│  ●● ●●  ●●  │  → 3 grup olarak algılanır              │
├──────────────┼─────────────────────────────────────────┤
│  Benzerlik   │  Benzer görünen elemanlar birlikte      │
│ (Similarity) │  algılanır. Renk, boyut, şekil.        │
│              │                                         │
│  ●●○○●●○○   │  → Siyah ve beyaz iki ayrı grup         │
├──────────────┼─────────────────────────────────────────┤
│  Süreklilik  │  Göz, düzgün çizgileri takip eder.     │
│ (Continuity) │  Navigasyon akışı, breadcrumb.         │
├──────────────┼─────────────────────────────────────────┤
│  Kapalılık   │  Tamamlanmamış şekiller zihinsel        │
│ (Closure)    │  olarak tamamlanır. Logo tasarımı.      │
├──────────────┼─────────────────────────────────────────┤
│  Figure/     │  Ön plan-arka plan ayrımı.             │
│  Ground      │  Modal overlay, kart yükseltme.         │
└──────────────┴─────────────────────────────────────────┘
```

**CSS ile Yakınlık İlkesi Uygulaması:**

```css
/* Yakın elemanları gruplayarak bilgiyi organize et */
.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);          /* Label-input arası: küçük (yakın, aynı grup) */
  margin-bottom: var(--space-6); /* Gruplar arası: büyük (farklı grup) */
}

.form-group label {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-secondary);
}

.form-group input {
  padding: var(--space-3);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  font-size: var(--text-base);
  transition: border-color var(--transition-fast);
}

.form-group input:focus {
  border-color: var(--color-primary-500);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

/* Hata durumu: form grubu bütünleşik */
.form-group--error input {
  border-color: var(--color-danger-500);
}

.form-group--error .form-error {
  font-size: var(--text-xs);
  color: var(--color-danger-500);
  margin-top: var(--space-1);
}
```

### 1.2 Hick's Law (Seçenek Sayısı ↔ Karar Süresi)

```
Karar süresi = a + b × log₂(n)

n = seçenek sayısı
Seçenek arttıkça karar süresi logaritmik artar.
```

**Uygulama Kuralları:**

```html
<!-- ❌ KÖTÜ: 12 buton yan yana → Kullanıcı ne yapacağını bilmez -->
<div class="toolbar">
  <button>Kaydet</button>
  <button>Sil</button>
  <button>Kopyala</button>
  <button>Taşı</button>
  <button>Paylaş</button>
  <button>İndir</button>
  <button>Yazdır</button>
  <button>Arşivle</button>
  <button>Sabitle</button>
  <button>Etiketle</button>
  <button>Dışa Aktar</button>
  <button>Geri Al</button>
</div>

<!-- ✅ İYİ: Birincil + ikincil + gizli menü hiyerarşisi -->
<div class="toolbar">
  <div class="toolbar__primary">
    <button class="btn btn--primary">Kaydet</button>
    <button class="btn btn--ghost">Paylaş</button>
  </div>
  <div class="toolbar__secondary">
    <button class="btn btn--icon" aria-label="Geri al" title="Geri Al">↩</button>
    <button class="btn btn--icon" aria-label="Daha fazla seçenek" aria-haspopup="menu">⋯</button>
  </div>
</div>

<!-- Dropdown menü: Seyrek kullanılan eylemler -->
<menu class="dropdown" role="menu" hidden>
  <li role="menuitem">Kopyala</li>
  <li role="menuitem">Taşı</li>
  <li role="menuitem">İndir</li>
  <li role="separator"></li>
  <li role="menuitem" class="text-danger">Sil</li>
</menu>
```

### 1.3 Fitts's Law (Hedef Boyutu ↔ Tıklama Hızı)

```
Tıklama süresi = a + b × log₂(1 + D/W)

D = hedefe uzaklık, W = hedef genişliği
→ Hedef büyükse ve yakınsa daha hızlı tıklanır.
```

```css
/* ---- Minimum Dokunma/Tıklama Alanları ---- */

/* Mobil: minimum 44x44px (Apple HIG) / 48x48px (Material) */
.btn {
  min-height: 44px;
  min-width: 44px;
  padding: var(--space-2) var(--space-4);
}

/* Küçük ikonlu butonlarda görünmez tıklama alanı genişlet */
.btn--icon {
  position: relative;
  width: 32px;
  height: 32px;
}

.btn--icon::before {
  content: '';
  position: absolute;
  inset: -8px;   /* 32 + 16 = 48px tıklama alanı */
}

/* İnteraktif elemanlar arası minimum 8px boşluk (yanlış tıklama önleme) */
.button-group {
  display: flex;
  gap: var(--space-2);   /* 8px minimum */
}

/* Birincil eylem: En büyük ve en belirgin */
.btn--primary {
  padding: var(--space-3) var(--space-8);
  font-weight: 600;
  font-size: var(--text-base);
}

/* Yıkıcı eylem: Küçük ve uzak (kazara tıklamayı önle) */
.btn--danger {
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-sm);
}
```

---

## 2. Renk Teorisi ve Palet Oluşturma

### 2.1 HSL Tabanlı Renk Sistemi

```css
:root {
  /*
   * HSL kullan, HEX değil.
   * HSL daha okunabilir ve manipüle edilebilir:
   * H (Hue): Renk tonu (0-360°)
   * S (Saturation): Doygunluk (0-100%)
   * L (Lightness): Parlaklık (0-100%)
   */

  /* ---- Marka Rengi: Tek hue, değişen lightness ---- */
  --brand-50:  hsl(220, 90%, 96%);   /* Çok açık */
  --brand-100: hsl(220, 85%, 90%);
  --brand-200: hsl(220, 80%, 80%);
  --brand-300: hsl(220, 75%, 68%);
  --brand-400: hsl(220, 70%, 56%);
  --brand-500: hsl(220, 70%, 48%);   /* Ana renk */
  --brand-600: hsl(220, 72%, 40%);
  --brand-700: hsl(220, 75%, 32%);
  --brand-800: hsl(220, 78%, 24%);
  --brand-900: hsl(220, 80%, 16%);   /* Çok koyu */

  /* ---- Semantik Renkler ---- */
  --color-success: hsl(142, 72%, 42%);
  --color-warning: hsl(38, 95%, 54%);
  --color-danger:  hsl(0, 84%, 56%);
  --color-info:    hsl(200, 85%, 50%);
  
  /* ---- Nötr (Gri) Skalası: Hafif mavi tonu ---- */
  /* Saf gri soğuk görünür, hafif hue ekle */
  --neutral-50:  hsl(220, 14%, 96%);
  --neutral-100: hsl(220, 13%, 91%);
  --neutral-200: hsl(220, 12%, 84%);
  --neutral-300: hsl(220, 10%, 69%);
  --neutral-400: hsl(220, 8%, 53%);
  --neutral-500: hsl(220, 8%, 40%);
  --neutral-600: hsl(220, 10%, 31%);
  --neutral-700: hsl(220, 14%, 22%);
  --neutral-800: hsl(220, 18%, 14%);
  --neutral-900: hsl(220, 22%, 8%);
}
```

### 2.2 Kontrast Oranı Kuralları (WCAG)

```
Minimum Kontrast Oranları:
┌─────────────────────┬────────────────┬────────────────┐
│ Eleman Türü         │ AA (Minimum)   │ AAA (Gelişmiş) │
├─────────────────────┼────────────────┼────────────────┤
│ Normal metin        │ 4.5:1          │ 7:1            │
│ Büyük metin (≥18px) │ 3:1            │ 4.5:1          │
│ UI bileşenleri      │ 3:1            │ —              │
│ Dekoratif/logo      │ Kural yok      │ —              │
└─────────────────────┴────────────────┴────────────────┘
```

```javascript
// Kontrast oranı hesaplama fonksiyonu
function getContrastRatio(color1, color2) {
  const lum1 = getRelativeLuminance(color1);
  const lum2 = getRelativeLuminance(color2);
  const lighter = Math.max(lum1, lum2);
  const darker = Math.min(lum1, lum2);
  return (lighter + 0.05) / (darker + 0.05);
}

function getRelativeLuminance({ r, g, b }) {
  const [rs, gs, bs] = [r, g, b].map((c) => {
    c = c / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}

// Kullanım
const bg = { r: 17, g: 24, b: 39 };     // --neutral-900
const text = { r: 249, g: 250, b: 251 }; // --neutral-50
console.log(getContrastRatio(bg, text));  // → ~16.3:1 ✅ AAA geçer
```

### 2.3 Dark Mode Renk Dönüşümü

```css
/* ---- KURAL: Dark mode'da renkleri tersine çevirme, yeniden tasarla ---- */

/* Light Mode */
:root {
  --surface-1: hsl(0, 0%, 100%);        /* Beyaz zemin */
  --surface-2: hsl(220, 14%, 96%);      /* Hafif gri */
  --surface-3: hsl(220, 13%, 91%);      /* Kart arka planı */
  --text-1:    hsl(220, 22%, 8%);       /* Ana metin */
  --text-2:    hsl(220, 8%, 40%);       /* İkincil metin */
  --shadow:    0 1px 3px hsl(0 0% 0% / 0.1);
}

/* Dark Mode — sadece renkleri değil, hiyerarşiyi yeniden düşün */
[data-theme='dark'] {
  --surface-1: hsl(220, 22%, 8%);       /* En koyu (arka plan) */
  --surface-2: hsl(220, 18%, 12%);      /* Biraz daha açık */
  --surface-3: hsl(220, 16%, 16%);      /* Kart (yükseltilmiş) */
  --text-1:    hsl(220, 14%, 90%);      /* Ana metin (saf beyaz DEGIL) */
  --text-2:    hsl(220, 8%, 55%);       /* İkincil metin */
  --shadow:    0 1px 3px hsl(0 0% 0% / 0.4); /* Daha yoğun gölge */
  
  /* ⚠️ Doygun renkler dark mode'da parlak görünür, hafiflet */
  --brand-500: hsl(220, 60%, 58%);      /* Light: 70%/48% → Dark: 60%/58% */
  --color-danger: hsl(0, 72%, 62%);     /* Daha açık kırmızı */
}

/* ---- Sistem tercihine uyum ---- */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme='light']) {
    /* Kullanıcı manuel seçmediyse sistem tercihine uy */
    /* dark mode değişkenleri buraya */
  }
}
```

**Theme Toggle JavaScript:**

```typescript
function initTheme(): void {
  const stored = localStorage.getItem('theme');
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme = stored || (systemPrefersDark ? 'dark' : 'light');
  
  document.documentElement.setAttribute('data-theme', theme);
}

function toggleTheme(): void {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);

  // Geçiş animasyonu
  document.documentElement.classList.add('theme-transitioning');
  setTimeout(() => {
    document.documentElement.classList.remove('theme-transitioning');
  }, 300);
}

// Yumuşak geçiş animasyonu
// .theme-transitioning * { transition: background-color 300ms ease, color 200ms ease; }
```

---

## 3. Tipografi Sistemi

### 3.1 Type Scale (Modüler Ölçek)

```css
/*
 * Modüler Ölçek: Her boyut bir öncekinin 1.25 katı (Major Third)
 * 16px × 1.25 = 20px × 1.25 = 25px × 1.25 = 31.25px ...
 *
 * Diğer yaygın oranlar:
 * 1.125 — Major Second (konservatif)
 * 1.200 — Minor Third (dengeli)
 * 1.250 — Major Third (çoğu site) ✓
 * 1.333 — Perfect Fourth (başlık ağırlıklı)
 * 1.618 — Golden Ratio (dramatik)
 */

:root {
  --text-xs:   0.75rem;     /* 12px — caption, badge */
  --text-sm:   0.875rem;    /* 14px — yardımcı metin, meta */
  --text-base: 1rem;        /* 16px — body metin */
  --text-lg:   1.125rem;    /* 18px — lead paragraf */
  --text-xl:   1.25rem;     /* 20px — h5 */
  --text-2xl:  1.5rem;      /* 24px — h4 */
  --text-3xl:  1.875rem;    /* 30px — h3 */
  --text-4xl:  2.25rem;     /* 36px — h2 */
  --text-5xl:  3rem;        /* 48px — h1 */
  --text-6xl:  3.75rem;     /* 60px — hero başlık */

  /* ---- Satır Yüksekliği ---- */
  --leading-tight:  1.25;   /* Başlıklar */
  --leading-snug:   1.375;  /* Alt başlıklar */
  --leading-normal: 1.6;    /* Body metin (okunabilirlik için ideal) */
  --leading-relaxed: 1.75;  /* Uzun paragraflar */

  /* ---- Font Ailesi ---- */
  --font-sans: 'Inter', 'SF Pro Display', system-ui, -apple-system, sans-serif;
  --font-serif: 'Merriweather', 'Georgia', serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;

  /* ---- Optimal Satır Genişliği ---- */
  --measure-narrow: 45ch;   /* Dar sütun */
  --measure-base: 65ch;     /* İdeal okunma genişliği (45-75ch arası) */
  --measure-wide: 80ch;     /* Geniş sütun */
}

/* ---- Başlık Stilleri ---- */
h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-sans);
  font-weight: 700;
  line-height: var(--leading-tight);
  color: var(--text-1);
  letter-spacing: -0.02em;          /* Büyük boyutlarda sıkıştır */
}

h1 { font-size: var(--text-5xl); letter-spacing: -0.025em; }
h2 { font-size: var(--text-4xl); }
h3 { font-size: var(--text-3xl); }
h4 { font-size: var(--text-2xl); letter-spacing: -0.01em; }

/* Body metin */
body {
  font-family: var(--font-sans);
  font-size: var(--text-base);
  line-height: var(--leading-normal);
  color: var(--text-1);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Paragraf okunabilirliği */
.prose p {
  max-width: var(--measure-base);    /* 65 karakter genişlik limiti */
  margin-bottom: 1.5em;
}

/* ---- Responsive Tipografi (Fluid) ---- */
/* clamp(minimum, tercih, maksimum) */
h1 {
  font-size: clamp(var(--text-3xl), 5vw + 1rem, var(--text-6xl));
}

h2 {
  font-size: clamp(var(--text-2xl), 3vw + 0.5rem, var(--text-4xl));
}
```

### 3.2 Font Yükleme Stratejisi

```html
<head>
  <!-- 1. Preconnect: DNS + TLS handshake'i önceden tamamla -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />

  <!-- 2. Font CSS'i yükle (display=swap ile fallback göster) -->
  <link rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" />
</head>
```

```css
/* Self-hosted font (daha hızlı, GDPR uyumlu) */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;               /* CLS'yi minimize et */
  unicode-range: U+0000-00FF,       /* Latin temel karakter seti */
                 U+0131, U+011E-011F, U+015E-015F; /* Türkçe karakterler */
}

@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter-Bold.woff2') format('woff2');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
  unicode-range: U+0000-00FF, U+0131, U+011E-011F, U+015E-015F;
}
```

---

## 4. Spacing ve Layout Sistemi

### 4.1 8px Grid Sistemi

```css
/*
 * 8px Grid: Tüm spacing değerleri 8'in katları
 * 4px - çok sıkı iç boşluk (ikon-metin arası)
 * 8px - elemanlar arası minimum
 * 16px - standart padding
 * 24px - kart iç boşluğu
 * 32px - bölümler arası
 * 48px - ana bölümler arası
 * 64px - sayfa bölümleri arası
 */

:root {
  --space-0:  0;
  --space-0.5: 0.125rem;  /* 2px */
  --space-1:  0.25rem;    /* 4px */
  --space-2:  0.5rem;     /* 8px */
  --space-3:  0.75rem;    /* 12px */
  --space-4:  1rem;       /* 16px */
  --space-5:  1.25rem;    /* 20px */
  --space-6:  1.5rem;     /* 24px */
  --space-8:  2rem;       /* 32px */
  --space-10: 2.5rem;     /* 40px */
  --space-12: 3rem;       /* 48px */
  --space-16: 4rem;       /* 64px */
  --space-20: 5rem;       /* 80px */
  --space-24: 6rem;       /* 96px */
}

/* ---- Tutarlı Bileşen Spacing ---- */
.card {
  padding: var(--space-6);         /* 24px iç boşluk */
  border-radius: var(--radius-lg);
  background: var(--surface-2);
}

.card__header {
  margin-bottom: var(--space-4);   /* 16px başlık-içerik arası */
}

.card__title {
  font-size: var(--text-xl);
  margin-bottom: var(--space-1);   /* 4px başlık-alt metin arası */
}

.card__subtitle {
  font-size: var(--text-sm);
  color: var(--text-2);
}

.card__body {
  margin-bottom: var(--space-6);   /* 24px içerik-aksiyon arası */
}

.card__actions {
  display: flex;
  gap: var(--space-3);             /* 12px butonlar arası */
  justify-content: flex-end;
}
```

### 4.2 İçerik Genişliği Kısıtlamaları

```css
/* ---- Max-Width Sistemi ---- */
.container {
  width: 100%;
  margin-inline: auto;                  /* Yatay ortalama */
  padding-inline: var(--space-4);       /* Mobil kenarlık */
}

.container--sm  { max-width: 640px; }   /* Blog, makale */
.container--md  { max-width: 768px; }   /* Form sayfası */
.container--lg  { max-width: 1024px; }  /* Dashboard */
.container--xl  { max-width: 1280px; }  /* E-ticaret grid */
.container--2xl { max-width: 1536px; }  /* Full-width */

/* ---- İçerik türüne göre genişlik ---- */
.prose {
  max-width: var(--measure-base);       /* Okunabilir metin: 65ch */
}

.form-layout {
  max-width: 480px;                     /* Form alanları: dar */
}

.grid-listing {
  max-width: 1280px;                    /* Ürün grid: geniş */
}
```

---

## 5. Mikro-etkileşimler (Micro-interactions)

### 5.1 Hover, Focus ve Active States

```css
/* ---- Buton State Matrisi ---- */
.btn {
  /* Varsayılan durum */
  background: var(--brand-500);
  color: white;
  border: none;
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-md);
  font-weight: 600;
  cursor: pointer;
  transition: 
    background-color var(--duration-fast) ease,
    transform var(--duration-fast) var(--ease-spring),
    box-shadow var(--duration-fast) ease;
  
  /* Tıklama dalga efekti hazırlığı */
  position: relative;
  overflow: hidden;
}

/* Hover: Hafif renk değişimi + yükseltme */
.btn:hover {
  background: var(--brand-600);
  box-shadow: 0 2px 8px hsl(220 70% 48% / 0.3);
  transform: translateY(-1px);
}

/* Active (tıklama anı): Aşağı basma hissi */
.btn:active {
  transform: translateY(0) scale(0.98);
  box-shadow: none;
  transition-duration: 50ms;
}

/* Focus (klavye): Belirgin halka */
.btn:focus-visible {
  outline: 2px solid var(--brand-400);
  outline-offset: 2px;
}

/* Disabled: Etkileşimi kapat */
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

/* Loading durumu */
.btn--loading {
  pointer-events: none;
  color: transparent;
}

.btn--loading::after {
  content: '';
  position: absolute;
  inset: 0;
  margin: auto;
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 600ms linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ---- Ripple (Dalga) Efekti ---- */
.btn .ripple {
  position: absolute;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  animation: ripple-expand 600ms ease-out forwards;
}

@keyframes ripple-expand {
  to {
    width: 300px;
    height: 300px;
    opacity: 0;
  }
}
```

```javascript
// Ripple efekti JavaScript
function addRipple(button, event) {
  const ripple = document.createElement('span');
  ripple.classList.add('ripple');

  const rect = button.getBoundingClientRect();
  ripple.style.left = `${event.clientX - rect.left}px`;
  ripple.style.top = `${event.clientY - rect.top}px`;

  button.appendChild(ripple);
  ripple.addEventListener('animationend', () => ripple.remove());
}

document.querySelectorAll('.btn').forEach((btn) => {
  btn.addEventListener('click', (e) => addRipple(btn, e));
});
```

### 5.2 Sayfa Geçiş Animasyonları

```css
/* ---- View Transitions API (Modern) ---- */
@view-transition {
  navigation: auto;
}

/* Varsayılan geçiş */
::view-transition-old(root) {
  animation: fade-out 200ms ease;
}

::view-transition-new(root) {
  animation: fade-in 300ms ease;
}

@keyframes fade-out {
  from { opacity: 1; }
  to { opacity: 0; }
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Belirli bir element için özel geçiş */
.product-card__image {
  view-transition-name: product-image;
}

::view-transition-old(product-image) {
  animation: scale-down 300ms var(--ease-in-out-circ);
}

::view-transition-new(product-image) {
  animation: scale-up 300ms var(--ease-in-out-circ);
}
```

### 5.3 Toast/Bildirim Animasyonu

```css
/* ---- Toast giriş/çıkış animasyonları ---- */
.toast {
  position: fixed;
  bottom: var(--space-6);
  right: var(--space-6);
  padding: var(--space-4) var(--space-6);
  border-radius: var(--radius-lg);
  background: var(--surface-3);
  color: var(--text-1);
  box-shadow: var(--shadow-lg);
  display: flex;
  align-items: center;
  gap: var(--space-3);
  z-index: 9999;

  /* Giriş animasyonu */
  animation: toast-in 400ms var(--ease-out-expo) both;
}

/* Çıkış animasyonu (JS ile class ekle) */
.toast--exiting {
  animation: toast-out 300ms ease-in forwards;
}

@keyframes toast-in {
  from {
    opacity: 0;
    transform: translateY(16px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes toast-out {
  to {
    opacity: 0;
    transform: translateX(100px);
  }
}

/* ---- Progress bar (otomatik kapanma göstergesi) ---- */
.toast__progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  background: var(--brand-500);
  border-radius: 0 0 var(--radius-lg) var(--radius-lg);
  animation: toast-progress 5s linear forwards;
}

@keyframes toast-progress {
  from { width: 100%; }
  to { width: 0%; }
}
```

---

## 6. Boş Durum ve Yükleme Tasarımı

### 6.1 Empty States

```html
<!-- ❌ KÖTÜ: Sadece "Veri bulunamadı" yazısı -->
<p>Veri bulunamadı.</p>

<!-- ✅ İYİ: Açıklayıcı, yönlendirici, görsel içeren boş durum -->
<div class="empty-state" role="status">
  <div class="empty-state__illustration">
    <svg><!-- İlgili illüstrasyon --></svg>
  </div>
  <h3 class="empty-state__title">Henüz bir projeniz yok</h3>
  <p class="empty-state__description">
    İlk projenizi oluşturarak başlayın. Projeler, görevlerinizi
    organize etmenizi ve ekibinizle iş birliği yapmanızı sağlar.
  </p>
  <button class="btn btn--primary">
    <span aria-hidden="true">+</span> Yeni Proje Oluştur
  </button>
</div>
```

```css
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: var(--space-16) var(--space-4);
  max-width: 400px;
  margin: 0 auto;
}

.empty-state__illustration {
  width: 200px;
  height: 200px;
  margin-bottom: var(--space-6);
  color: var(--neutral-300);
}

.empty-state__title {
  font-size: var(--text-xl);
  margin-bottom: var(--space-2);
}

.empty-state__description {
  font-size: var(--text-sm);
  color: var(--text-2);
  margin-bottom: var(--space-6);
  line-height: var(--leading-relaxed);
}
```

### 6.2 Skeleton Loading Deseni

```css
/* ---- Gerçekçi Skeleton: İçerik yapısını yansıt ---- */
.skeleton-card {
  padding: var(--space-6);
  border-radius: var(--radius-lg);
  background: var(--surface-2);
}

.skeleton-line {
  height: 14px;
  border-radius: var(--radius-sm);
  background: linear-gradient(
    90deg,
    var(--neutral-200) 25%,
    var(--neutral-100) 37%,
    var(--neutral-200) 63%
  );
  background-size: 400% 100%;
  animation: skeleton-pulse 1.4s ease infinite;
}

.skeleton-line--title   { width: 60%; height: 20px; margin-bottom: var(--space-3); }
.skeleton-line--text    { width: 100%; margin-bottom: var(--space-2); }
.skeleton-line--short   { width: 40%; }

.skeleton-avatar {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-full);
}

@keyframes skeleton-pulse {
  0%   { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

[data-theme='dark'] .skeleton-line {
  background: linear-gradient(
    90deg,
    var(--neutral-700) 25%,
    var(--neutral-600) 37%,
    var(--neutral-700) 63%
  );
  background-size: 400% 100%;
}
```

---

## 7. Responsive Tasarım Stratejisi

### 7.1 Breakpoint Kararları

```css
/*
 * Mobil-Öncelikli Breakpoint'ler:
 * Varsayılan stiller = mobil
 * min-width ile büyüğe doğru ekleme yap
 *
 * ┌──────────┬──────────┬──────────┬──────────┬──────────┐
 * │  Mobile  │  Tablet  │ Desktop  │   Wide   │  Ultra   │
 * │  <640px  │  640-    │  1024-   │  1280-   │  1536px+ │
 * │          │  1023px  │  1279px  │  1535px  │          │
 * └──────────┴──────────┴──────────┴──────────┴──────────┘
 */

/* Mobil (varsayılan) */
.hero { padding: var(--space-8) var(--space-4); }
.hero__title { font-size: var(--text-3xl); }

/* Tablet */
@media (min-width: 640px) {
  .hero { padding: var(--space-12) var(--space-8); }
  .hero__title { font-size: var(--text-4xl); }
}

/* Desktop */
@media (min-width: 1024px) {
  .hero { padding: var(--space-20) var(--space-12); }
  .hero__title { font-size: var(--text-5xl); }
}

/* ---- Kullanıcı Tercihleri ---- */

/* Büyük metin tercihi */
@media (prefers-reduced-data: reduce) {
  img[loading="lazy"] { display: none; }  /* Gereksiz yükleme yapma */
}

/* Yüksek kontrast modu */
@media (prefers-contrast: more) {
  :root {
    --text-2: var(--text-1);              /* İkincil metni de koyu yap */
    --border-default: var(--neutral-600); /* Kenarlıkları belirginleştir */
  }
}

/* Koyu tema tercihi */
@media (prefers-color-scheme: dark) {
  /* Otomatik dark mode */
}
```

---

## 8. Form Tasarımı Best Practices

### 8.1 Erişilebilir ve Kullanışlı Form

```html
<form class="form" novalidate>
  <!-- Her input'un mutlaka label'ı olmalı -->
  <div class="form-group">
    <label for="fullname">
      Ad Soyad
      <span class="form-required" aria-label="zorunlu alan">*</span>
    </label>
    <input
      id="fullname"
      name="fullname"
      type="text"
      required
      autocomplete="name"
      placeholder="Örn: Ahmet Yılmaz"
      aria-describedby="fullname-hint"
    />
    <small id="fullname-hint" class="form-hint">
      Resmi belgelerdeki adınızı girin.
    </small>
  </div>

  <!-- ✅ Şifre: autocomplete ile password manager desteği -->
  <div class="form-group">
    <label for="password">Şifre</label>
    <div class="input-group">
      <input
        id="password"
        name="password"
        type="password"
        required
        minlength="8"
        autocomplete="new-password"
        aria-describedby="password-rules"
      />
      <button
        type="button"
        class="input-group__toggle"
        aria-label="Şifreyi göster"
        onclick="togglePasswordVisibility(this)"
      >
        👁
      </button>
    </div>
    <div id="password-rules" class="password-strength">
      <small>En az 8 karakter, 1 büyük harf, 1 rakam, 1 özel karakter</small>
    </div>
  </div>

  <!-- ✅ Tek gönderim butonu, net eylem metni -->
  <button type="submit" class="btn btn--primary btn--full-width">
    Hesap Oluştur
  </button>
</form>
```

```css
/* Inline validation göstergeleri */
.form-group--success input { border-color: var(--color-success); }
.form-group--error input   { border-color: var(--color-danger); }

.form-group--success .form-icon::after { content: '✓'; color: var(--color-success); }
.form-group--error .form-icon::after   { content: '✕'; color: var(--color-danger); }

/* Hata mesajı: kırmızı, küçük, altta */
.form-error {
  font-size: var(--text-xs);
  color: var(--color-danger);
  margin-top: var(--space-1);
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

/* Tam genişlik buton */
.btn--full-width {
  width: 100%;
  justify-content: center;
}
```

---

## 9. UI Tasarımı Kontrol Listesi

### Her Sayfa/Bileşen İçin Kontrol Et

- [ ] **Kontrast:** Metin/arka plan kontrast oranı ≥ 4.5:1 (AA)
- [ ] **Touch target:** Tıklanabilir elemanlar ≥ 44px
- [ ] **Spacing:** Tüm boşluklar 4/8px grid'e uygun
- [ ] **Tipografi:** max-width ≤ 75ch, line-height ≥ 1.5
- [ ] **Hover state:** Her tıklanabilir elemanın hover, focus, active durumu var
- [ ] **Loading:** Yükleme durumu skeleton veya spinner ile gösteriliyor
- [ ] **Empty state:** Boş liste/veri durumu açıklayıcı ve yönlendirici
- [ ] **Error state:** Hata mesajları kullanıcı dilinde ve çözüm önerili
- [ ] **Dark mode:** Tüm renkler, gölgeler ve görseller dark mode'da uyumlu
- [ ] **Mobil:** Tüm sayfalar 320px genişlikte sorunsuz görünüyor
- [ ] **Animasyon:** prefers-reduced-motion saygı duyuluyor
- [ ] **Form:** Her input'un label'ı, hata mesajı ve autocomplete'i var

---

## 10. Referanslar

- Refactoring UI (Adam Wathan & Steve Schoger): https://www.refactoringui.com/
- Inclusive Components (Heydon Pickering): https://inclusive-components.design/
- Laws of UX: https://lawsofux.com/
- Material Design 3: https://m3.material.io/
- Apple HIG: https://developer.apple.com/design/human-interface-guidelines/
- Contrast Checker: https://webaim.org/resources/contrastchecker/
- Type Scale Calculator: https://typescale.com/
- Open Props (Design Tokens): https://open-props.style/
