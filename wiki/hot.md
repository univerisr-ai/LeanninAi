# Sicak Bellek (Hot Cache)

Bu bolum en son uretilen draft bilgisinin hizli ozetidir.

## MCP Sunucuları ile Claude için Güvenlik Zekâsı Sağlama
→ [[review/mcp-sunuculari-ile-claude-icin-guvenlik-zek-si-saglama]]

Bu konsept, mukul975/cve-mcp-server projesi üzerinden bir Model Context Protocol (MCP) sunucusunun nasıl production-grade güvenlik zekâsı sağlayabileceğini açıklar. Özellikle Claude AI ile entegre çalışarak CVE, EPSS, CISA KEV, MITRE ATT&CK gibi 21 farklı API’den gelen verilerle tehdit istihbaratı sağlar.
- FastMCP framework kullanılarak geliştirilmiş, yüksek performanslı bir güvenlik zekâsı sunucusudur.
- 27 farklı güvenlik aracı ile Claude’a bağlamsal siber güvenlik bilgisi sağlar.
- Desteklenen kaynaklar arasında Shodan, VirusTotal, NVD, OSV ve MITRE ATT&CK yer alır.

## HTML-in-Canvas: İnteraktif Web Deneyimlerini Dönüştürebilecek Deneysel API
→ [[review/html-in-canvas-interaktif-web-deneyimlerini-donusturebilecek-deneysel-api]]

Bu konsept, henüz deneysel aşamada olan HTML-in-Canvas API'sini tanıtıyor. Bu yeni yaklaşım, HTML elementlerinin doğrudan <canvas> içerisine yerleştirilerek hem görsel performansın korunmasını hem de erişilebilirlik, form elemanları ve metin seçimi gibi native tarayıcı özelliklerinden vazgeçilmeden zengin interaktif deneyimler oluşturulmasını sağlıyor.
- HTML-in-Canvas, WICG tarafından önerilen ve şu anda yalnızca Chrome Canary'de aktif edilebilen deneysel bir özelliktir.
- Temel amaç, canvas üzerinde çizilen içeriklerde erişilebilirlik, form elemanları ve metin işlemleri gibi HTML'in sunduğu avantajlardan faydalanabilmektir.
- Üç temel yapı taşından oluşur: `layoutsubtree` özelliği, `drawElementImage()` metodu ve `paint` olayı.

## HTML'den Markdown'a Dönüştürerek LLM Maliyetlerini Azaltmak
→ [[review/html-den-markdown-a-donusturerek-llm-maliyetlerini-azaltmak]]

Bu makalede, web içeriklerinin LLM'lere gönderilmeden önce HTML'den Markdown formatına dönüştürülmesinin, token tüketimini önemli ölçüde azalttığı ve maliyet tasarrufu sağladığı ele alınıyor. Özellikle veri kazıma, özetleme ve RAG sistemleri gibi işlemlerde bu yöntemin etkin bir optimizasyon olduğu gösteriliyor.
- HTML içerikler, özellikle sınıf adları ve yapısal etiketlerle birlikte, LLM token tüketimini ciddi şekilde artırır.
- Markdown formatı, aynı bilgiyi daha düşük token maliyetiyle sunar çünkü daha sade ve modele tanıdık bir yapıdadır.
- Pratik bir örnek olarak, Wikipedia'nın HTML hali ~48.000 token iken Markdown hali sadece ~8.900 tokendir.

## CVE-2026-34197: 13 Yıldır Gizli Kalan ActiveMQ RCE Açığı ve Acil Patch Zorunluluğu
→ [[review/cve-2026-34197-13-yildir-gizli-kalan-activemq-rce-acigi-ve-acil-patch-zorunlulugu]]

CVE-2026-34197, Apache ActiveMQ'de 13 yıldır fark edilmeyen kritik bir RCE (Remote Code Execution) açığıdır. CISA bu açığı KEV kataloğuna ekleyerek tüm federal kurumların 30 Nisan 2026 tarihine kadar patch uygulamasını zorunlu kılmıştır. Bu konsept, teknik detaylar, risk analizi ve korunma stratejileri üzerine pratik bilgiler içerir.
- Açık, ActiveMQ'nin Jolokia API'si üzerinden kimlik doğrulaması olmadan uzaktan kod çalıştırılmasına izin veriyor.
- Varsayılan admin:admin kimlik bilgilerinin varlığı ve Jolokia'nın açık yapılandırması riski artırıyor.
- Horizon3.ai tarafından keşfedilmiş ve CISA tarafından aktif sömürüldüğü teyit edilmiş.

## Supabase Row Level Security (RLS) Üretim Ortamı Desenleri
→ [[review/supabase-row-level-security-rls-uretim-ortami-desenleri]]

Supabase RLS (Row Level Security), PostgreSQL'in veri katmanında yerleşik erişim kontrolü sağlayan bir sistemdir. Bu konsept, üretim ortamında güvenli veri erişimi için uygulanabilir RLS desenlerini ve sık karşılaşılan hataları ele alır.
- RLS etkinleştirildiğinde, politikalar olmadan tablolardan veri çekilmez.
- Her kullanıcıya özel veri erişimi için dört temel politika (SELECT, INSERT, UPDATE, DELETE) tanımlanmalıdır.
- `USING` koşulu mevcut satırlar üzerinde filtreleme yaparken, `WITH CHECK` yeni yazılan satırları doğrular.

