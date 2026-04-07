import datetime as dt
import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Dict, List

from .models import SourceItem
from .utils import now_utc_iso, sha256_text, strip_html


USER_AGENT = "AiBeyinBot/0.1 (+https://openrouter.ai)"


def _http_get(url: str, timeout_seconds: int = 30) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        return response.read().decode("utf-8", errors="ignore")


def collect_sources(config: Dict) -> List[SourceItem]:
    items: List[SourceItem] = []
    items.extend(_collect_github_repos(config.get("github_repos", {})))
    items.extend(_collect_owasp_cve(config.get("owasp_cve_rss", {})))
    items.extend(_collect_frontend_feeds(config.get("frontend_feeds", {})))
    items.extend(_collect_hackernews(config.get("hackernews", {})))
    items.extend(_collect_extra_rss(config.get("extra_rss", {})))
    return items


def _collect_github_repos(cfg: Dict) -> List[SourceItem]:
    if not cfg.get("enabled", False):
        return []

    lookback_days = int(cfg.get("lookback_days", 14))
    limit = int(cfg.get("limit", 10))
    date_str = (dt.date.today() - dt.timedelta(days=lookback_days)).isoformat()
    query_template = cfg.get(
        "query",
        "(frontend OR backend OR security OR accessibility) stars:>200 created:>={date}",
    )
    query = query_template.replace("{date}", date_str)
    encoded_query = urllib.parse.quote(query, safe="")
    url = (
        "https://api.github.com/search/repositories"
        f"?q={encoded_query}&sort=stars&order=desc&per_page={limit}"
    )

    raw = _http_get(url)
    payload = json.loads(raw)
    repos = payload.get("items", [])
    items: List[SourceItem] = []

    for repo in repos:
        title = repo.get("full_name", "")
        description = repo.get("description") or ""
        topics = ", ".join(repo.get("topics", []))
        content = f"Repository: {title}. Description: {description}. Topics: {topics}."
        items.append(
            SourceItem(
                source_name="github_repos",
                url=repo.get("html_url", ""),
                title=title,
                published_at=repo.get("updated_at") or now_utc_iso(),
                category="backend",
                content=content,
                content_hash=sha256_text(content),
            )
        )
    return items


def _collect_owasp_cve(cfg: Dict) -> List[SourceItem]:
    if not cfg.get("enabled", False):
        return []

    limit = int(cfg.get("limit", 8))
    feeds = cfg.get("feeds", [])
    items: List[SourceItem] = []
    for feed in feeds:
        try:
            xml_data = _http_get(feed)
            root = ET.fromstring(xml_data)
        except Exception:
            continue

        rss_items = root.findall(".//item")[:limit]
        for entry in rss_items:
            title = (entry.findtext("title") or "").strip()
            link = (entry.findtext("link") or "").strip()
            desc = (entry.findtext("description") or "").strip()
            pub_date = (entry.findtext("pubDate") or now_utc_iso()).strip()
            content = strip_html(desc)
            if not title or not link:
                continue
            items.append(
                SourceItem(
                    source_name="owasp_cve_rss",
                    url=link,
                    title=title,
                    published_at=pub_date,
                    category="security",
                    content=content,
                    content_hash=sha256_text(content),
                )
            )
    return items


def _collect_frontend_feeds(cfg: Dict) -> List[SourceItem]:
    if not cfg.get("enabled", False):
        return []

    limit = int(cfg.get("limit", 12))
    tags = cfg.get("devto_tags", [])
    rss = cfg.get("rss", [])

    items: List[SourceItem] = []
    items.extend(_collect_devto(tags, limit))
    items.extend(_collect_rss(rss, limit))
    return items


def _collect_devto(tags: List[str], limit: int) -> List[SourceItem]:
    items: List[SourceItem] = []
    for tag in tags:
        url = f"https://dev.to/api/articles?tag={urllib.parse.quote(tag)}&per_page={limit}"
        try:
            payload = json.loads(_http_get(url))
        except Exception:
            continue
        for article in payload:
            title = article.get("title", "")
            link = article.get("url", "")
            desc = article.get("description") or ""
            body = article.get("body_markdown") or ""
            content = f"{desc}\n\n{body}".strip()
            if not title or not link:
                continue
            items.append(
                SourceItem(
                    source_name="devto",
                    url=link,
                    title=title,
                    published_at=article.get("published_at") or now_utc_iso(),
                    category="frontend",
                    content=content,
                    content_hash=sha256_text(content),
                )
            )
    return items


def _collect_rss(feed_urls: List[str], limit: int) -> List[SourceItem]:
    items: List[SourceItem] = []
    for url in feed_urls:
        try:
            xml_data = _http_get(url)
            root = ET.fromstring(xml_data)
        except Exception:
            continue
        entries = root.findall(".//item")[:limit]
        for entry in entries:
            title = (entry.findtext("title") or "").strip()
            link = (entry.findtext("link") or "").strip()
            desc = (entry.findtext("description") or "").strip()
            pub_date = (entry.findtext("pubDate") or now_utc_iso()).strip()
            content = strip_html(desc)
            if not title or not link:
                continue
            items.append(
                SourceItem(
                    source_name="frontend_rss",
                    url=link,
                    title=title,
                    published_at=pub_date,
                    category="frontend",
                    content=content,
                    content_hash=sha256_text(content),
                )
            )
    return items


def _collect_hackernews(cfg: Dict) -> List[SourceItem]:
    """HackerNews Algolia API — web/backend/security etiketli hikayeler."""
    if not cfg.get("enabled", False):
        return []

    limit = int(cfg.get("limit", 10))
    lookback_hours = int(cfg.get("lookback_hours", 48))
    keywords = cfg.get(
        "keywords",
        ["frontend", "backend", "web", "security", "api", "css", "javascript", "typescript", "node"],
    )

    cutoff_ts = int(
        (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=lookback_hours)).timestamp()
    )
    items: List[SourceItem] = []

    try:
        url = (
            "https://hn.algolia.com/api/v1/search_by_date"
            f"?tags=story"
            f"&numericFilters=created_at_i>{cutoff_ts},points>10"
            f"&hitsPerPage={limit * 3}"
        )
        payload = json.loads(_http_get(url))
    except Exception:
        return []

    for hit in payload.get("hits", []):
        title = (hit.get("title") or "").strip()
        story_url = (hit.get("url") or "").strip()
        created = hit.get("created_at") or now_utc_iso()

        if not title or not story_url:
            continue

        lower_title = title.lower()
        if not any(kw in lower_title for kw in keywords):
            continue

        content = f"{title}. {strip_html(hit.get('story_text') or '')}"
        items.append(
            SourceItem(
                source_name="hackernews",
                url=story_url,
                title=title,
                published_at=created,
                category=_guess_hn_category(lower_title),
                content=content,
                content_hash=sha256_text(content),
            )
        )
        if len(items) >= limit:
            break

    return items


def _guess_hn_category(lower_title: str) -> str:
    if any(w in lower_title for w in ["security", "vulnerability", "cve", "hack", "auth", "xss", "csrf"]):
        return "security"
    if any(w in lower_title for w in ["css", "ui", "ux", "design", "animation", "layout", "tailwind"]):
        return "ui-ux"
    if any(w in lower_title for w in ["react", "vue", "svelte", "next", "nuxt", "frontend", "browser", "a11y"]):
        return "frontend"
    return "backend"


def _collect_extra_rss(cfg: Dict) -> List[SourceItem]:
    """Ek RSS kaynakları — web.dev, MDN Blog, web teknolojileri."""
    if not cfg.get("enabled", False):
        return []

    feeds = cfg.get("feeds", [])
    limit = int(cfg.get("limit", 10))
    items: List[SourceItem] = []

    for feed_entry in feeds:
        feed_url = feed_entry.get("url", "") if isinstance(feed_entry, dict) else str(feed_entry)
        category = feed_entry.get("category", "frontend") if isinstance(feed_entry, dict) else "frontend"
        if not feed_url:
            continue
        try:
            xml_data = _http_get(feed_url)
            root = ET.fromstring(xml_data)
        except Exception:
            continue

        atom_ns = "{http://www.w3.org/2005/Atom}"
        rss_items = root.findall(".//item") or root.findall(f".//{atom_ns}entry")
        for entry in rss_items[:limit]:
            title = (
                entry.findtext("title") or entry.findtext(f"{atom_ns}title") or ""
            ).strip()
            link_el = entry.find("link") or entry.find(f"{atom_ns}link")
            link = ""
            if link_el is not None:
                link = (link_el.text or link_el.get("href") or "").strip()
            desc = (
                entry.findtext("description")
                or entry.findtext(f"{atom_ns}summary")
                or entry.findtext(f"{atom_ns}content")
                or ""
            ).strip()
            pub_date = (
                entry.findtext("pubDate")
                or entry.findtext(f"{atom_ns}updated")
                or now_utc_iso()
            ).strip()

            if not title or not link:
                continue
            content = strip_html(desc)
            items.append(
                SourceItem(
                    source_name="extra_rss",
                    url=link,
                    title=title,
                    published_at=pub_date,
                    category=category,
                    content=content,
                    content_hash=sha256_text(content),
                )
            )

    return items[:limit]
