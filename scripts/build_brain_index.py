import argparse
import json
import sys
from pathlib import Path


def bootstrap_path() -> Path:
    root = Path(__file__).resolve().parents[1]
    src = root / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
    return root


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build query and graph indexes for AiBeyin")
    parser.add_argument(
        "--project-root",
        default=".",
        help="Project root path",
    )
    return parser.parse_args()


def main() -> int:
    bootstrap_path()

    from aibeyin.query_engine import write_brain_index

    args = parse_args()
    project_root = Path(args.project_root).resolve()
    payload = write_brain_index(project_root)
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
