from pathlib import Path
from typing import Tuple

from .utils import iter_markdown_files, jaccard_similarity, read_text


def detect_wiki_duplicate(
    wiki_root: Path,
    candidate_text: str,
    max_similarity: float,
) -> Tuple[bool, str, float]:
    best_file = ""
    best_score = 0.0

    for path in iter_markdown_files(wiki_root):
        name = path.name.lower()
        if name in {"index.md", "log.md", "hot.md"}:
            continue
        existing = read_text(path)
        score = jaccard_similarity(existing, candidate_text)
        if score > best_score:
            best_score = score
            best_file = str(path)

    return best_score >= max_similarity, best_file, best_score
