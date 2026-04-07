from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class SourceItem:
    source_name: str
    url: str
    title: str
    published_at: str
    category: str
    content: str
    content_hash: str


@dataclass
class ConceptDraft:
    slug: str
    title: str
    category: str
    summary: str
    key_points: List[str] = field(default_factory=list)
    links_to_existing: List[str] = field(default_factory=list)
    confidence: int = 0
    novelty: int = 0
    model_used: str = ""
    source_url: str = ""


@dataclass
class PipelineStats:
    collected: int = 0
    skipped_unchanged: int = 0
    skipped_duplicate: int = 0
    rejected_quality: int = 0
    drafted: int = 0
    errors: int = 0

    def as_dict(self) -> Dict[str, int]:
        return {
            "collected": self.collected,
            "skipped_unchanged": self.skipped_unchanged,
            "skipped_duplicate": self.skipped_duplicate,
            "rejected_quality": self.rejected_quality,
            "drafted": self.drafted,
            "errors": self.errors,
        }
