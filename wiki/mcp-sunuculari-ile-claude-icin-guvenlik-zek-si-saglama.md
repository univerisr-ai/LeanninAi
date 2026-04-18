# MCP Sunucuları ile Claude için Güvenlik Zekâsı Sağlama

## Meta
- status: published
- category: backend
- confidence: 90
- novelty: 75
- model: qwen/qwen3-coder:free
- source: https://github.com/mukul975/cve-mcp-server
- source_name: github_repos
- generated_at: 2026-04-18T02:52:34+00:00

## Ozet
Bu konsept, mukul975/cve-mcp-server projesi üzerinden bir Model Context Protocol (MCP) sunucusunun nasıl production-grade güvenlik zekâsı sağlayabileceğini açıklar. Özellikle Claude AI ile entegre çalışarak CVE, EPSS, CISA KEV, MITRE ATT&CK gibi 21 farklı API’den gelen verilerle tehdit istihbaratı sağlar.

## Ana Noktalar
- FastMCP framework kullanılarak geliştirilmiş, yüksek performanslı bir güvenlik zekâsı sunucusudur.
- 27 farklı güvenlik aracı ile Claude’a bağlamsal siber güvenlik bilgisi sağlar.
- Desteklenen kaynaklar arasında Shodan, VirusTotal, NVD, OSV ve MITRE ATT&CK yer alır.
- DevSecOps süreçlerine entegre olacak şekilde tasarlanmış, otomasyon dostu yapı sunar.
- Python tabanlıdır ve modüler araç mimarisi sayesinde genişletilebilirlik sunar.

## Iliskili Sayfalar
- [[MCP Sunucuları: Geliştiriciler İçin Yeni Bir Backend Paradigması]]
- [[AI Tehdit Modelleme: STRIDE-AI ve MITRE-ATLAS ile Güvenlik Analizi]]
- [[Veritabani-ve-Caching-Stratejileri]]
- [[index]]
- [[review/index]]
- [[Clean-Architecture]]
- [[Veritabani-ve-Caching-Stratejileri]]

## Kaynak Basligi
mukul975/cve-mcp-server
