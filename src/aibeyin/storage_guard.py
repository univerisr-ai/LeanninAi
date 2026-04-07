from pathlib import Path


def get_project_size_bytes(root: Path) -> int:
    total = 0
    for path in root.rglob("*"):
        if path.is_file():
            total += path.stat().st_size
    return total


def enforce_disk_quota(root: Path, limit_gb: float) -> None:
    size_bytes = get_project_size_bytes(root)
    limit_bytes = int(limit_gb * 1024 * 1024 * 1024)
    if size_bytes > limit_bytes:
        raise RuntimeError(
            f"Project disk quota exceeded: {size_bytes} > {limit_bytes}. "
            "No new writes are allowed."
        )
