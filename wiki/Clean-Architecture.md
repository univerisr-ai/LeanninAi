# Clean Architecture (Katmanlı Mimari)

## Meta
- category: backend
- status: published


Yazılımda değişikliklerin birbirini etkilemesini en aza indiren en etkili yapıdır. Temel kural: **Bağımlılıklar daima dışardan içeriye, çekirdeğe (Domain) doğru bakmalıdır.** Çekirdek hiçbir dış aracı (Veritabanı, Framework) bilmez.

## Katmanlar (İçten Dışa)

1. **Domain Layer (Çekirdek):** Saf iş kuralları. Entity'ler, Value Object'ler ve özel Error sınıfları burada yaşar. Dış dünyadan habersizdir, sadece TypeScript/JavaScript içerir. Örn: Bir E-Ticaret sepeti kuralları.
2. **Application Layer (Use Cases):** İş akışı orkestrasyonudur. Servisler burada yer alır. Domain nesnelerini çağırır, manipüle eder. Ancak veritabanı işlemlerini *Interface'ler (Soyutlamalar)* üzerinden yapar, Prisma'yı doğrudan import etmez.
3. **Infrastructure Layer:** Gerçek dış dünya. Prisma (DB), Redis, Axios, BullMQ, AWS entegrasyonları burada bulunur. Application katmanındaki arayüzlerin (Interface) gerçek implementasyonudur.
4. **Presentation (Arayüz/Route) Layer:** HTTP isteklerini karşılama (Express/Fastify controller'ları) veya terminal/CRON işleri. Datayı alır, Application servisine gönderir ve sonucu DTO olarak döner.

> **Neden?** Veritabanınızı MongoDB'den PostgreSQL'e değiştirirseniz, sadece Infrastructure katmanında tek bir dosya değişir; İş kurallarınız (Domain) ve Servisleriniz (Application) etkilenmez.

**İlgili Bağlantılar:**
- [[Veritabani-ve-Caching-Stratejileri]]
- [[State-Yonetimi-Zustand-TanStack]] (Frontend Mimari Bağlantısı)

## 📚 İlgili Draftlar
- [[review/api-response-yapilari-flat-vs-nested-duzlestirilmis-vs-ic-ice]]
- [[review/mcp-sunuculari-gelistiriciler-icin-yeni-bir-backend-paradigmasi]]
- [[review/mimari-dokumantasyonu-ai-destekli-kalite-kontrolunde-onemli-bir-varlik]]
- [[review/spec-driven-ai-development-gercek-dunya-ornegi-ile-uygulamali-yaklasim]]
- [[review/mcp-sunuculari-ile-claude-icin-guvenlik-zek-si-saglama]]
- [[review/ai-ajanlari-icin-odeme-protokolu-x402-ve-yetki-katmani-l4]]
- [[review/benchmark-skorlarinin-guvenilirliginin-sorgulanmasi-ve-davranissal-telemetri-ile-dogrulama]]
- [[review/tanstack-query-v5-ile-olceklenebilir-sunucu-durumu-yonetimi]]
- [[review/tariff-refund-portali-yuksek-trafige-hazirlikli-ozel-bir-web-uygulamasi]]