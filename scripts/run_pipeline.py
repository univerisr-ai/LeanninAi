import argparse
import json
import os
import sys
from pathlib import Path


def bootstrap_path() -> None:
    root = Path(__file__).resolve().parents[1]
    src = root / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run AiBeyin automation pipeline")
    parser.add_argument(
        "--config",
        default="config/pipeline.json",
        help="Path to pipeline config JSON relative to project root",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Collect and score content but do not write draft files",
    )
    return parser.parse_args()


def main() -> int:
    bootstrap_path()

    from aibeyin.pipeline import run_pipeline  # Imported after path bootstrap

    args = parse_args()
    project_root = Path(__file__).resolve().parents[1]
    config_path = project_root / args.config

    result = run_pipeline(project_root=project_root, config_path=config_path, dry_run=args.dry_run)
    print(json.dumps(result, ensure_ascii=True, indent=2))

    return 0 if result.get("status") == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
