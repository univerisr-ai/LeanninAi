# Backend Geliştirme — En Üst Seviye Profesyonel Rehber

**Tarih:** 2026-04-07  
**Kategori:** Backend Mimarisi, API Design, Veritabanı, DevOps  
**Seviye:** İleri  
**İlişkili Konular:** [Frontend Geliştirme](./frontend-gelistirme-rehberi.md), [Web Güvenliği](./web-guvenlik-rehberi.md), [Anti-Bot](./anti-bot-guvenligi-ve-rate-limit.md)

---

## 1. Mimari Desenler (Architectural Patterns)

### 1.1 Katmanlı Mimari (Layered Architecture)

Her katman yalnızca altındaki katmanı bilir. Bu sayede değişiklikler izole kalır.

```
┌──────────────────────────────────────────────┐
│              Presentation Layer              │  ← Route/Controller
│         (HTTP isteklerini karşılar)          │
├──────────────────────────────────────────────┤
│              Application Layer               │  ← Service/Use Case
│       (İş mantığı orkestrasyon katmanı)      │
├──────────────────────────────────────────────┤
│               Domain Layer                   │  ← Entity/Value Object
│       (Çekirdek iş kuralları, saf mantık)    │
├──────────────────────────────────────────────┤
│            Infrastructure Layer              │  ← Repository/External API
│     (DB, cache, mail, 3rd party servisler)   │
└──────────────────────────────────────────────┘
```

**Proje Yapısı:**

```
src/
├── presentation/
│   ├── routes/
│   │   ├── userRoutes.ts
│   │   ├── productRoutes.ts
│   │   └── orderRoutes.ts
│   ├── middlewares/
│   │   ├── authMiddleware.ts
│   │   ├── errorHandler.ts
│   │   ├── rateLimiter.ts
│   │   └── validator.ts
│   └── controllers/
│       ├── UserController.ts
│       └── ProductController.ts
├── application/
│   ├── services/
│   │   ├── UserService.ts
│   │   ├── ProductService.ts
│   │   └── OrderService.ts
│   ├── dtos/
│   │   ├── CreateUserDTO.ts
│   │   └── ProductResponseDTO.ts
│   └── interfaces/
│       ├── IUserRepository.ts
│       └── IEmailService.ts
├── domain/
│   ├── entities/
│   │   ├── User.ts
│   │   ├── Product.ts
│   │   └── Order.ts
│   ├── valueObjects/
│   │   ├── Email.ts
│   │   ├── Money.ts
│   │   └── Address.ts
│   └── errors/
│       ├── DomainError.ts
│       └── NotFoundError.ts
├── infrastructure/
│   ├── database/
│   │   ├── prisma/
│   │   │   └── schema.prisma
│   │   ├── repositories/
│   │   │   ├── PrismaUserRepository.ts
│   │   │   └── PrismaProductRepository.ts
│   │   └── migrations/
│   ├── cache/
│   │   └── RedisCache.ts
│   ├── email/
│   │   └── SendGridEmailService.ts
│   └── queue/
│       └── BullMQProducer.ts
├── config/
│   ├── env.ts
│   ├── database.ts
│   └── logger.ts
├── app.ts
└── server.ts
```

### 1.2 Katmanlar Arası Akış Örneği

```typescript
// ═══════════════════════════════════════════
// 1. DOMAIN LAYER — Saf iş kuralları
// ═══════════════════════════════════════════

// domain/valueObjects/Email.ts
export class Email {
  private readonly value: string;

  private constructor(email: string) {
    this.value = email;
  }

  static create(email: string): Email {
    const trimmed = email.trim().toLowerCase();
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!regex.test(trimmed)) {
      throw new DomainError(`Geçersiz email: ${email}`);
    }
    if (trimmed.length > 255) {
      throw new DomainError('Email 255 karakteri aşamaz.');
    }
    return new Email(trimmed);
  }

  toString(): string {
    return this.value;
  }

  equals(other: Email): boolean {
    return this.value === other.value;
  }
}

// domain/entities/User.ts
export class User {
  constructor(
    public readonly id: string,
    private _email: Email,
    private _displayName: string,
    private _role: 'admin' | 'user',
    public readonly createdAt: Date,
    private _updatedAt: Date,
  ) {}

  get email(): string { return this._email.toString(); }
  get displayName(): string { return this._displayName; }
  get role(): string { return this._role; }

  changeEmail(newEmail: string): void {
    this._email = Email.create(newEmail);
    this._updatedAt = new Date();
  }

  promote(): void {
    if (this._role === 'admin') {
      throw new DomainError('Kullanıcı zaten admin.');
    }
    this._role = 'admin';
    this._updatedAt = new Date();
  }
}

// domain/errors/DomainError.ts
export class DomainError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'DomainError';
  }
}

export class NotFoundError extends DomainError {
  constructor(entity: string, id: string) {
    super(`${entity} bulunamadı: ${id}`);
    this.name = 'NotFoundError';
  }
}

// ═══════════════════════════════════════════
// 2. APPLICATION LAYER — İş akışı
// ═══════════════════════════════════════════

// application/interfaces/IUserRepository.ts
export interface IUserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  save(user: User): Promise<void>;
  delete(id: string): Promise<void>;
}

// application/dtos/CreateUserDTO.ts
export interface CreateUserDTO {
  email: string;
  displayName: string;
  password: string;
}

export interface UserResponseDTO {
  id: string;
  email: string;
  displayName: string;
  role: string;
  createdAt: string;
}

// application/services/UserService.ts
import { IUserRepository } from '../interfaces/IUserRepository';
import { IEmailService } from '../interfaces/IEmailService';
import { IPasswordHasher } from '../interfaces/IPasswordHasher';

export class UserService {
  constructor(
    private userRepo: IUserRepository,
    private emailService: IEmailService,
    private hasher: IPasswordHasher,
  ) {}

  async createUser(dto: CreateUserDTO): Promise<UserResponseDTO> {
    // İş kuralı: Email benzersiz mi?
    const existing = await this.userRepo.findByEmail(dto.email);
    if (existing) {
      throw new DomainError('Bu email zaten kayıtlı.');
    }

    // Domain nesnesi oluştur (validation burada)
    const email = Email.create(dto.email);
    const hashedPassword = await this.hasher.hash(dto.password);

    const user = new User(
      crypto.randomUUID(),
      email,
      dto.displayName,
      'user',
      new Date(),
      new Date(),
    );

    await this.userRepo.save(user);

    // Yan etki: Hoşgeldin maili
    await this.emailService.sendWelcome(user.email, user.displayName);

    return this.toDTO(user);
  }

  async getUserById(id: string): Promise<UserResponseDTO> {
    const user = await this.userRepo.findById(id);
    if (!user) throw new NotFoundError('User', id);
    return this.toDTO(user);
  }

  private toDTO(user: User): UserResponseDTO {
    return {
      id: user.id,
      email: user.email,
      displayName: user.displayName,
      role: user.role,
      createdAt: user.createdAt.toISOString(),
    };
  }
}

// ═══════════════════════════════════════════
// 3. INFRASTRUCTURE LAYER — Dış dünya
// ═══════════════════════════════════════════

// infrastructure/database/repositories/PrismaUserRepository.ts
import { PrismaClient } from '@prisma/client';

export class PrismaUserRepository implements IUserRepository {
  constructor(private prisma: PrismaClient) {}

  async findById(id: string): Promise<User | null> {
    const row = await this.prisma.user.findUnique({ where: { id } });
    return row ? this.toDomain(row) : null;
  }

  async findByEmail(email: string): Promise<User | null> {
    const row = await this.prisma.user.findUnique({ where: { email } });
    return row ? this.toDomain(row) : null;
  }

  async save(user: User): Promise<void> {
    await this.prisma.user.upsert({
      where: { id: user.id },
      create: {
        id: user.id,
        email: user.email,
        displayName: user.displayName,
        role: user.role,
        createdAt: user.createdAt,
      },
      update: {
        email: user.email,
        displayName: user.displayName,
        role: user.role,
      },
    });
  }

  async delete(id: string): Promise<void> {
    await this.prisma.user.delete({ where: { id } });
  }

  private toDomain(row: any): User {
    return new User(
      row.id,
      Email.create(row.email),
      row.displayName,
      row.role,
      row.createdAt,
      row.updatedAt,
    );
  }
}

// ═══════════════════════════════════════════
// 4. PRESENTATION LAYER — HTTP arayüzü
// ═══════════════════════════════════════════

// presentation/controllers/UserController.ts
import { Request, Response, NextFunction } from 'express';

export class UserController {
  constructor(private userService: UserService) {}

  create = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const user = await this.userService.createUser(req.body);
      res.status(201).json({ data: user });
    } catch (error) {
      next(error); // Error handler middleware'e ilet
    }
  };

  getById = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const user = await this.userService.getUserById(req.params.id);
      res.json({ data: user });
    } catch (error) {
      next(error);
    }
  };
}

// presentation/routes/userRoutes.ts
import { Router } from 'express';

export function createUserRoutes(controller: UserController): Router {
  const router = Router();
  router.post('/', validate(CreateUserSchema), controller.create);
  router.get('/:id', controller.getById);
  return router;
}
```

---

## 2. RESTful API Tasarımı

### 2.1 URL Konvansiyonları

```
# ---- Doğru API URL tasarımı ----

# Koleksiyon (çoğul isim kullan, fiil KULLANMA)
GET    /api/v1/products              → Tüm ürünleri listele
POST   /api/v1/products              → Yeni ürün oluştur
GET    /api/v1/products/:id          → Tek ürün getir
PUT    /api/v1/products/:id          → Ürünü tamamen güncelle
PATCH  /api/v1/products/:id          → Ürünü kısmen güncelle
DELETE /api/v1/products/:id          → Ürünü sil

# İlişkili kaynaklar (nested resources)
GET    /api/v1/products/:id/reviews  → Ürünün yorumları
POST   /api/v1/products/:id/reviews  → Ürüne yorum ekle

# Filtreleme, sıralama, sayfalama → Query parametreleri
GET    /api/v1/products?category=electronics&sort=-price&page=2&limit=20

# Arama
GET    /api/v1/products/search?q=laptop&minPrice=1000

# ---- YANLIŞ API URL tasarımı ----
# ❌ GET /api/getProducts          → Fiil kullanma
# ❌ GET /api/product              → Tekil kullanma
# ❌ POST /api/products/create     → POST zaten "create" demek
# ❌ GET /api/products/delete/5    → GET ile silme YAPMA
```

### 2.2 Standart API Response Formatı

```typescript
// ---- Başarılı Response ----
interface ApiResponse<T> {
  success: true;
  data: T;
  meta?: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

// ---- Hata Response ----
interface ApiError {
  success: false;
  error: {
    code: string;           // Makine-okunabilir: 'VALIDATION_ERROR'
    message: string;        // İnsan-okunabilir
    details?: Array<{       // Validation hataları
      field: string;
      message: string;
    }>;
    requestId: string;      // Debug için izleme ID'si
  };
}

// ---- Express Implementasyonu ----
class ApiResponseBuilder {
  static success<T>(data: T, meta?: ApiResponse<T>['meta']): ApiResponse<T> {
    return { success: true, data, ...(meta && { meta }) };
  }

  static paginated<T>(
    data: T[],
    total: number,
    page: number,
    limit: number,
  ): ApiResponse<T[]> {
    return {
      success: true,
      data,
      meta: {
        page,
        limit,
        total,
        totalPages: Math.ceil(total / limit),
      },
    };
  }

  static error(code: string, message: string, details?: any[]): ApiError {
    return {
      success: false,
      error: {
        code,
        message,
        details,
        requestId: crypto.randomUUID(),
      },
    };
  }
}

// ---- Kullanım ----
app.get('/api/v1/products', async (req, res) => {
  const page = parseInt(req.query.page as string) || 1;
  const limit = Math.min(parseInt(req.query.limit as string) || 20, 100);
  const offset = (page - 1) * limit;

  const [products, total] = await Promise.all([
    productRepo.findMany({ skip: offset, take: limit }),
    productRepo.count(),
  ]);

  res.json(ApiResponseBuilder.paginated(products, total, page, limit));
});
```

### 2.3 HTTP Status Code Rehberi

| Status | Anlam | Ne Zaman Kullanılır |
|---|---|---|
| `200 OK` | Başarılı | GET, PUT, PATCH başarılı |
| `201 Created` | Oluşturuldu | POST ile yeni kaynak yaratıldı |
| `204 No Content` | İçerik yok | DELETE başarılı, body dönme |
| `400 Bad Request` | Hatalı istek | Validation hatası |
| `401 Unauthorized` | Kimlik doğrulanmadı | Token yok veya geçersiz |
| `403 Forbidden` | Yetki yok | Giriş yapmış ama yetkisiz |
| `404 Not Found` | Bulunamadı | Kaynak mevcut değil |
| `409 Conflict` | Çakışma | Duplicate email, sürüm çakışması |
| `422 Unprocessable` | İşlenemez | İş kuralı ihlali |
| `429 Too Many Requests` | Rate limit | Çok fazla istek |
| `500 Internal Error` | Sunucu hatası | Beklenmeyen hata |

---

## 3. Veritabanı Tasarımı

### 3.1 Prisma Schema — İlişkisel Tasarım

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// ---- Kullanıcı ----
model User {
  id           String    @id @default(uuid())
  email        String    @unique
  passwordHash String    @map("password_hash")
  displayName  String    @map("display_name")
  role         Role      @default(USER)
  avatarUrl    String?   @map("avatar_url")
  isActive     Boolean   @default(true) @map("is_active")
  lastLoginAt  DateTime? @map("last_login_at")
  createdAt    DateTime  @default(now()) @map("created_at")
  updatedAt    DateTime  @updatedAt @map("updated_at")

  // İlişkiler
  orders       Order[]
  reviews      Review[]
  sessions     Session[]
  addresses    Address[]

  @@map("users")                          // Tablo adı: snake_case
  @@index([email])                        // Sık sorgulanan alan
  @@index([createdAt(sort: Desc)])
}

enum Role {
  USER
  ADMIN
  MODERATOR
}

// ---- Ürün ----
model Product {
  id          String   @id @default(uuid())
  name        String
  slug        String   @unique                 // SEO-friendly URL
  description String?
  price       Decimal  @db.Decimal(10, 2)      // Para birimi: tam hassasiyet
  stock       Int      @default(0)
  isPublished Boolean  @default(false) @map("is_published")
  categoryId  String   @map("category_id")
  createdAt   DateTime @default(now()) @map("created_at")
  updatedAt   DateTime @updatedAt @map("updated_at")

  category    Category @relation(fields: [categoryId], references: [id])
  images      ProductImage[]
  reviews     Review[]
  orderItems  OrderItem[]

  @@map("products")
  @@index([categoryId])
  @@index([slug])
  @@index([price])
  @@index([isPublished, createdAt(sort: Desc)])  // Bileşik index
}

// ---- Sipariş (Soft Delete + Status Machine) ----
model Order {
  id          String      @id @default(uuid())
  userId      String      @map("user_id")
  status      OrderStatus @default(PENDING)
  totalAmount Decimal     @db.Decimal(10, 2) @map("total_amount")
  currency    String      @default("TRY") @db.VarChar(3)
  notes       String?
  cancelledAt DateTime?   @map("cancelled_at")
  completedAt DateTime?   @map("completed_at")
  createdAt   DateTime    @default(now()) @map("created_at")
  updatedAt   DateTime    @updatedAt @map("updated_at")

  user        User        @relation(fields: [userId], references: [id])
  items       OrderItem[]
  payments    Payment[]

  @@map("orders")
  @@index([userId, status])
  @@index([createdAt(sort: Desc)])
}

enum OrderStatus {
  PENDING
  CONFIRMED
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
  REFUNDED
}

model OrderItem {
  id        String  @id @default(uuid())
  orderId   String  @map("order_id")
  productId String  @map("product_id")
  quantity  Int
  unitPrice Decimal @db.Decimal(10, 2) @map("unit_price")

  order     Order   @relation(fields: [orderId], references: [id], onDelete: Cascade)
  product   Product @relation(fields: [productId], references: [id])

  @@map("order_items")
  @@unique([orderId, productId])       // Aynı üründen tekrar ekleme engeli
}
```

### 3.2 Veritabanı Index Stratejisi

```sql
-- ---- Performans için kritik index'ler ----

-- Bileşik index: Sık beraber filtrelenen alanlar
CREATE INDEX idx_products_category_price
  ON products (category_id, price);

-- Kısmi index: Sadece aktif kayıtlar
CREATE INDEX idx_users_active_email
  ON users (email)
  WHERE is_active = true;

-- Covering index: Sorgunun tüm ihtiyacını karşılar (index-only scan)
CREATE INDEX idx_orders_user_summary
  ON orders (user_id, status, total_amount, created_at);

-- Full-text search index (PostgreSQL)
CREATE INDEX idx_products_search
  ON products
  USING GIN (to_tsvector('turkish', name || ' ' || COALESCE(description, '')));

-- GIN index: JSONB alanları sorgulamak için
CREATE INDEX idx_products_metadata
  ON products
  USING GIN (metadata jsonb_path_ops);
```

### 3.3 N+1 Sorgu Problemi ve Çözümü

```typescript
// ❌ N+1 PROBLEM: Listedeki her sipariş için ayrı sorgu
async function getOrdersBAD(userId: string) {
  const orders = await prisma.order.findMany({ where: { userId } });
  // Her order için ayrı sorgu = N+1
  for (const order of orders) {
    order.items = await prisma.orderItem.findMany({
      where: { orderId: order.id }
    });
    // Her item için ayrı ürün sorgusu = N*M+1 😱
    for (const item of order.items) {
      item.product = await prisma.product.findUnique({
        where: { id: item.productId }
      });
    }
  }
}

// ✅ ÇÖZÜM: Eager loading ile tek sorguda
async function getOrdersGOOD(userId: string) {
  return prisma.order.findMany({
    where: { userId },
    include: {
      items: {
        include: {
          product: {
            select: { id: true, name: true, slug: true, price: true }
          }
        }
      }
    },
    orderBy: { createdAt: 'desc' },
    take: 20,
  });
  // → Prisma bunu 2-3 SQL sorgusuna çevirir (JOIN veya IN)
}
```

---

## 4. Caching Stratejileri

### 4.1 Redis Cache Katmanı

```typescript
// infrastructure/cache/RedisCache.ts
import Redis from 'ioredis';

export class RedisCache {
  private redis: Redis;

  constructor(url: string) {
    this.redis = new Redis(url, {
      maxRetriesPerRequest: 3,
      retryStrategy: (times) => Math.min(times * 50, 2000),
    });
  }

  // ---- Temel Operasyonlar ----
  async get<T>(key: string): Promise<T | null> {
    const data = await this.redis.get(key);
    return data ? JSON.parse(data) : null;
  }

  async set(key: string, value: unknown, ttlSeconds: number): Promise<void> {
    await this.redis.setex(key, ttlSeconds, JSON.stringify(value));
  }

  async del(key: string): Promise<void> {
    await this.redis.del(key);
  }

  // ---- Pattern ile toplu silme ----
  async invalidatePattern(pattern: string): Promise<void> {
    const keys = await this.redis.keys(pattern);
    if (keys.length > 0) {
      await this.redis.del(...keys);
    }
  }

  // ---- Cache-Aside Pattern ----
  async getOrSet<T>(
    key: string,
    fetcher: () => Promise<T>,
    ttlSeconds: number,
  ): Promise<T> {
    const cached = await this.get<T>(key);
    if (cached !== null) return cached;

    const fresh = await fetcher();
    await this.set(key, fresh, ttlSeconds);
    return fresh;
  }
}

// ---- Service'te kullanım ----
class ProductService {
  constructor(
    private productRepo: IProductRepository,
    private cache: RedisCache,
  ) {}

  async getProduct(id: string): Promise<Product> {
    return this.cache.getOrSet(
      `product:${id}`,
      () => this.productRepo.findById(id),
      300, // 5 dakika cache
    );
  }

  async updateProduct(id: string, data: UpdateProductDTO): Promise<Product> {
    const product = await this.productRepo.update(id, data);

    // Cache invalidation
    await this.cache.del(`product:${id}`);
    await this.cache.invalidatePattern('products:list:*');

    return product;
  }
}
```

### 4.2 Cache Stratejileri Karşılaştırma

| Strateji | Akış | Kullanım Alanı |
|---|---|---|
| **Cache-Aside** | App cache'i kontrol eder, yoksa DB'den alır, cache'e yazar | Genel kullanım |
| **Write-Through** | Yazma işlemi hem DB hem cache'e yapılır | Tutarlılık kritik |
| **Write-Behind** | Yazma önce cache'e, sonra asenkron DB'ye | Yüksek yazma trafiği |
| **Read-Through** | Cache otomatik DB'den yükler (cache sağlayıcı yönetir) | CDN, Varnish |

---

## 5. Hata Yönetimi (Error Handling)

### 5.1 Merkezi Error Handler

```typescript
// domain/errors/AppError.ts
export class AppError extends Error {
  constructor(
    public readonly statusCode: number,
    public readonly code: string,
    message: string,
    public readonly isOperational: boolean = true,
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

export class ValidationError extends AppError {
  constructor(
    message: string,
    public readonly details: Array<{ field: string; message: string }>,
  ) {
    super(400, 'VALIDATION_ERROR', message);
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Kimlik doğrulaması gerekli.') {
    super(401, 'UNAUTHORIZED', message);
  }
}

export class ForbiddenError extends AppError {
  constructor(message = 'Bu işlem için yetkiniz yok.') {
    super(403, 'FORBIDDEN', message);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string, id?: string) {
    super(404, 'NOT_FOUND', `${resource}${id ? ` (${id})` : ''} bulunamadı.`);
  }
}

export class ConflictError extends AppError {
  constructor(message: string) {
    super(409, 'CONFLICT', message);
  }
}

// ---- Middleware ----
// presentation/middlewares/errorHandler.ts
import { Request, Response, NextFunction } from 'express';

export function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  _next: NextFunction,
) {
  // Bilinen hata
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      success: false,
      error: {
        code: err.code,
        message: err.message,
        ...(err instanceof ValidationError && { details: err.details }),
        requestId: req.id,
      },
    });
  }

  // Prisma hataları
  if (err.constructor.name === 'PrismaClientKnownRequestError') {
    const prismaErr = err as any;
    if (prismaErr.code === 'P2002') {
      return res.status(409).json({
        success: false,
        error: {
          code: 'DUPLICATE_ENTRY',
          message: `${prismaErr.meta?.target} zaten mevcut.`,
          requestId: req.id,
        },
      });
    }
    if (prismaErr.code === 'P2025') {
      return res.status(404).json({
        success: false,
        error: {
          code: 'NOT_FOUND',
          message: 'Kayıt bulunamadı.',
          requestId: req.id,
        },
      });
    }
  }

  // Bilinmeyen hata → log'la ama detayı client'a verme
  logger.error('Unhandled error', {
    error: err.message,
    stack: err.stack,
    url: req.originalUrl,
    method: req.method,
    requestId: req.id,
  });

  res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_ERROR',
      message: 'Beklenmeyen bir hata oluştu.',
      requestId: req.id,
    },
  });
}

// app.ts
app.use(errorHandler); // En son middleware olarak ekle
```

---

## 6. Loglama ve Gözlemleme (Observability)

### 6.1 Yapılandırılmış Loglama (Structured Logging)

```typescript
// config/logger.ts
import pino from 'pino';

export const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport:
    process.env.NODE_ENV === 'development'
      ? { target: 'pino-pretty', options: { colorize: true } }
      : undefined, // Production: JSON formatı
  base: {
    service: 'api-server',
    env: process.env.NODE_ENV,
    version: process.env.APP_VERSION,
  },
  serializers: {
    req: pino.stdSerializers.req,
    err: pino.stdSerializers.err,
  },
  redact: {
    paths: ['req.headers.authorization', 'req.body.password', 'req.body.creditCard'],
    censor: '***REDACTED***',
  },
});

// ---- Request Logger Middleware ----
import { randomUUID } from 'crypto';

app.use((req, res, next) => {
  req.id = req.headers['x-request-id']?.toString() || randomUUID();
  const start = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - start;
    logger.info({
      requestId: req.id,
      method: req.method,
      url: req.originalUrl,
      statusCode: res.statusCode,
      duration: `${duration}ms`,
      userAgent: req.headers['user-agent'],
      ip: req.ip,
    });
  });

  next();
});
```

---

## 7. Mesaj Kuyrukları (Message Queues)

### 7.1 BullMQ ile Asenkron İş İşleme

```typescript
// infrastructure/queue/emailQueue.ts
import { Queue, Worker, Job } from 'bullmq';
import IORedis from 'ioredis';

const connection = new IORedis(process.env.REDIS_URL!, { maxRetriesPerRequest: null });

// ---- Producer (Kuyruğa ekleme) ----
export const emailQueue = new Queue('email', {
  connection,
  defaultJobOptions: {
    attempts: 3,
    backoff: { type: 'exponential', delay: 2000 },
    removeOnComplete: { count: 1000 },   // Son 1000 başarılı job'ı tut
    removeOnFail: { count: 5000 },
  },
});

// Farklı iş türleri
export async function queueWelcomeEmail(email: string, name: string) {
  await emailQueue.add('welcome', { email, name }, { priority: 1 });
}

export async function queueOrderConfirmation(orderId: string) {
  await emailQueue.add(
    'order-confirmation',
    { orderId },
    { priority: 2, delay: 5000 }, // 5 saniye sonra gönder
  );
}

export async function queueWeeklyDigest() {
  await emailQueue.add(
    'weekly-digest',
    {},
    {
      repeat: { pattern: '0 9 * * 1' }, // Her pazartesi saat 09:00
    },
  );
}

// ---- Consumer (İşleme) ----
const emailWorker = new Worker(
  'email',
  async (job: Job) => {
    switch (job.name) {
      case 'welcome':
        await sendWelcomeEmail(job.data.email, job.data.name);
        break;
      case 'order-confirmation':
        await sendOrderConfirmation(job.data.orderId);
        break;
      case 'weekly-digest':
        await sendWeeklyDigest();
        break;
      default:
        throw new Error(`Bilinmeyen iş türü: ${job.name}`);
    }
  },
  {
    connection,
    concurrency: 5,                // Aynı anda 5 iş
    limiter: { max: 10, duration: 1000 }, // Saniyede max 10 iş
  },
);

emailWorker.on('completed', (job) => {
  logger.info({ jobId: job.id, name: job.name }, 'Email gönderildi');
});

emailWorker.on('failed', (job, err) => {
  logger.error({ jobId: job?.id, error: err.message }, 'Email gönderilemedi');
});
```

---

## 8. Authentication ve Authorization

### 8.1 Rol Tabanlı Erişim Kontrolü (RBAC)

```typescript
// presentation/middlewares/authMiddleware.ts
import jwt from 'jsonwebtoken';

// Token doğrulama
export function authenticate(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;

  if (!authHeader?.startsWith('Bearer ')) {
    throw new UnauthorizedError('Bearer token gerekli.');
  }

  const token = authHeader.split(' ')[1];

  try {
    const payload = jwt.verify(token, process.env.JWT_ACCESS_SECRET!) as {
      userId: string;
      role: Role;
    };
    req.user = payload;
    next();
  } catch (err) {
    if (err instanceof jwt.TokenExpiredError) {
      throw new UnauthorizedError('Token süresi dolmuş.');
    }
    throw new UnauthorizedError('Geçersiz token.');
  }
}

// Rol kontrolü — Higher-Order Middleware
export function authorize(...allowedRoles: Role[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      throw new UnauthorizedError();
    }

    if (!allowedRoles.includes(req.user.role)) {
      throw new ForbiddenError(
        `Bu işlem ${allowedRoles.join(', ')} rolü gerektirir.`
      );
    }

    next();
  };
}

// ---- Route'larda kullanım ----
const router = Router();

// Herkes erişebilir
router.get('/products', productController.list);

// Giriş yapmış kullanıcı
router.get('/profile', authenticate, userController.getProfile);

// Sadece admin
router.delete(
  '/users/:id',
  authenticate,
  authorize('ADMIN'),
  userController.delete,
);

// Admin veya moderatör
router.patch(
  '/reviews/:id/approve',
  authenticate,
  authorize('ADMIN', 'MODERATOR'),
  reviewController.approve,
);
```

---

## 9. Environment Yönetimi

### 9.1 Tip-Güvenli Environment Variables

```typescript
// config/env.ts
import { z } from 'zod';

const envSchema = z.object({
  // Sunucu
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  PORT: z.coerce.number().default(3000),
  HOST: z.string().default('0.0.0.0'),

  // Veritabanı
  DATABASE_URL: z.string().url(),

  // Redis
  REDIS_URL: z.string().url(),

  // JWT
  JWT_ACCESS_SECRET: z.string().min(32),
  JWT_REFRESH_SECRET: z.string().min(32),

  // CORS
  CORS_ORIGINS: z
    .string()
    .transform((s) => s.split(',').map((o) => o.trim()))
    .pipe(z.array(z.string().url())),

  // Email
  SENDGRID_API_KEY: z.string().optional(),
  EMAIL_FROM: z.string().email().default('noreply@example.com'),

  // Loglama
  LOG_LEVEL: z.enum(['fatal', 'error', 'warn', 'info', 'debug', 'trace']).default('info'),
});

// Parse et — hata varsa sunucu BAŞLAMAZ
function validateEnv() {
  const result = envSchema.safeParse(process.env);

  if (!result.success) {
    console.error('❌ Environment validation hatası:');
    for (const issue of result.error.issues) {
      console.error(`   ${issue.path.join('.')}: ${issue.message}`);
    }
    process.exit(1);
  }

  return result.data;
}

export const env = validateEnv();

// Kullanım: env.DATABASE_URL (tam tip güvenli) ✅
// process.env.DATABASE_URL (string | undefined) ❌
```

---

## 10. Güvenli Şifre Yönetimi

```typescript
// infrastructure/auth/PasswordHasher.ts
import argon2 from 'argon2';

export class Argon2PasswordHasher implements IPasswordHasher {
  async hash(password: string): Promise<string> {
    return argon2.hash(password, {
      type: argon2.argon2id,       // Argon2id: brute-force + side-channel dayanıklı
      memoryCost: 65536,           // 64 MB RAM
      timeCost: 3,                 // 3 iterasyon
      parallelism: 4,             // 4 thread
    });
  }

  async verify(hash: string, password: string): Promise<boolean> {
    try {
      return await argon2.verify(hash, password);
    } catch {
      return false;
    }
  }
}

// ❌ YANLIŞ: MD5, SHA-256 (kırılabilir), bcrypt (yeterli ama eski)
// ✅ DOĞRU: Argon2id (2024+ standart)
```

---

## 11. Dependency Injection

```typescript
// container.ts — Basit DI Container
import { PrismaClient } from '@prisma/client';

// Bağımlılıkları oluştur
const prisma = new PrismaClient();
const cache = new RedisCache(env.REDIS_URL);
const hasher = new Argon2PasswordHasher();
const emailService = new SendGridEmailService(env.SENDGRID_API_KEY);

// Repository'ler
const userRepo = new PrismaUserRepository(prisma);
const productRepo = new PrismaProductRepository(prisma);

// Service'ler
const userService = new UserService(userRepo, emailService, hasher);
const productService = new ProductService(productRepo, cache);

// Controller'lar
const userController = new UserController(userService);
const productController = new ProductController(productService);

// Router
const apiRouter = Router();
apiRouter.use('/users', createUserRoutes(userController));
apiRouter.use('/products', createProductRoutes(productController));

export { apiRouter, prisma };
```

---

## 12. Hızlı Referans Matrisi

| Konu | En İyi Pratik | Araç |
|---|---|---|
| Mimari | Katmanlı (Clean Architecture) | Domain → App → Infra → Presentation |
| API Tasarımı | REST + versiyonlama | `GET /api/v1/resources` |
| DB Erişim | ORM + Raw SQL hibrit | Prisma + pg |
| Cache | Cache-Aside + TTL | Redis (ioredis) |
| Queue | Asenkron iş kuyruğu | BullMQ |
| Auth | JWT (Access + Refresh) | jsonwebtoken + Argon2id |
| Validation | Schema-first | Zod |
| Hata Yönetimi | Merkezi error handler | AppError hiyerarşisi |
| Loglama | Structured JSON logging | Pino |
| Env | Tip-güvenli doğrulama | Zod + dotenv |
| DI | Constructor injection | Manuel veya tsyringe |
| Test | Repository mock + Integration | Vitest + Supertest |

---

## 13. Referanslar

- Node.js Best Practices: https://github.com/goldbergyoni/nodebestpractices
- The Twelve-Factor App: https://12factor.net/
- Prisma Docs: https://www.prisma.io/docs
- BullMQ Docs: https://docs.bullmq.io/
- Pino Logger: https://getpino.io/
- OWASP API Security Top 10: https://owasp.org/API-Security/
- Redis Best Practices: https://redis.io/docs/management/optimization/
