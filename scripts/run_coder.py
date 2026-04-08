import argparse
import sys
import os
import subprocess
from pathlib import Path

def bootstrap_path() -> None:
    root = Path(__file__).resolve().parents[1]
    src = root / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Multi-Agent AI Coder")
    parser.add_argument(
        "--task",
        required=True,
        help="Task description for the Maker agent (e.g. 'Write a Python script to scrape a website').",
    )
    parser.add_argument(
        "--config",
        default="config/pipeline.json",
        help="Path to pipeline config JSON relative to project root.",
    )
    parser.add_argument(
        "--auto-commit",
        action="store_true",
        help="Whether to automatically commit the changes to Github without interactive confirmation."
    )
    return parser.parse_args()

def main() -> int:
    bootstrap_path()
    
    from aibeyin.config import load_pipeline_config
    from aibeyin.agents import MultiAgentSystem
    
    args = parse_args()
    project_root = Path(__file__).resolve().parents[1]
    config_path = project_root / args.config
    
    cfg = load_pipeline_config(config_path)
    
    if not cfg.data.get("multi_agent", {}).get("enabled", False):
         print("Error: Multi-agent system is not enabled in config.")
         return 1
         
    agent_sys = MultiAgentSystem(
         openrouter_config=cfg.openrouter,
         multi_agent_config=cfg.data.get("multi_agent", {})
    )
    
    # Run the coding task
    final_path = agent_sys.run_coding_task(args.task, project_root)
    
    # Git sync
    relative_path = os.path.relpath(final_path, project_root).replace("\\", "/")
    
    if args.auto_commit:
        do_commit = True
    else:
        answer = input(f"\nFinal code is located at: {relative_path}\nDo you want to commit and push this to Github? (y/n): ")
        do_commit = answer.strip().lower() == "y"
        
    if do_commit:
        print("[*] Committing to Github...")
        try:
             # Staging files include review logs and the final output
             subprocess.run(["git", "add", "src/output/", "logs/reviews/"], cwd=project_root, check=True)
             subprocess.run(["git", "commit", "-m", f"feat(ai-coder): generated code for '{args.task[:30]}...'"], cwd=project_root, check=True)
             subprocess.run(["git", "push"], cwd=project_root, check=True)
             print("[✅] Successfully pushed to Github!")
        except Exception as e:
             print(f"[❌] Git error: {e}")
             return 1
    else:
        print("[*] Operation finished without committing.")
        
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
