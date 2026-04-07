import datetime as dt
import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List
from zoneinfo import ZoneInfo

from .utils import now_utc_iso


def append_run_history(storage_root: Path, report: Dict) -> Path:
    history_path = storage_root / "run_history.jsonl"
    history_path.parent.mkdir(parents=True, exist_ok=True)
    with history_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(report, ensure_ascii=True) + "\n")
    return history_path


def maybe_generate_weekly_digest(project_root: Path, config_data: Dict, dry_run: bool) -> Dict:
    weekly_cfg = config_data.get("weekly_digest", {})
    enabled = bool(weekly_cfg.get("enabled", True))
    if not enabled:
        return {"generated": False, "reason": "disabled"}

    if dry_run:
        return {"generated": False, "reason": "dry_run"}

    timezone_name = str(config_data.get("timezone", "Europe/Istanbul"))
    lookback_days = int(weekly_cfg.get("lookback_days", 7))
    run_day_of_week = int(weekly_cfg.get("run_day_of_week", 6))

    now_local = dt.datetime.now(ZoneInfo(timezone_name))
    if now_local.weekday() != run_day_of_week:
        return {
            "generated": False,
            "reason": "not_scheduled_day",
            "run_day_of_week": run_day_of_week,
            "today_weekday": now_local.weekday(),
        }

    history_path = project_root / "storage" / "run_history.jsonl"
    if not history_path.exists():
        return {"generated": False, "reason": "history_missing"}

    runs = _load_recent_runs(history_path, lookback_days)
    if not runs:
        return {"generated": False, "reason": "no_recent_runs"}

    report_dir = project_root / "wiki" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    iso = now_local.isocalendar()
    report_name = f"weekly-{iso.year}-w{iso.week:02d}.md"
    report_path = report_dir / report_name

    markdown = _build_weekly_markdown(runs=runs, now_local=now_local, lookback_days=lookback_days)
    report_path.write_text(markdown, encoding="utf-8")
    _upsert_reports_index(report_dir=report_dir, report_name=report_name, now_local=now_local)

    return {
        "generated": True,
        "path": str(report_path.relative_to(project_root)).replace("\\", "/"),
        "included_runs": len(runs),
        "lookback_days": lookback_days,
    }


def _load_recent_runs(history_path: Path, lookback_days: int) -> List[Dict]:
    threshold = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=lookback_days)
    runs: List[Dict] = []
    for line in history_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
            started_at = _parse_iso_utc(str(payload.get("started_at", "")))
            if started_at >= threshold:
                runs.append(payload)
        except Exception:
            continue
    return runs


def _build_weekly_markdown(runs: List[Dict], now_local: dt.datetime, lookback_days: int) -> str:
    totals = defaultdict(int)
    status_count = defaultdict(int)
    for run in runs:
        status_count[str(run.get("status", "unknown"))] += 1
        stats = run.get("stats", {})
        for key in [
            "collected",
            "skipped_unchanged",
            "skipped_duplicate",
            "rejected_quality",
            "drafted",
            "errors",
        ]:
            totals[key] += int(stats.get(key, 0))

    lines = [
        f"# Haftalik AI Ozeti - {now_local.strftime('%Y-%m-%d')}",
        "",
        f"- generated_at: {now_utc_iso()}",
        f"- lookback_days: {lookback_days}",
        f"- included_runs: {len(runs)}",
        "",
        "## Toplamlar",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| collected | {totals['collected']} |",
        f"| skipped_unchanged | {totals['skipped_unchanged']} |",
        f"| skipped_duplicate | {totals['skipped_duplicate']} |",
        f"| rejected_quality | {totals['rejected_quality']} |",
        f"| drafted | {totals['drafted']} |",
        f"| errors | {totals['errors']} |",
        "",
        "## Run Durumlari",
        "",
    ]

    for status, count in sorted(status_count.items()):
        lines.append(f"- {status}: {count}")

    lines.extend([
        "",
        "## Son Calisma Ozeti",
        "",
    ])

    for run in sorted(runs, key=lambda r: str(r.get("started_at", "")), reverse=True)[:7]:
        started_at = str(run.get("started_at", ""))
        status = str(run.get("status", "unknown"))
        stats = run.get("stats", {})
        drafted = int(stats.get("drafted", 0))
        skipped = int(stats.get("skipped_unchanged", 0))
        lines.append(f"- {started_at} | status={status} | drafted={drafted} | skipped_unchanged={skipped}")

    lines.extend(
        [
            "",
            "## Not",
            "",
            "Bu dosya gunluk pipeline tarafindan otomatik uretilmistir.",
        ]
    )

    return "\n".join(lines) + "\n"


def _upsert_reports_index(report_dir: Path, report_name: str, now_local: dt.datetime) -> None:
    index_path = report_dir / "index.md"
    entry = f"- [{report_name}](./{report_name}) - generated {now_local.strftime('%Y-%m-%d')}"
    if index_path.exists():
        content = index_path.read_text(encoding="utf-8")
    else:
        content = "# Haftalik Raporlar\n\n"

    if entry not in content:
        content = content.rstrip() + "\n" + entry + "\n"
    index_path.write_text(content, encoding="utf-8")


def _parse_iso_utc(value: str) -> dt.datetime:
    normalized = value.replace("Z", "+00:00")
    parsed = dt.datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)
