# Arayüz (Frontend) Mimarisi — Kapsamlı Profesyonel Rehber

**Tarih:** 2026-04-07  
**Kategori:** Frontend Mimarisi, UI/UX, Erişilebilirlik, Performans  
**Seviye:** Orta-İleri  
**İlişkili Konular:** [Web Site Güvenliği](./web-guvenlik-rehberi.md), [Anti-Bot Güvenliği](./anti-bot-guvenligi-ve-rate-limit.md)

---

## 1. Giriş

Modern frontend geliştirme; yalnızca "görüntü oluşturma" değil, ölçeklenebilir mimari tasarlamak, kullanıcı deneyimini optimize etmek, performansı yönetmek ve güvenliği sağlamaktan oluşan disiplinler arası bir mühendislik alanıdır. Bu rehber, profesyonel seviyede frontend mimarisinin temel direklerini kapsar.

---

## 2. Proje Yapısı ve Modüler Mimari

### 2.1 Feature-Based (Özellik Tabanlı) Klasör Yapısı

Büyük projelerde dosyaları türe göre değil, özelliğe göre gruplamak bakımı kolaylaştırır.

```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   │   ├── LoginForm.tsx
│   │   │   ├── LoginForm.test.tsx
│   │   │   └── LoginForm.module.css
│   │   ├── hooks/
│   │   │   └── useAuth.ts
│   │   ├── services/
│   │   │   └── authApi.ts
│   │   ├── store/
│   │   │   └── authSlice.ts
│   │   └── index.ts          ← Public API (barrel export)
│   ├── dashboard/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── index.ts
│   └── products/
│       ├── components/
│       ├── hooks/
│       ├── services/
│       └── index.ts
├── shared/
│   ├── components/            ← Button, Modal, Toast vb.
│   ├── hooks/                 ← useDebounce, useLocalStorage
│   ├── utils/                 ← formatDate, cn() helper
│   ├── types/                 ← Ortak TypeScript tipleri
│   └── constants/
├── layouts/                   ← AppLayout, AuthLayout
├── routes/                    ← Route tanımları
├── styles/                    ← Global CSS, design tokens
└── App.tsx
```

**Barrel Export Deseni — `features/auth/index.ts`:**

```typescript
// Sadece dışarıya açılacak API'yi export et
// İç implementasyon detaylarını gizle
export { LoginForm } from './components/LoginForm';
export { useAuth } from './hooks/useAuth';
export type { AuthState, LoginCredentials } from './store/authSlice';

// ❌ Yanlış: Tüm dosyaları doğrudan import etmek
// import { validateEmail } from '../auth/services/authApi';
// ✅ Doğru: Barrel üzerinden import
// import { LoginForm, useAuth } from '@/features/auth';
```

---

### 2.2 Path Alias Konfigürasyonu

**`tsconfig.json` (veya `vite.config.ts`):**

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@features/*": ["src/features/*"],
      "@shared/*": ["src/shared/*"],
      "@layouts/*": ["src/layouts/*"]
    }
  }
}
```

```typescript
// ❌ Kötü: Göreli yol cehennemi
import { Button } from '../../../shared/components/Button';

// ✅ İyi: Temiz ve okunabilir
import { Button } from '@shared/components/Button';
```

---

## 3. Component Mimarisi

### 3.1 Compound Component Pattern

Birbiriyle ilişkili bileşenleri esnek bir API ile sunma deseni.

```tsx
import React, { createContext, useContext, useState, ReactNode } from 'react';

// ---- Context ----
interface AccordionContextType {
  activeIndex: number | null;
  toggle: (index: number) => void;
}

const AccordionCtx = createContext<AccordionContextType | null>(null);

function useAccordionCtx() {
  const ctx = useContext(AccordionCtx);
  if (!ctx) throw new Error('Accordion bileşenleri <Accordion> içinde kullanılmalıdır.');
  return ctx;
}

// ---- Ana Bileşen ----
interface AccordionProps {
  children: ReactNode;
  defaultIndex?: number;
}

function Accordion({ children, defaultIndex = null }: AccordionProps) {
  const [activeIndex, setActiveIndex] = useState<number | null>(defaultIndex);
  const toggle = (index: number) =>
    setActiveIndex(prev => (prev === index ? null : index));

  return (
    <AccordionCtx.Provider value={{ activeIndex, toggle }}>
      <div className="accordion" role="tablist">{children}</div>
    </AccordionCtx.Provider>
  );
}

// ---- Alt Bileşenler ----
function Item({ children, index }: { children: ReactNode; index: number }) {
  return <div className="accordion-item">{children}</div>;
}

function Header({ children, index }: { children: ReactNode; index: number }) {
  const { activeIndex, toggle } = useAccordionCtx();
  const isOpen = activeIndex === index;

  return (
    <button
      role="tab"
      aria-expanded={isOpen}
      aria-controls={`panel-${index}`}
      className="accordion-header"
      onClick={() => toggle(index)}
    >
      {children}
      <span className="accordion-icon">{isOpen ? '−' : '+'}</span>
    </button>
  );
}

function Panel({ children, index }: { children: ReactNode; index: number }) {
  const { activeIndex } = useAccordionCtx();
  const isOpen = activeIndex === index;

  return (
    <div
      id={`panel-${index}`}
      role="tabpanel"
      hidden={!isOpen}
      className="accordion-panel"
    >
      {isOpen && children}
    </div>
  );
}

// ---- API'yi birleştir ----
Accordion.Item = Item;
Accordion.Header = Header;
Accordion.Panel = Panel;

export { Accordion };

// ---- Kullanım ----
/*
<Accordion defaultIndex={0}>
  <Accordion.Item index={0}>
    <Accordion.Header index={0}>SSS Başlık 1</Accordion.Header>
    <Accordion.Panel index={0}>Cevap içeriği...</Accordion.Panel>
  </Accordion.Item>
  <Accordion.Item index={1}>
    <Accordion.Header index={1}>SSS Başlık 2</Accordion.Header>
    <Accordion.Panel index={1}>Cevap içeriği...</Accordion.Panel>
  </Accordion.Item>
</Accordion>
*/
```

---

### 3.2 Custom Hook'lar ile Logic Ayrımı

Bileşen mantığını UI'dan ayırmak test edilebilirliği artırır.

```typescript
// hooks/usePagination.ts
import { useState, useMemo } from 'react';

interface UsePaginationProps<T> {
  data: T[];
  itemsPerPage: number;
}

interface UsePaginationReturn<T> {
  currentPage: number;
  totalPages: number;
  paginatedData: T[];
  goToPage: (page: number) => void;
  nextPage: () => void;
  prevPage: () => void;
  isFirstPage: boolean;
  isLastPage: boolean;
}

export function usePagination<T>({
  data,
  itemsPerPage,
}: UsePaginationProps<T>): UsePaginationReturn<T> {
  const [currentPage, setCurrentPage] = useState(1);

  const totalPages = Math.ceil(data.length / itemsPerPage);

  const paginatedData = useMemo(() => {
    const start = (currentPage - 1) * itemsPerPage;
    return data.slice(start, start + itemsPerPage);
  }, [data, currentPage, itemsPerPage]);

  const goToPage = (page: number) => {
    setCurrentPage(Math.max(1, Math.min(page, totalPages)));
  };

  return {
    currentPage,
    totalPages,
    paginatedData,
    goToPage,
    nextPage: () => goToPage(currentPage + 1),
    prevPage: () => goToPage(currentPage - 1),
    isFirstPage: currentPage === 1,
    isLastPage: currentPage === totalPages,
  };
}
```

---

### 3.3 Render Props vs. Hook Karşılaştırma

```tsx
// ❌ Eski yöntem: Render Props (gereksiz iç içe geçme)
<DataFetcher url="/api/users">
  {({ data, loading, error }) => (
    <FilterableList data={data}>
      {({ filteredData }) => (
        <SortableList data={filteredData}>
          {({ sortedData }) => <UserList users={sortedData} />}
        </SortableList>
      )}
    </FilterableList>
  )}
</DataFetcher>

// ✅ Modern yöntem: Custom Hooks (düz ve okunabilir)
function UserListPage() {
  const { data, loading, error } = useFetch<User[]>('/api/users');
  const { filteredData } = useFilter(data, filterCriteria);
  const { sortedData } = useSort(filteredData, sortConfig);

  if (loading) return <Skeleton count={5} />;
  if (error) return <ErrorBoundary error={error} />;

  return <UserList users={sortedData} />;
}
```

---

## 4. State Management Stratejileri

### 4.1 State Yerleşim Karar Matrisi

| State Türü | Kapsam | Araç | Örnek |
|---|---|---|---|
| **UI State** | Tek bileşen | `useState` | Modal açık/kapalı, form input |
| **Shared UI** | Birkaç bileşen | Context API | Tema, dil seçimi |
| **Server State** | Sunucu verisi | TanStack Query | API verileri, cache |
| **Global App** | Tüm uygulama | Zustand / Redux | Auth, bildirimler |
| **URL State** | Navigasyon | React Router | Filtreler, arama, sayfa |
| **Form State** | Form yönetimi | React Hook Form | Karmaşık formlar |

### 4.2 Zustand ile Minimal Global State

```typescript
// store/useAppStore.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

interface Notification {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info';
}

interface AppState {
  // Auth
  user: User | null;
  isAuthenticated: boolean;
  login: (user: User) => void;
  logout: () => void;

  // Notifications
  notifications: Notification[];
  addNotification: (n: Omit<Notification, 'id'>) => void;
  removeNotification: (id: string) => void;

  // Theme
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

export const useAppStore = create<AppState>()(
  devtools(
    persist(
      (set, get) => ({
        // Auth
        user: null,
        isAuthenticated: false,
        login: (user) => set({ user, isAuthenticated: true }, false, 'auth/login'),
        logout: () => set({ user: null, isAuthenticated: false }, false, 'auth/logout'),

        // Notifications
        notifications: [],
        addNotification: (n) =>
          set(
            (state) => ({
              notifications: [
                ...state.notifications,
                { ...n, id: crypto.randomUUID() },
              ],
            }),
            false,
            'notifications/add'
          ),
        removeNotification: (id) =>
          set(
            (state) => ({
              notifications: state.notifications.filter((n) => n.id !== id),
            }),
            false,
            'notifications/remove'
          ),

        // Theme
        theme: 'dark',
        toggleTheme: () =>
          set(
            (state) => ({ theme: state.theme === 'dark' ? 'light' : 'dark' }),
            false,
            'theme/toggle'
          ),
      }),
      { name: 'app-storage', partialize: (state) => ({ theme: state.theme }) }
    )
  )
);

// ---- Selector ile Optimizasyon ----
// her bileşen sadece kendi ihtiyacı olan slice'ı dinler
// ❌ Kötü: Tüm store'u dinler → gereksiz yeniden render
// const { theme } = useAppStore();

// ✅ İyi: Sadece theme değişince render olur
// const theme = useAppStore((s) => s.theme);
```

### 4.3 TanStack Query ile Server State

```typescript
// services/productApi.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

interface Product {
  id: string;
  name: string;
  price: number;
  stock: number;
}

// ---- Query Keys Fabrikası ----
export const productKeys = {
  all:    ['products'] as const,
  lists:  () => [...productKeys.all, 'list'] as const,
  list:   (filters: Record<string, string>) => [...productKeys.lists(), filters] as const,
  detail: (id: string) => [...productKeys.all, 'detail', id] as const,
};

// ---- API Fonksiyonları ----
async function fetchProducts(filters: Record<string, string>): Promise<Product[]> {
  const params = new URLSearchParams(filters);
  const res = await fetch(`/api/products?${params}`, {
    credentials: 'include',       // Cookie gönder (→ güvenlik rehberine bkz.)
    headers: { 'Accept': 'application/json' },
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

async function createProduct(data: Omit<Product, 'id'>): Promise<Product> {
  const res = await fetch('/api/products', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRF-Token': getCSRFToken(),   // → güvenlik rehberine bkz.
    },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// ---- React Hooks ----
export function useProducts(filters: Record<string, string> = {}) {
  return useQuery({
    queryKey: productKeys.list(filters),
    queryFn: () => fetchProducts(filters),
    staleTime: 5 * 60 * 1000,        // 5 dk boyunca taze kabul et
    gcTime: 10 * 60 * 1000,          // 10 dk cache'te tut
    retry: 2,
    refetchOnWindowFocus: false,
  });
}

export function useCreateProduct() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createProduct,
    onSuccess: () => {
      // Ürün listesini otomatik yenile
      queryClient.invalidateQueries({ queryKey: productKeys.lists() });
    },
    onError: (error) => {
      console.error('Ürün oluşturulamadı:', error);
    },
  });
}

function getCSRFToken(): string {
  return document.querySelector<HTMLMetaElement>('meta[name="csrf-token"]')?.content ?? '';
}
```

---

## 5. Modern CSS Mimarisi

### 5.1 Design Tokens (CSS Custom Properties)

```css
/* styles/tokens.css */
:root {
  /* ---- Renk Skalası ---- */
  --color-gray-50:  #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-700: #374151;
  --color-gray-800: #1f2937;
  --color-gray-900: #111827;

  --color-primary-400: #60a5fa;
  --color-primary-500: #3b82f6;
  --color-primary-600: #2563eb;

  --color-danger-500: #ef4444;
  --color-success-500: #22c55e;

  /* ---- Semantic Tokens (Tema Bağımlı) ---- */
  --bg-primary:   var(--color-gray-50);
  --bg-surface:   #ffffff;
  --bg-elevated:  #ffffff;
  --text-primary: var(--color-gray-900);
  --text-secondary: var(--color-gray-700);
  --border-default: var(--color-gray-200);

  /* ---- Tipografi ---- */
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  --text-xs:  0.75rem;    /* 12px */
  --text-sm:  0.875rem;   /* 14px */
  --text-base: 1rem;      /* 16px */
  --text-lg:  1.125rem;   /* 18px */
  --text-xl:  1.25rem;    /* 20px */
  --text-2xl: 1.5rem;     /* 24px */
  --text-3xl: 1.875rem;   /* 30px */

  /* ---- Aralık (Spacing) ---- */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;

  /* ---- Gölge ---- */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);

  /* ---- Köşe Yuvarlaklığı ---- */
  --radius-sm: 0.375rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-full: 9999px;

  /* ---- Geçiş ---- */
  --transition-fast: 150ms ease;
  --transition-base: 250ms ease;
}

/* ---- Dark Mode ---- */
[data-theme='dark'] {
  --bg-primary:   var(--color-gray-900);
  --bg-surface:   var(--color-gray-800);
  --bg-elevated:  var(--color-gray-700);
  --text-primary: var(--color-gray-50);
  --text-secondary: var(--color-gray-200);
  --border-default: var(--color-gray-700);

  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
}
```

### 5.2 Responsive Tasarım — Container Query + Media Query

```css
/* ---- Mobile-First Media Queries ---- */
/* Küçükten büyüğe doğru yazılır */
.grid-layout {
  display: grid;
  gap: var(--space-4);
  grid-template-columns: 1fr;             /* Mobil: tek sütun */
}

@media (min-width: 640px) {                /* sm: Tablet */
  .grid-layout { grid-template-columns: repeat(2, 1fr); }
}

@media (min-width: 1024px) {               /* lg: Desktop */
  .grid-layout { grid-template-columns: repeat(3, 1fr); }
}

@media (min-width: 1280px) {               /* xl: Geniş ekran */
  .grid-layout { grid-template-columns: repeat(4, 1fr); }
}

/* ---- Container Queries (Bileşen Bazlı Responsive) ---- */
/* Media query: viewport'a göre. Container query: parent'a göre. */
.card-container {
  container-type: inline-size;
  container-name: card;
}

.card {
  display: flex;
  flex-direction: column;
  padding: var(--space-4);
}

/* Kart konteyneri 400px'den genişse yatay düzene geç */
@container card (min-width: 400px) {
  .card {
    flex-direction: row;
    align-items: center;
    gap: var(--space-4);
  }
  .card__image { width: 40%; flex-shrink: 0; }
  .card__content { flex: 1; }
}
```

---

## 6. Erişilebilirlik (a11y) — WCAG 2.2 Uyumluluğu

### 6.1 Semantik HTML Kuralları

```html
<!-- ❌ Kötü: Tüm yapı div ile -->
<div class="header">
  <div class="nav">
    <div class="nav-item" onclick="navigate('/')">Ana Sayfa</div>
  </div>
</div>
<div class="content">
  <div class="article-title">Başlık</div>
  <div class="text">İçerik</div>
</div>

<!-- ✅ İyi: Semantik HTML5 etiketleri -->
<header>
  <nav aria-label="Ana menü">
    <ul role="menubar">
      <li role="none">
        <a href="/" role="menuitem">Ana Sayfa</a>
      </li>
      <li role="none">
        <a href="/urunler" role="menuitem">Ürünler</a>
      </li>
    </ul>
  </nav>
</header>

<main id="main-content">
  <article>
    <h1>Sayfa Başlığı</h1>
    <p>İçerik metni...</p>
  </article>

  <aside aria-label="İlgili yazılar">
    <h2>Bunları da okuyun</h2>
    <!-- ... -->
  </aside>
</main>

<footer>
  <p>&copy; 2026 Şirket Adı</p>
</footer>
```

### 6.2 Klavye Navigasyonu ve Focus Yönetimi

```css
/* ---- Focus Görseli: Asla kaldırma, özelleştir ---- */
/* ❌ outline: none; YAPMAYIN */

*:focus-visible {
  outline: 2px solid var(--color-primary-500);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}

/* Fare ile tıklamada focus halkası gösterme, sadece klavyede göster */
*:focus:not(:focus-visible) {
  outline: none;
}

/* Skip Link — Klavye kullanıcıları için */
.skip-link {
  position: absolute;
  top: -100%;
  left: var(--space-4);
  z-index: 9999;
  padding: var(--space-2) var(--space-4);
  background: var(--color-primary-500);
  color: white;
  border-radius: var(--radius-md);
  text-decoration: none;
  font-weight: 600;
}

.skip-link:focus {
  top: var(--space-4);
}
```

```html
<body>
  <a href="#main-content" class="skip-link">İçeriğe atla</a>
  <!-- header, nav... -->
  <main id="main-content" tabindex="-1">
    <!-- Ana içerik -->
  </main>
</body>
```

### 6.3 ARIA ile Erişilebilir Modal

```tsx
import { useEffect, useRef, useCallback } from 'react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export function AccessibleModal({ isOpen, onClose, title, children }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  // Açılınca focus'u yakala, kapanınca geri ver
  useEffect(() => {
    if (isOpen) {
      previousFocusRef.current = document.activeElement as HTMLElement;
      // İlk focuslanabilir elemana odaklan
      const firstFocusable = modalRef.current?.querySelector<HTMLElement>(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      firstFocusable?.focus();
    } else {
      previousFocusRef.current?.focus();
    }
  }, [isOpen]);

  // ESC ile kapatma
  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
        return;
      }

      // Focus Trap: Tab ile modal dışına çıkmayı engelle
      if (e.key === 'Tab') {
        const focusableEls = modalRef.current?.querySelectorAll<HTMLElement>(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        if (!focusableEls?.length) return;

        const firstEl = focusableEls[0];
        const lastEl = focusableEls[focusableEls.length - 1];

        if (e.shiftKey && document.activeElement === firstEl) {
          e.preventDefault();
          lastEl.focus();
        } else if (!e.shiftKey && document.activeElement === lastEl) {
          e.preventDefault();
          firstEl.focus();
        }
      }
    },
    [onClose]
  );

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div className="modal-backdrop" aria-hidden="true" onClick={onClose} />

      {/* Modal */}
      <div
        ref={modalRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        className="modal"
        onKeyDown={handleKeyDown}
      >
        <h2 id="modal-title">{title}</h2>
        <div className="modal-body">{children}</div>
        <button onClick={onClose} aria-label="Modalı kapat" className="modal-close">
          ✕
        </button>
      </div>
    </>
  );
}
```

---

## 7. Performans Optimizasyonu

### 7.1 Code Splitting ve Lazy Loading

```tsx
import { lazy, Suspense } from 'react';

// Route bazlı code splitting
const Dashboard = lazy(() => import('./features/dashboard/pages/DashboardPage'));
const Settings = lazy(() => import('./features/settings/pages/SettingsPage'));
const Analytics = lazy(() =>
  import('./features/analytics/pages/AnalyticsPage')
    .then(module => ({ default: module.AnalyticsPage })) // Named export varsa
);

function AppRoutes() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/analytics" element={<Analytics />} />
      </Routes>
    </Suspense>
  );
}

// Skeleton Loading bileşeni
function PageSkeleton() {
  return (
    <div className="skeleton-page" role="progressbar" aria-label="Sayfa yükleniyor">
      <div className="skeleton-header pulse" />
      <div className="skeleton-content">
        <div className="skeleton-line pulse" style={{ width: '80%' }} />
        <div className="skeleton-line pulse" style={{ width: '60%' }} />
        <div className="skeleton-line pulse" style={{ width: '70%' }} />
      </div>
    </div>
  );
}
```

### 7.2 Görüntü Optimizasyonu

```html
<!-- ---- Responsive Images ---- -->
<picture>
  <!-- Modern format: AVIF (en küçük boyut) -->
  <source
    type="image/avif"
    srcset="hero-400.avif 400w, hero-800.avif 800w, hero-1200.avif 1200w"
    sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
  />
  <!-- Fallback: WebP -->
  <source
    type="image/webp"
    srcset="hero-400.webp 400w, hero-800.webp 800w, hero-1200.webp 1200w"
    sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
  />
  <!-- Son çare: JPEG -->
  <img
    src="hero-800.jpg"
    alt="Ürün görseli açıklaması"
    width="800"
    height="600"
    loading="lazy"
    decoding="async"
    fetchpriority="low"
  />
</picture>

<!-- ---- LCP (Largest Contentful Paint) Hero Görseli ---- -->
<!-- Sayfa başındaki büyük görsel: lazy YAPMA, preload yap -->
<link rel="preload" as="image" href="hero-main.avif" type="image/avif" />
<img
  src="hero-main.avif"
  alt="Ana banner"
  width="1200"
  height="600"
  fetchpriority="high"
  decoding="async"
/>
```

### 7.3 Debounce ve Throttle

```typescript
// hooks/useDebounce.ts
import { useState, useEffect } from 'react';

export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// ---- Kullanım: Arama sayfası ----
function SearchPage() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 300);

  // debouncedQuery değiştiğinde API çağrısı yap
  const { data, isLoading } = useProducts({ search: debouncedQuery });

  return (
    <div>
      <input
        type="search"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ürün ara..."
        aria-label="Ürün arama"
      />
      {isLoading ? <Spinner /> : <ProductGrid products={data} />}
    </div>
  );
}
```

---

## 8. Test Stratejisi

### 8.1 Test Piramidi

```
        ╱╲
       ╱  ╲         E2E Testler (Playwright/Cypress)
      ╱    ╲        → Kritik kullanıcı akışları (login, checkout)
     ╱──────╲       → Yavaş, az sayıda
    ╱        ╲
   ╱  Entegr. ╲    Entegrasyon Testleri (Testing Library)
  ╱            ╲   → Hook + bileşen birlikte test
 ╱──────────────╲  → Orta hız, orta sayıda
╱                ╲
╱   Birim Test    ╲ Unit Testler (Vitest/Jest)
╱──────────────────╲ → Saf fonksiyonlar, util'ler
                     → Hızlı, çok sayıda
```

### 8.2 Bileşen Testi Örneği (Testing Library)

```typescript
// components/LoginForm.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  const mockOnSubmit = vi.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  it('boş form gönderilince hata gösterir', async () => {
    render(<LoginForm onSubmit={mockOnSubmit} />);
    
    await userEvent.click(screen.getByRole('button', { name: /giriş yap/i }));

    expect(screen.getByText(/email gerekli/i)).toBeInTheDocument();
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('geçerli bilgilerle form gönderir', async () => {
    render(<LoginForm onSubmit={mockOnSubmit} />);
    
    await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com');
    await userEvent.type(screen.getByLabelText(/şifre/i), 'SecurePass123!');
    await userEvent.click(screen.getByRole('button', { name: /giriş yap/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'SecurePass123!',
      });
    });
  });

  it('şifre alanı type="password" olmalı', () => {
    render(<LoginForm onSubmit={mockOnSubmit} />);
    expect(screen.getByLabelText(/şifre/i)).toHaveAttribute('type', 'password');
  });
});
```

---

## 9. Hızlı Referans Cheatsheet

| Konu | Kural | Neden |
|---|---|---|
| Proje yapısı | Feature-based klasörleme | Ölçeklenebilirlik, kolay navigasyon |
| Import | Path alias (`@/`) kullan | Göreli yol karmaşası önlenir |
| State | Server state ≠ Client state | TanStack Query vs Zustand ayrımı |
| CSS | Design tokens kullan | Tutarlılık, tema desteği |
| Responsive | Mobile-first + Container Query | Bileşen bazlı uyumluluk |
| Erişilebilirlik | Semantik HTML + ARIA | Yasal zorunluluk + daha iyi UX |
| Focus | `:focus-visible` özelleştir | Klavye kullanıcıları için kritik |
| Performans | Lazy load + Code split | İlk yükleme süresini düşürür |
| Görseller | AVIF > WebP > JPEG, `loading="lazy"` | Bant genişliği tasarrufu |
| Test | Testing Library + Vitest | Kullanıcı davranışı odaklı test |

---

## 10. Referanslar ve İleri Okuma

- MDN Web Docs — HTML Semantics: https://developer.mozilla.org/en-US/docs/Web/HTML
- WCAG 2.2 Guidelines: https://www.w3.org/TR/WCAG22/
- web.dev — Performance: https://web.dev/performance/
- TanStack Query Docs: https://tanstack.com/query
- Zustand GitHub: https://github.com/pmndrs/zustand
- Testing Library: https://testing-library.com/
- CSS Container Queries: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries
- Patterns.dev — React Design Patterns: https://www.patterns.dev/
