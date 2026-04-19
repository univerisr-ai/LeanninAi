import tempfile
import unittest
from pathlib import Path

from aibeyin.query_engine import build_brain_index, query_brain


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class QueryEngineTests(unittest.TestCase):
    def test_query_prefers_relevant_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki_root = Path(tmp) / "wiki"
            write_file(
                wiki_root / "Rate-Limiting-Token-Bucket.md",
                """# Rate Limiting ve Token Bucket

## Meta
- status: published
- category: security

## Ozet
Token bucket algoritmasi API kotasi ve bot korumasinda kullanilir.

## Ana Noktalar
- Rate limit burst trafigi dengeler.

## Iliskili Sayfalar
- [[Bot-Tespiti-ve-Honeypot]]
""",
            )
            write_file(
                wiki_root / "Bot-Tespiti-ve-Honeypot.md",
                """# Bot Tespiti ve Honeypot

## Meta
- status: published
- category: security

## Ozet
Honeypot alanlari botlari ayiklamak icin faydalidir.

## Ana Noktalar
- Gizli alanlar davranissal tespit saglar.

## Iliskili Sayfalar
- [[Rate-Limiting-Token-Bucket]]
""",
            )

            payload = query_brain(wiki_root, "token bucket rate limit", limit=1)
            self.assertEqual(payload["result_count"], 1)
            self.assertEqual(payload["results"][0]["slug"], "Rate-Limiting-Token-Bucket")

    def test_build_brain_index_reports_graph(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki_root = Path(tmp) / "wiki"
            write_file(
                wiki_root / "A.md",
                """# A

## Meta
- status: published
- category: frontend

## Ozet
Alpha.

## Iliskili Sayfalar
- [[B]]
""",
            )
            write_file(
                wiki_root / "B.md",
                """# B

## Meta
- status: published
- category: frontend

## Ozet
Beta.

## Iliskili Sayfalar
- [[A]]
""",
            )
            write_file(
                wiki_root / "C.md",
                """# C

## Meta
- status: published
- category: frontend

## Ozet
Gamma.
""",
            )

            payload = build_brain_index(wiki_root)
            self.assertEqual(payload["page_count"], 3)
            self.assertEqual(payload["edge_count"], 1)
            self.assertIn("C", payload["orphans"])


if __name__ == "__main__":
    unittest.main()
