import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Tuple

from .utils import jaccard_similarity, now_utc_iso, normalize_space, read_text, safe_slug, tokenize, write_json


SKIP_FILES = {"index.md", "log.md", "hot.md", "system-memory.md"}
WIKILINK_PATTERN = re.compile(r"\[\[([^\]|#]+)")


@dataclass
class PageRecord:
    slug: str
    title: str
    category: str
    status: str
    summary: str
    key_points: List[str] = field(default_factory=list)
    related_links: List[str] = field(default_factory=list)
    source_url: str = ""
    generated_at: str = ""
    path: str = ""
    word_count: int = 0


def load_pages(wiki_root: Path) -> List[PageRecord]:
    pages: List[PageRecord] = []
    for path in sorted(wiki_root.rglob("*.md")):
        if path.name.lower() in SKIP_FILES:
            continue
        if path.relative_to(wiki_root).as_posix() == "review/index.md":
            continue
        page = _parse_page(path, wiki_root)
        if page:
            pages.append(page)
    return pages


def build_brain_index(wiki_root: Path) -> Dict:
    pages = load_pages(wiki_root)
    _canonicalize_page_links(pages)
    edges, degree_map = _build_graph(pages)
    orphans = sorted(page.slug for page in pages if degree_map.get(page.slug, 0) == 0)

    hottest = _canonicalize_slug_list(_load_hot_slugs(wiki_root / "hot.md"), pages)
    page_lookup = {page.slug: page for page in pages}
    central_pages = sorted(
        (
            {
                "slug": page.slug,
                "title": page.title,
                "degree": degree_map.get(page.slug, 0),
                "category": page.category,
            }
            for page in pages
        ),
        key=lambda item: (-item["degree"], item["title"].lower()),
    )[:12]

    hot_pages = []
    for slug in hottest:
        page = page_lookup.get(slug)
        if not page:
            continue
        hot_pages.append(
            {
                "slug": page.slug,
                "title": page.title,
                "category": page.category,
                "summary": page.summary,
                "degree": degree_map.get(page.slug, 0),
            }
        )

    return {
        "generated_at": now_utc_iso(),
        "page_count": len(pages),
        "edge_count": len(edges),
        "orphan_count": len(orphans),
        "hot_slugs": hottest,
        "hot_pages": hot_pages,
        "central_pages": central_pages,
        "orphans": orphans[:50],
        "pages": [
            {
                **asdict(page),
                "degree": degree_map.get(page.slug, 0),
                "is_hot": page.slug in hottest,
            }
            for page in pages
        ],
        "graph": {
            "nodes": [
                {
                    "slug": page.slug,
                    "title": page.title,
                    "category": page.category,
                    "status": page.status,
                    "degree": degree_map.get(page.slug, 0),
                }
                for page in pages
            ],
            "edges": [
                {"source": source, "target": target}
                for source, target in sorted(edges)
            ],
        },
    }


def write_brain_index(project_root: Path) -> Dict[str, str]:
    wiki_root = project_root / "wiki"
    storage_root = project_root / "storage"
    payload = build_brain_index(wiki_root)

    index_path = storage_root / "query_index.json"
    graph_path = storage_root / "knowledge_graph.json"
    write_json(index_path, payload)
    write_json(graph_path, payload["graph"])
    frontend_exports = _write_frontend_exports(project_root, payload)

    return {
        "query_index": str(index_path),
        "knowledge_graph": str(graph_path),
        "page_count": str(payload["page_count"]),
        "edge_count": str(payload["edge_count"]),
        "orphan_count": str(payload["orphan_count"]),
        **frontend_exports,
    }


def query_brain(wiki_root: Path, query: str, limit: int = 5) -> Dict:
    pages = load_pages(wiki_root)
    _canonicalize_page_links(pages)
    edges, degree_map = _build_graph(pages)
    hot_slugs = set(_canonicalize_slug_list(_load_hot_slugs(wiki_root / "hot.md"), pages))
    results = []
    query_norm = normalize_space(query)

    for page in pages:
        score, reasons = _score_page(query_norm, page, degree_map.get(page.slug, 0), hot_slugs)
        if score <= 0:
            continue
        results.append(
            {
                "slug": page.slug,
                "title": page.title,
                "category": page.category,
                "status": page.status,
                "score": round(score, 3),
                "reasons": reasons,
                "summary": page.summary,
                "key_points": page.key_points[:3],
                "related_links": page.related_links[:6],
                "source_url": page.source_url,
                "path": page.path,
            }
        )

    results.sort(key=lambda item: (-item["score"], item["title"].lower()))
    top = results[:limit]

    return {
        "query": query,
        "result_count": len(top),
        "graph_edge_count": len(edges),
        "results": top,
    }


def _parse_page(path: Path, wiki_root: Path) -> PageRecord:
    text = read_text(path)
    lines = text.splitlines()
    title = path.stem
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()

    rel = path.relative_to(wiki_root).with_suffix("")
    slug = str(rel).replace("\\", "/")
    meta = _parse_meta(lines)
    summary = _section_body(text, "## Ozet")
    key_points = _section_bullets(text, "## Ana Noktalar")
    related_links = _extract_wikilinks(_section_body(text, "## Iliskili Sayfalar"))

    return PageRecord(
        slug=slug,
        title=title,
        category=meta.get("category", "other"),
        status=meta.get("status", "published"),
        summary=summary,
        key_points=key_points,
        related_links=related_links,
        source_url=meta.get("source", ""),
        generated_at=meta.get("generated_at", ""),
        path=str(path),
        word_count=len(text.split()),
    )


def _parse_meta(lines: List[str]) -> Dict[str, str]:
    meta: Dict[str, str] = {}
    in_meta = False
    for line in lines:
        stripped = line.strip()
        if stripped == "## Meta":
            in_meta = True
            continue
        if in_meta and stripped.startswith("## "):
            break
        if in_meta and stripped.startswith("- ") and ":" in stripped:
            key, value = stripped[2:].split(":", 1)
            meta[key.strip()] = value.strip()
    return meta


def _section_body(text: str, heading: str) -> str:
    pattern = re.escape(heading) + r"\s*(.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, re.S)
    if not match:
        return ""
    return normalize_space(match.group(1).strip())


def _section_bullets(text: str, heading: str) -> List[str]:
    body = _section_body(text, heading)
    bullets: List[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            bullets.append(stripped[2:].strip())
    if bullets:
        return bullets
    # Section body normalize_space collapses line breaks; fallback to raw slice.
    pattern = re.escape(heading) + r"\s*(.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, re.S)
    if not match:
        return []
    raw_body = match.group(1)
    return [line.strip()[2:].strip() for line in raw_body.splitlines() if line.strip().startswith("- ")]


def _extract_wikilinks(text: str) -> List[str]:
    links: List[str] = []
    seen: Set[str] = set()
    for match in WIKILINK_PATTERN.finditer(text or ""):
        target = safe_slug(match.group(1).strip())
        if not target or target in seen:
            continue
        seen.add(target)
        links.append(target)
    return links


def _load_hot_slugs(hot_path: Path) -> List[str]:
    if not hot_path.exists():
        return []
    text = read_text(hot_path)
    slugs = _extract_wikilinks(text)
    return slugs[:10]


def _canonicalize_page_links(pages: List[PageRecord]) -> None:
    slug_map = {page.slug.lower(): page.slug for page in pages}
    stem_map = {page.slug.split("/")[-1].lower(): page.slug for page in pages}

    for page in pages:
        canonical_links: List[str] = []
        seen: Set[str] = set()
        for raw_link in page.related_links:
            target = slug_map.get(raw_link.lower()) or stem_map.get(raw_link.lower())
            if not target or target == page.slug or target in seen:
                continue
            seen.add(target)
            canonical_links.append(target)
        page.related_links = canonical_links


def _canonicalize_slug_list(raw_slugs: List[str], pages: List[PageRecord]) -> List[str]:
    slug_map = {page.slug.lower(): page.slug for page in pages}
    stem_map = {page.slug.split("/")[-1].lower(): page.slug for page in pages}
    canonical: List[str] = []
    seen: Set[str] = set()

    for raw_slug in raw_slugs:
        target = slug_map.get(raw_slug.lower()) or stem_map.get(raw_slug.lower())
        if not target or target in seen:
            continue
        seen.add(target)
        canonical.append(target)

    return canonical


def _build_graph(pages: List[PageRecord]) -> Tuple[Set[Tuple[str, str]], Dict[str, int]]:
    slug_map = {page.slug.lower(): page.slug for page in pages}
    stem_map = {page.slug.split("/")[-1].lower(): page.slug for page in pages}
    edges: Set[Tuple[str, str]] = set()
    degree_map: Dict[str, int] = {page.slug: 0 for page in pages}

    for page in pages:
        for raw_link in page.related_links:
            target = slug_map.get(raw_link.lower()) or stem_map.get(raw_link.lower())
            if not target or target == page.slug:
                continue
            edge = tuple(sorted((page.slug, target)))
            if edge in edges:
                continue
            edges.add(edge)
            degree_map[page.slug] += 1
            degree_map[target] += 1

    return edges, degree_map


def _score_page(query: str, page: PageRecord, degree: int, hot_slugs: Set[str]) -> Tuple[float, List[str]]:
    reasons: List[str] = []
    query_lower = query.lower()
    haystack = " ".join(
        [
            page.title,
            page.category,
            page.summary,
            " ".join(page.key_points),
            " ".join(page.related_links),
        ]
    )
    title_sim = jaccard_similarity(query_lower, page.title.lower())
    body_sim = jaccard_similarity(query_lower, haystack.lower())
    token_overlap = len(set(tokenize(query_lower)) & set(tokenize(haystack.lower())))

    score = (title_sim * 5.0) + (body_sim * 3.5) + min(token_overlap, 5) * 0.8

    if query_lower in page.title.lower():
        score += 4.0
        reasons.append("title-match")
    if query_lower in page.summary.lower():
        score += 2.5
        reasons.append("summary-match")
    if page.status == "published":
        score += 1.0
        reasons.append("published")
    if degree > 0:
        score += min(degree, 8) * 0.15
        reasons.append(f"linked:{degree}")
    if page.slug in hot_slugs:
        score += 0.75
        reasons.append("hot-cache")

    if score < 1.0:
        return 0.0, []
    return score, reasons


def _write_frontend_exports(project_root: Path, payload: Dict) -> Dict[str, str]:
    frontend_root = project_root / "frontend"
    if not frontend_root.exists():
        return {}

    data_root = frontend_root / "public" / "data"
    query_index_path = data_root / "query_index.json"
    graph_path = data_root / "knowledge_graph.json"

    write_json(query_index_path, payload)
    write_json(graph_path, payload["graph"])

    return {
        "frontend_query_index": str(query_index_path),
        "frontend_knowledge_graph": str(graph_path),
    }
