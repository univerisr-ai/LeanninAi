# Frontend Geliştirme — En Üst Seviye Profesyonel Rehber

**Tarih:** 2026-04-07  
**Kategori:** Frontend Geliştirme, React, TypeScript, Performans, PWA  
**Seviye:** İleri  
**İlişkili Konular:** [Frontend Mimarisi](./frontend-mimarisi-rehberi.md), [Backend Geliştirme](./backend-gelistirme-rehberi.md), [Web Güvenliği](./web-guvenlik-rehberi.md)

---

## 1. İleri TypeScript Desenleri

### 1.1 Discriminated Unions ile Tip-Güvenli State

```typescript
// ---- API Response State Machine ----
// Her durumun hangi alanları taşıdığı derleme zamanında garanti altında

type AsyncState<T, E = Error> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T; updatedAt: Date }
  | { status: 'error'; error: E; retryCount: number };

// Kullanım: TypeScript compiler duruma göre alanları bilir
function renderState<T>(state: AsyncState<T>): string {
  switch (state.status) {
    case 'idle':
      return 'Bekleniyor...';
    case 'loading':
      return 'Yükleniyor...';
    case 'success':
      // ✅ state.data burada güvenli, TypeScript bilir
      return `Veri: ${JSON.stringify(state.data)}`;
    case 'error':
      // ✅ state.error burada güvenli
      return `Hata: ${state.error.message} (${state.retryCount}. deneme)`;
  }
}

// ---- Exhaustive Check: Tüm durumların ele alındığını garanti et ----
function assertNever(x: never): never {
  throw new Error(`Beklenmeyen değer: ${x}`);
}

function handleAction(action: UserAction): void {
  switch (action.type) {
    case 'LOGIN': /* ... */ break;
    case 'LOGOUT': /* ... */ break;
    case 'UPDATE_PROFILE': /* ... */ break;
    default:
      // Yeni bir action eklendiğinde TypeScript burada hata verir
      assertNever(action);
  }
}
```

### 1.2 Generic Constraint'ler ve Utility Types

```typescript
// ---- API Client: Tip-güvenli endpoint tanımları ----
interface ApiEndpoints {
  '/users': {
    GET: { response: User[]; query: { role?: string; page?: number } };
    POST: { response: User; body: CreateUserDTO };
  };
  '/users/:id': {
    GET: { response: User };
    PUT: { response: User; body: UpdateUserDTO };
    DELETE: { response: void };
  };
  '/products': {
    GET: { response: Product[]; query: { category?: string } };
  };
}

// Generic fetch fonksiyonu: URL ve metoda göre tip çıkarımı
type EndpointConfig<
  Path extends keyof ApiEndpoints,
  Method extends keyof ApiEndpoints[Path]
> = ApiEndpoints[Path][Method];

async function apiCall<
  Path extends keyof ApiEndpoints,
  Method extends keyof ApiEndpoints[Path]
>(
  path: Path,
  method: Method,
  options?: {
    body?: 'body' extends keyof EndpointConfig<Path, Method>
      ? EndpointConfig<Path, Method>['body']
      : never;
    query?: 'query' extends keyof EndpointConfig<Path, Method>
      ? EndpointConfig<Path, Method>['query']
      : never;
  }
): Promise<EndpointConfig<Path, Method>['response']> {
  // Implementasyon...
  const url = new URL(path, BASE_URL);
  if (options?.query) {
    Object.entries(options.query).forEach(([k, v]) => {
      if (v !== undefined) url.searchParams.set(k, String(v));
    });
  }

  const res = await fetch(url.toString(), {
    method: method as string,
    headers: { 'Content-Type': 'application/json' },
    body: options?.body ? JSON.stringify(options.body) : undefined,
  });

  return res.json();
}

// ✅ Tam tip güvenliği
const users = await apiCall('/users', 'GET', { query: { role: 'admin' } });
// users tipi: User[]

const newUser = await apiCall('/users', 'POST', {
  body: { email: 'test@test.com', name: 'Test' }
});
// newUser tipi: User

// ❌ TypeScript hatası: '/users' POST endpoint'i query almaz
// await apiCall('/users', 'POST', { query: { page: 1 } });
```

### 1.3 Branded Types (Değer Nesneleri)

```typescript
// Aynı "string" olan ama birbirine karıştırılmaması gereken değerler
type UserId = string & { readonly __brand: 'UserId' };
type OrderId = string & { readonly __brand: 'OrderId' };
type ProductId = string & { readonly __brand: 'ProductId' };

// Fabrika fonksiyonları
function UserId(id: string): UserId { return id as UserId; }
function OrderId(id: string): OrderId { return id as OrderId; }

// Kullanım
function getOrder(orderId: OrderId): Promise<Order> { /* ... */ }

const userId = UserId('user-123');
const orderId = OrderId('order-456');

getOrder(orderId);   // ✅ Doğru
// getOrder(userId); // ❌ TypeScript hatası! UserId ≠ OrderId
```

---

## 2. İleri React Desenleri

### 2.1 Polymorphic Components (as prop)

Bir bileşenin farklı HTML elementleri olarak render edilmesi.

```tsx
import React, { ElementType, ComponentPropsWithoutRef } from 'react';

// ---- Tip tanımları ----
type PolymorphicProps<E extends ElementType, Props = {}> = Props &
  Omit<ComponentPropsWithoutRef<E>, keyof Props> & {
    as?: E;
  };

// ---- Button bileşeni: <button>, <a>, <Link> olarak render edilebilir ----
interface ButtonBaseProps {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

type ButtonProps<E extends ElementType = 'button'> = PolymorphicProps<E, ButtonBaseProps>;

function Button<E extends ElementType = 'button'>({
  as,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  children,
  className,
  disabled,
  ...rest
}: ButtonProps<E>) {
  const Component = as || 'button';

  const classes = [
    'btn',
    `btn--${variant}`,
    `btn--${size}`,
    isLoading && 'btn--loading',
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <Component
      className={classes}
      disabled={disabled || isLoading}
      {...rest}
    >
      {isLoading && <span className="btn__spinner" aria-hidden="true" />}
      <span className={isLoading ? 'btn__text--hidden' : ''}>
        {children}
      </span>
    </Component>
  );
}

// ---- Kullanım ----
// Normal button
<Button variant="primary" onClick={handleClick}>Kaydet</Button>

// Link olarak
<Button as="a" href="/about" variant="ghost">Hakkımızda</Button>

// React Router Link olarak
<Button as={Link} to="/dashboard" variant="secondary">Dashboard</Button>
```

### 2.2 Optimistic Updates (İyimser Güncelleme)

Kullanıcı deneyimini hızlandırmak için sunucu yanıtını beklemeden UI'ı güncelleme.

```typescript
// hooks/useOptimisticUpdate.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';

interface Todo {
  id: string;
  text: string;
  completed: boolean;
}

export function useToggleTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (todoId: string) => {
      const res = await fetch(`/api/todos/${todoId}/toggle`, { method: 'PATCH' });
      return res.json() as Promise<Todo>;
    },

    // 1. Mutasyon başlamadan önce çağrılır
    onMutate: async (todoId: string) => {
      // Devam eden refetch'leri iptal et (çakışma önleme)
      await queryClient.cancelQueries({ queryKey: ['todos'] });

      // Mevcut veriyi yedekle (rollback için)
      const previousTodos = queryClient.getQueryData<Todo[]>(['todos']);

      // Cache'i iyimser güncelle
      queryClient.setQueryData<Todo[]>(['todos'], (old) =>
        old?.map((todo) =>
          todo.id === todoId
            ? { ...todo, completed: !todo.completed }
            : todo
        )
      );

      // Context olarak döndür (onError'da kullanılacak)
      return { previousTodos };
    },

    // 2. Hata durumunda rollback
    onError: (_err, _todoId, context) => {
      if (context?.previousTodos) {
        queryClient.setQueryData(['todos'], context.previousTodos);
      }
      toast.error('Güncelleme başarısız oldu.');
    },

    // 3. Her durumda (başarılı/başarısız) sunucu ile senkronize ol
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });
}

// ---- Bileşende kullanım ----
function TodoItem({ todo }: { todo: Todo }) {
  const toggleMutation = useToggleTodo();

  return (
    <li
      className={`todo-item ${todo.completed ? 'todo-item--done' : ''}`}
      onClick={() => toggleMutation.mutate(todo.id)}
      role="checkbox"
      aria-checked={todo.completed}
      tabIndex={0}
      onKeyDown={(e) => e.key === 'Enter' && toggleMutation.mutate(todo.id)}
    >
      <span className="todo-item__checkbox">
        {todo.completed ? '✓' : '○'}
      </span>
      <span className="todo-item__text">{todo.text}</span>
    </li>
  );
}
```

### 2.3 Error Boundary ile Hata İzolasyonu

```tsx
// shared/components/ErrorBoundary.tsx
import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode | ((error: Error, reset: () => void) => ReactNode);
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Hata raporlama servisine gönder
    this.props.onError?.(error, errorInfo);
    
    console.error('[ErrorBoundary]', {
      error: error.message,
      componentStack: errorInfo.componentStack,
    });
  }

  reset = () => {
    this.setState({ error: null });
  };

  render() {
    if (this.state.error) {
      // Custom fallback
      if (typeof this.props.fallback === 'function') {
        return this.props.fallback(this.state.error, this.reset);
      }
      if (this.props.fallback) {
        return this.props.fallback;
      }

      // Varsayılan hata ekranı
      return (
        <div className="error-boundary" role="alert">
          <div className="error-boundary__icon">⚠️</div>
          <h2>Bir sorun oluştu</h2>
          <p className="error-boundary__message">
            {this.state.error.message}
          </p>
          <button
            className="btn btn--primary"
            onClick={this.reset}
          >
            Tekrar Dene
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

// ---- Kullanım: Sayfa bazlı izolasyon ----
function App() {
  return (
    <ErrorBoundary onError={(err) => Sentry.captureException(err)}>
      <Header />
      <main>
        {/* Her feature kendi ErrorBoundary'sine sahip */}
        <ErrorBoundary
          fallback={(error, reset) => (
            <div className="section-error">
              <p>Dashboard yüklenemedi: {error.message}</p>
              <button onClick={reset}>Yeniden Yükle</button>
            </div>
          )}
        >
          <Dashboard />
        </ErrorBoundary>
      </main>
    </ErrorBoundary>
  );
}
```

---

## 3. İleri CSS Teknikleri

### 3.1 CSS Animasyon Sistemi

```css
/* ---- Temel Animasyon Token'ları ---- */
:root {
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out-circ: cubic-bezier(0.85, 0, 0.15, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);

  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --duration-slow: 500ms;
}

/* ---- Prefers Reduced Motion: Animasyonu devre dışı bırak ---- */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* ---- Sayfa Geçiş Animasyonları ---- */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

/* ---- Bileşen Animasyonları ---- */
.page-enter {
  animation: fadeInUp var(--duration-slow) var(--ease-out-expo) both;
}

.card {
  transition: transform var(--duration-normal) var(--ease-spring),
              box-shadow var(--duration-normal) ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

/* Stagger animasyon: Liste elemanları sırayla belirsin */
.stagger-list > * {
  animation: fadeInUp var(--duration-normal) var(--ease-out-expo) both;
}

.stagger-list > *:nth-child(1) { animation-delay: 0ms; }
.stagger-list > *:nth-child(2) { animation-delay: 50ms; }
.stagger-list > *:nth-child(3) { animation-delay: 100ms; }
.stagger-list > *:nth-child(4) { animation-delay: 150ms; }
.stagger-list > *:nth-child(5) { animation-delay: 200ms; }
.stagger-list > *:nth-child(n+6) { animation-delay: 250ms; }

/* Skeleton Loading */
.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-gray-200) 25%,
    var(--color-gray-100) 50%,
    var(--color-gray-200) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite linear;
  border-radius: var(--radius-sm);
}

/* ---- Glassmorphism ---- */
.glass {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(12px) saturate(150%);
  -webkit-backdrop-filter: blur(12px) saturate(150%);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: var(--radius-lg);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
}

[data-theme='dark'] .glass {
  background: rgba(0, 0, 0, 0.25);
  border-color: rgba(255, 255, 255, 0.08);
}
```

### 3.2 Modern Layout Desenleri

```css
/* ---- Holy Grail Layout (Grid) ---- */
.app-layout {
  display: grid;
  grid-template-areas:
    "header  header  header"
    "sidebar main   aside"
    "footer  footer  footer";
  grid-template-columns: 260px 1fr 300px;
  grid-template-rows: auto 1fr auto;
  min-height: 100dvh;             /* dvh: Dynamic viewport height (mobil uyumlu) */
}

.app-layout__header  { grid-area: header; }
.app-layout__sidebar { grid-area: sidebar; }
.app-layout__main    { grid-area: main; overflow-y: auto; }
.app-layout__aside   { grid-area: aside; }
.app-layout__footer  { grid-area: footer; }

/* Mobilde: tek sütun */
@media (max-width: 1024px) {
  .app-layout {
    grid-template-areas:
      "header"
      "main"
      "footer";
    grid-template-columns: 1fr;
  }
  .app-layout__sidebar,
  .app-layout__aside {
    display: none;  /* veya off-canvas menü */
  }
}

/* ---- Intrinsic Design: İçeriğe göre uyumlu grid ---- */
.auto-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(280px, 100%), 1fr));
  gap: var(--space-6);
}

/* ---- Sticky Header + Scroll Shadow ---- */
.sticky-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--bg-surface);
  transition: box-shadow var(--duration-fast) ease;
}

/* JavaScript ile scroll olunca shadow ekle */
.sticky-header[data-scrolled='true'] {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* ---- CSS Scroll Snap (Carousel) ---- */
.carousel {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scrollbar-width: none;           /* Firefox */
  -ms-overflow-style: none;        /* IE/Edge */
  gap: var(--space-4);
  padding: var(--space-4);
}

.carousel::-webkit-scrollbar { display: none; }  /* Chrome/Safari */

.carousel__item {
  scroll-snap-align: start;
  flex: 0 0 calc(33.333% - var(--space-4));
  min-width: 280px;
}
```

---

## 4. Gerçek Zamanlı Özellikler (Real-time)

### 4.1 WebSocket ile Canlı Veri

```typescript
// hooks/useWebSocket.ts
import { useEffect, useRef, useCallback, useState } from 'react';

type WSStatus = 'connecting' | 'open' | 'closed' | 'error';

interface UseWebSocketOptions {
  url: string;
  onMessage?: (data: any) => void;
  reconnectAttempts?: number;
  reconnectInterval?: number;
  heartbeatInterval?: number;
}

export function useWebSocket({
  url,
  onMessage,
  reconnectAttempts = 5,
  reconnectInterval = 3000,
  heartbeatInterval = 30000,
}: UseWebSocketOptions) {
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectCountRef = useRef(0);
  const heartbeatRef = useRef<NodeJS.Timeout>();
  const [status, setStatus] = useState<WSStatus>('connecting');

  const connect = useCallback(() => {
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => {
      setStatus('open');
      reconnectCountRef.current = 0;

      // Heartbeat: bağlantı canlı mı kontrol et
      heartbeatRef.current = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: 'ping' }));
        }
      }, heartbeatInterval);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'pong') return; // Heartbeat yanıtı
        onMessage?.(data);
      } catch (err) {
        console.error('WS mesaj parse hatası:', err);
      }
    };

    ws.onclose = (event) => {
      setStatus('closed');
      clearInterval(heartbeatRef.current);

      // Otomatik yeniden bağlanma
      if (!event.wasClean && reconnectCountRef.current < reconnectAttempts) {
        reconnectCountRef.current++;
        const delay = reconnectInterval * Math.pow(1.5, reconnectCountRef.current);
        console.log(`WS yeniden bağlanma: ${reconnectCountRef.current}/${reconnectAttempts}`);
        setTimeout(connect, delay);
      }
    };

    ws.onerror = () => setStatus('error');
  }, [url, onMessage, reconnectAttempts, reconnectInterval, heartbeatInterval]);

  // Mesaj gönderme
  const send = useCallback((data: unknown) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data));
    }
  }, []);

  // Bağlantıyı başlat ve temizle
  useEffect(() => {
    connect();
    return () => {
      clearInterval(heartbeatRef.current);
      wsRef.current?.close(1000, 'Component unmount');
    };
  }, [connect]);

  return { status, send };
}

// ---- Kullanım: Canlı bildirimler ----
function NotificationCenter() {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const { status } = useWebSocket({
    url: `wss://api.example.com/ws?token=${accessToken}`,
    onMessage: (data) => {
      if (data.type === 'notification') {
        setNotifications((prev) => [data.payload, ...prev].slice(0, 50));
        // Tarayıcı bildirimi
        if (Notification.permission === 'granted') {
          new Notification(data.payload.title, { body: data.payload.message });
        }
      }
    },
  });

  return (
    <div className="notification-center">
      <div className={`ws-status ws-status--${status}`}>
        {status === 'open' ? '🟢 Canlı' : '🔴 Bağlantı kesildi'}
      </div>
      <ul className="notification-list stagger-list">
        {notifications.map((n) => (
          <li key={n.id} className="notification-item">
            <strong>{n.title}</strong>
            <p>{n.message}</p>
            <time>{formatRelativeTime(n.createdAt)}</time>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### 4.2 Server-Sent Events (SSE) — Tek Yönlü Stream

```typescript
// hooks/useSSE.ts
export function useServerSentEvents<T>(
  url: string,
  onEvent: (data: T) => void,
) {
  useEffect(() => {
    const eventSource = new EventSource(url, { withCredentials: true });

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as T;
        onEvent(data);
      } catch (err) {
        console.error('SSE parse hatası:', err);
      }
    };

    eventSource.onerror = () => {
      // Tarayıcı otomatik yeniden bağlanır
      console.warn('SSE bağlantı hatası, yeniden bağlanılıyor...');
    };

    return () => eventSource.close();
  }, [url, onEvent]);
}

// ---- Backend: Express SSE endpoint ----
app.get('/api/stream/prices', authenticate, (req, res) => {
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'X-Accel-Buffering': 'no',   // Nginx buffering'i kapat
  });

  const interval = setInterval(() => {
    const priceUpdate = { symbol: 'BTC', price: getLatestPrice(), timestamp: Date.now() };
    res.write(`data: ${JSON.stringify(priceUpdate)}\n\n`);
  }, 1000);

  req.on('close', () => {
    clearInterval(interval);
    res.end();
  });
});
```

---

## 5. Progressive Web App (PWA)

### 5.1 Service Worker (Cache Stratejileri)

```javascript
// public/sw.js
const CACHE_NAME = 'app-v1.0.0';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/assets/main.css',
  '/assets/main.js',
  '/offline.html',
];

// ---- Install: Statik dosyaları cache'le ----
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting(); // Hemen aktif ol
});

// ---- Activate: Eski cache'leri temizle ----
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      )
    )
  );
  self.clients.claim(); // Tüm tab'ları hemen kontrol et
});

// ---- Fetch: İstek yakalama stratejileri ----
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // API istekleri: Network First (önce sunucu, offline'da cache)
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(networkFirst(request));
    return;
  }

  // Statik assetler: Cache First (önce cache, yoksa download)
  if (isStaticAsset(url.pathname)) {
    event.respondWith(cacheFirst(request));
    return;
  }

  // Sayfalar: Stale While Revalidate (cache'ten göster, arka planda güncelle)
  event.respondWith(staleWhileRevalidate(request));
});

// ---- Stratejiler ----
async function cacheFirst(request) {
  const cached = await caches.match(request);
  if (cached) return cached;

  try {
    const response = await fetch(request);
    const cache = await caches.open(CACHE_NAME);
    cache.put(request, response.clone());
    return response;
  } catch {
    return new Response('Offline', { status: 503 });
  }
}

async function networkFirst(request) {
  try {
    const response = await fetch(request);
    const cache = await caches.open(CACHE_NAME);
    cache.put(request, response.clone());
    return response;
  } catch {
    const cached = await caches.match(request);
    return cached || new Response(
      JSON.stringify({ error: 'Çevrimdışı' }),
      { status: 503, headers: { 'Content-Type': 'application/json' } }
    );
  }
}

async function staleWhileRevalidate(request) {
  const cached = await caches.match(request);

  const fetchPromise = fetch(request)
    .then((response) => {
      const cache = caches.open(CACHE_NAME);
      cache.then((c) => c.put(request, response.clone()));
      return response;
    })
    .catch(() => cached || caches.match('/offline.html'));

  return cached || fetchPromise;
}

function isStaticAsset(pathname) {
  return /\.(js|css|png|jpg|jpeg|webp|avif|svg|woff2?|ttf)$/.test(pathname);
}
```

### 5.2 Web App Manifest

```json
{
  "name": "Uygulama Adı",
  "short_name": "Uygulama",
  "description": "Profesyonel web uygulaması",
  "start_url": "/",
  "display": "standalone",
  "orientation": "portrait-primary",
  "theme_color": "#3b82f6",
  "background_color": "#111827",
  "icons": [
    { "src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "/icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ],
  "screenshots": [
    { "src": "/screenshots/wide.png", "sizes": "1280x720", "type": "image/png", "form_factor": "wide" },
    { "src": "/screenshots/narrow.png", "sizes": "750x1334", "type": "image/png", "form_factor": "narrow" }
  ],
  "categories": ["utilities", "productivity"],
  "shortcuts": [
    {
      "name": "Yeni Görev",
      "short_name": "Görev",
      "url": "/tasks/new",
      "icons": [{ "src": "/icons/shortcut-task.png", "sizes": "96x96" }]
    }
  ]
}
```

---

## 6. Web Performans Metrikleri (Core Web Vitals)

### 6.1 Metrikleri Ölçme

```typescript
// utils/webVitals.ts
import { onLCP, onFID, onCLS, onFCP, onTTFB, onINP, Metric } from 'web-vitals';

interface VitalMetric {
  name: string;
  value: number;
  rating: 'good' | 'needs-improvement' | 'poor';
  path: string;
}

function sendToAnalytics(metric: VitalMetric) {
  // Analytics servisine gönder
  navigator.sendBeacon('/api/analytics/vitals', JSON.stringify(metric));
}

function handleMetric(metric: Metric) {
  const vital: VitalMetric = {
    name: metric.name,
    value: Math.round(metric.value),
    rating: metric.rating,
    path: window.location.pathname,
  };
  sendToAnalytics(vital);

  // Geliştirme ortamında konsola yaz
  if (import.meta.env.DEV) {
    const color = metric.rating === 'good' ? '🟢' : metric.rating === 'needs-improvement' ? '🟡' : '🔴';
    console.log(`${color} ${metric.name}: ${Math.round(metric.value)}ms — ${metric.rating}`);
  }
}

// Tüm metrikleri kaydet
export function reportWebVitals() {
  onLCP(handleMetric);   // Largest Contentful Paint (< 2.5s)
  onFID(handleMetric);   // First Input Delay (< 100ms)
  onCLS(handleMetric);   // Cumulative Layout Shift (< 0.1)
  onFCP(handleMetric);   // First Contentful Paint (< 1.8s)
  onTTFB(handleMetric);  // Time to First Byte (< 800ms)
  onINP(handleMetric);   // Interaction to Next Paint (< 200ms)
}
```

### 6.2 CLS Önleme Teknikleri

```css
/* ---- Layout Shift'i önlemek için boyut belirt ---- */

/* Görseller: width/height ile aspect ratio ayarla */
img, video {
  max-width: 100%;
  height: auto;
  aspect-ratio: attr(width) / attr(height);  /* HTML width/height'tan çıkar */
}

/* Font yüklenirken layout kayması önleme */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter-Regular.woff2') format('woff2');
  font-display: swap;           /* fallback font göster, sonra değiştir */
  size-adjust: 100%;            /* Fallback ile boyut uyumu */
  ascent-override: 90%;
  descent-override: 22%;
  line-gap-override: 0%;
}

/* Skeleton placeholder: gerçek içerikle aynı boyutta */
.card-skeleton {
  width: 100%;
  aspect-ratio: 16 / 9;         /* Gerçek kart ile aynı oran */
  border-radius: var(--radius-md);
}
```

---

## 7. İleri Erişilebilirlik

### 7.1 Live Region ile Dinamik Bildirimler

```tsx
// shared/components/Announcer.tsx — Ekran okuyucular için seslendirme
import { useState, useCallback, createContext, useContext } from 'react';

const AnnouncerCtx = createContext<(msg: string, priority?: 'polite' | 'assertive') => void>(() => {});

export function AnnouncerProvider({ children }: { children: React.ReactNode }) {
  const [politeMsg, setPoliteMsg] = useState('');
  const [assertiveMsg, setAssertiveMsg] = useState('');

  const announce = useCallback((msg: string, priority: 'polite' | 'assertive' = 'polite') => {
    if (priority === 'assertive') {
      setAssertiveMsg('');
      requestAnimationFrame(() => setAssertiveMsg(msg));
    } else {
      setPoliteMsg('');
      requestAnimationFrame(() => setPoliteMsg(msg));
    }
  }, []);

  return (
    <AnnouncerCtx.Provider value={announce}>
      {children}
      {/* Görsel olarak gizli ama ekran okuyucu tarafından okunur */}
      <div className="sr-only" aria-live="polite" aria-atomic="true">
        {politeMsg}
      </div>
      <div className="sr-only" aria-live="assertive" aria-atomic="true">
        {assertiveMsg}
      </div>
    </AnnouncerCtx.Provider>
  );
}

export const useAnnounce = () => useContext(AnnouncerCtx);

// ---- sr-only CSS ----
// .sr-only {
//   position: absolute;
//   width: 1px; height: 1px;
//   padding: 0; margin: -1px;
//   overflow: hidden;
//   clip: rect(0, 0, 0, 0);
//   white-space: nowrap;
//   border: 0;
// }

// ---- Kullanım ----
function ProductPage() {
  const announce = useAnnounce();
  const addToCart = useMutation({
    onSuccess: () => {
      announce('Ürün sepete eklendi', 'polite');
    },
    onError: () => {
      announce('Ürün sepete eklenemedi! Lütfen tekrar deneyin.', 'assertive');
    },
  });
  // ...
}
```

---

## 8. Build ve Tooling Optimizasyonu

### 8.1 Vite Konfigürasyonu (Production)

```typescript
// vite.config.ts
import { defineConfig, splitVendorChunkPlugin } from 'vite';
import react from '@vitejs/plugin-react-swc';    // SWC: Babel'den 20x hızlı
import { visualizer } from 'rollup-plugin-visualizer';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig(({ mode }) => ({
  plugins: [
    react(),
    splitVendorChunkPlugin(),
    VitePWA({
      registerType: 'autoUpdate',
      workbox: { globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}'] },
    }),
    mode === 'analyze' && visualizer({
      open: true,
      gzipSize: true,    // gzip sonrası boyutları göster
      template: 'treemap',
    }),
  ],

  build: {
    target: 'es2022',                           // Modern tarayıcılar
    cssMinify: 'lightningcss',                  // CSS minify hızlandırma
    rollupOptions: {
      output: {
        // Manuel chunk bölme
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'router': ['react-router-dom'],
          'query': ['@tanstack/react-query'],
          'ui-vendor': ['framer-motion'],
        },
      },
    },
    // Dosya boyutu uyarı limiti
    chunkSizeWarningLimit: 500,                  // 500 KB
  },

  // Path alias'lar
  resolve: {
    alias: {
      '@': '/src',
      '@features': '/src/features',
      '@shared': '/src/shared',
    },
  },

  server: {
    port: 3000,
    // Backend proxy
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
}));
```

---

## 9. Frontend ve Backend Entegrasyon Haritası

Bu tablo, frontend ve backend rehberlerinin kesişim noktalarını gösterir:

| Frontend Katmanı | Backend Katmanı | İletişim |
|---|---|---|
| `apiCall()` fetch | Presentation → Controller | REST JSON |
| TanStack Query cache | Redis cache | Cache invalidation |
| Zustand auth store | JWT middleware | Access + Refresh token |
| React Hook Form + Zod | Zod validation middleware | Aynı şema paylaşılabilir |
| Error Boundary | Merkezi Error Handler | Standart error response |
| WebSocket hook | BullMQ + WS server | Gerçek zamanlı bildirim |
| Service Worker | Static file serving | Cache stratejisi |
| CSP meta tag | Helmet CSP header | Güvenlik katmanı |

---

## 10. Hızlı Referans Cheatsheet

| Konu | En İyi Pratik | Araç/Teknik |
|---|---|---|
| TypeScript | Discriminated unions + branded types | Compile-time güvenlik |
| Components | Polymorphic + Compound patterns | Esnek, yeniden kullanılabilir |
| Veri yönetimi | Optimistic updates | TanStack Query `onMutate` |
| Hata yönetimi | Sayfa bazlı ErrorBoundary | Hata izolasyonu |
| Animasyon | CSS custom properties + prefers-reduced-motion | Erişilebilir animasyon |
| Layout | CSS Grid + Container Query + auto-fill | Intrinsic design |
| Real-time | WebSocket (çift yönlü) / SSE (tek yönlü) | useWebSocket hook |
| PWA | Service Worker + Manifest | Offline destek |
| Performans | Core Web Vitals ölçümü | web-vitals kütüphanesi |
| CLS | Boyut belirt, font-display: swap | Layout shift önleme |
| Erişilebilirlik | aria-live region + sr-only announcer | Dinamik içerik bildirimi |
| Build | Vite + SWC + manual chunks | Hızlı build, küçük bundle |

---

## 11. Referanslar

- React Docs (beta): https://react.dev/
- TypeScript Handbook: https://www.typescriptlang.org/docs/
- Vite Docs: https://vitejs.dev/
- TanStack Query: https://tanstack.com/query
- web.dev — Core Web Vitals: https://web.dev/vitals/
- MDN — Service Worker API: https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API
- MDN — WebSocket API: https://developer.mozilla.org/en-US/docs/Web/API/WebSocket
- WAI-ARIA Practices: https://www.w3.org/WAI/ARIA/apg/
- Patterns.dev: https://www.patterns.dev/
- Lightning CSS: https://lightningcss.dev/
