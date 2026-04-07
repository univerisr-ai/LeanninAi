import json
from pathlib import Path
from typing import Dict, List

from .config import load_pipeline_config
from .dedup import detect_wiki_duplicate
from .inventory import InventoryStore
from .models import ConceptDraft, PipelineStats, SourceItem
from .openrouter import OpenRouterClient
from .sources import collect_sources
from .storage_guard import enforce_disk_quota
from .utils import now_utc_iso, read_text, safe_slug, sha256_text, write_json
from .wiki_writer import WikiWriter


def run_pipeline(project_root: Path, config_path: Path, dry_run: bool = False) -> Dict:
    config = load_pipeline_config(config_path)
    enforce_disk_quota(project_root, config.disk_limit_gb)

    storage_root = project_root / "storage"
    inventory_path = storage_root / "inventory.json"
    run_report_path = storage_root / "last_run_report.json"
    storage_root.mkdir(parents=True, exist_ok=True)

    inventory = InventoryStore(inventory_path)
    snapshot_delta = inventory.sync_repo_snapshot(project_root)
    writer = WikiWriter(project_root)
    llm = OpenRouterClient(config.openrouter)

    stats = PipelineStats()
    drafted_items: List[ConceptDraft] = []
    existing_titles = _collect_existing_titles(project_root / "wiki")

    collected = collect_sources(config.sources)
    stats.collected = len(collected)

    for item in collected:
        try:
            if inventory.source_unchanged(item.url, item.content_hash):
                stats.skipped_unchanged += 1
                inventory.upsert_source(item.url, item.content_hash, status="skipped_unchanged")
                continue

            duplicate, matched_file, similarity = detect_wiki_duplicate(
                wiki_root=project_root / "wiki",
                candidate_text=item.content,
                max_similarity=float(config.quality.get("max_semantic_similarity", 0.86)),
            )
            if duplicate:
                stats.skipped_duplicate += 1
                inventory.upsert_source(item.url, item.content_hash, status="skipped_duplicate")
                continue

            draft = llm.create_draft(item, existing_titles=existing_titles, dry_run=dry_run)
            if not _passes_quality(draft, config):
                stats.rejected_quality += 1
                inventory.upsert_source(item.url, item.content_hash, status="rejected_quality")
                continue

            if not dry_run:
                writer.write_draft(draft, item)
                inventory.upsert_concept(draft.slug, sha256_text(draft.summary), item.url)
                stats.drafted += 1
            drafted_items.append(draft)
            inventory.upsert_source(item.url, item.content_hash, status="processed")
        except Exception:
            stats.errors += 1
            inventory.upsert_source(item.url, item.content_hash, status="error")

    if not dry_run:
        writer.refresh_hot_cache(drafted_items)

    inventory.save()

    report = {
        "status": "ok" if stats.errors == 0 else "partial",
        "started_at": now_utc_iso(),
        "dry_run": dry_run,
        "snapshot_delta": {
            "raw_changed": snapshot_delta.raw_changed,
            "wiki_changed": snapshot_delta.wiki_changed,
        },
        "stats": stats.as_dict(),
        "drafts_preview": [
            {
                "slug": d.slug,
                "title": d.title,
                "category": d.category,
                "confidence": d.confidence,
                "novelty": d.novelty,
            }
            for d in drafted_items[:10]
        ],
    }
    write_json(run_report_path, report)
    return report


def _collect_existing_titles(wiki_root: Path) -> List[str]:
    titles: List[str] = []
    if not wiki_root.exists():
        return titles
    for path in wiki_root.rglob("*.md"):
        name = path.name.lower()
        if name in {"index.md", "log.md", "hot.md"}:
            continue
        try:
            first_line = read_text(path).splitlines()[0].strip()
        except Exception:
            continue
        if first_line.startswith("# "):
            titles.append(first_line[2:].strip())
        else:
            titles.append(safe_slug(path.stem))
    return titles


def _passes_quality(draft: ConceptDraft, config) -> bool:
    quality = config.quality
    min_conf = int(quality.get("min_confidence", 70))
    min_novelty = int(quality.get("min_novelty", 60))
    allowed = set(quality.get("allowed_categories", []))
    if draft.confidence < min_conf:
        return False
    if draft.novelty < min_novelty:
        return False
    if allowed and draft.category not in allowed:
        return False
    if not draft.summary.strip():
        return False
    return True
