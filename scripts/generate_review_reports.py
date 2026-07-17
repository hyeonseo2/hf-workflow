from __future__ import annotations

import argparse
import json
import subprocess
from collections.abc import Callable
from pathlib import Path


def workflow_manifest_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute() or (path.parts and path.parts[0] == "translation-flow"):
        return path
    return Path("translation-flow") / path


def generate_review_reports(
    summary_path: Path,
    target_root: Path,
    *,
    run: Callable[..., object] = subprocess.run,
) -> None:
    if not summary_path.exists():
        raise FileNotFoundError(f"Run summary not found: {summary_path}")
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    for result in summary.get("results", []):
        if result.get("status") != "created":
            continue
        commit_sha = str(result.get("commit_sha") or "")
        if not commit_sha:
            raise ValueError(f"Created result is missing commit_sha: {result.get('slug') or 'unknown'}")
        manifest = workflow_manifest_path(str(result.get("manifest_path") or ""))
        run(
            ["git", "-C", str(target_root), "checkout", "--detach", commit_sha],
            check=True,
        )
        run(
            [
                "python",
                "scripts/run_local_review.py",
                "--manifest",
                str(manifest),
                "--target-root",
                str(target_root),
            ],
            check=True,
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate SEO and quality reports for exact translated commits.")
    parser.add_argument("--summary", default="run-summary.json")
    parser.add_argument("--target-root", default="target-repo")
    args = parser.parse_args(argv)
    generate_review_reports(Path(args.summary), Path(args.target_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
