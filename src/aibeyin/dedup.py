from pathlib import Path
from typing import List, Tuple

from .utils import iter_markdown_files, jaccard_similarity, read_text, tokenize


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

