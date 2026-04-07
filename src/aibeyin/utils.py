import datetime as dt
import hashlib
import json
import re
from pathlib import Path
from typing import Dict, Iterable, List


TURKISH_ASCII_MAP = {
    "c": "c",
    "g": "g",
    "i": "i",
    "o": "o",
    "s": "s",
    "u": "u",
    "C": "c",
    "G": "g",
    "I": "i",
    "O": "o",
    "S": "s",
    "U": "u",
}


def now_utc_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", errors="ignore")).hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def read_json(path: Path) -> Dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")


def iter_markdown_files(root: Path) -> Iterable[Path]:
    if not root.exists():
        return []
    return sorted(root.rglob("*.md"))


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9_]{3,}", text.lower())


def jaccard_similarity(left: str, right: str) -> float:
    l_tokens = set(tokenize(left))
    r_tokens = set(tokenize(right))
    if not l_tokens or not r_tokens:
        return 0.0
    return len(l_tokens & r_tokens) / len(l_tokens | r_tokens)


def safe_slug(text: str) -> str:
    converted = []
    replacements = {
        "ç": "c",
        "ğ": "g",
        "ı": "i",
        "ö": "o",
        "ş": "s",
        "ü": "u",
        "Ç": "c",
        "Ğ": "g",
        "İ": "i",
        "Ö": "o",
        "Ş": "s",
        "Ü": "u",
    }
    for char in text:
        converted.append(replacements.get(char, char))
    lowered = "".join(converted).lower()
    lowered = re.sub(r"[^a-z0-9]+", "-", lowered)
    lowered = re.sub(r"-+", "-", lowered)
    return lowered.strip("-") or "untitled"


def strip_html(raw_html: str) -> str:
    without_tags = re.sub(r"<[^>]+>", " ", raw_html)
    return normalize_space(without_tags)
