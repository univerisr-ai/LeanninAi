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
    parser = argparse.ArgumentParser(description="Test configured LLM provider profiles")
    parser.add_argument(
        "--config",
        default="config/model_profiles.json",
        help="Path to model profile config JSON relative to project root",
    )
    parser.add_argument(
        "--profile",
        action="append",
        dest="profiles",
        help="Specific profile name to test. Can be passed multiple times.",
    )
    parser.add_argument(
        "--prompt",
        default="Return only the exact text OK",
        help="Prompt sent to each test profile",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available profiles and exit",
    )
    return parser.parse_args()


def main() -> int:
    project_root = bootstrap_path()

    from aibeyin.utils import load_env_file, read_json
    from aibeyin.llm_client import LLMClient

    args = parse_args()
    load_env_file(project_root / ".env")

    config_path = project_root / args.config
    payload = read_json(config_path)
    profiles = payload.get("profiles", {})
    if not profiles:
        print(json.dumps({"error": f"No profiles found in {config_path}"}, ensure_ascii=True, indent=2))
        return 1

    if args.list:
        print(json.dumps({"profiles": sorted(profiles.keys())}, ensure_ascii=True, indent=2))
        return 0

    selected_names = args.profiles or payload.get("default_profiles") or sorted(profiles.keys())
    results = []
    had_error = False

    for name in selected_names:
        profile = profiles.get(name)
        if not profile:
            results.append({"profile": name, "status": "missing"})
            had_error = True
            continue

        try:
            client = LLMClient(profile)
            outcome = client.test_text(
                prompt=args.prompt,
                system_prompt="Reply with a final answer only. Do not expose reasoning. Keep it short.",
            )
            results.append(
                {
                    "profile": name,
                    "status": "ok",
                    "provider": outcome["provider"],
                    "model": outcome["model"],
                    "latency_ms": int(outcome["latency_ms"]),
                    "preview": outcome["content"][:180],
                }
            )
        except Exception as exc:
            results.append(
                {
                    "profile": name,
                    "status": "error",
                    "error": f"{type(exc).__name__}: {str(exc)}",
                }
            )
            had_error = True

    print(json.dumps({"results": results}, ensure_ascii=True, indent=2))
    return 1 if had_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
