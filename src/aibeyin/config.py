from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from .utils import read_json


@dataclass
class PipelineConfig:
    data: Dict[str, Any]

    @property
    def disk_limit_gb(self) -> float:
        return float(self.data.get("project_disk_limit_gb", 10))

    @property
    def quality(self) -> Dict[str, Any]:
        return self.data.get("quality_gates", {})

    @property
    def llm(self) -> Dict[str, Any]:
        return self.data.get("llm") or self.data.get("openrouter") or {}

    @property
    def openrouter(self) -> Dict[str, Any]:
        return self.llm

    @property
    def model_profiles(self) -> Dict[str, Any]:
        return self.data.get("model_profiles", {})

    @property
    def sources(self) -> Dict[str, Any]:
        return self.data.get("sources", {})


def load_pipeline_config(path: Path) -> PipelineConfig:
    payload = read_json(path)
    if not payload:
        raise FileNotFoundError(f"Pipeline config missing or empty: {path}")
    return PipelineConfig(payload)
