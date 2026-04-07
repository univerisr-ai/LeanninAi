# Veri Çekme (Scraping) Botlarına Karşı Alınan Anti-Bot Güvenlik Önlemleri ve Rate Limit Aşımı

**Tarih:** 2026-04-07  
**Kategori:** Backend Güvenliği, Web Scraping  
**Seviye:** Orta-İleri

---

## 1. Giriş

Web scraping, internet üzerindeki verileri otomatik olarak toplama işlemidir. Site sahipleri bu botları engellemek için çeşitli teknikler kullanırken, scraper geliştiricileri de bu engelleri aşmak için karşı teknikler geliştirir. Bu rehber her iki tarafı da ele alır.

---

## 2. Anti-Bot Mekanizmaları (Savunma Tarafı)

### 2.1 Rate Limiting

Rate limiting, belirli bir zaman diliminde aynı IP'den gelen istek sayısını sınırlar.

**Node.js — Express ile Rate Limiter (express-rate-limit):**

```javascript
const express = require('express');
const rateLimit = require('express-rate-limit');

const app = express();

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 dakika
  max: 100,                  // 15 dakikada maksimum 100 istek
  standardHeaders: true,     // RateLimit-* headerları döner
  legacyHeaders: false,
  handler: (req, res) => {
    res.status(429).json({
      error: 'Çok fazla istek gönderdiniz. Lütfen bekleyin.',
      retryAfter: Math.ceil(req.rateLimit.resetTime / 1000)
    });
  }
});

app.use('/api/', limiter);

app.get('/api/data', (req, res) => {
  res.json({ data: 'Korunan endpoint verisi' });
});

app.listen(3000);
```

**Python — FastAPI ile Rate Limiter (slowapi):**

```python
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/data")
@limiter.limit("10/minute")  # Dakikada 10 istek
async def get_data(request: Request):
    return {"data": "Korunan endpoint verisi"}
```

---

### 2.2 IP Engelleme ve Coğrafi Kısıtlama

Kötü amaçlı IP'leri veya belirli ülkeleri bloke etme.

**Python — Flask ile IP Kara Liste Kontrolü:**

```python
from flask import Flask, request, jsonify, abort
import ipaddress

app = Flask(__name__)

# Kara listedeki IP aralıkları
BLACKLISTED_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("192.168.0.0/16"),
]

# Bilinen proxy/VPN CIDR'ları buraya eklenebilir
BLOCKED_IPS = {"1.2.3.4", "5.6.7.8"}

def is_blocked(ip_str: str) -> bool:
    try:
        ip = ipaddress.ip_address(ip_str)
        if ip_str in BLOCKED_IPS:
            return True
        for network in BLACKLISTED_RANGES:
            if ip in network:
                return True
    except ValueError:
        return True
    return False

@app.before_request
def check_ip():
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    real_ip = client_ip.split(",")[0].strip()
    if is_blocked(real_ip):
        abort(403)

@app.get("/api/data")
def get_data():
    return jsonify({"data": "Güvenli veri"})
```

---

### 2.3 User-Agent Analizi ve Fingerprinting

Botlar genellikle sahte veya eksik User-Agent gönderir. Tarayıcı parmak izi (fingerprinting) daha gelişmiş bir yöntemdir.

**Node.js — Şüpheli User-Agent Tespiti:**

```javascript
const suspiciousPatterns = [
  /python-requests/i,
  /axios/i,
  /curl/i,
  /wget/i,
  /scrapy/i,
  /java\/\d/i,
  /go-http-client/i,
  /^$/  // Boş User-Agent
];

function isSuspiciousUserAgent(ua) {
  if (!ua) return true;
  return suspiciousPatterns.some(pattern => pattern.test(ua));
}

app.use((req, res, next) => {
  const ua = req.headers['user-agent'];
  if (isSuspiciousUserAgent(ua)) {
    return res.status(403).json({ error: 'Erişim reddedildi.' });
  }
  next();
});
```

---

### 2.4 CAPTCHA Entegrasyonu

**Node.js — Google reCAPTCHA v3 Doğrulama:**

```javascript
const axios = require('axios');

async function verifyRecaptcha(token, remoteip) {
  const secret = process.env.RECAPTCHA_SECRET_KEY;
  const response = await axios.post(
    'https://www.google.com/recaptcha/api/siteverify',
    null,
    {
      params: { secret, response: token, remoteip }
    }
  );

  const { success, score, action } = response.data;

  // Score: 0.0 (bot) → 1.0 (insan)
  if (!success || score < 0.5) {
    throw new Error('CAPTCHA doğrulaması başarısız.');
  }
  return true;
}

app.post('/api/submit', async (req, res) => {
  try {
    const { captchaToken, data } = req.body;
    await verifyRecaptcha(captchaToken, req.ip);
    // İşleme devam et
    res.json({ success: true });
  } catch (err) {
    res.status(403).json({ error: err.message });
  }
});
```

---

### 2.5 Honeypot Alanları

Botların görünmez alanlara tıklamasını veya form doldurmasını tespit etme.

**HTML + Node.js Honeypot Örneği:**

```html
<!-- Kullanıcıya görünmez, bot doldurur -->
<form action="/api/submit" method="POST">
  <input type="text" name="username" placeholder="Kullanıcı adı">
  
  <!-- Honeypot: display:none ile gizli -->
  <input type="text" name="website" style="display:none" tabindex="-1" autocomplete="off">
  
  <button type="submit">Gönder</button>
</form>
```

```javascript
app.post('/api/submit', (req, res) => {
  // Honeypot dolu ise bot
  if (req.body.website && req.body.website.length > 0) {
    // Botu sessizce reddet veya sahte başarı döndür
    return res.json({ success: true }); // Bot'u yanıltmak için
  }
  // Gerçek işlem
  res.json({ success: true, message: 'Form alındı.' });
});
```

---

### 2.6 JavaScript Challenge (JS Fingerprinting)

Cloudflare gibi sistemler JavaScript çalıştırabilme kabiliyetini test eder. Headless tarayıcılar genellikle eksik Web API'larına sahiptir.

**Node.js — Basit JS Challenge Token Üretimi:**

```javascript
const crypto = require('crypto');

// Sunucu bir challenge token üretir
app.get('/challenge', (req, res) => {
  const challenge = crypto.randomBytes(16).toString('hex');
  req.session.challenge = challenge;
  
  // Client-side JS bu challenge'ı çözecek
  res.json({ challenge });
});

// Client challenge'ı çözüp geri gönderir
app.post('/verify-challenge', (req, res) => {
  const { solution } = req.body;
  const expected = crypto
    .createHash('sha256')
    .update(req.session.challenge + 'SECRET_SALT')
    .digest('hex');

  if (solution !== expected) {
    return res.status(403).json({ error: 'Challenge başarısız.' });
  }

  req.session.verified = true;
  res.json({ success: true });
});
```

---

## 3. Rate Limit Aşma Teknikleri (Saldırgan/Test Tarafı)

> **Etik Not:** Bu teknikler yalnızca kendi sistemlerinizi test etmek, eğitim veya yetkili penetrasyon testleri için kullanılmalıdır.

### 3.1 İstek Geciktirme (Request Throttling)

**Python — Rastgele Gecikmeli Scraper:**

```python
import requests
import time
import random
from typing import Optional

class ThrottledScraper:
    def __init__(self, min_delay: float = 1.0, max_delay: float = 5.0):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.session = requests.Session()

    def get(self, url: str, **kwargs) -> Optional[requests.Response]:
        delay = random.uniform(self.min_delay, self.max_delay)
        time.sleep(delay)
        
        try:
            response = self.session.get(url, timeout=10, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"İstek hatası: {e}")
            return None

# Kullanım
scraper = ThrottledScraper(min_delay=2.0, max_delay=6.0)
response = scraper.get("https://example.com/api/data")
```

---

### 3.2 Rotating Proxy Kullanımı

**Python — Proxy Rotasyonu:**

```python
import requests
import random
import time

PROXY_LIST = [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
    "http://proxy3.example.com:8080",
]

def get_random_proxy() -> dict:
    proxy = random.choice(PROXY_LIST)
    return {"http": proxy, "https": proxy}

def fetch_with_rotating_proxy(url: str, max_retries: int = 3):
    for attempt in range(max_retries):
        proxy = get_random_proxy()
        try:
            response = requests.get(
                url,
                proxies=proxy,
                timeout=15,
                headers={"User-Agent": get_random_ua()}
            )
            if response.status_code == 200:
                return response
            elif response.status_code == 429:
                wait = 2 ** attempt  # Exponential backoff
                print(f"Rate limit. {wait}s bekleniyor...")
                time.sleep(wait)
        except requests.ProxyError:
            print(f"Proxy hatası, değiştiriliyor: {proxy}")
            continue
    return None

def get_random_ua() -> str:
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    ]
    return random.choice(agents)
```

---

### 3.3 Header Rotasyonu ve Tarayıcı Taklidi

**Python — Gerçekçi Header Seti:**

```python
import requests
import random

def build_browser_headers(referer: str = None) -> dict:
    headers = {
        "User-Agent": get_random_ua(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none" if not referer else "same-origin",
        "Cache-Control": "max-age=0",
    }
    if referer:
        headers["Referer"] = referer
    return headers

session = requests.Session()
session.headers.update(build_browser_headers())
response = session.get("https://example.com")
```

---

### 3.4 Exponential Backoff ile Akıllı Yeniden Deneme

**Node.js — Retry Mekanizması:**

```javascript
const axios = require('axios');

async function fetchWithBackoff(url, options = {}, maxRetries = 5) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const response = await axios.get(url, {
        ...options,
        timeout: 10000,
      });
      return response.data;
    } catch (error) {
      const status = error.response?.status;

      if (status === 429) {
        // Sunucunun önerdiği bekleme süresi
        const retryAfter = error.response.headers['retry-after'];
        const waitMs = retryAfter
          ? parseInt(retryAfter) * 1000
          : Math.pow(2, attempt) * 1000 + Math.random() * 1000;

        console.log(`Rate limit — ${attempt + 1}. deneme, ${waitMs}ms bekleniyor`);
        await new Promise(resolve => setTimeout(resolve, waitMs));
        continue;
      }

      if (status === 403 || status === 401) {
        throw new Error(`Erişim reddedildi: ${status}`);
      }

      throw error;
    }
  }
  throw new Error('Maksimum deneme sayısına ulaşıldı.');
}

// Kullanım
fetchWithBackoff('https://api.example.com/data')
  .then(data => console.log(data))
  .catch(err => console.error(err.message));
```

---

### 3.5 Session ve Cookie Yönetimi

**Python — Oturum Çerezi ile Scraping:**

```python
import requests
from http.cookiejar import MozillaCookieJar

class SessionScraper:
    def __init__(self):
        self.session = requests.Session()
        self.cookie_jar = MozillaCookieJar()
        self.session.cookies = self.cookie_jar

    def login(self, login_url: str, credentials: dict) -> bool:
        """Önce giriş yaparak oturum çerezi al"""
        response = self.session.post(
            login_url,
            data=credentials,
            headers=build_browser_headers(),
            allow_redirects=True
        )
        return response.status_code == 200

    def fetch_authenticated(self, url: str):
        """Oturum çerezi ile veri çek"""
        return self.session.get(
            url,
            headers=build_browser_headers(referer=url)
        )

    def save_cookies(self, path: str):
        self.cookie_jar.save(path, ignore_discard=True)

    def load_cookies(self, path: str):
        self.cookie_jar.load(path, ignore_discard=True)
```

---

## 4. Tespit ve Savunma Matrisi

| Saldırı Tekniği | Tespit Yöntemi | Savunma |
|---|---|---|
| Yüksek frekanslı istek | Rate limit sayacı | Token Bucket / Sliding Window |
| Tek IP rotasyonu | IP bazlı limit | CIDR bloklama, ASN filtresi |
| Sahte User-Agent | UA pattern matching | ML tabanlı sınıflandırma |
| Headless tarayıcı | JS challenge, TLS fingerprint | Cloudflare, PerimeterX |
| Proxy rotasyonu | Proxy IP veritabanı | IPQualityScore, MaxMind |
| Cookie/session manipülasyonu | Session anomali tespiti | HttpOnly + SameSite cookie |
| Slowloris / düşük hızlı bot | Zaman bazlı anomali | Nginx timeout + connection limit |

---

## 5. Token Bucket Algoritması (Rate Limit Uygulaması)

**Python — Token Bucket İmplementasyonu:**

```python
import time
import threading
from collections import defaultdict

class TokenBucket:
    """
    Her IP için ayrı token bucket tutar.
    capacity: maksimum token sayısı
    refill_rate: saniyede eklenen token
    """
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.buckets: dict = defaultdict(lambda: {"tokens": capacity, "last_refill": time.time()})
        self.lock = threading.Lock()

    def consume(self, key: str, tokens: int = 1) -> bool:
        with self.lock:
            bucket = self.buckets[key]
            now = time.time()
            elapsed = now - bucket["last_refill"]
            
            # Token yenile
            bucket["tokens"] = min(
                self.capacity,
                bucket["tokens"] + elapsed * self.refill_rate
            )
            bucket["last_refill"] = now

            if bucket["tokens"] >= tokens:
                bucket["tokens"] -= tokens
                return True  # İzin verildi
            return False  # Rate limit aşıldı

# Flask middleware olarak kullanım
from flask import Flask, request, jsonify, abort

bucket = TokenBucket(capacity=20, refill_rate=1.0)  # Saniyede 1 token
app = Flask(__name__)

@app.before_request
def rate_limit():
    ip = request.remote_addr
    if not bucket.consume(ip):
        abort(429)
```

---

## 6. Referanslar ve İleri Okuma

- OWASP Automated Threats to Web Applications: https://owasp.org/www-project-automated-threats-to-web-applications/
- RFC 6585 — HTTP 429 Status Code: https://tools.ietf.org/html/rfc6585
- Cloudflare Bot Management Docs
- `express-rate-limit` npm paketi
- `slowapi` Python kütüphanesi
- MaxMind GeoIP2 veritabanı (IP coğrafi engelleme için)
