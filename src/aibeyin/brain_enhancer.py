"""
BrainEnhancer — İkinci Beyin Modülü

Pazar günü çalışan ikinci beyin: mevcut wiki sayfalarını geliştirir,
zayıf sayfaları derinleştirir ve izole konseptleri birbirine bağlar.
"""
import datetime as dt
import json
import os
import re
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple

from .utils import now_utc_iso, read_text, safe_slug, sha256_text, write_text


@dataclass
class EnhancementCandidate:
    path: Path
    slug: str
    title: str
    age_days: float
    word_count: int
    key_points_count: int
    link_count: int
    score: float  # higher = more in need of enhancement


@dataclass
class EnhancementResult:
    candidates_found: int = 0
    enhanced: int = 0
    skipped_dry_run: int = 0
    errors: int = 0
    enhanced_slugs: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict:
        return {
            "candidates_found": self.candidates_found,
            "enhanced": self.enhanced,
            "skipped_dry_run": self.skipped_dry_run,
            "errors": self.errors,
            "enhanced_slugs": self.enhanced_slugs,
        }


class BrainEnhancer:
    """
    İkinci beyin: mevcut wiki sayfalarını derinleştirir ve geliştirir.

    Strateji:
    - Kısa, eski veya izole (bağlantısız) sayfalar öncelikle seçilir.
    - LLM bu sayfaları daha profesyonel ve kapsamlı hale getirir.
    - Çıktı wiki/review/enhanced/ altına draft olarak yazılır.
    """

    def __init__(self, openrouter_config: Dict, enhancement_config: Dict) -> None:
        self.base_url = openrouter_config.get(
            "base_url", "https://openrouter.ai/api/v1/chat/completions"
        )
        self.primary_model = openrouter_config.get("primary_model", "qwen/qwen3-coder:free")
        self.fallback_model = openrouter_config.get("fallback_model", "stepfun/step-3.5-flash:free")
        self.max_tokens = int(openrouter_config.get("max_tokens", 1600))
        self.temperature = float(openrouter_config.get("temperature", 0.3))
        self.timeout_seconds = int(openrouter_config.get("request_timeout_seconds", 60))
        self.api_key = os.getenv("OPENROUTER_API_KEY", "").strip()

        self.max_pages_per_run = int(enhancement_config.get("max_pages_per_run", 5))
        self.min_score_threshold = float(enhancement_config.get("min_score_threshold", 30.0))
        self.min_age_days = float(enhancement_config.get("min_age_days", 7.0))

    def run(self, wiki_root: Path, dry_run: bool = False) -> EnhancementResult:
        result = EnhancementResult()
        review_dir = wiki_root / "review"
        enhanced_dir = wiki_root / "review" / "enhanced"

        candidates = self._find_candidates(wiki_root)
        result.candidates_found = len(candidates)

        for candidate in candidates[: self.max_pages_per_run]:
            if dry_run:
                result.skipped_dry_run += 1
                continue
            if not self.api_key:
                result.errors += 1
                continue
            try:
                original_text = read_text(candidate.path)
                enhanced_md = self._enhance_page(candidate, original_text)
                if enhanced_md:
                    out_path = enhanced_dir / f"{candidate.slug}-enhanced.md"
                    enhanced_dir.mkdir(parents=True, exist_ok=True)
                    write_text(out_path, enhanced_md)
                    result.enhanced += 1
                    result.enhanced_slugs.append(candidate.slug)
            except Exception:
                result.errors += 1

        return result

    def _find_candidates(self, wiki_root: Path) -> List[EnhancementCandidate]:
        candidates: List[EnhancementCandidate] = []
        review_dir = wiki_root / "review"
        skip_names = {"index.md", "log.md", "hot.md"}

        for path in sorted(wiki_root.rglob("*.md")):
            if path.name.lower() in skip_names:
                continue
            if "enhanced" in str(path):
                continue
            if "reports" in str(path):
                continue

            try:
                text = read_text(path)
                age_days = self._get_age_days(path, text)
                if age_days < self.min_age_days:
                    continue
                score, word_count, kp_count, link_count = self._score_page(text)
                if score < self.min_score_threshold:
                    continue
                title = self._extract_title(text, path)
                candidates.append(
                    EnhancementCandidate(
                        path=path,
                        slug=safe_slug(title),
                        title=title,
                        age_days=age_days,
                        word_count=word_count,
                        key_points_count=kp_count,
                        link_count=link_count,
                        score=score,
                    )
                )
            except Exception:
                continue

        candidates.sort(key=lambda c: c.score, reverse=True)
        return candidates

    def _score_page(self, text: str) -> Tuple[float, int, int, int]:
        words = text.split()
        word_count = len(words)
        key_points = len(re.findall(r"^[-*]\s+.+", text, re.MULTILINE))
        links = len(re.findall(r"\[\[.+?\]\]", text))

        score = 0.0
        if word_count < 150:
            score += 40
        elif word_count < 300:
            score += 20
        elif word_count < 500:
            score += 10

        if key_points < 3:
            score += 30
        elif key_points < 5:
            score += 15

        if links == 0:
            score += 20
        elif links < 2:
            score += 10

        return score, word_count, key_points, links

    def _get_age_days(self, path: Path, text: str) -> float:
        match = re.search(r"generated_at:\s*(\d{4}-\d{2}-\d{2}T[\d:+Z.-]+)", text)
        if match:
            try:
                ts_str = match.group(1).replace("Z", "+00:00")
                ts = dt.datetime.fromisoformat(ts_str)
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=dt.timezone.utc)
                delta = dt.datetime.now(dt.timezone.utc) - ts.astimezone(dt.timezone.utc)
                return delta.total_seconds() / 86400
            except Exception:
                pass
        try:
            mtime = path.stat().st_mtime
            delta = dt.datetime.now(dt.timezone.utc).timestamp() - mtime
            return delta / 86400
        except Exception:
            return 999.0

    def _extract_title(self, text: str, path: Path) -> str:
        lines = text.splitlines()
        for line in lines:
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
        return path.stem.replace("-", " ").title()

    def _enhance_page(self, candidate: EnhancementCandidate, original_text: str) -> str:
        prompt = (
            "Task: Deepen and improve the following Turkish wiki page about web development.\n"
            f"Page title: {candidate.title}\n"
            f"Current word count: {candidate.word_count}\n"
            f"Current key points: {candidate.key_points_count}\n"
            f"Current wiki-links: {candidate.link_count}\n\n"
            "Original content:\n"
            f"{original_text[:4000]}\n\n"
            "Instructions:\n"
            "- Keep the ## Meta section unchanged.\n"
            "- Expand ## Ozet with deeper technical insight (at least 3 paragraphs).\n"
            "- Expand ## Ana Noktalar to at least 7 professional, actionable bullet points.\n"
            "- Add concrete code examples where appropriate (use fenced code blocks).\n"
            "- Add [[WikiLink]] cross-references to related topics.\n"
            "- Add a new ## Profesyonel Ipuclar section with 3-5 advanced tips.\n"
            "- Write in Turkish, keep it professional and technically accurate.\n"
            "- Return only the complete improved Markdown content (no extra JSON or explanation)."
        )

        try:
            content = self._request_model(self.primary_model, prompt)
        except Exception:
            try:
                content = self._request_model(self.fallback_model, prompt)
            except Exception:
                return ""

        if not content or len(content.split()) < 50:
            return ""

        header = (
            f"<!-- enhancement: generated_at={now_utc_iso()} "
            f"original={candidate.slug} status=draft-enhanced -->\n\n"
        )
        return header + content

    def _request_model(self, model_name: str, prompt: str) -> str:
        request_body = {
            "model": model_name,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Sen Türkçe web geliştirme wiki'si için uzman bir teknik editörsün. "
                        "Mevcut sayfa içeriklerini daha derin, profesyonel ve kapsamlı hale getiriyorsun. "
                        "Kod örnekleri, en iyi uygulamalar ve güncel teknikler ekle."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
        data = json.dumps(request_body).encode("utf-8")
        request = urllib.request.Request(
            self.base_url,
            data=data,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/univerisr-ai/LeanninAi",
                "X-Title": "AiBeyin-Enhancer",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
            raw = response.read().decode("utf-8", errors="ignore")
        parsed = json.loads(raw)
        return parsed["choices"][0]["message"]["content"]
