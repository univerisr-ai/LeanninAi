# Web Site Güvenliği — Kapsamlı Profesyonel Rehber

**Tarih:** 2026-04-07  
**Kategori:** Web Güvenliği, OWASP, API Security  
**Seviye:** Orta-İleri  
**İlişkili Konular:** [Frontend Mimarisi](./frontend-mimarisi-rehberi.md), [Anti-Bot Güvenliği](./anti-bot-guvenligi-ve-rate-limit.md)

---

## 1. Giriş

Web güvenliği, kullanıcı verilerini korumaktan altyapıyı saldırılara karşı dayanıklı kılmaya kadar uzanan geniş bir disiplindir. Bu rehber OWASP Top 10 temelinde, frontend ve backend'in kesiştiği noktaları kod örnekleriyle ele alır.

---

## 2. XSS (Cross-Site Scripting) Koruması

### 2.1 XSS Türleri ve Saldırı Vektörleri

| Tür | Açıklama | Tehlike |
|---|---|---|
| **Stored XSS** | Zararlı kod DB'ye kaydedilir, her ziyaretçiye sunulur | En tehlikeli |
| **Reflected XSS** | URL parametresindeki kod sayfaya yansıtılır | Sosyal mühendislik ile |
| **DOM XSS** | JavaScript ile DOM'a enjekte edilir, sunucu görmez | Client-side saldırı |

### 2.2 Input Sanitization (Sunucu Tarafı)

**Node.js — DOMPurify ile HTML Temizleme:**

```javascript
import createDOMPurify from 'dompurify';
import { JSDOM } from 'jsdom';

const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window);

function sanitizeInput(dirty) {
  return DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br', 'ul', 'ol', 'li'],
    ALLOWED_ATTR: ['href', 'title', 'target'],
    ALLOW_DATA_ATTR: false,
    ADD_ATTR: ['rel'],               // noopener için
    FORBID_TAGS: ['script', 'style', 'iframe', 'object', 'embed', 'form'],
    FORBID_ATTR: ['onerror', 'onload', 'onclick', 'onmouseover'],
  });
}

// Express middleware
function xssSanitizer(req, res, next) {
  if (req.body) {
    for (const key of Object.keys(req.body)) {
      if (typeof req.body[key] === 'string') {
        req.body[key] = sanitizeInput(req.body[key]);
      }
    }
  }
  next();
}

app.use(express.json());
app.use(xssSanitizer);

// Test
console.log(sanitizeInput('<script>alert("XSS")</script><b>Güvenli</b>'));
// Çıktı: <b>Güvenli</b>
```

### 2.3 Output Encoding (Frontend)

```typescript
// ❌ TEHLİKELİ: Kullanıcı girdisini doğrudan DOM'a yaz
element.innerHTML = userComment;
// → <img src=x onerror="steal(document.cookie)"> çalışır!

// ✅ GÜVENLİ: textContent kullan (HTML yorumlanmaz)
element.textContent = userComment;
// → Metin olarak render edilir, kod çalışmaz

// ✅ GÜVENLİ: React otomatik escape eder
function Comment({ text }: { text: string }) {
  return <p>{text}</p>; // React XSS'i otomatik engeller
}

// ❌ TEHLİKELİ: React'te bile dangerouslySetInnerHTML kullanma
function UnsafeComment({ html }: { html: string }) {
  // Sadece sanitize edilmiş HTML ile kullanılmalı
  return <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(html) }} />;
}
```

### 2.4 Content Security Policy (CSP)

```javascript
// Express — Helmet ile CSP
import helmet from 'helmet';

app.use(
  helmet.contentSecurityPolicy({
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: [
        "'self'",
        "'nonce-{RANDOM}'",         // Nonce ile inline script izni
        "https://cdn.trusted.com",
      ],
      styleSrc: [
        "'self'",
        "'unsafe-inline'",           // CSS-in-JS için gerekli olabilir
        "https://fonts.googleapis.com",
      ],
      imgSrc: ["'self'", "data:", "https://images.trusted.com"],
      fontSrc: ["'self'", "https://fonts.gstatic.com"],
      connectSrc: ["'self'", "https://api.example.com"],
      frameSrc: ["'none'"],          // iframe tamamen engelle
      objectSrc: ["'none'"],         // Flash/Java engelle
      baseUri: ["'self'"],           // <base> tag manipülasyonunu engelle
      formAction: ["'self'"],        // Form gönderimini kısıtla
      upgradeInsecureRequests: [],   // HTTP → HTTPS zorunlu yükseltme
    },
  })
);

// ---- CSP Nonce Üretimi ----
import crypto from 'crypto';

app.use((req, res, next) => {
  res.locals.cspNonce = crypto.randomBytes(16).toString('base64');
  next();
});

// HTML template'te kullanım:
// <script nonce="<%= cspNonce %>">...</script>
```

**HTML Meta Tag ile CSP (Frontend-only projeler):**

```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' https://cdn.trusted.com; 
               style-src 'self' 'unsafe-inline'; 
               img-src 'self' data: https:; 
               connect-src 'self' https://api.example.com;
               frame-src 'none';
               object-src 'none';">
```

---

## 3. CSRF (Cross-Site Request Forgery) Koruması

### 3.1 Saldırı Mekanizması

```
1. Kullanıcı bank.com'a giriş yapar → oturum çerezi alır
2. Aynı tarayıcıda evil.com'u ziyaret eder
3. evil.com gizli bir form ile bank.com/transfer'a POST gönderir
4. Tarayıcı çerezleri otomatik ekler → transfer gerçekleşir!
```

### 3.2 CSRF Token Implementasyonu

**Node.js — Double Submit Cookie Pattern:**

```javascript
import crypto from 'crypto';
import cookieParser from 'cookie-parser';

app.use(cookieParser());

// ---- Token Üretimi ----
function generateCSRFToken() {
  return crypto.randomBytes(32).toString('hex');
}

// ---- Token Gönderimi (GET isteklerinde) ----
app.get('/api/csrf-token', (req, res) => {
  const token = generateCSRFToken();

  // HttpOnly OLMAYAN cookie (JS'in okuması gerekiyor)
  res.cookie('XSRF-TOKEN', token, {
    httpOnly: false,          // Frontend JS erişebilmeli
    secure: true,             // Sadece HTTPS
    sameSite: 'strict',
    maxAge: 3600000,          // 1 saat
    path: '/',
  });

  // Ayrıca session'a kaydet (doğrulama için)
  req.session.csrfToken = token;

  res.json({ csrfToken: token });
});

// ---- Token Doğrulama Middleware ----
function csrfProtection(req, res, next) {
  // GET, HEAD, OPTIONS atlanır (side-effect yok)
  if (['GET', 'HEAD', 'OPTIONS'].includes(req.method)) {
    return next();
  }

  const tokenFromHeader = req.headers['x-csrf-token'] || req.headers['x-xsrf-token'];
  const tokenFromCookie = req.cookies['XSRF-TOKEN'];
  const tokenFromSession = req.session?.csrfToken;

  if (!tokenFromHeader || !tokenFromCookie) {
    return res.status(403).json({ error: 'CSRF token eksik.' });
  }

  // Double-submit doğrulaması
  if (tokenFromHeader !== tokenFromCookie) {
    return res.status(403).json({ error: 'CSRF token uyuşmuyor.' });
  }

  // Session bazlı doğrulama (opsiyonel, daha güvenli)
  if (tokenFromSession && tokenFromHeader !== tokenFromSession) {
    return res.status(403).json({ error: 'CSRF session token geçersiz.' });
  }

  next();
}

app.use(csrfProtection);
```

**Frontend — CSRF Token ile API İsteği:**

```typescript
// utils/apiClient.ts
class SecureApiClient {
  private baseUrl: string;
  private csrfToken: string | null = null;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  // Sayfa yüklendiğinde token'ı al
  async initCSRF(): Promise<void> {
    const res = await fetch(`${this.baseUrl}/api/csrf-token`, {
      credentials: 'include',
    });
    const data = await res.json();
    this.csrfToken = data.csrfToken;
  }

  // Cookie'den oku (alternatif)
  private getCSRFFromCookie(): string {
    const match = document.cookie.match(/XSRF-TOKEN=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : '';
  }

  async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const token = this.csrfToken || this.getCSRFFromCookie();

    const res = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      credentials: 'include',       // Cookie gönder
      headers: {
        'Content-Type': 'application/json',
        'X-CSRF-Token': token,       // CSRF token header'da
        ...options.headers,
      },
    });

    if (res.status === 403) {
      // Token expired — yenile ve tekrar dene
      await this.initCSRF();
      return this.request(endpoint, options);
    }

    if (!res.ok) throw new Error(`API Error: ${res.status}`);
    return res.json();
  }

  async post<T>(endpoint: string, body: unknown): Promise<T> {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(body),
    });
  }
}

// Kullanım
const api = new SecureApiClient('https://api.example.com');
await api.initCSRF();
await api.post('/api/transfer', { to: 'user123', amount: 100 });
```

---

## 4. Güvenli API İletişimi

### 4.1 HTTPS Zorunluluğu ve HSTS

```javascript
// Express — HTTPS Yönlendirme + HSTS
app.use((req, res, next) => {
  if (req.headers['x-forwarded-proto'] !== 'https') {
    return res.redirect(301, `https://${req.hostname}${req.url}`);
  }
  next();
});

app.use(
  helmet.hsts({
    maxAge: 63072000,               // 2 yıl
    includeSubDomains: true,
    preload: true,                  // HSTS Preload listesine ekle
  })
);
```

### 4.2 JWT Güvenlik Best Practices

```typescript
// ---- Token Yapısı ----
// Access Token:  Kısa ömürlü (15 dk), memory'de tut
// Refresh Token: Uzun ömürlü (7 gün), HttpOnly cookie'de

import jwt from 'jsonwebtoken';

interface TokenPayload {
  userId: string;
  role: 'admin' | 'user';
}

const ACCESS_SECRET = process.env.JWT_ACCESS_SECRET!;
const REFRESH_SECRET = process.env.JWT_REFRESH_SECRET!;

function generateAccessToken(payload: TokenPayload): string {
  return jwt.sign(payload, ACCESS_SECRET, {
    expiresIn: '15m',
    issuer: 'api.example.com',
    audience: 'web-client',
    algorithm: 'HS256',
  });
}

function generateRefreshToken(payload: TokenPayload): string {
  return jwt.sign({ userId: payload.userId }, REFRESH_SECRET, {
    expiresIn: '7d',
    issuer: 'api.example.com',
    algorithm: 'HS256',
  });
}

// ---- Login Endpoint ----
app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;
  const user = await authenticateUser(email, password);

  if (!user) return res.status(401).json({ error: 'Geçersiz kimlik bilgileri.' });

  const accessToken = generateAccessToken({ userId: user.id, role: user.role });
  const refreshToken = generateRefreshToken({ userId: user.id, role: user.role });

  // Refresh token'ı HttpOnly cookie olarak gönder
  res.cookie('refreshToken', refreshToken, {
    httpOnly: true,             // JavaScript erişemez (XSS koruması)
    secure: true,               // Sadece HTTPS
    sameSite: 'strict',         // CSRF koruması
    maxAge: 7 * 24 * 60 * 60 * 1000,
    path: '/api/auth/refresh',  // Sadece refresh endpoint'ine gönderilir
  });

  // Access token'ı body'de döndür (memory'de tutulacak)
  res.json({ accessToken, expiresIn: 900 });
});

// ---- Token Yenileme ----
app.post('/api/auth/refresh', (req, res) => {
  const refreshToken = req.cookies.refreshToken;

  if (!refreshToken) return res.status(401).json({ error: 'Token yok.' });

  try {
    const payload = jwt.verify(refreshToken, REFRESH_SECRET) as TokenPayload;
    const newAccessToken = generateAccessToken({ userId: payload.userId, role: 'user' });
    res.json({ accessToken: newAccessToken, expiresIn: 900 });
  } catch {
    res.clearCookie('refreshToken');
    res.status(401).json({ error: 'Geçersiz refresh token.' });
  }
});
```

**Frontend — Token Yönetimi:**

```typescript
// auth/tokenManager.ts
class TokenManager {
  private accessToken: string | null = null;
  private refreshPromise: Promise<string> | null = null;

  setAccessToken(token: string) {
    this.accessToken = token;
  }

  getAccessToken(): string | null {
    return this.accessToken;
  }

  clear() {
    this.accessToken = null;
  }

  // Eşzamanlı refresh isteklerini birleştir (race condition önleme)
  async refreshAccessToken(): Promise<string> {
    if (this.refreshPromise) return this.refreshPromise;

    this.refreshPromise = fetch('/api/auth/refresh', {
      method: 'POST',
      credentials: 'include',    // HttpOnly cookie gönderilir
    })
      .then(async (res) => {
        if (!res.ok) throw new Error('Token yenileme başarısız');
        const { accessToken } = await res.json();
        this.accessToken = accessToken;
        return accessToken;
      })
      .finally(() => {
        this.refreshPromise = null;
      });

    return this.refreshPromise;
  }
}

export const tokenManager = new TokenManager();

// ---- Fetch Interceptor ----
async function secureFetch(url: string, options: RequestInit = {}): Promise<Response> {
  const token = tokenManager.getAccessToken();

  const res = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': token ? `Bearer ${token}` : '',
    },
  });

  // 401 → Token expired → Yenile ve tekrar dene
  if (res.status === 401) {
    try {
      const newToken = await tokenManager.refreshAccessToken();
      return fetch(url, {
        ...options,
        headers: {
          ...options.headers,
          'Authorization': `Bearer ${newToken}`,
        },
      });
    } catch {
      tokenManager.clear();
      window.location.href = '/login';
      throw new Error('Oturum süresi doldu.');
    }
  }

  return res;
}
```

### 4.3 Cookie Güvenlik Bayrakları Cheatsheet

| Bayrak | Değer | Amaç |
|---|---|---|
| `HttpOnly` | `true` | XSS ile JS erişimini engeller |
| `Secure` | `true` | Sadece HTTPS üzerinden gönderilir |
| `SameSite` | `Strict` | CSRF koruması, cross-origin istek engellenir |
| `SameSite` | `Lax` | GET navigasyonlarında gönderilir (varsayılan) |
| `Path` | `/api/auth` | Sadece belirtilen yola gönderilir |
| `Domain` | `.example.com` | Subdomain'leri kapsar |
| `Max-Age` | `604800` | 7 gün sonra süresi dolar |

---

## 5. Güvenlik Header'ları

```javascript
// Express — Tüm Güvenlik Header'ları
import helmet from 'helmet';

app.use(helmet());

// Veya detaylı yapılandırma:
app.use(helmet.frameguard({ action: 'deny' }));        // Clickjacking koruması
app.use(helmet.noSniff());                              // MIME type sniffing engelle
app.use(helmet.xssFilter());                            // X-XSS-Protection
app.use(helmet.referrerPolicy({ policy: 'strict-origin-when-cross-origin' }));

// Ek özel header'lar
app.use((req, res, next) => {
  // Tarayıcıya hangi özelliklere erişim izni verildiğini bildir
  res.setHeader('Permissions-Policy',
    'camera=(), microphone=(), geolocation=(self), payment=(self)'
  );

  // Cross-Origin izolasyon (Spectre saldırı koruması)
  res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
  res.setHeader('Cross-Origin-Embedder-Policy', 'require-corp');

  next();
});
```

**Güvenlik Header'ları Kontrol Listesi:**

| Header | Değer | Korunan Saldırı |
|---|---|---|
| `Content-Security-Policy` | (detaylı) | XSS, veri enjeksiyonu |
| `Strict-Transport-Security` | `max-age=63072000; includeSubDomains` | Downgrade saldırısı |
| `X-Content-Type-Options` | `nosniff` | MIME confusion |
| `X-Frame-Options` | `DENY` | Clickjacking |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Bilgi sızıntısı |
| `Permissions-Policy` | `camera=(), microphone=()` | Özellik kötüye kullanımı |
| `Cross-Origin-Opener-Policy` | `same-origin` | Spectre |

---

## 6. Input Validation (Giriş Doğrulama)

### 6.1 Sunucu Tarafı — Zod ile Şema Doğrulama

```typescript
import { z } from 'zod';

// ---- Şema Tanımlama ----
const UserRegistrationSchema = z.object({
  email: z
    .string()
    .email('Geçersiz email formatı')
    .max(255, 'Email çok uzun')
    .transform((v) => v.toLowerCase().trim()),

  password: z
    .string()
    .min(8, 'Şifre en az 8 karakter olmalı')
    .max(128, 'Şifre çok uzun')
    .regex(/[A-Z]/, 'En az bir büyük harf gerekli')
    .regex(/[a-z]/, 'En az bir küçük harf gerekli')
    .regex(/[0-9]/, 'En az bir rakam gerekli')
    .regex(/[^A-Za-z0-9]/, 'En az bir özel karakter gerekli'),

  displayName: z
    .string()
    .min(2, 'İsim en az 2 karakter olmalı')
    .max(50, 'İsim çok uzun')
    .regex(/^[\p{L}\p{N}\s]+$/u, 'Geçersiz karakterler içeriyor'),

  age: z
    .number()
    .int('Yaş tam sayı olmalı')
    .min(13, 'Minimum yaş 13')
    .max(120, 'Geçersiz yaş')
    .optional(),
});

type UserRegistration = z.infer<typeof UserRegistrationSchema>;

// ---- Express Middleware ----
function validate(schema: z.ZodSchema) {
  return (req, res, next) => {
    const result = schema.safeParse(req.body);

    if (!result.success) {
      const errors = result.error.issues.map((issue) => ({
        field: issue.path.join('.'),
        message: issue.message,
      }));
      return res.status(400).json({ errors });
    }

    req.body = result.data; // Temizlenmiş ve dönüştürülmüş veri
    next();
  };
}

app.post('/api/register', validate(UserRegistrationSchema), async (req, res) => {
  // req.body artık tip-güvenli ve doğrulanmış
  const { email, password, displayName } = req.body;
  // ...
});
```

### 6.2 Frontend — React Hook Form + Zod

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const LoginSchema = z.object({
  email: z.string().email('Geçerli bir email girin'),
  password: z.string().min(8, 'Şifre en az 8 karakter'),
});

type LoginForm = z.infer<typeof LoginSchema>;

function LoginPage() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginForm>({
    resolver: zodResolver(LoginSchema),
  });

  const onSubmit = async (data: LoginForm) => {
    await api.post('/api/auth/login', data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          autoComplete="email"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? 'email-error' : undefined}
          {...register('email')}
        />
        {errors.email && (
          <p id="email-error" role="alert" className="error">
            {errors.email.message}
          </p>
        )}
      </div>

      <div>
        <label htmlFor="password">Şifre</label>
        <input
          id="password"
          type="password"
          autoComplete="current-password"
          aria-invalid={!!errors.password}
          aria-describedby={errors.password ? 'password-error' : undefined}
          {...register('password')}
        />
        {errors.password && (
          <p id="password-error" role="alert" className="error">
            {errors.password.message}
          </p>
        )}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Giriş yapılıyor...' : 'Giriş Yap'}
      </button>
    </form>
  );
}
```

---

## 7. SQL Injection Koruması

```typescript
// ❌ TEHLİKELİ: String birleştirme
const query = `SELECT * FROM users WHERE email = '${email}'`;
// Saldırı: email = "' OR '1'='1' --"
// → SELECT * FROM users WHERE email = '' OR '1'='1' --'

// ✅ GÜVENLİ: Parametreli sorgu (Prepared Statement)
// PostgreSQL (node-postgres)
import { Pool } from 'pg';
const pool = new Pool();

async function getUserByEmail(email: string) {
  const result = await pool.query(
    'SELECT id, email, display_name FROM users WHERE email = $1',
    [email]  // Parametre olarak geçir, asla string concat yapma
  );
  return result.rows[0];
}

// ✅ GÜVENLİ: ORM kullanımı (Prisma)
async function getUserByEmailPrisma(email: string) {
  return prisma.user.findUnique({
    where: { email },  // Prisma otomatik parametrize eder
    select: { id: true, email: true, displayName: true },
  });
}
```

---

## 8. Subresource Integrity (SRI)

Dış kaynakların değiştirilip değiştirilmediğini doğrulama.

```html
<!-- CDN'den yüklenen script → SRI hash'i ekle -->
<script
  src="https://cdn.example.com/lib/react.production.min.js"
  integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/uxy9rx7HNQlGYl1kPzQho1wx4JwY8w"
  crossorigin="anonymous"
></script>

<!-- CSS için de kullanılabilir -->
<link
  rel="stylesheet"
  href="https://cdn.example.com/styles/normalize.css"
  integrity="sha384-abc123..."
  crossorigin="anonymous"
/>
```

**Hash üretimi (terminal):**

```bash
# SHA-384 hash üretimi
cat react.production.min.js | openssl dgst -sha384 -binary | openssl base64 -A
# Sonuç: integrity="sha384-oqVuAfX..."
```

---

## 9. CORS (Cross-Origin Resource Sharing)

```javascript
import cors from 'cors';

// ❌ TEHLİKELİ: Tüm origin'lere izin verme
// app.use(cors()); // Access-Control-Allow-Origin: *

// ✅ GÜVENLİ: Whitelist yaklaşımı
const ALLOWED_ORIGINS = [
  'https://www.example.com',
  'https://app.example.com',
  'https://admin.example.com',
];

// Geliştirme ortamında localhost ekle
if (process.env.NODE_ENV === 'development') {
  ALLOWED_ORIGINS.push('http://localhost:3000', 'http://localhost:5173');
}

app.use(cors({
  origin: (origin, callback) => {
    // Origin olmayan istekler (server-to-server, Postman)
    if (!origin) return callback(null, true);

    if (ALLOWED_ORIGINS.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error(`CORS ihlali: ${origin} izin listesinde yok.`));
    }
  },
  credentials: true,                   // Cookie gönderime izin ver
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-CSRF-Token'],
  exposedHeaders: ['X-Total-Count'],    // Frontend'in görmesi gereken custom header
  maxAge: 86400,                        // Preflight cache: 24 saat
}));
```

---

## 10. Güvenli Dosya Yükleme

```typescript
import multer from 'multer';
import path from 'path';
import crypto from 'crypto';

// ---- Güvenlik kontrolleri ----
const ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png', 'image/webp', 'application/pdf'];
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB

const storage = multer.diskStorage({
  destination: './uploads/temp',
  filename: (req, file, cb) => {
    // Orijinal dosya adını KULLANMA → Path Traversal riski
    const uniqueName = `${crypto.randomUUID()}${path.extname(file.originalname)}`;
    cb(null, uniqueName);
  },
});

const upload = multer({
  storage,
  limits: { fileSize: MAX_FILE_SIZE },
  fileFilter: (req, file, cb) => {
    // MIME type kontrolü
    if (!ALLOWED_MIME_TYPES.includes(file.mimetype)) {
      return cb(new Error(`İzin verilmeyen dosya türü: ${file.mimetype}`));
    }

    // Uzantı kontrolü (double extension saldırısı: image.jpg.exe)
    const ext = path.extname(file.originalname).toLowerCase();
    const safeExtensions = ['.jpg', '.jpeg', '.png', '.webp', '.pdf'];
    if (!safeExtensions.includes(ext)) {
      return cb(new Error(`İzin verilmeyen uzantı: ${ext}`));
    }

    cb(null, true);
  },
});

app.post('/api/upload', upload.single('file'), async (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'Dosya yüklenmedi.' });

  // Ek güvenlik: magic bytes kontrolü (gerçek dosya türü doğrulama)
  const { fileTypeFromFile } = await import('file-type');
  const detected = await fileTypeFromFile(req.file.path);

  if (!detected || !ALLOWED_MIME_TYPES.includes(detected.mime)) {
    // Sahte uzantı tespit edildi → sil
    await fs.unlink(req.file.path);
    return res.status(400).json({ error: 'Dosya türü doğrulanamadı.' });
  }

  res.json({ url: `/uploads/${req.file.filename}` });
});
```

---

## 11. Frontend ve Backend Güvenlik Bağlantı Matrisi

Bu tablo, frontend mimarisi rehberiyle güvenlik rehberinin kesişim noktalarını gösterir:

| Frontend Eylemi | Güvenlik Önlemi | Detay |
|---|---|---|
| API çağrısı (`fetch`) | CSRF token header'da gönder | §3.2 CSRF Token |
| Form gönderimi | Zod ile hem FE hem BE doğrula | §6 Input Validation |
| Kullanıcı girdisi gösterme | `textContent` veya React escape | §2.3 Output Encoding |
| CDN'den script yükleme | SRI hash kontrolü | §8 SRI |
| Cookie yönetimi | `HttpOnly + Secure + SameSite` | §4.3 Cookie Bayrakları |
| Auth state yönetimi | Access token memory'de, refresh HttpOnly | §4.2 JWT |
| Image upload UI | Frontend'de dosya türü + boyut kontrolü | §10 Dosya Yükleme |
| CSP meta tag | Inline script/style kısıtlaması | §2.4 CSP |

---

## 12. Güvenlik Denetim Kontrol Listesi

### Production'a Çıkmadan Önce Kontrol Et

- [ ] Tüm endpoint'lerde input validation var mı?
- [ ] SQL sorguları parametrize mi?
- [ ] XSS koruması: CSP header'ı + output encoding
- [ ] CSRF token sistemi aktif mi?
- [ ] Cookie'ler `HttpOnly + Secure + SameSite` mi?
- [ ] HTTPS zorunlu mu? HSTS aktif mi?
- [ ] CORS whitelist doğru mu?
- [ ] Rate limiting uygulandı mı?
- [ ] Dosya yükleme güvenliği (MIME + magic bytes)
- [ ] Güvenlik header'ları (Helmet) aktif mi?
- [ ] Dependency audit (`npm audit`) temiz mi?
- [ ] Error response'larda stack trace sızdırılmıyor mu?
- [ ] `.env` dosyası `.gitignore`'da mı?
- [ ] JWT secret yeterince güçlü ve env variable'da mı?

---

## 13. Referanslar ve İleri Okuma

- OWASP Top 10 (2021): https://owasp.org/www-project-top-ten/
- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/
- MDN — Content Security Policy: https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
- MDN — CORS: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
- Helmet.js Docs: https://helmetjs.github.io/
- Zod Documentation: https://zod.dev/
- JWT Best Practices (Auth0): https://auth0.com/docs/secure/tokens/json-web-tokens
- web.dev — Security: https://web.dev/secure/
