from __future__ import annotations

import json
import hashlib
from pathlib import Path

from tools.translation_quality_harness import MetricConfig, build_report, main


FIXTURES = Path(__file__).parent / "fixtures" / "translation_quality_harness"


def manifest_for(tmp_path: Path, target_name: str) -> Path:
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(
        f"""version: 1
source:
  url: https://huggingface.co/blog/testing-spaces
  title: Testing Hugging Face Spaces
translation:
  file_path: {target_name}
handoff:
  quality:
    enabled: true
    checks:
      - hard_gates
""",
        encoding="utf-8",
    )
    return manifest


def manifest_with_source_hash(tmp_path: Path, target_name: str, source_hash: str) -> Path:
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(
        f"""version: 1
source:
  url: https://huggingface.co/blog/testing-spaces
  title: Testing Hugging Face Spaces
  hash: {source_hash}
translation:
  file_path: {target_name}
handoff:
  quality:
    enabled: true
    checks:
      - hard_gates
      - segments
      - glossary
""",
        encoding="utf-8",
    )
    return manifest


def test_harness_accepts_good_translation_without_hard_failures(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_good.md")

    report = build_report(manifest, FIXTURES, source_path=FIXTURES / "source.md")

    assert report["status"] == "auto_pass"
    assert report["hard_failures"] == []
    assert report["dimension_scores"]["publishing_integrity"] == 100.0
    assert report["metadata"]["source_segment_count"] == report["metadata"]["target_segment_count"]
    assert report["metadata"]["aligned_segment_count"] == report["metadata"]["source_segment_count"]
    assert report["metadata"]["target_source_length_ratio"] > 0
    assert report["segments"]["source"]
    assert report["segments"]["target"]
    assert report["segment_alignment"]


def test_harness_rejects_code_mutation(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_bad_code.md")

    report = build_report(manifest, FIXTURES, source_path=FIXTURES / "source.md")

    assert report["status"] == "reject"
    categories = {issue["category"] for issue in report["hard_failures"]}
    assert "technical" in categories


def test_harness_rejects_number_mutation(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_bad_number.md")

    report = build_report(manifest, FIXTURES, source_path=FIXTURES / "source.md")

    assert report["status"] == "reject"
    assert any("number/unit token" in issue["message"] for issue in report["hard_failures"])


def test_harness_rejects_link_and_image_mutation(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_bad_link.md")

    report = build_report(manifest, FIXTURES, source_path=FIXTURES / "source.md")

    assert report["status"] == "reject"
    messages = "\n".join(issue["message"] for issue in report["hard_failures"])
    assert "link target mismatch" in messages
    assert "image target mismatch" in messages


def test_harness_rejects_frontmatter_mutation(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_bad_frontmatter.md")

    report = build_report(manifest, FIXTURES, source_path=FIXTURES / "source.md")

    assert report["status"] == "reject"
    assert any("Front matter key `authors`" in issue["message"] for issue in report["hard_failures"])


def test_harness_rejects_table_and_latex_mutation(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_bad_table_latex.md")

    report = build_report(manifest, FIXTURES, source_path=FIXTURES / "source.md")

    assert report["status"] == "reject"
    messages = "\n".join(issue["message"] for issue in report["hard_failures"])
    assert "Markdown table shape mismatch" in messages
    assert "LaTeX token mismatch" in messages


def test_cli_writes_markdown_and_json_reports(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_good.md")
    output_md = tmp_path / "quality-report.md"
    output_json = tmp_path / "quality-report.json"

    exit_code = main(
        [
            "--manifest",
            str(manifest),
            "--target-root",
            str(FIXTURES),
            "--source",
            str(FIXTURES / "source.md"),
            "--output-md",
            str(output_md),
            "--output-json",
            str(output_json),
            "--fail-on-reject",
        ]
    )

    assert exit_code == 0
    assert "Status: auto_pass" in output_md.read_text(encoding="utf-8")
    loaded = json.loads(output_json.read_text(encoding="utf-8"))
    assert loaded["status"] == "auto_pass"


def test_cli_fail_on_reject_returns_nonzero(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_bad_number.md")

    exit_code = main(
        [
            "--manifest",
            str(manifest),
            "--target-root",
            str(FIXTURES),
            "--source",
            str(FIXTURES / "source.md"),
            "--output-md",
            str(tmp_path / "quality-report.md"),
            "--output-json",
            str(tmp_path / "quality-report.json"),
            "--fail-on-reject",
        ]
    )

    assert exit_code == 1


def test_harness_reports_glossary_violation_as_terminology(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_bad_glossary.md")

    report = build_report(manifest, FIXTURES, source_path=FIXTURES / "source.md")

    assert report["status"] == "review_required"
    assert any(issue["category"] == "terminology" for issue in report["issues"])
    assert report["dimension_scores"]["terminology"] < 100.0


def test_harness_detects_additional_and_duplicate_segments(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_bad_addition_duplicate.md")

    report = build_report(manifest, FIXTURES, source_path=FIXTURES / "source.md")

    assert report["status"] == "review_required"
    messages = "\n".join(issue["message"] for issue in report["issues"])
    assert "Target has additional text segments" in messages
    assert "Duplicate target segments detected" in messages
    assert report["dimension_scores"]["completeness"] < 100.0


def test_harness_detects_omitted_segments(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_bad_omission.md")

    report = build_report(manifest, FIXTURES, source_path=FIXTURES / "source.md")

    messages = "\n".join(issue["message"] for issue in report["issues"])
    assert "Source segment coverage is low" in messages


def test_harness_reports_source_changed_from_manifest_hash(tmp_path: Path) -> None:
    manifest = manifest_with_source_hash(tmp_path, "target_good.md", "not-the-current-source-hash")

    report = build_report(manifest, FIXTURES, source_path=FIXTURES / "source.md")

    assert report["status"] == "source_changed"
    assert report["metadata"]["source_changed"] is True
    assert any("Source hash changed" in issue["message"] for issue in report["issues"])


def test_harness_accepts_matching_manifest_source_hash(tmp_path: Path) -> None:
    source_text = (FIXTURES / "source.md").read_text(encoding="utf-8")
    source_hash = hashlib.sha256(source_text.encode("utf-8")).hexdigest()
    manifest = manifest_with_source_hash(tmp_path, "target_good.md", source_hash)

    report = build_report(manifest, FIXTURES, source_path=FIXTURES / "source.md")

    assert report["status"] == "auto_pass"
    assert report["metadata"]["source_changed"] is False


def test_cli_writes_segment_jsonl_and_reads_translation_memory(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_good.md")
    output_source_segments = tmp_path / "source-segments.jsonl"
    output_target_segments = tmp_path / "target-segments.jsonl"
    output_json = tmp_path / "quality-report.json"

    exit_code = main(
        [
            "--manifest",
            str(manifest),
            "--target-root",
            str(FIXTURES),
            "--source",
            str(FIXTURES / "source.md"),
            "--translation-memory",
            str(FIXTURES / "translation_memory.jsonl"),
            "--output-md",
            str(tmp_path / "quality-report.md"),
            "--output-json",
            str(output_json),
            "--output-source-segments",
            str(output_source_segments),
            "--output-target-segments",
            str(output_target_segments),
        ]
    )

    assert exit_code == 0
    assert output_source_segments.read_text(encoding="utf-8").strip()
    assert output_target_segments.read_text(encoding="utf-8").strip()
    loaded = json.loads(output_json.read_text(encoding="utf-8"))
    assert loaded["metadata"]["translation_memory_entry_count"] == 2
    assert loaded["metadata"]["translation_memory_match_count"] >= 1


def write_metric_fixture(tmp_path: Path, target_body: str) -> tuple[Path, Path]:
    source = tmp_path / "source.md"
    target = tmp_path / "target.md"
    manifest = tmp_path / "manifest.yaml"
    source.write_text(
        """---
title: "Simple Review"
---

# Simple Review

This article explains a careful review process for a long technical post.

The workflow helps reviewers find risky segments before publication.
""",
        encoding="utf-8",
    )
    target.write_text(
        f"""---
title: "간단한 리뷰"
---

{target_body}
""",
        encoding="utf-8",
    )
    manifest.write_text(
        """version: 1
source:
  url: https://huggingface.co/blog/simple-review
  title: Simple Review
translation:
  file_path: target.md
""",
        encoding="utf-8",
    )
    return manifest, source


def test_qe_metric_can_be_disabled(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_good.md")

    report = build_report(
        manifest,
        FIXTURES,
        source_path=FIXTURES / "source.md",
        metric_config=MetricConfig(qe_metric="off", enable_embedding_similarity=False),
    )

    assert report["status"] == "auto_pass"
    assert report["metrics"]["summary"]["qe_enabled"] is False
    assert report["metrics"]["summary"]["embedding_similarity_enabled"] is False
    assert all("QE metric score is low" not in issue["message"] for issue in report["issues"])


def test_low_qe_segment_routes_to_review_required(tmp_path: Path) -> None:
    manifest, source = write_metric_fixture(
        tmp_path,
        """# 간단한 리뷰

짧음.

부족.
""",
    )

    report = build_report(manifest, tmp_path, source_path=source, metric_config=MetricConfig(qe_review_threshold=0.70))

    assert report["status"] == "review_required"
    assert report["metrics"]["summary"]["qe_enabled"] is True
    assert report["metrics"]["summary"]["qe_min"] < 0.70
    assert any(issue["message"] == "QE metric score is low." for issue in report["issues"])


def test_metric_cache_records_hits_on_second_run(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_good.md")
    cache_path = tmp_path / "metric-cache.json"
    config = MetricConfig(metric_cache_path=cache_path)

    first = build_report(manifest, FIXTURES, source_path=FIXTURES / "source.md", metric_config=config)
    second = build_report(manifest, FIXTURES, source_path=FIXTURES / "source.md", metric_config=config)

    assert cache_path.exists()
    assert first["metrics"]["summary"]["cache_misses"] > 0
    assert second["metrics"]["summary"]["cache_hits"] > 0


def test_chrf_reference_metric_is_reported(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_good.md")
    config = MetricConfig(enable_chrf=True, reference_path=FIXTURES / "target_good.md")

    report = build_report(manifest, FIXTURES, source_path=FIXTURES / "source.md", metric_config=config)

    assert report["metrics"]["summary"]["chrf_enabled"] is True
    assert report["metrics"]["summary"]["chrf_average"] == 1.0


def test_cometkiwi_wrapper_falls_back_without_breaking_deterministic_gates(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_good.md")
    config = MetricConfig(qe_metric="cometkiwi")

    report = build_report(manifest, FIXTURES, source_path=FIXTURES / "source.md", metric_config=config)

    assert report["status"] == "auto_pass"
    assert report["metrics"]["summary"]["qe_metric"] == "cometkiwi"
    assert "qe_average" in report["metrics"]["summary"]
    assert report["metrics"]["summary"]["warnings"]
