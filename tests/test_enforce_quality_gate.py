from __future__ import annotations

import json
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from enforce_quality_gate import enforce_quality_gate, quality_status_state


def test_quality_status_state_blocks_reject_and_source_changed() -> None:
    assert quality_status_state("auto_pass")[0] == "success"
    assert quality_status_state("review_required")[0] == "success"
    assert quality_status_state("reject")[0] == "failure"
    assert quality_status_state("source_changed")[0] == "failure"
    assert quality_status_state("unexpected")[0] == "error"


def test_enforce_quality_gate_publishes_status_to_target_pr_head(tmp_path: Path) -> None:
    summary = tmp_path / "run-summary.json"
    report = tmp_path / "reports" / "pr-42" / "quality-report.json"
    report.parent.mkdir(parents=True)
    summary.write_text(
        json.dumps(
            {
                "results": [
                    {
                        "status": "created",
                        "slug": "example",
                        "pr_url": "https://github.com/acme/blog/pull/42",
                        "commit_sha": "abc123",
                        "file_path": "_posts/example.md",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    report.write_text(
        json.dumps(
            {
                "status": "source_changed",
                "metadata": {
                    "target_commit_sha": "abc123",
                    "target_hash": hashlib.sha256(b"evaluated content\n").hexdigest(),
                },
            }
        ),
        encoding="utf-8",
    )
    calls: list[list[str]] = []

    def fake_output(cmd: list[str], **_: object) -> str:
        calls.append(cmd)
        return json.dumps({"head": {"sha": "abc123"}})

    def fake_run(cmd: list[str], **_: object) -> object:
        calls.append(cmd)
        return object()

    def fake_git_output(cmd: list[str], **_: object) -> bytes:
        calls.append(cmd)
        return b"evaluated content\n"

    failures = enforce_quality_gate(
        summary,
        tmp_path / "reports",
        gh_output=fake_output,
        gh_run=fake_run,
        git_output=fake_git_output,
    )

    assert failures == ["example: quality status=source_changed"]
    assert ["gh", "api", "repos/acme/blog/pulls/42"] in calls
    status_call = next(
        call for call in calls if "repos/acme/blog/statuses/abc123" in call and "state=failure" in call
    )
    assert "state=failure" in status_call
    assert "context=hf-workflow/translation-quality" in status_call
    assert ["git", "-C", "target-repo", "show", "abc123:_posts/example.md"] in calls


def test_enforce_quality_gate_never_publishes_stale_report_as_success(tmp_path: Path) -> None:
    summary = tmp_path / "run-summary.json"
    report = tmp_path / "reports" / "pr-42" / "quality-report.json"
    report.parent.mkdir(parents=True)
    summary.write_text(
        json.dumps(
            {
                "results": [
                    {
                        "status": "created",
                        "slug": "example",
                        "pr_url": "https://github.com/acme/blog/pull/42",
                        "commit_sha": "evaluated123",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    report.write_text(
        json.dumps({"status": "auto_pass", "metadata": {"target_commit_sha": "evaluated123"}}),
        encoding="utf-8",
    )
    calls: list[list[str]] = []

    def fake_output(cmd: list[str], **_: object) -> str:
        return json.dumps({"head": {"sha": "newhead456"}})

    def fake_run(cmd: list[str], **_: object) -> object:
        calls.append(cmd)
        return object()

    failures = enforce_quality_gate(
        summary,
        tmp_path / "reports",
        gh_output=fake_output,
        gh_run=fake_run,
    )

    assert failures == ["example: PR head changed after quality evaluation"]
    status_call = next(call for call in calls if "repos/acme/blog/statuses/newhead456" in call)
    assert "state=error" in status_call


def test_enforce_quality_gate_blocks_report_from_another_commit(tmp_path: Path) -> None:
    summary = tmp_path / "run-summary.json"
    report = tmp_path / "reports" / "pr-42" / "quality-report.json"
    report.parent.mkdir(parents=True)
    summary.write_text(
        json.dumps(
            {
                "results": [
                    {
                        "status": "created",
                        "slug": "example",
                        "pr_url": "https://github.com/acme/blog/pull/42",
                        "commit_sha": "expected123",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    report.write_text(
        json.dumps({"status": "auto_pass", "metadata": {"target_commit_sha": "stale999"}}),
        encoding="utf-8",
    )
    calls: list[list[str]] = []

    def fake_output(cmd: list[str], **_: object) -> str:
        return json.dumps({"head": {"sha": "expected123"}})

    def fake_run(cmd: list[str], **_: object) -> object:
        calls.append(cmd)
        return object()

    failures = enforce_quality_gate(
        summary,
        tmp_path / "reports",
        gh_output=fake_output,
        gh_run=fake_run,
    )

    assert failures == ["example: report commit SHA does not match evaluated commit"]
    status_call = next(
        call for call in calls if "repos/acme/blog/statuses/expected123" in call and "state=error" in call
    )
    assert "state=error" in status_call


def test_enforce_quality_gate_blocks_target_content_hash_mismatch(tmp_path: Path) -> None:
    summary = tmp_path / "run-summary.json"
    report = tmp_path / "reports" / "pr-42" / "quality-report.json"
    report.parent.mkdir(parents=True)
    summary.write_text(
        json.dumps(
            {
                "results": [
                    {
                        "status": "created",
                        "slug": "example",
                        "pr_url": "https://github.com/acme/blog/pull/42",
                        "commit_sha": "expected123",
                        "file_path": "_posts/example.md",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    report.write_text(
        json.dumps(
            {
                "status": "auto_pass",
                "metadata": {"target_commit_sha": "expected123", "target_hash": "stale-content-hash"},
            }
        ),
        encoding="utf-8",
    )
    calls: list[list[str]] = []

    def fake_output(cmd: list[str], **_: object) -> str:
        return json.dumps({"head": {"sha": "expected123"}})

    def fake_git_output(cmd: list[str], **_: object) -> bytes:
        return b"current content\n"

    def fake_run(cmd: list[str], **_: object) -> object:
        calls.append(cmd)
        return object()

    failures = enforce_quality_gate(
        summary,
        tmp_path / "reports",
        gh_output=fake_output,
        gh_run=fake_run,
        git_output=fake_git_output,
    )

    assert failures == ["example: report target hash does not match evaluated commit"]
    status_call = next(
        call for call in calls if "repos/acme/blog/statuses/expected123" in call and "state=error" in call
    )
    assert "state=error" in status_call


def test_enforce_quality_gate_fails_closed_when_validation_raises(tmp_path: Path) -> None:
    summary = tmp_path / "run-summary.json"
    report = tmp_path / "reports" / "pr-42" / "quality-report.json"
    report.parent.mkdir(parents=True)
    summary.write_text(
        json.dumps(
            {
                "results": [
                    {
                        "status": "created",
                        "slug": "example",
                        "pr_url": "https://github.com/acme/blog/pull/42",
                        "commit_sha": "expected123",
                        "file_path": "_posts/example.md",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    report.write_text(
        json.dumps(
            {
                "status": "auto_pass",
                "metadata": {"target_commit_sha": "expected123", "target_hash": "hash"},
            }
        ),
        encoding="utf-8",
    )
    calls: list[list[str]] = []

    def fake_output(cmd: list[str], **_: object) -> str:
        return json.dumps({"head": {"sha": "expected123"}})

    def failing_git_output(cmd: list[str], **_: object) -> bytes:
        raise OSError("git object unavailable")

    def fake_run(cmd: list[str], **_: object) -> object:
        calls.append(cmd)
        return object()

    failures = enforce_quality_gate(
        summary,
        tmp_path / "reports",
        gh_output=fake_output,
        gh_run=fake_run,
        git_output=failing_git_output,
    )

    assert failures == ["example: quality verification error: git object unavailable"]
    states = [part for call in calls for part in call if part.startswith("state=")]
    assert states == ["state=pending", "state=error"]
