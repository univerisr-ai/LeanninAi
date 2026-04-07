# Web Erişilebilirliği (a11y) — Kapsamlı Profesyonel Rehber

**Tarih:** 2026-04-07  
**Kategori:** Erişilebilirlik, WCAG 2.2, ARIA, Klavye Navigasyonu  
**Seviye:** Orta-İleri  
**İlişkili Konular:** [UI/UX Prensipleri](./modern-ui-ux-prensipleri.md), [Frontend Mimarisi](./frontend-mimarisi-rehberi.md), [Frontend Geliştirme](./frontend-gelistirme-rehberi.md)

---

## 1. WCAG 2.2 Uyumluluk Seviyeleri

```
┌─────────┬────────────────────────────────────────────────────┐
│ Seviye  │ Açıklama                                           │
├─────────┼────────────────────────────────────────────────────┤
│ A       │ Temel erişilebilirlik (minimum yasal gereksinim)   │
│ AA      │ Kabul gören standart (çoğu yasa bunu hedefler) ✓  │
│ AAA     │ En yüksek seviye (özel gereksinimler için)         │
└─────────┴────────────────────────────────────────────────────┘

Dört temel ilke (POUR):
P — Perceivable (Algılanabilir): İçerik tüm duyularla algılanmalı
O — Operable (Kullanılabilir): Arayüz klavye ile kullanılabilmeli
U — Understandable (Anlaşılabilir): İçerik ve etkileşim anlaşılabilmeli
R — Robust (Sağlam): Farklı teknolojilerle uyumlu olmalı
```

---

## 2. Semantik HTML — Erişilebilirliğin Temeli

### 2.1 Doğru Element Seçimi

```html
<!-- ═══════════════════════════════════════ -->
<!--     ❌ YANLIŞ: Her şey div ve span     -->
<!-- ═══════════════════════════════════════ -->
<div class="page">
  <div class="top-bar">
    <div class="logo">Site Adı</div>
    <div class="menu">
      <div class="menu-item" onclick="go('/')">Ana Sayfa</div>
      <div class="menu-item" onclick="go('/about')">Hakkımızda</div>
    </div>
  </div>
  <div class="content">
    <div class="title">Başlık</div>
    <div class="text">İçerik...</div>
    <div class="action" onclick="submit()">Gönder</div>
  </div>
</div>

<!-- ═══════════════════════════════════════ -->
<!--    ✅ DOĞRU: Semantik HTML5 etiketleri  -->
<!-- ═══════════════════════════════════════ -->
<body>
  <header>
    <a href="/" class="logo" aria-label="Site Adı - Ana Sayfa">Site Adı</a>
    <nav aria-label="Ana Navigasyon">
      <ul>
        <li><a href="/" aria-current="page">Ana Sayfa</a></li>
        <li><a href="/about">Hakkımızda</a></li>
      </ul>
    </nav>
  </header>

  <main id="main-content">
    <article>
      <h1>Başlık</h1>
      <p>İçerik...</p>
      <button type="submit">Gönder</button>
    </article>
  </main>

  <footer>
    <p>&copy; 2026 Site Adı</p>
  </footer>
</body>
```

### 2.2 Landmark Rolleri

```html
<!-- Ekran okuyucu kullanıcıları landmark'lar arasında hızlıca atlar -->

<header>                          <!-- role="banner" (otomatik) -->
  <nav aria-label="Ana menü">    <!-- role="navigation" -->
    <!-- ... -->
  </nav>
</header>

<main>                            <!-- role="main" → Sayfada TEK olmalı -->
  <section aria-labelledby="products-heading">  <!-- role="region" -->
    <h2 id="products-heading">Ürünler</h2>
  </section>

  <aside aria-label="Filtreler">  <!-- role="complementary" -->
    <!-- Yan panel -->
  </aside>
</main>

<footer>                          <!-- role="contentinfo" (otomatik) -->
  <!-- ... -->
</footer>

<!--
Birden fazla <nav> varsa aria-label ile ayırt et:
✅ <nav aria-label="Ana menü">
✅ <nav aria-label="Footer bağlantıları">
❌ <nav> <nav> → Ayırt edemez!
-->
```

### 2.3 Başlık Hiyerarşisi

```html
<!-- ✅ Doğru başlık hiyerarşisi (seviye atlamayın) -->
<h1>Ürünler</h1>                    <!-- Sayfa başlığı — TEK h1 -->
  <h2>Elektronik</h2>               <!-- Kategori -->
    <h3>Telefonlar</h3>             <!-- Alt kategori -->
      <h4>iPhone 15 Pro</h4>        <!-- Ürün -->
    <h3>Laptoplar</h3>
      <h4>MacBook Air</h4>
  <h2>Giyim</h2>
    <h3>Erkek</h3>
    <h3>Kadın</h3>

<!-- ❌ Yanlış: h1 → h3 atlaması -->
<h1>Başlık</h1>
<h3>Alt başlık</h3>  <!-- h2 nerede? -->

<!-- 
Görsel boyutu başlık seviyesini belirlemez!
Yanlış: h1'i küçük göstermek için h4 kullanmak
Doğru: CSS ile istediğin boyutu ver
-->
<h2 class="text-sm">Küçük Görünen h2</h2>
```

---

## 3. Klavye Erişilebilirliği

### 3.1 Focus Yönetimi

```css
/* ============================================= */
/*    KURAL: outline: none ASLA tek başına!       */
/* ============================================= */

/* ❌ YAPMAYIN */
*:focus { outline: none; }

/* ✅ Sadece fare kullanıcılarında gizle, klavyede göster */
*:focus:not(:focus-visible) {
  outline: none;
}

*:focus-visible {
  outline: 3px solid var(--brand-500);
  outline-offset: 2px;
  border-radius: 2px;
}

/* ---- Skip Link ---- */
.skip-link {
  position: absolute;
  top: -100%;
  left: var(--space-4);
  z-index: 10000;
  padding: var(--space-3) var(--space-6);
  background: var(--brand-500);
  color: white;
  font-weight: 600;
  text-decoration: none;
  border-radius: 0 0 var(--radius-md) var(--radius-md);
  transition: top 200ms ease;
}

.skip-link:focus {
  top: 0;
}
```

```html
<!-- Skip link: Her sayfanın en başına ekle -->
<body>
  <a href="#main-content" class="skip-link">İçeriğe Atla</a>
  <header><!-- ... --></header>
  <main id="main-content" tabindex="-1">
    <!-- tabindex="-1": JS ile focus edilebilir ama tab sırasında değil -->
  </main>
</body>
```

### 3.2 Tab Sırası ve tabindex Kuralları

```html
<!-- 
tabindex değerleri:
  0  → Doğal tab sırasına dahil (DOM sırasına göre)
 -1  → Tab ile ulaşılamaz ama JS ile focus edilebilir
  1+ → KULLANMAYINız! Tab sırasını bozar.
-->

<!-- ✅ Doğal sıra: DOM sırasını düzgün yaz -->
<button>Birinci</button>          <!-- Tab: 1. -->
<button>İkinci</button>           <!-- Tab: 2. -->
<a href="/link">Üçüncü</a>       <!-- Tab: 3. -->

<!-- ❌ tabindex pozitif değer KULLANMAYINız -->
<button tabindex="3">Birinci?</button>
<button tabindex="1">Hangisi önce?</button>
<button tabindex="2">Karmaşık!</button>

<!-- ✅ tabindex="-1" kullanım alanı: JS ile focus yönetimi -->
<!-- Modal açıldığında focus'u modal'a taşı -->
<div class="modal" tabindex="-1" role="dialog">
  <!-- Modal içeriği -->
</div>

<!-- Sayfa içi navigasyonda hedef bölüme focus -->
<section id="results" tabindex="-1">
  <!-- Arama sonuçları yüklendikten sonra buraya focus -->
</section>
```

### 3.3 Özel Bileşenlerde Klavye Desteği

```typescript
// ---- Dropdown Menü: Tam klavye desteği ----
function DropdownMenu({ trigger, items }: DropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const menuRef = useRef<HTMLUListElement>(null);
  const triggerRef = useRef<HTMLButtonElement>(null);

  function handleTriggerKeyDown(e: React.KeyboardEvent) {
    switch (e.key) {
      case 'Enter':
      case ' ':
      case 'ArrowDown':
        e.preventDefault();
        setIsOpen(true);
        setActiveIndex(0);
        break;
      case 'ArrowUp':
        e.preventDefault();
        setIsOpen(true);
        setActiveIndex(items.length - 1);
        break;
    }
  }

  function handleMenuKeyDown(e: React.KeyboardEvent) {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setActiveIndex((prev) => (prev + 1) % items.length);
        break;
      case 'ArrowUp':
        e.preventDefault();
        setActiveIndex((prev) => (prev - 1 + items.length) % items.length);
        break;
      case 'Home':
        e.preventDefault();
        setActiveIndex(0);
        break;
      case 'End':
        e.preventDefault();
        setActiveIndex(items.length - 1);
        break;
      case 'Enter':
      case ' ':
        e.preventDefault();
        items[activeIndex]?.onSelect?.();
        setIsOpen(false);
        triggerRef.current?.focus();
        break;
      case 'Escape':
        setIsOpen(false);
        triggerRef.current?.focus(); // Focus'u tetikleyiciye geri ver
        break;
      case 'Tab':
        setIsOpen(false);           // Tab ile çıkınca kapat
        break;
    }
  }

  // Harf ile arama (type-ahead)
  function handleCharSearch(e: React.KeyboardEvent) {
    if (e.key.length === 1) {
      const char = e.key.toLowerCase();
      const matchIndex = items.findIndex(
        (item, i) => i > activeIndex && item.label.toLowerCase().startsWith(char)
      );
      if (matchIndex !== -1) setActiveIndex(matchIndex);
    }
  }

  return (
    <div className="dropdown">
      <button
        ref={triggerRef}
        aria-haspopup="menu"
        aria-expanded={isOpen}
        aria-controls="dropdown-menu"
        onClick={() => setIsOpen(!isOpen)}
        onKeyDown={handleTriggerKeyDown}
      >
        {trigger}
      </button>

      {isOpen && (
        <ul
          ref={menuRef}
          id="dropdown-menu"
          role="menu"
          aria-label="Seçenekler"
          onKeyDown={(e) => { handleMenuKeyDown(e); handleCharSearch(e); }}
        >
          {items.map((item, index) => (
            <li
              key={item.id}
              role="menuitem"
              tabIndex={index === activeIndex ? 0 : -1}
              aria-disabled={item.disabled}
              className={index === activeIndex ? 'dropdown__item--active' : ''}
              onClick={() => {
                if (!item.disabled) {
                  item.onSelect?.();
                  setIsOpen(false);
                }
              }}
              ref={(el) => {
                if (index === activeIndex) el?.focus();
              }}
            >
              {item.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

---

## 4. ARIA (Accessible Rich Internet Applications)

### 4.1 ARIA Kuralları

```
╔══════════════════════════════════════════════════════════════╗
║                  ARIA'NIN 5 ALTIN KURALI                    ║
╠══════════════════════════════════════════════════════════════╣
║ 1. Yerel HTML elementi yeterliyse ARIA KULLANMA            ║
║    <button> > <div role="button">                          ║
║                                                            ║
║ 2. Yerel semantiği ARIA ile değiştirme                     ║
║    ❌ <h2 role="tab"> → ✅ <div role="tab"><h2>...</h2>    ║
║                                                            ║
║ 3. Tüm interaktif ARIA elementleri klavye ile              ║
║    kullanılabilir olmalı                                   ║
║                                                            ║
║ 4. Görünür, focuslanabilir elemanlarda                     ║
║    role="presentation" veya aria-hidden="true" KULLANMA    ║
║                                                            ║
║ 5. Tüm interaktif elemanların erişilebilir adı olmalı     ║
║    (label, aria-label, aria-labelledby)                    ║
╚══════════════════════════════════════════════════════════════╝
```

### 4.2 Sık Kullanılan ARIA Desenleri

```html
<!-- ═══════ Tabs (Sekme) ═══════ -->
<div class="tabs">
  <div role="tablist" aria-label="Hesap ayarları">
    <button
      role="tab"
      id="tab-profile"
      aria-selected="true"
      aria-controls="panel-profile"
    >
      Profil
    </button>
    <button
      role="tab"
      id="tab-security"
      aria-selected="false"
      aria-controls="panel-security"
      tabindex="-1"
    >
      Güvenlik
    </button>
    <button
      role="tab"
      id="tab-notifications"
      aria-selected="false"
      aria-controls="panel-notifications"
      tabindex="-1"
    >
      Bildirimler
    </button>
  </div>

  <div
    role="tabpanel"
    id="panel-profile"
    aria-labelledby="tab-profile"
    tabindex="0"
  >
    Profil içeriği...
  </div>

  <div
    role="tabpanel"
    id="panel-security"
    aria-labelledby="tab-security"
    tabindex="0"
    hidden
  >
    Güvenlik içeriği...
  </div>
</div>

<!--
Klavye etkileşimi:
- Sol/Sağ ok: Sekme değiştir
- Home: İlk sekmeye git
- End: Son sekmeye git
- Tab sırasını düzgün yönet (sadece aktif tab tabindex="0")
-->

<!-- ═══════ Arama Kutusu (Combobox) ═══════ -->
<div class="search" role="combobox" aria-expanded="true" aria-haspopup="listbox">
  <label for="search-input" class="sr-only">Ürün Ara</label>
  <input
    id="search-input"
    type="search"
    role="searchbox"
    aria-autocomplete="list"
    aria-controls="search-results"
    aria-activedescendant="result-2"
    placeholder="Ürün ara..."
  />
  <ul id="search-results" role="listbox" aria-label="Arama sonuçları">
    <li id="result-1" role="option" aria-selected="false">iPhone 15</li>
    <li id="result-2" role="option" aria-selected="true">iPhone 15 Pro</li>
    <li id="result-3" role="option" aria-selected="false">iPhone 15 Pro Max</li>
  </ul>
</div>

<!-- ═══════ Progress Bar ═══════ -->
<div
  role="progressbar"
  aria-label="Dosya yükleme"
  aria-valuenow="65"
  aria-valuemin="0"
  aria-valuemax="100"
  aria-valuetext="%65 tamamlandı"
>
  <div class="progress-bar__fill" style="width: 65%"></div>
</div>

<!-- ═══════ Alert / Durum Mesajı ═══════ -->
<div role="alert">
  <!-- role="alert" → aria-live="assertive" + aria-atomic="true" -->
  Şifreniz başarıyla değiştirildi.
</div>

<div role="status">
  <!-- role="status" → aria-live="polite" -->
  3 sonuç bulundu.
</div>
```

### 4.3 aria-live Bölgeleri

```html
<!--
aria-live değerleri:
  "off"       → Değişiklikleri duyurma (varsayılan)
  "polite"    → Kullanıcı boştayken duyur (çoğu durum)
  "assertive" → Hemen duyur (kritik hatalar, acil bildirimler)

aria-atomic:
  "true"  → Tüm bölgeyi oku (tablo güncellemesi)
  "false" → Sadece değişen kısmı oku (varsayılan)

aria-relevant:
  "additions"  → Yeni eklenen elemanları duyur
  "removals"   → Kaldırılan elemanları duyur
  "text"       → Metin değişikliklerini duyur
  "all"        → Tüm değişiklikleri duyur
-->

<!-- Arama sonuç sayısı (kibar bildirim) -->
<div aria-live="polite" aria-atomic="true">
  <span id="result-count">15 sonuç bulundu</span>
</div>

<!-- Sepet güncelleme (kibar) -->
<div aria-live="polite" aria-atomic="true">
  Sepetinizde <strong>3</strong> ürün var.
</div>

<!-- Form hatası (acil) -->
<div aria-live="assertive" role="alert">
  E-posta adresi geçersiz. Lütfen kontrol edin.
</div>

<!-- Zamanlayıcı (düzenli güncelleme) -->
<div aria-live="polite" aria-atomic="true" aria-relevant="text">
  Kalan süre: <time>04:32</time>
</div>
```

---

## 5. Görsel Erişilebilirlik

### 5.1 Alternatif Metin (alt)

```html
<!-- ═══════ Alt Metin Kuralları ═══════ -->

<!-- 1. Bilgilendirici görsel: İçeriği açıkla -->
<img
  src="sales-chart.png"
  alt="2025 satış grafiği: Q1 $50K, Q2 $75K, Q3 $120K, Q4 $90K. En yüksek satış Q3'te."
/>

<!-- 2. Fonksiyonel görsel: Eylemi açıkla -->
<button>
  <img src="search-icon.svg" alt="Ara" />
</button>

<!-- 3. Dekoratif görsel: Boş alt (yok sayılır) -->
<img src="decorative-border.svg" alt="" role="presentation" />

<!-- 4. Karmaşık görsel: Uzun açıklama -->
<figure>
  <img
    src="architecture-diagram.png"
    alt="Sistem mimarisi diyagramı"
    aria-describedby="diagram-desc"
  />
  <figcaption id="diagram-desc">
    Sistem 3 katmandan oluşur: Frontend (React), API Gateway (Nginx),
    Backend (Node.js + PostgreSQL). İstemci istekleri API Gateway
    üzerinden yonlendirilir...
  </figcaption>
</figure>

<!-- 5. SVG İkon -->
<!-- Bağımsız ikon: aria-label ekle -->
<svg aria-label="Uyarı" role="img">
  <path d="..." />
</svg>

<!-- Metin yanında ikon: gizle -->
<button>
  <svg aria-hidden="true"><path d="..." /></svg>
  <span>Sil</span>
</button>
```

### 5.2 Renk Bağımsızlığı

```css
/* ❌ KÖTÜ: Sadece renk ile bilgi iletme */
.status-active { color: green; }
.status-error  { color: red; }

/* ✅ İYİ: Renk + ikon/metin/desen ile birlikte bilgi ilet */
.status-active {
  color: var(--color-success);
}
.status-active::before {
  content: '✓ ';    /* Renk körlüğünde bile ikon görünür */
}

.status-error {
  color: var(--color-danger);
}
.status-error::before {
  content: '✕ ';
}

/* Form hataları: Sadece kırmızı kenarlık değil, ikon + metin de ekle */
.input--error {
  border-color: var(--color-danger);
  border-width: 2px;                    /* Kalınlık ile de belirt */
  background-image: url('error-icon.svg');
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 40px;
}
```

---

## 6. Medya Erişilebilirliği

```html
<!-- Video: Altyazı ve transkript -->
<video controls>
  <source src="tutorial.mp4" type="video/mp4" />
  <track
    kind="captions"
    src="tutorial-tr.vtt"
    srclang="tr"
    label="Türkçe"
    default
  />
  <track
    kind="descriptions"
    src="tutorial-desc.vtt"
    srclang="tr"
    label="Sesli betimleme"
  />
  Tarayıcınız video etiketini desteklemiyor.
  <a href="tutorial.mp4">Videoyu indirin</a>.
</video>

<!-- Ses: Transkript bağlantısı -->
<audio controls>
  <source src="podcast.mp3" type="audio/mpeg" />
</audio>
<a href="/podcast-transcript">Metin transkripti</a>

<!-- Otomatik oynatma YAPMAYIN (veya sessize alın) -->
<!-- ❌ <video autoplay> -->
<!-- ✅ <video autoplay muted> (sessiz otomatik oynatma kabul edilebilir) -->
```

---

## 7. Test ve Denetim Araçları

### 7.1 Otomatik Test

```bash
# axe-core ile komut satırı testi
npx @axe-core/cli https://localhost:3000/

# Lighthouse erişilebilirlik denetimi
npx lighthouse https://localhost:3000/ --only-categories=accessibility --output=json

# pa11y (otomatik a11y tester)
npx pa11y https://localhost:3000/ --standard WCAG2AA
```

```typescript
// Jest + axe-core entegrasyonu
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

describe('LoginForm erişilebilirlik', () => {
  it('axe ihlali olmamalı', async () => {
    const { container } = render(<LoginForm />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

### 7.2 Manuel Test Kontrol Listesi

```
✅ Sadece Klavye Testi:
   1. Tab ile tüm interaktif elemanlara ulaşabiliyor musun?
   2. Focus göstergesi her elemanda görünüyor mu?
   3. Modal açıldığında focus trap çalışıyor mu?
   4. ESC ile modal/dropdown kapanıyor mu?
   5. Skip link çalışıyor mu?

✅ Ekran Okuyucu Testi (NVDA/VoiceOver):
   1. Sayfa başlığı okunuyor mu?
   2. Landmark'lar arasında navigasyon çalışıyor mu?
   3. Butonlar ve linkler ne yaptığını söylüyor mu?
   4. Form hataları duyuruluyor mu?
   5. Dinamik içerik (toast, sonuç sayısı) duyuruluyor mu?

✅ Görsel Test:
   1. 200% zoom'da sayfa bozulmuyor mu?
   2. 400% zoom'da yatay scroll olmuyor mu?
   3. Renk kontrastı AA geçiyor mu?
   4. Bilgi sadece renkle iletilmiyor mu?
   5. Hareket azaltma moda saygı duyuluyor mu?
```

---

## 8. Hızlı Referans

| Kural | Uygulama | WCAG Kriteri |
|---|---|---|
| Her `<img>` için `alt` | Bilgilendirici: açıkla, Dekoratif: `alt=""` | 1.1.1 (A) |
| Kontrast ≥ 4.5:1 | Normal metin | 1.4.3 (AA) |
| Kontrast ≥ 3:1 | Büyük metin + UI bileşenleri | 1.4.11 (AA) |
| Klavye erişimi | Tüm fonksiyonlar Tab/Enter/Space/Ok ile | 2.1.1 (A) |
| Focus göstergesi | `:focus-visible` ile belirgin outline | 2.4.7 (AA) |
| Skip link | Sayfanın başında `#main-content` linki | 2.4.1 (A) |
| Başlık hiyerarşisi | h1→h2→h3 sıralı, seviye atlamadan | 1.3.1 (A) |
| Form label | Her input'a bağlı `<label for="...">` | 1.3.1 (A) |
| Hata tanımlama | `aria-invalid` + `aria-describedby` | 3.3.1 (A) |
| Sayfa dili | `<html lang="tr">` | 3.1.1 (A) |
| 200% zoom | Yatay scroll olmadan okunabilir | 1.4.4 (AA) |
| Animasyon | `prefers-reduced-motion` saygı | 2.3.3 (AAA) |
| Zaman sınırı | Uzatılabilir veya kapatılabilir | 2.2.1 (A) |

---

## 9. Referanslar

- WCAG 2.2 teknik şartname: https://www.w3.org/TR/WCAG22/
- WAI-ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
- A11y Project Checklist: https://www.a11yproject.com/checklist/
- Inclusive Components: https://inclusive-components.design/
- Deque axe-core: https://github.com/dequelabs/axe-core
- WebAIM: https://webaim.org/
- MDN ARIA docs: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA
