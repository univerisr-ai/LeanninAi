"""
dedup.py — Çok Katmanlı Tekrar Öğrenme Engelleme

Katman 1: Kaynak URL hash → aynı URL tekrar işlenmez (inventory'de)
Katman 2: Başlık benzerliği → "React Hooks Guide" vs "Modern React Hooks" yakalanır
Katman 3: İçerik Jaccard benzerliği → metin düzeyinde overlap kontrolü
Katman 4: Konsept parmak izi → "react, hooks, state" vs "hooks, react, state management" yakalanır
Katman 5: Çekirdek wiki overlap → zaten derin kapsanan konuları yüksek eşikle kontrol et
"""
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

from .utils import iter_markdown_files, jaccard_similarity, read_text, tokenize


# ── Çekirdek wiki sayfalarında zaten DERIN kapsanan kavramlar ──────────
# Bu konular zaten 14 ana wiki sayfasında detaylı yazılmış.
# Bunlarla ilgili yeni draft'lar SADECE gerçekten yeni bilgi getiriyorsa kabul edilir.
DEEPLY_COVERED_CONCEPTS: Dict[str, Set[str]] = {
    "react": {
        "hooks", "usestate", "useeffect", "usememo", "usecallback", "useref",
        "context", "compound", "polymorphic", "component", "composition",
        "props", "drilling", "state", "render", "lifecycle", "error boundary",
        "suspense", "lazy", "memo", "portal", "ref", "forward ref",
        "custom hook", "higher order", "hoc",
    },
    "state_management": {
        "zustand", "tanstack", "query", "redux", "valtio", "jotai", "recoil",
        "state", "store", "selector", "mutation", "optimistic", "cache",
        "server state", "client state", "global state",
    },
    "css_styling": {
        "css", "flexbox", "grid", "tailwind", "panda", "stylex",
        "design token", "container query", "media query", "responsive",
        "dark mode", "animation", "transition", "keyframe",
        "variable", "custom property", "specificity", "cascade",
    },
    "security": {
        "xss", "csrf", "jwt", "cors", "csp", "token", "cookie",
        "httponly", "samesite", "refresh token", "access token",
        "rbac", "authorization", "authentication", "oauth",
        "sanitize", "dompurify", "injection", "sql injection",
        "rate limit", "token bucket", "bot", "honeypot", "captcha",
    },
    "architecture": {
        "clean architecture", "domain", "application layer", "infrastructure",
        "dependency injection", "repository pattern", "service",
        "rest api", "graphql", "prisma", "redis", "cache",
        "n+1", "bullmq", "queue", "middleware",
    },
    "accessibility": {
        "wcag", "aria", "landmark", "role", "tabindex", "focus",
        "screen reader", "keyboard", "skip link", "alt text",
        "contrast", "color blind", "semantic html",
    },
    "performance": {
        "core web vitals", "lcp", "cls", "inp", "fid",
        "service worker", "pwa", "lazy loading", "code splitting",
        "bundle", "tree shaking", "minification", "compression",
        "preload", "prefetch", "preconnect", "lighthouse",
    },
    "ui_ux": {
        "gestalt", "hick", "fitts", "color theory", "hsl",
        "typography", "type scale", "spacing", "grid system",
        "micro interaction", "skeleton", "loading", "toast",
        "modal", "form", "validation", "responsive",
    },
}


def detect_wiki_duplicate(
    wiki_root: Path,
    candidate_text: str,
    max_similarity: float,
) -> Tuple[bool, str, float]:
    best_file = ""
    best_score = 0.0

    for path in iter_markdown_files(wiki_root):
        name = path.name.lower()
        if name in {"index.md", "log.md", "hot.md", "system-memory.md"}:
            continue
        existing = read_text(path)
        score = jaccard_similarity(existing, candidate_text)
        if score > best_score:
            best_score = score
            best_file = str(path)

    return best_score >= max_similarity, best_file, best_score


def detect_concept_title_duplicate(
    candidate_title: str,
    existing_concept_slugs: List[str],
    existing_concept_titles: List[str],
    max_title_similarity: float = 0.75,
) -> Tuple[bool, str]:
    """
    Başlık düzeyinde kavram tekrarını tespit eder.

    Yeni bir draft'ın başlığı mevcut envanter kavramlarıyla çok benzerse
    gerçek içerik benzerliği olmasa bile atlanır. Bu sayede aynı konu
    farklı kelimelerle yeniden öğrenilmez.
    """
    candidate_tokens = set(tokenize(candidate_title))
    if not candidate_tokens:
        return False, ""

    for title in existing_concept_titles:
        existing_tokens = set(tokenize(title))
        if not existing_tokens:
            continue
        intersection = candidate_tokens & existing_tokens
        union = candidate_tokens | existing_tokens
        similarity = len(intersection) / len(union)
        if similarity >= max_title_similarity:
            return True, title

    return False, ""


def detect_concept_fingerprint_duplicate(
    candidate_title: str,
    candidate_summary: str,
    candidate_key_points: List[str],
    existing_concept_titles: List[str],
    wiki_root: Path,
    threshold: float = 0.50,
) -> Tuple[bool, str, str]:
    """
    Konsept parmak izi ile tekrar tespiti.

    Başlık + özet + ana noktalardan anahtar kavramlar çıkarır,
    mevcut wiki+review dosyalarıyla karşılaştırır.
    Aynı kavram setini kapsayan mevcut dosya varsa reddeder.

    Returns:
        (is_duplicate, reason, matched_against)
    """
    # Adayın kavram parmak izini çıkar
    all_text = f"{candidate_title} {candidate_summary} {' '.join(candidate_key_points)}"
    candidate_concepts = _extract_concept_fingerprint(all_text)

    if len(candidate_concepts) < 3:
        return False, "", ""

    # 1. Çekirdek wiki konularıyla karşılaştır (daha sıkı eşik)
    core_match = _check_deeply_covered(candidate_concepts)
    if core_match:
        domain, overlap_ratio = core_match
        if overlap_ratio >= 0.65:
            return True, f"core_topic_overlap ({domain}: {overlap_ratio:.0%})", domain

    # 2. Mevcut review dosyalarıyla kavram benzerliği
    review_dir = wiki_root / "review"
    if review_dir.exists():
        for path in sorted(review_dir.glob("*.md")):
            if path.name.lower() in {"index.md", ".gitkeep"}:
                continue
            try:
                existing_text = read_text(path)
                existing_concepts = _extract_concept_fingerprint(existing_text)
                if len(existing_concepts) < 3:
                    continue

                overlap = len(candidate_concepts & existing_concepts)
                union_size = len(candidate_concepts | existing_concepts)
                if union_size == 0:
                    continue

                concept_sim = overlap / union_size
                if concept_sim >= threshold:
                    return True, f"concept_overlap ({concept_sim:.0%})", path.stem
            except Exception:
                continue

    return False, "", ""


def _extract_concept_fingerprint(text: str) -> Set[str]:
    """
    Metinden teknik kavram parmak izini çıkarır.

    Tek kelimeler değil, anlamlı teknik terimler çıkarılır:
    - "react hooks" → tek birim
    - "clean architecture" → tek birim
    - "server components" → tek birim
    """
    lower = text.lower()

    # Bilinen çok-kelimeli teknik terimleri önce yakala
    COMPOUND_TERMS = [
        "react hooks", "react server components", "server components",
        "error boundary", "error boundaries", "compound components",
        "polymorphic components", "custom hooks", "custom hook",
        "higher order component", "render props", "forward ref",
        "optimistic update", "optimistic updates",
        "state management", "server state", "client state", "global state",
        "tanstack query", "react query",
        "clean architecture", "domain driven", "dependency injection",
        "design token", "design tokens", "design system",
        "container query", "media query",
        "core web vitals", "web vitals",
        "service worker", "code splitting", "tree shaking", "lazy loading",
        "dark mode", "color theory", "type scale",
        "micro interaction", "micro interactions", "skeleton loading",
        "rate limit", "rate limiting", "token bucket",
        "access token", "refresh token",
        "sql injection", "prompt injection",
        "skip link", "screen reader",
        "cross site scripting", "cross site request forgery",
        "content security policy",
        "module federation", "micro frontend", "micro frontends",
        "streaming ssr", "server side rendering",
        "static site generation", "incremental static",
        "web component", "web components",
        "api gateway", "rest api", "graphql",
        "typescript generics", "branded types", "type guard",
        "css grid", "css flexbox", "css animation",
        "tailwind css", "panda css", "stylex",
        "web assembly", "webassembly", "wasm",
        "web worker", "web workers",
        "data fetching", "cache invalidation",
    ]

    concepts: Set[str] = set()

    for term in COMPOUND_TERMS:
        if term in lower:
            concepts.add(term)

    # Tek kelimelik teknik terimler (compound'da olmayan)
    SINGLE_TERMS = {
        "react", "vue", "svelte", "next", "nuxt", "remix", "astro",
        "vite", "webpack", "rollup", "esbuild", "turbopack",
        "typescript", "javascript", "css", "html", "dom",
        "hooks", "suspense", "portal", "context", "reducer",
        "zustand", "redux", "valtio", "jotai", "recoil", "mobx",
        "prisma", "drizzle", "sequelize",
        "express", "fastify", "node", "deno", "bun",
        "redis", "postgresql", "mongodb", "sqlite",
        "jwt", "oauth", "cors", "csp", "xss", "csrf",
        "wcag", "aria", "a11y", "accessibility",
        "pwa", "lcp", "cls", "inp", "fid",
        "figma", "storybook",
        "playwright", "cypress", "vitest", "jest",
        "docker", "ci/cd", "github actions",
    }

    words = set(re.findall(r"[a-z][a-z0-9/.]+", lower))
    for term in SINGLE_TERMS:
        if term in words:
            concepts.add(term)

    return concepts


def _check_deeply_covered(candidate_concepts: Set[str]) -> Tuple[str, float] | None:
    """
    Adayın konseptlerinin çekirdek wiki'de zaten derin kapsanıp kapsamadığını kontrol et.
    """
    best_domain = ""
    best_ratio = 0.0

    for domain, domain_concepts in DEEPLY_COVERED_CONCEPTS.items():
        overlap = 0
        for concept in candidate_concepts:
            # Hem tam eşleşme hem de alt-string eşleşme
            for dc in domain_concepts:
                if dc in concept or concept in dc:
                    overlap += 1
                    break

        if len(candidate_concepts) > 0:
            ratio = overlap / len(candidate_concepts)
            if ratio > best_ratio:
                best_ratio = ratio
                best_domain = domain

    if best_ratio >= 0.50:
        return best_domain, best_ratio
    return None
