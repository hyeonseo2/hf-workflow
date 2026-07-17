from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from generate_review_reports import generate_review_reports


def test_generate_review_reports_checks_out_each_created_commit(tmp_path: Path) -> None:
    summary = tmp_path / "run-summary.json"
    summary.write_text(
        json.dumps(
            {
                "results": [
                    {"status": "created", "commit_sha": "sha-one", "manifest_path": "manifests/one.yaml"},
                    {"status": "created", "commit_sha": "sha-two", "manifest_path": "manifests/two.yaml"},
                ]
            }
        ),
        encoding="utf-8",
    )
    calls: list[list[str]] = []

    def fake_run(cmd: list[str], **_: object) -> object:
        calls.append(cmd)
        return object()

    generate_review_reports(summary, Path("target-repo"), run=fake_run)

    assert calls == [
        ["git", "-C", "target-repo", "checkout", "--detach", "sha-one"],
        [
            "python",
            "scripts/run_local_review.py",
            "--manifest",
            "translation-flow/manifests/one.yaml",
            "--target-root",
            "target-repo",
        ],
        ["git", "-C", "target-repo", "checkout", "--detach", "sha-two"],
        [
            "python",
            "scripts/run_local_review.py",
            "--manifest",
            "translation-flow/manifests/two.yaml",
            "--target-root",
            "target-repo",
        ],
    ]
