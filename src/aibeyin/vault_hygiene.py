"""
vault_hygiene.py — Otomatik Vault Bakım Modülü

Her pipeline çalışmasında otomatik olarak:
1. Konu dışı review'ları tespit edip siler
2. Kırık wikilink'leri tespit edip loglar
3. Review ↔ Core wiki arasında çift yönlü bağlantı kurar
4. Duplike review dosyalarını tespit eder
5. Temizlik istatistiklerini döndürür
"""
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Tuple

from .utils import iter_markdown_files, jaccard_similarity, read_text, write_text


# ── Konu dışı içerik tespiti için anahtar kelimeler ──────────────────────
OFF_TOPIC_KEYWORDS: List[str] = [
    # Blockchain / Web3
    "solidity", "ethereum", "blockchain", "smart contract", "web3",
    "zcash", "eip-152", "chainlink", "twap", "oracle manipulation",
    "defi", "nft", "token swap",
    # Mobile native (Flutter, Swift, Kotlin)
    "flutter", "dart ", "swiftui", "kotlin ", "android native",
    "ios native", "jetpack compose",
    # .NET / C#
    ".net ", "c# ", "csharp", "blazor", "maui", "wpf", "asp.net",
    # Go / Rust (sistem dili, web backend değil)
    "golang", "go error handling", "cargo ",
    # Oyun geliştirme
    "unity ", "unreal engine", "gamedev", "game dev",
    # ML/AI modelleme (web AI entegrasyonu hariç)
    "tensorflow", "pytorch", "model training", "fine-tuning llm",
    # DevOps sertifika / kariyer
    "cks exam", "kubestronaut", "certification exam",
    # Tamamen konu dışı
    "baseball", "sports analytics", "pajamas", "date night",
    "telemedicine", "clinic", "medical",
]


@dataclass
class HygieneResult:
    off_topic_deleted: int = 0
    broken_links_found: int = 0
    bidirectional_links_added: int = 0
    near_duplicates_found: int = 0
    deleted_files: List[str] = field(default_factory=list)
    broken_link_details: List[str] = field(default_factory=list)
    duplicate_pairs: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict:
        return {
            "off_topic_deleted": self.off_topic_deleted,
            "broken_links_found": self.broken_links_found,
            "bidirectional_links_added": self.bidirectional_links_added,
            "near_duplicates_found": self.near_duplicates_found,
            "deleted_files": self.deleted_files[:20],
            "broken_link_details": self.broken_link_details[:20],
            "duplicate_pairs": self.duplicate_pairs[:10],
        }


def run_hygiene(project_root: Path, dry_run: bool = False) -> HygieneResult:
    """Pipeline sonunda çağrılan ana bakım fonksiyonu."""
    result = HygieneResult()
    wiki_root = project_root / "wiki"
    review_root = wiki_root / "review"

    if not review_root.exists():
        return result

    # 1. Konu dışı review'ları tespit et ve sil
    _clean_off_topic_reviews(review_root, result, dry_run)

    # 2. Kırık wikilink'leri tara
    _scan_broken_links(wiki_root, result)

    # 3. Çift yönlü bağlantıları senkronize et
    _sync_bidirectional_links(wiki_root, review_root, result, dry_run)

    # 4. Duplike review dosyalarını tara
    _scan_near_duplicates(review_root, result)

    return result


def _clean_off_topic_reviews(review_root: Path, result: HygieneResult, dry_run: bool) -> None:
    """Review dosyalarını OFF_TOPIC_KEYWORDS ile tara, eşleşenleri sil."""
    skip_names = {"index.md", ".gitkeep"}

    for path in sorted(review_root.glob("*.md")):
        if path.name.lower() in skip_names:
            continue

        try:
            text = read_text(path).lower()
        except Exception:
            continue

        # Başlığı ve özeti birleştirip kontrol et
        check_text = text[:2000]  # İlk 2000 karakter yeterli

        for keyword in OFF_TOPIC_KEYWORDS:
            if keyword in check_text:
                if not dry_run:
                    path.unlink(missing_ok=True)
                result.off_topic_deleted += 1
                result.deleted_files.append(path.name)
                break


def _scan_broken_links(wiki_root: Path, result: HygieneResult) -> None:
    """Tüm markdown dosyalarındaki [[wikilink]]'leri tara, kırık olanları bul."""
    # Mevcut dosya sluglarını topla
    existing_slugs: Set[str] = set()
    for path in iter_markdown_files(wiki_root):
        rel = path.relative_to(wiki_root)
        # "review/dosya-adi" ve "dosya-adi" formatlarını ekle
        slug_with_dir = str(rel.with_suffix("")).replace("\\", "/")
        slug_base = path.stem
        existing_slugs.add(slug_with_dir.lower())
        existing_slugs.add(slug_base.lower())

    # Sistem dosyalarını da ekle
    for name in ["index", "log", "hot", "system-memory"]:
        existing_slugs.add(name)

    # Tüm dosyalarda wikilink'leri tara
    wikilink_pattern = re.compile(r"\[\[([^\]|]+?)(?:\|[^\]]+)?\]\]")

    for path in iter_markdown_files(wiki_root):
        try:
            text = read_text(path)
        except Exception:
            continue

        for match in wikilink_pattern.finditer(text):
            target = match.group(1).strip()
            target_lower = target.lower()

            # Gömülü başlık referanslarını kaldır (ör. "page#heading")
            if "#" in target_lower:
                target_lower = target_lower.split("#")[0]

            if target_lower and target_lower not in existing_slugs:
                detail = f"{path.name} -> [[{target}]]"
                if detail not in result.broken_link_details:
                    result.broken_links_found += 1
                    result.broken_link_details.append(detail)


def _sync_bidirectional_links(
    wiki_root: Path, review_root: Path, result: HygieneResult, dry_run: bool
) -> None:
    """Review dosyalarının bağlantı kurduğu ana wiki sayfalarına ters bağlantı ekle."""
    # Ana wiki sayfalarını bul (review/ dışındakiler)
    core_pages: Dict[str, Path] = {}
    for path in sorted(wiki_root.glob("*.md")):
        name = path.name.lower()
        if name in {"index.md", "log.md", "hot.md", "system-memory.md"}:
            continue
        core_pages[path.stem.lower()] = path

    # Her review dosyasının hangi ana sayfalara link verdiğini bul
    wikilink_pattern = re.compile(r"\[\[([^\]|]+?)(?:\|[^\]]+)?\]\]")
    reverse_map: Dict[str, List[str]] = {}  # core_slug → [review_slugs]

    for path in sorted(review_root.glob("*.md")):
        if path.name.lower() in {"index.md", ".gitkeep"}:
            continue

        try:
            text = read_text(path)
        except Exception:
            continue

        review_slug = path.stem

        for match in wikilink_pattern.finditer(text):
            target = match.group(1).strip()
            # "review/" prefix'li linkleri atla (kendine veya diğer review'a link)
            if target.lower().startswith("review/"):
                continue
            target_lower = target.lower()
            if target_lower in core_pages:
                reverse_map.setdefault(target_lower, [])
                review_ref = f"[[review/{review_slug}]]"
                if review_ref not in reverse_map[target_lower]:
                    reverse_map[target_lower].append(review_ref)

    # Her ana sayfaya "## 📚 İlgili Draftlar" bölümü ekle/güncelle
    SECTION_HEADER = "## 📚 İlgili Draftlar"

    for core_slug, review_links in reverse_map.items():
        if core_slug not in core_pages:
            continue

        core_path = core_pages[core_slug]
        try:
            text = read_text(core_path)
        except Exception:
            continue

        if not review_links:
            continue

        # Mevcut bölümü bul veya oluştur
        if SECTION_HEADER in text:
            # Mevcut bölümdeki linkleri parse et
            section_start = text.index(SECTION_HEADER)
            after_header = text[section_start + len(SECTION_HEADER):]

            # Sonraki ## bölümüne kadar olan kısmı al
            next_section = re.search(r"\n## ", after_header)
            if next_section:
                existing_section = after_header[:next_section.start()]
            else:
                existing_section = after_header

            existing_links = set(re.findall(r"\[\[review/[^\]]+\]\]", existing_section))
            new_links = [link for link in review_links if link not in existing_links]

            if new_links:
                insert_point = section_start + len(SECTION_HEADER) + len(existing_section.rstrip())
                new_lines = "\n" + "\n".join(f"- {link}" for link in sorted(new_links))

                text = text[:insert_point] + new_lines + text[insert_point:]
                if not dry_run:
                    write_text(core_path, text)
                result.bidirectional_links_added += len(new_links)
        else:
            # Yeni bölüm ekle
            links_md = "\n".join(f"- {link}" for link in sorted(review_links))
            new_section = f"\n\n{SECTION_HEADER}\n{links_md}\n"

            text = text.rstrip() + new_section
            if not dry_run:
                write_text(core_path, text)
            result.bidirectional_links_added += len(review_links)


def _scan_near_duplicates(review_root: Path, result: HygieneResult) -> None:
    """Review dosyaları arasında %90+ Jaccard benzerliğini tespit et."""
    files: List[Tuple[str, str]] = []

    for path in sorted(review_root.glob("*.md")):
        if path.name.lower() in {"index.md", ".gitkeep"}:
            continue
        try:
            text = read_text(path)
            files.append((path.stem, text))
        except Exception:
            continue

    # O(n²) ama dosya sayısı genelde < 200 olduğundan sorun değil
    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            sim = jaccard_similarity(files[i][1], files[j][1])
            if sim >= 0.90:
                pair = f"{files[i][0]} ↔ {files[j][0]} (sim={sim:.2f})"
                result.near_duplicates_found += 1
                result.duplicate_pairs.append(pair)
