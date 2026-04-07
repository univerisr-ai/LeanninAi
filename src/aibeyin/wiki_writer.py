from pathlib import Path
from typing import List

from .models import ConceptDraft, SourceItem
from .utils import now_utc_iso, read_text, write_text


class WikiWriter:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.wiki_root = repo_root / "wiki"
        self.review_root = self.wiki_root / "review"
        self.log_path = self.wiki_root / "log.md"
        self.hot_path = self.wiki_root / "hot.md"

    def write_draft(self, draft: ConceptDraft, source: SourceItem) -> Path:
        self.review_root.mkdir(parents=True, exist_ok=True)
        draft_path = self.review_root / f"{draft.slug}.md"

        content = self._render_draft_markdown(draft, source)
        write_text(draft_path, content)
        self.append_log_entry(draft, source)
        return draft_path

    def append_log_entry(self, draft: ConceptDraft, source: SourceItem) -> None:
        line = (
            f"- **{now_utc_iso()}**: Draft olusturuldu -> review/{draft.slug}.md "
            f"| model={draft.model_used} | confidence={draft.confidence} "
            f"| novelty={draft.novelty} | source={source.url}\n"
        )
        existing = read_text(self.log_path) if self.log_path.exists() else "# Islem Gecmisi\n\n"
        write_text(self.log_path, existing.rstrip() + "\n" + line)

    def refresh_hot_cache(self, latest_drafts: List[ConceptDraft]) -> None:
        if not latest_drafts:
            return

        sections = [
            "# Sicak Bellek (Hot Cache)",
            "",
            "Bu bolum en son uretilen draft bilgisinin hizli ozetidir.",
            "",
        ]
        for draft in latest_drafts[:5]:
            sections.append(f"## {draft.title}")
            sections.append(draft.summary)
            if draft.key_points:
                for point in draft.key_points[:3]:
                    sections.append(f"- {point}")
            sections.append("")

        content = "\n".join(sections)
        words = content.split()
        if len(words) > 520:
            content = " ".join(words[:520])
        write_text(self.hot_path, content + "\n")

    @staticmethod
    def _render_draft_markdown(draft: ConceptDraft, source: SourceItem) -> str:
        lines = [
            f"# {draft.title}",
            "",
            "## Meta",
            f"- status: draft-review",
            f"- category: {draft.category}",
            f"- confidence: {draft.confidence}",
            f"- novelty: {draft.novelty}",
            f"- model: {draft.model_used}",
            f"- source: {source.url}",
            f"- source_name: {source.source_name}",
            f"- generated_at: {now_utc_iso()}",
            "",
            "## Ozet",
            draft.summary,
            "",
            "## Ana Noktalar",
        ]
        for point in draft.key_points or ["No key points generated."]:
            lines.append(f"- {point}")

        lines.extend(["", "## Iliskili Sayfalar"]) 
        for link in draft.links_to_existing or ["-"]:
            lines.append(f"- {link}")
        lines.extend(["", "## Kaynak Basligi", source.title, ""])
        return "\n".join(lines)
