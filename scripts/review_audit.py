"""Mevcut review dosyalarini analiz et ve auto-publish/purge uygula."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.aibeyin.wiki_writer import WikiWriter

project_root = Path(__file__).resolve().parent.parent

publish_config = {
    "enabled": True,
    "min_confidence": 85,
    "min_novelty": 70,
    "min_word_count": 80,
    "purge_low_quality": True,
    "purge_max_confidence": 50,
}

writer = WikiWriter(project_root)

# Oncelikle mevcut review dosyalarini analiz edelim
review_root = project_root / "wiki" / "review"
skip = {"index.md", ".gitkeep"}
stats = {"high": 0, "mid": 0, "low": 0, "fallback": 0}

for path in sorted(review_root.glob("*.md")):
    if path.name.lower() in skip:
        continue
    try:
        text = path.read_text(encoding="utf-8")
        meta = writer._parse_review_meta(text)
        conf = meta.get("confidence", 0)
        nov = meta.get("novelty", 0)
        model = meta.get("model", "")
        is_fb = "fallback:" in model

        if is_fb:
            stats["fallback"] += 1
        elif conf >= 85 and nov >= 70:
            stats["high"] += 1
        elif conf >= 70:
            stats["mid"] += 1
        else:
            stats["low"] += 1
    except Exception:
        stats["low"] += 1

print("=== Mevcut Review Analizi ===")
print(json.dumps(stats, indent=2))
print(f"\nToplam: {sum(stats.values())} dosya")
print(f"  Yuksek kalite (publish edilecek): {stats['high']}")
print(f"  Orta kalite (kalacak): {stats['mid']}")
print(f"  Dusuk kalite (silinecek): {stats['low']}")
print(f"  Fallback (silinecek): {stats['fallback']}")

# Simdi auto-publish uygula
if "--apply" in sys.argv:
    result = writer.auto_publish_reviews(publish_config)
    print(f"\n=== Auto-Publish Sonucu ===")
    print(json.dumps(result, indent=2))
else:
    print("\nUygulamak icin: python scripts/review_audit.py --apply")
