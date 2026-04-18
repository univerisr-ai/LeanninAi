import argparse
import datetime as dt
import json
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Tuple


SPECIAL_WIKI_FILES = {"index.md", "hot.md", "log.md"}


def bootstrap_path() -> Path:
    root = Path(__file__).resolve().parents[1]
    src = root / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
    return root


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Merge fresh knowledge from another AiBeyin-compatible repo")
    parser.add_argument(
        "--source",
        required=True,
        help="Path to the source repo that contains fresher wiki/storage data",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing files",
    )
    return parser.parse_args()


def main() -> int:
    project_root = bootstrap_path()

    from aibeyin.inventory import InventoryStore
    from aibeyin.utils import read_json, read_text, write_json, write_text
    from aibeyin.wiki_writer import WikiWriter

    args = parse_args()
    source_root = Path(args.source).resolve()
    target_root = project_root.resolve()

    if not source_root.exists():
        print(json.dumps({"error": f"Source repo does not exist: {source_root}"}, ensure_ascii=True, indent=2))
        return 1

    current_inventory = read_json(target_root / "storage" / "inventory.json")
    source_inventory = read_json(source_root / "storage" / "inventory.json")

    copied, updated = sync_wiki_files(
        source_root=source_root,
        target_root=target_root,
        current_inventory=current_inventory,
        source_inventory=source_inventory,
        dry_run=args.dry_run,
    )
    merged_log = merge_log_file(source_root, target_root, dry_run=args.dry_run)
    merged_history = merge_run_history(source_root, target_root, dry_run=args.dry_run)
    report_updated = update_last_run_report(source_root, target_root, dry_run=args.dry_run)
    hot_updated = copy_special_file(source_root / "wiki" / "hot.md", target_root / "wiki" / "hot.md", dry_run=args.dry_run)
    reports_synced = sync_reports(source_root, target_root, dry_run=args.dry_run)

    merged_inventory = merge_inventories(current_inventory, source_inventory)
    if not args.dry_run:
        inventory_store = InventoryStore(target_root / "storage" / "inventory.json")
        inventory_store.payload = merged_inventory
        inventory_store.sync_repo_snapshot(target_root)
        inventory_store.save()

        writer = WikiWriter(target_root)
        writer.refresh_review_index()
        writer._refresh_wiki_index()
    else:
        inventory_store = None

    summary = {
        "source": str(source_root),
        "copied_wiki_files": copied,
        "updated_wiki_files": updated,
        "reports_synced": reports_synced,
        "log_updated": merged_log,
        "hot_updated": hot_updated,
        "run_history_merged": merged_history,
        "last_run_report_updated": report_updated,
        "concepts_after_merge": len(merged_inventory.get("concepts", {})),
        "sources_after_merge": len(merged_inventory.get("sources", {})),
        "dry_run": args.dry_run,
    }
    print(json.dumps(summary, ensure_ascii=True, indent=2))
    return 0


def sync_wiki_files(
    source_root: Path,
    target_root: Path,
    current_inventory: Dict,
    source_inventory: Dict,
    dry_run: bool,
) -> Tuple[int, int]:
    copied = 0
    updated = 0
    source_wiki = source_root / "wiki"
    target_wiki = target_root / "wiki"

    current_concepts = current_inventory.get("concepts", {})
    source_concepts = source_inventory.get("concepts", {})

    for source_path in sorted(source_wiki.rglob("*.md")):
        rel = source_path.relative_to(source_wiki)
        if rel.as_posix() in SPECIAL_WIKI_FILES or rel.as_posix() == "review/index.md":
            continue

        target_path = target_wiki / rel
        slug = source_path.stem

        if not target_path.exists():
            copied += 1
            if not dry_run:
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_path, target_path)
            continue

        if should_replace_file(slug, current_concepts, source_concepts):
            source_text = source_path.read_text(encoding="utf-8")
            target_text = target_path.read_text(encoding="utf-8")
            if source_text != target_text:
                updated += 1
                if not dry_run:
                    write_text(target_path, source_text)

    return copied, updated


def sync_reports(source_root: Path, target_root: Path, dry_run: bool) -> int:
    source_reports = source_root / "wiki" / "reports"
    if not source_reports.exists():
        return 0

    count = 0
    for source_path in sorted(source_reports.rglob("*.md")):
        rel = source_path.relative_to(source_root / "wiki")
        target_path = target_root / "wiki" / rel
        source_text = source_path.read_text(encoding="utf-8")
        target_text = target_path.read_text(encoding="utf-8") if target_path.exists() else None
        if target_text == source_text:
            continue
        count += 1
        if not dry_run:
            write_text(target_path, source_text)
    return count


def should_replace_file(slug: str, current_concepts: Dict, source_concepts: Dict) -> bool:
    source_meta = source_concepts.get(slug)
    current_meta = current_concepts.get(slug)
    if source_meta and not current_meta:
        return True
    if not source_meta:
        return False
    return parse_iso(source_meta.get("last_written_at")) > parse_iso((current_meta or {}).get("last_written_at"))


def merge_inventories(current_inventory: Dict, source_inventory: Dict) -> Dict:
    merged = {
        "version": max(int(current_inventory.get("version", 1)), int(source_inventory.get("version", 1))),
        "updated_at": max(
            current_inventory.get("updated_at", ""),
            source_inventory.get("updated_at", ""),
        ),
        "repo_snapshot": current_inventory.get("repo_snapshot", {"raw": {}, "wiki": {}}),
        "sources": merge_records_by_timestamp(
            current_inventory.get("sources", {}),
            source_inventory.get("sources", {}),
            "last_seen_at",
        ),
        "concepts": merge_records_by_timestamp(
            current_inventory.get("concepts", {}),
            source_inventory.get("concepts", {}),
            "last_written_at",
        ),
    }
    return merged


def merge_records_by_timestamp(current_records: Dict, source_records: Dict, timestamp_key: str) -> Dict:
    merged = dict(current_records)
    for key, source_value in source_records.items():
        current_value = merged.get(key)
        if current_value is None:
            merged[key] = source_value
            continue

        if parse_iso(source_value.get(timestamp_key)) >= parse_iso(current_value.get(timestamp_key)):
            new_record = dict(current_value)
            new_record.update(source_value)
            merged[key] = new_record
    return merged


def merge_log_file(source_root: Path, target_root: Path, dry_run: bool) -> bool:
    source_path = source_root / "wiki" / "log.md"
    target_path = target_root / "wiki" / "log.md"
    if not source_path.exists():
        return False

    source_lines = source_path.read_text(encoding="utf-8").splitlines()
    target_lines = target_path.read_text(encoding="utf-8").splitlines() if target_path.exists() else []

    existing = set(target_lines)
    merged_lines = list(target_lines)
    changed = False

    for line in source_lines:
        if line not in existing:
            merged_lines.append(line)
            existing.add(line)
            changed = True

    if changed and not dry_run:
        write_text(target_path, "\n".join(merged_lines).rstrip() + "\n")
    return changed


def merge_run_history(source_root: Path, target_root: Path, dry_run: bool) -> bool:
    source_path = source_root / "storage" / "run_history.jsonl"
    target_path = target_root / "storage" / "run_history.jsonl"
    if not source_path.exists():
        return False

    entries = {}
    for path in [target_path, source_path]:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            obj = json.loads(stripped)
            key = obj.get("started_at") or stripped
            entries[key] = obj

    ordered = [entries[key] for key in sorted(entries.keys())]
    serialized = "\n".join(json.dumps(item, ensure_ascii=True) for item in ordered).rstrip() + "\n"
    current = target_path.read_text(encoding="utf-8") if target_path.exists() else ""
    changed = current != serialized
    if changed and not dry_run:
        write_text(target_path, serialized)
    return changed


def update_last_run_report(source_root: Path, target_root: Path, dry_run: bool) -> bool:
    source_path = source_root / "storage" / "last_run_report.json"
    target_path = target_root / "storage" / "last_run_report.json"
    if not source_path.exists():
        return False

    source_report = read_json_safe(source_path)
    target_report = read_json_safe(target_path)
    use_source = parse_iso(source_report.get("started_at")) >= parse_iso(target_report.get("started_at"))
    if not use_source:
        return False

    changed = source_report != target_report
    if changed and not dry_run:
        write_json(target_path, source_report)
    return changed


def copy_special_file(source_path: Path, target_path: Path, dry_run: bool) -> bool:
    if not source_path.exists():
        return False
    source_text = source_path.read_text(encoding="utf-8")
    target_text = target_path.read_text(encoding="utf-8") if target_path.exists() else ""
    changed = source_text != target_text
    if changed and not dry_run:
        write_text(target_path, source_text)
    return changed


def parse_iso(value: str):
    if not value:
        return dt.datetime.min.replace(tzinfo=dt.timezone.utc)
    try:
        return dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return dt.datetime.min.replace(tzinfo=dt.timezone.utc)


def read_json_safe(path: Path) -> Dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, payload: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
