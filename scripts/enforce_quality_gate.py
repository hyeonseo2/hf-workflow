from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections.abc import Callable
from pathlib import Path


QUALITY_CONTEXT = "hf-workflow/translation-quality"


def quality_status_state(status: str) -> tuple[str, str]:
    mapping = {
        "auto_pass": ("success", "Translation quality gate passed."),
        "review_required": ("success", "Quality checks passed; human review is required."),
        "reject": ("failure", "Translation quality gate rejected this revision."),
        "source_changed": ("failure", "Source changed; refresh and review the translation."),
    }
    return mapping.get(status, ("error", f"Unknown translation quality status: {status or 'missing'}."))


def parse_pr_url(pr_url: str) -> tuple[str, str] | None:
    match = re.fullmatch(r"https://github\.com/([^/]+/[^/]+)/pull/(\d+)/?", pr_url.strip())
    return match.groups() if match else None


def publish_target_status(
    repo: str,
    head_sha: str,
    state: str,
    description: str,
    *,
    gh_run: Callable[..., object] = subprocess.run,
) -> None:
    gh_run(
        [
            "gh",
            "api",
            f"repos/{repo}/statuses/{head_sha}",
            "-X",
            "POST",
            "-f",
            f"state={state}",
            "-f",
            f"context={QUALITY_CONTEXT}",
            "-f",
            f"description={description[:140]}",
        ],
        check=True,
    )


def enforce_quality_gate(
    summary_path: Path,
    reports_root: Path,
    *,
    target_root: Path = Path("target-repo"),
    gh_output: Callable[..., str] = subprocess.check_output,
    gh_run: Callable[..., object] = subprocess.run,
    git_output: Callable[..., bytes] = subprocess.check_output,
) -> list[str]:
    if not summary_path.exists():
        return [f"missing {summary_path}"]

    failures: list[str] = []
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    for result in summary.get("results", []):
        if result.get("status") != "created":
            continue
        slug = str(result.get("slug") or "unknown")
        parsed = parse_pr_url(str(result.get("pr_url") or ""))
        if parsed is None:
            failures.append(f"{slug}: invalid or missing PR URL")
            continue
        repo, pr_number = parsed
        evaluated_sha = str(result.get("commit_sha") or "")
        status_sha = evaluated_sha
        try:
            if evaluated_sha:
                publish_target_status(
                    repo,
                    evaluated_sha,
                    "pending",
                    "Translation quality verification is in progress.",
                    gh_run=gh_run,
                )
            pr = json.loads(gh_output(["gh", "api", f"repos/{repo}/pulls/{pr_number}"], text=True))
            head_sha = str(pr.get("head", {}).get("sha") or "")
            status_sha = head_sha or status_sha
            if not head_sha:
                failures.append(f"{slug}: target PR head SHA is missing")
                continue
            if not evaluated_sha:
                publish_target_status(
                    repo,
                    head_sha,
                    "error",
                    "Evaluated commit SHA is missing; rerun the quality workflow.",
                    gh_run=gh_run,
                )
                failures.append(f"{slug}: evaluated commit SHA is missing")
                continue
            if evaluated_sha != head_sha:
                publish_target_status(
                    repo,
                    head_sha,
                    "error",
                    "PR head changed after quality evaluation; rerun the workflow.",
                    gh_run=gh_run,
                )
                failures.append(f"{slug}: PR head changed after quality evaluation")
                continue

            report_path = reports_root / f"pr-{pr_number}" / "quality-report.json"
            if report_path.exists():
                report = json.loads(report_path.read_text(encoding="utf-8"))
                report_commit_sha = str(report.get("metadata", {}).get("target_commit_sha") or "")
                if report_commit_sha != evaluated_sha:
                    publish_target_status(
                        repo,
                        head_sha,
                        "error",
                        "Quality report commit does not match the evaluated revision.",
                        gh_run=gh_run,
                    )
                    failures.append(f"{slug}: report commit SHA does not match evaluated commit")
                    continue
                file_path = str(result.get("file_path") or "")
                report_target_hash = str(report.get("metadata", {}).get("target_hash") or "")
                if not file_path or not report_target_hash:
                    publish_target_status(
                        repo,
                        head_sha,
                        "error",
                        "Target path or report content hash is missing.",
                        gh_run=gh_run,
                    )
                    failures.append(f"{slug}: target path or report target hash is missing")
                    continue
                target_content = git_output(
                    ["git", "-C", str(target_root), "show", f"{evaluated_sha}:{file_path}"]
                )
                if isinstance(target_content, str):
                    target_content = target_content.encode("utf-8")
                evaluated_target_hash = hashlib.sha256(target_content).hexdigest()
                if evaluated_target_hash != report_target_hash:
                    publish_target_status(
                        repo,
                        head_sha,
                        "error",
                        "Quality report content hash does not match the evaluated revision.",
                        gh_run=gh_run,
                    )
                    failures.append(f"{slug}: report target hash does not match evaluated commit")
                    continue
                quality_status = str(report.get("status") or "")
                state, description = quality_status_state(quality_status)
            else:
                quality_status = "missing_report"
                state, description = "error", f"Quality report is missing: {report_path}."

            publish_target_status(repo, head_sha, state, description, gh_run=gh_run)
            print(f"Published {QUALITY_CONTEXT}={state} for {repo}@{head_sha} ({quality_status}).")
            if state in {"failure", "error"}:
                failures.append(f"{slug}: quality status={quality_status}")
        except Exception as exc:
            try:
                if status_sha:
                    publish_target_status(
                        repo,
                        status_sha,
                        "error",
                        "Translation quality verification failed unexpectedly.",
                        gh_run=gh_run,
                    )
            except Exception:
                pass
            failures.append(f"{slug}: quality verification error: {exc}")
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Publish translation quality status to target PR commits and enforce it.")
    parser.add_argument("--summary", default="run-summary.json")
    parser.add_argument("--reports-root", default="reports")
    parser.add_argument("--target-root", default="target-repo")
    args = parser.parse_args(argv)

    failures = enforce_quality_gate(
        Path(args.summary),
        Path(args.reports_root),
        target_root=Path(args.target_root),
    )
    if failures:
        print("Translation quality gate failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Translation quality gate found no blocking reports.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
