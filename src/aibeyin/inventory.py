from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

from .utils import iter_markdown_files, now_utc_iso, read_json, read_text, sha256_text, write_json


@dataclass
class SnapshotDelta:
    raw_changed: int
    wiki_changed: int


class InventoryStore:
    def __init__(self, inventory_path: Path) -> None:
        self.path = inventory_path
        self.payload = read_json(inventory_path) or {
            "version": 1,
            "updated_at": now_utc_iso(),
            "repo_snapshot": {"raw": {}, "wiki": {}},
            "sources": {},
            "concepts": {},
        }

    def save(self) -> None:
        self.payload["updated_at"] = now_utc_iso()
        write_json(self.path, self.payload)

    def source_unchanged(self, url: str, content_hash: str) -> bool:
        record = self.payload.get("sources", {}).get(url)
        if not record:
            return False
        return record.get("content_hash") == content_hash

    def upsert_source(self, url: str, content_hash: str, status: str) -> None:
        sources = self.payload.setdefault("sources", {})
        current = sources.get(url, {})
        current.update(
            {
                "content_hash": content_hash,
                "last_seen_at": now_utc_iso(),
                "last_status": status,
            }
        )
        if status == "processed":
            current["last_processed_at"] = now_utc_iso()
        sources[url] = current

    def upsert_concept(self, slug: str, content_hash: str, source_url: str) -> None:
        concepts = self.payload.setdefault("concepts", {})
        concepts[slug] = {
            "content_hash": content_hash,
            "source_url": source_url,
            "last_written_at": now_utc_iso(),
        }

    def sync_repo_snapshot(self, repo_root: Path) -> SnapshotDelta:
        raw_dir = repo_root / "raw"
        wiki_dir = repo_root / "wiki"
        old_raw = self.payload.setdefault("repo_snapshot", {}).setdefault("raw", {})
        old_wiki = self.payload.setdefault("repo_snapshot", {}).setdefault("wiki", {})

        new_raw = self._snapshot_dir(raw_dir, repo_root)
        new_wiki = self._snapshot_dir(wiki_dir, repo_root)

        raw_changed = self._count_changed(old_raw, new_raw)
        wiki_changed = self._count_changed(old_wiki, new_wiki)

        self.payload["repo_snapshot"]["raw"] = new_raw
        self.payload["repo_snapshot"]["wiki"] = new_wiki
        return SnapshotDelta(raw_changed=raw_changed, wiki_changed=wiki_changed)

    def _snapshot_dir(self, directory: Path, repo_root: Path) -> Dict[str, Dict[str, str]]:
        snapshot: Dict[str, Dict[str, str]] = {}
        for path in iter_markdown_files(directory):
            text = read_text(path)
            rel = str(path.relative_to(repo_root)).replace("\\", "/")
            snapshot[rel] = {
                "sha256": sha256_text(text),
                "size": str(len(text.encode("utf-8"))),
            }
        return snapshot

    @staticmethod
    def _count_changed(old_state: Dict[str, Dict[str, str]], new_state: Dict[str, Dict[str, str]]) -> int:
        changed = 0
        all_keys = set(old_state.keys()) | set(new_state.keys())
        for key in all_keys:
            if old_state.get(key, {}).get("sha256") != new_state.get(key, {}).get("sha256"):
                changed += 1
        return changed
