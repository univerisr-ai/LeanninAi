from pathlib import Path
import re
from typing import List

from .models import ConceptDraft, SourceItem
from .utils import now_utc_iso, read_text, write_text


class WikiWriter:
    LINK_ALIASES = {
        "Web Performansı ve PWA": "Web-Performansi-PWA",
        "Web Performansı ve PWA (Service Worker)": "Web-Performansi-PWA",
        "State Yönetimi: Zustand ve TanStack Query": "State-Yonetimi-Zustand-TanStack",
        "JWT ve Kimlik Doğrulama": "JWT-ve-Kimlik-Dogrulama",
        "Rate Limiting ve Token Bucket Algoritması": "Rate-Limiting-Token-Bucket",
        "CORS ve Güvenlik Headerları": "CORS-ve-Guvenlik-Headerlari",
        "Clean Architecture (Katmanlı Mimari)": "Clean-Architecture",
        "Modern React Desenleri": "Modern-React-Desenleri",
        "Veritabanı ve Caching Stratejileri": "Veritabani-ve-Caching-Stratejileri",
        "Renk Teorisi ve Tipografi": "Renk-Teorisi-ve-Tipografi",
        "Tasarım Psikolojisi ve Gestalt-Hick": "Tasarim-Psikolojisi-Gestalt-Hick",
        "Tasarım Psikolojisi: Gestalt ve Hick": "Tasarim-Psikolojisi-Gestalt-Hick",
        "Erişilebilirlik WCAG ve ARIA": "Erisilebilirlik-WCAG-ve-ARIA",
        "Erişilebilirlik: WCAG ve ARIA": "Erisilebilirlik-WCAG-ve-ARIA",
        "Klavye Navigasyon ve Focus": "Klavye-Navigasyon-Focus",
        "XSS ve CSRF Açıkları": "XSS-ve-CSRF-Açiklari",
        "Bot Tespiti ve Honeypot": "Bot-Tespiti-ve-Honeypot",
        "Bot Tespiti ve Honeypot (Bal Küpü)": "Bot-Tespiti-ve-Honeypot",
        "API Response Yapıları: Flat vs. Nested": "review/api-response-yapilari-flat-vs-nested-duzlestirilmis-vs-ic-ice",
        "Geliştirici Deneyimi ve Araç Seçimi Psikolojisi": "review/gelistirici-deneyimi-ve-arac-secimi-psikolojisi",
        "Günlük Kullandığım TypeScript İpuçları ve Püf Noktaları": "review/gunluk-kullandigim-typescript-ipuclari-ve-puf-noktalari",
        "TypeScript Hata Gruplama ve AI Bağlam Optimizasyonu (ContextZip)": "review/typescript-hata-gruplama-ve-ai-baglam-optimizasyonu-contextzip",
        "Yerel LLM Entegrasyonu: React Hooks ile Yapay Zeka Uygulamaları": "review/yerel-llm-entegrasyonu-react-hooks-ile-yapay-zeka-uygulamalari",
    }

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
        self.refresh_review_index()
        self.append_log_entry(draft, source)
        return draft_path

    def auto_publish_reviews(self, publish_config: dict) -> dict:
        """Yuksek kaliteli review draft'larini ana wiki'ye promote et."""
        if not publish_config.get("enabled", False):
            return {"published": 0, "purged": 0}

        min_confidence = int(publish_config.get("min_confidence", 85))
        min_novelty = int(publish_config.get("min_novelty", 70))
        min_words = int(publish_config.get("min_word_count", 80))
        do_purge = bool(publish_config.get("purge_low_quality", False))
        purge_max_conf = int(publish_config.get("purge_max_confidence", 50))

        published = 0
        purged = 0

        skip_names = {"index.md", ".gitkeep"}
        review_files = [
            p for p in sorted(self.review_root.glob("*.md"))
            if p.name.lower() not in skip_names
        ]

        for path in review_files:
            try:
                text = read_text(path)
                meta = self._parse_review_meta(text)
                confidence = meta.get("confidence", 0)
                novelty = meta.get("novelty", 0)
                word_count = len(text.split())
                is_fallback = "fallback:" in meta.get("model", "")

                # Publish: yuksek kaliteli ve yeterli uzunlukta
                if (confidence >= min_confidence and
                        novelty >= min_novelty and
                        word_count >= min_words and
                        not is_fallback):
                    dest = self.wiki_root / path.name
                    if not dest.exists():
                        # Status'u guncelle
                        text = text.replace("- status: draft-review", "- status: published")
                        write_text(dest, text)
                        path.unlink(missing_ok=True)
                        published += 1

                # Purge: cok dusuk kaliteli veya fallback
                elif do_purge and (confidence <= purge_max_conf or is_fallback):
                    path.unlink(missing_ok=True)
                    purged += 1

            except Exception:
                continue

        if published > 0:
            self._refresh_wiki_index()
            self.refresh_review_index()
            log_line = (
                f"- **{now_utc_iso()}**: Auto-publish: {published} draft wiki'ye tasinip publish edildi, "
                f"{purged} dusuk kaliteli draft temizlendi.\n"
            )
            existing = read_text(self.log_path) if self.log_path.exists() else "# Islem Gecmisi\n\n"
            write_text(self.log_path, existing.rstrip() + "\n" + log_line)

        return {"published": published, "purged": purged}

    def _parse_review_meta(self, text: str) -> dict:
        """Review dosyasindan meta bilgileri cikar."""
        meta = {}
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("- confidence:"):
                try:
                    meta["confidence"] = int(line.split(":", 1)[1].strip())
                except ValueError:
                    pass
            elif line.startswith("- novelty:"):
                try:
                    meta["novelty"] = int(line.split(":", 1)[1].strip())
                except ValueError:
                    pass
            elif line.startswith("- model:"):
                meta["model"] = line.split(":", 1)[1].strip()
            elif line.startswith("- category:"):
                meta["category"] = line.split(":", 1)[1].strip()
            elif line.startswith("# "):
                if "title" not in meta:
                    meta["title"] = line[2:].strip()
        return meta

    def _refresh_wiki_index(self) -> None:
        """Ana wiki index.md dosyasini mevcut tum wiki sayfalarindan yeniden olustur."""
        index_path = self.wiki_root / "index.md"
        skip = {"index.md", "log.md", "hot.md", "system-memory.md"}

        categories: dict = {
            "frontend": [], "backend": [], "security": [],
            "ui-ux": [], "a11y": [], "other": [],
        }
        cat_labels = {
            "frontend": "🏗️ Frontend",
            "backend": "🔧 Backend",
            "security": "🛡️ Security",
            "ui-ux": "🎨 UI/UX",
            "a11y": "♿ Erişilebilirlik",
            "other": "📦 Diğer",
        }

        for path in sorted(self.wiki_root.glob("*.md")):
            if path.name.lower() in skip:
                continue
            try:
                text = read_text(path)
                cat = "other"
                for line in text.splitlines():
                    if line.strip().startswith("- category:"):
                        cat = line.split(":", 1)[1].strip().lower()
                        break
                if cat not in categories:
                    cat = "other"
                title = path.stem.replace("-", " ").title()
                for line in text.splitlines():
                    if line.startswith("# "):
                        title = line[2:].strip()
                        break
                categories[cat].append((path.stem, title))
            except Exception:
                categories["other"].append((path.stem, path.stem))

        lines = [
            "# 🧠 AiBeyin Wiki — Ana Indeks",
            "",
            "Bu sayfa, bilgi tabanindaki tum konseptleri kategorilere gore siralar.",
            "",
            f"Son guncelleme: {now_utc_iso()}",
            "",
            "* Islem gecmisi: [[log]]",
            "* Son bilgi ozeti: [[hot]]",
            "",
        ]

        for cat_key, label in cat_labels.items():
            items = categories.get(cat_key, [])
            if not items:
                continue
            lines.append(f"## {label}")
            lines.append("")
            for slug, title in items:
                lines.append(f"- [[{slug}|{title}]]")
            lines.append("")

        write_text(index_path, "\n".join(lines) + "\n")

    def refresh_review_index(self) -> None:
        self.review_root.mkdir(parents=True, exist_ok=True)
        index_path = self.review_root / "index.md"

        # Dosyaları kategoriye göre grupla
        categories: dict = {
            "frontend": [],
            "backend": [],
            "security": [],
            "ui-ux": [],
            "a11y": [],
            "other": [],
        }
        category_labels = {
            "frontend": "🏗️ Frontend",
            "backend": "🔧 Backend",
            "security": "🛡️ Security",
            "ui-ux": "🎨 UI/UX",
            "a11y": "♿ Erişilebilirlik",
            "other": "📦 Diğer",
        }

        review_files = [
            path
            for path in sorted(self.review_root.glob("*.md"))
            if path.name.lower() != "index.md"
        ]

        for path in review_files:
            slug = path.stem
            # Dosyadan kategoriyi oku
            try:
                text = read_text(path)
                cat = "other"
                for line in text.splitlines():
                    if line.strip().startswith("- category:"):
                        cat = line.split(":", 1)[1].strip().lower()
                        break
                if cat not in categories:
                    cat = "other"
                categories[cat].append(slug)
            except Exception:
                categories["other"].append(slug)

        lines = [
            "# Review Index",
            "",
            "Bu sayfa tüm review notlarını kategorilere ayrılmış şekilde bağlar.",
            "",
        ]

        for cat_key, cat_label in category_labels.items():
            slugs = categories.get(cat_key, [])
            if not slugs:
                continue
            lines.append(f"## {cat_label}")
            lines.append("")
            for slug in slugs:
                lines.append(f"- [[review/{slug}]]")
            lines.append("")

        write_text(index_path, "\n".join(lines) + "\n")

    def repair_existing_review_links(self) -> dict:
        self.review_root.mkdir(parents=True, exist_ok=True)
        changed_files = 0
        total_replacements = 0

        for path in sorted(self.review_root.glob("*.md")):
            if path.name.lower() == "index.md":
                continue

            content = read_text(path)
            original = content

            for alias, canonical in self.LINK_ALIASES.items():
                old_token = f"[[{alias}]]"
                new_token = f"[[{canonical}]]"
                if old_token in content:
                    count = content.count(old_token)
                    content = content.replace(old_token, new_token)
                    total_replacements += count

            if "## Iliskili Sayfalar" in content and "[[index]]" not in content:
                content = content.replace("## Iliskili Sayfalar", "## Iliskili Sayfalar\n- [[index]]", 1)

            if content != original:
                write_text(path, content)
                changed_files += 1

        return {
            "changed_files": changed_files,
            "link_replacements": total_replacements,
        }

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
            sections.append(f"→ [[review/{draft.slug}]]")
            sections.append("")
            sections.append(draft.summary)
            if draft.key_points:
                for point in draft.key_points[:3]:
                    sections.append(f"- {point}")
            sections.append("")

        content = "\n".join(sections)
        words = content.split()
        if len(words) > 600:
            content = " ".join(words[:600])
        write_text(self.hot_path, content + "\n")

    def _render_draft_markdown(self, draft: ConceptDraft, source: SourceItem) -> str:
        related_links = self._prepare_related_links(draft)
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
        for link in related_links:
            lines.append(f"- {link}")
        lines.extend(["", "## Kaynak Basligi", source.title, ""])
        return "\n".join(lines)

    def _prepare_related_links(self, draft: ConceptDraft) -> List[str]:
        links: List[str] = []

        for raw in draft.links_to_existing or []:
            token = raw.strip()
            if token.startswith("[[") and token.endswith("]]"):
                links.append(token)

        # Always keep review notes attached to the main graph hubs.
        links.append("[[index]]")
        links.append("[[review/index]]")
        links.extend(self._category_hubs(draft.category))

        # Deduplicate while preserving order.
        deduped: List[str] = []
        seen = set()
        for link in links:
            key = link.lower()
            if key in seen:
                continue
            seen.add(key)
            deduped.append(link)
        return deduped

    @staticmethod
    def _category_hubs(category: str) -> List[str]:
        hub_map = {
            "frontend": ["[[Modern-React-Desenleri]]", "[[Web-Performansi-PWA]]"],
            "backend": ["[[Clean-Architecture]]", "[[Veritabani-ve-Caching-Stratejileri]]"],
            "security": ["[[XSS-ve-CSRF-Açiklari]]", "[[CORS-ve-Guvenlik-Headerlari]]"],
            "ui-ux": ["[[Tasarim-Psikolojisi-Gestalt-Hick]]", "[[Renk-Teorisi-ve-Tipografi]]"],
            "a11y": ["[[Erisilebilirlik-WCAG-ve-ARIA]]", "[[Klavye-Navigasyon-Focus]]"],
        }
        return hub_map.get((category or "").strip().lower(), ["[[Modern-React-Desenleri]]"])
