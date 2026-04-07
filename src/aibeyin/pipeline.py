import datetime as dt
import json
from pathlib import Path
from typing import Dict, List
from zoneinfo import ZoneInfo

from .brain_enhancer import BrainEnhancer
from .config import load_pipeline_config
from .dedup import detect_concept_title_duplicate, detect_wiki_duplicate
from .inventory import InventoryStore
from .models import ConceptDraft, PipelineStats, SourceItem
from .openrouter import OpenRouterClient
from .reporting import append_run_history, maybe_generate_weekly_digest
from .sources import collect_sources
from .storage_guard import enforce_disk_quota
from .utils import now_utc_iso, read_text, safe_slug, sha256_text, write_json
from .wiki_writer import WikiWriter


def run_pipeline(project_root: Path, config_path: Path, dry_run: bool = False) -> Dict:
    config = load_pipeline_config(config_path)
    enforce_disk_quota(project_root, config.disk_limit_gb)
    started_at = now_utc_iso()

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

    existing_concept_slugs = list(inventory.payload.get("concepts", {}).keys())
    existing_concept_titles = [
        rec.get("title", slug.replace("-", " "))
        for slug, rec in inventory.payload.get("concepts", {}).items()
    ]

    title_dedup_threshold = float(config.quality.get("max_title_similarity", 0.75))
    max_similarity = float(config.quality.get("max_semantic_similarity", 0.86))

    collected = collect_sources(config.sources)
    stats.collected = len(collected)

    for item in collected:
        try:
            if inventory.source_unchanged(item.url, item.content_hash):
                stats.skipped_unchanged += 1
                inventory.upsert_source(item.url, item.content_hash, status="skipped_unchanged")
                continue

            title_dup, matched_title = detect_concept_title_duplicate(
                candidate_title=item.title,
                existing_concept_slugs=existing_concept_slugs,
                existing_concept_titles=existing_concept_titles,
                max_title_similarity=title_dedup_threshold,
            )
            if title_dup:
                stats.skipped_duplicate += 1
                inventory.upsert_source(item.url, item.content_hash, status="skipped_title_duplicate")
                continue

            duplicate, matched_file, similarity = detect_wiki_duplicate(
                wiki_root=project_root / "wiki",
                candidate_text=item.content,
                max_similarity=max_similarity,
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
                inventory.upsert_concept(draft.slug, sha256_text(draft.summary), item.url, draft.title)
                existing_concept_slugs.append(draft.slug)
                existing_concept_titles.append(draft.title)
                stats.drafted += 1
            drafted_items.append(draft)
            inventory.upsert_source(item.url, item.content_hash, status="processed")
        except Exception:
            stats.errors += 1
            inventory.upsert_source(item.url, item.content_hash, status="error")

    if not dry_run:
        writer.refresh_hot_cache(drafted_items)

    inventory.save()

    enhancement_result: Dict = {}
    if _is_sunday(config.data.get("timezone", "Europe/Istanbul")):
        enhancement_cfg = config.data.get("brain_enhancement", {})
        if enhancement_cfg.get("enabled", True):
            enhancer = BrainEnhancer(
                openrouter_config=config.openrouter,
                enhancement_config=enhancement_cfg,
            )
            enh = enhancer.run(wiki_root=project_root / "wiki", dry_run=dry_run)
            enhancement_result = enh.as_dict()

    report = {
        "status": "ok" if stats.errors == 0 else "partial",
        "started_at": started_at,
        "dry_run": dry_run,
        "snapshot_delta": {
            "raw_changed": snapshot_delta.raw_changed,
            "wiki_changed": snapshot_delta.wiki_changed,
        },
        "stats": stats.as_dict(),
        "enhancement": enhancement_result,
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

    if not dry_run:
        append_run_history(storage_root=storage_root, report=report)
    weekly_digest = maybe_generate_weekly_digest(
        project_root=project_root,
        config_data=config.data,
        dry_run=dry_run,
    )
    report["weekly_digest"] = weekly_digest

    write_json(run_report_path, report)
    return report


def _is_sunday(timezone_name: str) -> bool:
    try:
        now_local = dt.datetime.now(ZoneInfo(timezone_name))
        return now_local.weekday() == 6
    except Exception:
        return dt.datetime.now(dt.timezone.utc).weekday() == 6


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


# Inline import to avoid circular dependency at module level
from .wiki_writer import WikiWriter  # noqa: E402
