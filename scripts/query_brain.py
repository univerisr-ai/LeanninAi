import argparse
import json
import sys
from pathlib import Path


def bootstrap_path() -> Path:
    root = Path(__file__).resolve().parents[1]
    src = root / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
    return root


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Query AiBeyin like a second-brain retrieval layer")
    parser.add_argument("query", help="Search question or topic")
    parser.add_argument("--limit", type=int, default=5, help="Maximum result count")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    return parser.parse_args()


def main() -> int:
    project_root = bootstrap_path()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    from aibeyin.query_engine import query_brain

    args = parse_args()
    payload = query_brain(project_root / "wiki", args.query, limit=max(1, args.limit))

    if args.json:
        print(json.dumps(payload, ensure_ascii=True, indent=2))
        return 0

    print(f"Sorgu: {payload['query']}")
    print(f"Sonuc sayisi: {payload['result_count']}")
    print("")

    for index, item in enumerate(payload["results"], start=1):
        print(f"{index}. {item['title']} [{item['category']}] score={item['score']}")
        print(f"   path: {item['path']}")
        if item["reasons"]:
            print(f"   neden: {', '.join(item['reasons'])}")
        if item["summary"]:
            print(f"   ozet: {item['summary']}")
        if item["key_points"]:
            print(f"   ana_noktalar: {' | '.join(item['key_points'])}")
        if item["related_links"]:
            print(f"   baglantilar: {', '.join(item['related_links'])}")
        if item["source_url"]:
            print(f"   kaynak: {item['source_url']}")
        print("")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
