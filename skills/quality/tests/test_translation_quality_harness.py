from __future__ import annotations

import json
import hashlib
from pathlib import Path

from tools.translation_quality_harness import (
    DEFAULT_MQM_PROMPT_PATH,
    DEFAULT_STYLE_GUIDE_PATH,
    MetricConfig,
    align_segments,
    build_report,
    load_mqm_prompt,
    main,
    markdown_doc,
    metric_cache_key,
    normalized_numbers,
    normalize_mqm_result,
    openai_mqm_task,
    style_guide_digest,
)


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


def test_harness_routes_good_translation_to_review_without_semantic_evaluation(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_good.md")

    report = build_report(manifest, FIXTURES, source_path=FIXTURES / "source.md")

    assert report["status"] == "review_required"
    assert report["hard_failures"] == []
    assert report["dimension_scores"]["publishing_integrity"] == 100.0
    assert report["metadata"]["source_segment_count"] == report["metadata"]["target_segment_count"]
    assert report["metadata"]["aligned_segment_count"] == report["metadata"]["source_segment_count"]
    assert report["metadata"]["target_source_length_ratio"] > 0
    assert report["segments"]["source"]
    assert report["segments"]["target"]
    assert report["segment_alignment"]


def test_harness_rejects_when_source_is_unavailable(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_good.md")

    report = build_report(manifest, FIXTURES, fetch_source_url=False)

    assert report["status"] == "reject"
    assert report["metadata"]["source_available"] is False
    assert any("Source document is unavailable" in issue["message"] for issue in report["hard_failures"])


def test_harness_does_not_auto_pass_unrelated_same_length_korean(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    target = tmp_path / "target.md"
    manifest = tmp_path / "manifest.yaml"
    source.write_text(
        """---
title: Original
---

# Technical update

This article explains a reliable process for teams working together in demanding production environments.
""",
        encoding="utf-8",
    )
    target.write_text(
        """---
title: 오늘의 점심 메뉴
---

# 주말 여행 계획

이번 글에서는 가족과 함께 떠나는 여름 바다 여행과 맛있는 지역 음식점에 관한 즐거운 경험을 자세히 소개합니다.
""",
        encoding="utf-8",
    )
    manifest.write_text(
        """version: 1
source:
  file_path: source.md
translation:
  file_path: target.md
""",
        encoding="utf-8",
    )

    report = build_report(manifest, tmp_path)

    assert report["metrics"]["summary"]["qe_average"] == 1.0
    assert report["status"] == "review_required"
    assert report["metadata"]["semantic_evaluation_complete"] is False


def test_harness_loads_evaluation_thresholds_from_config(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_good.md")
    config = tmp_path / "eval-config.yml"
    config.write_text(
        """version: 1
language:
  min_korean_letter_ratio: 0.99
""",
        encoding="utf-8",
    )

    report = build_report(
        manifest,
        FIXTURES,
        source_path=FIXTURES / "source.md",
        evaluation_config_path=config,
    )

    assert any("Korean letter ratio is low" in issue["message"] for issue in report["issues"])
    assert report["metadata"]["evaluation_config_path"] == str(config)


def test_harness_loads_number_gate_from_config(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    target = tmp_path / "target.md"
    manifest = tmp_path / "manifest.yaml"
    gates = tmp_path / "gates.yml"
    source.write_text("---\ntitle: Numbers\n---\n\nThe system uses 3 workers.\n", encoding="utf-8")
    target.write_text("---\ntitle: 숫자\n---\n\n시스템은 4개의 워커를 사용합니다.\n", encoding="utf-8")
    manifest.write_text(
        "version: 1\nsource:\n  file_path: source.md\ntranslation:\n  file_path: target.md\n",
        encoding="utf-8",
    )
    gates.write_text(
        "version: 1\nhard_gates:\n  numbers:\n    status: reject\n",
        encoding="utf-8",
    )

    report = build_report(manifest, tmp_path, gates_config_path=gates)

    assert any("number/unit token" in issue["message"] for issue in report["hard_failures"])
    assert report["metadata"]["gates_config_path"] == str(gates)


def test_harness_rejects_code_mutation(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_bad_code.md")

    report = build_report(manifest, FIXTURES, source_path=FIXTURES / "source.md")

    assert report["status"] == "reject"
    categories = {issue["category"] for issue in report["hard_failures"]}
    assert "technical" in categories


def test_harness_routes_number_mutation_to_review(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    target = tmp_path / "target.md"
    manifest = tmp_path / "manifest.yaml"
    source.write_text(
        """---
title: "Number Review"
---

# Number Review

The model has 3 layers and 20 checkpoints.
""",
        encoding="utf-8",
    )
    target.write_text(
        """---
title: "숫자 리뷰"
---

# 숫자 리뷰

이 모델에는 4개의 레이어와 20개의 체크포인트가 있습니다.
""",
        encoding="utf-8",
    )
    manifest.write_text(
        """version: 1
source:
  url: https://huggingface.co/blog/number-review
  title: Number Review
translation:
  file_path: target.md
""",
        encoding="utf-8",
    )

    report = build_report(manifest, tmp_path, source_path=source)

    assert report["status"] == "review_required"
    assert any("number/unit token" in issue["message"] for issue in report["issues"])
    assert not any("number/unit token" in issue["message"] for issue in report["hard_failures"])


def test_number_extraction_does_not_fold_next_word_into_unit() -> None:
    text = "56 Skill runs, 14 simulated rooms, 200 benchmarks, Step 2 should pass, 45s, 65B, 30%"

    assert normalized_numbers(text) == ["56", "14", "200", "2", "45s", "65B", "30%"]


def test_markdown_doc_numbers_ignore_links_code_and_html_attributes() -> None:
    doc = markdown_doc(
        """
[paper](https://arxiv.org/abs/2602.04998)
<div style="font-size: 1.1rem; padding: 1.5rem">Shown 30%</div>
`dev0`
"""
    )

    assert doc.link_targets == ["https://arxiv.org/abs/2602.04998"]
    assert doc.urls == []
    assert doc.numbers == ["30%"]


def test_markdown_doc_ignores_placeholder_markers_inside_code_blocks() -> None:
    doc = markdown_doc(
        """
```python
payload = {"extra_body": {"enable_thinking": False}}
```

This prose still has {{ unresolved marker.
"""
    )

    assert doc.todo_markers == ["{{"]


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
    assert any("Front matter key `authors`" in issue["message"] for issue in report["issues"])
    assert not any("Front matter key `authors`" in issue["message"] for issue in report["hard_failures"])
    assert any("Front matter key `thumbnail`" in issue["message"] for issue in report["hard_failures"])


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
    assert "Status: review_required" in output_md.read_text(encoding="utf-8")
    loaded = json.loads(output_json.read_text(encoding="utf-8"))
    assert loaded["status"] == "review_required"


def test_cli_fail_on_reject_returns_nonzero(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_bad_code.md")

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

    assert report["status"] == "review_required"
    assert report["metadata"]["source_changed"] is False


def test_harness_fetches_source_url_when_source_file_is_absent(tmp_path: Path) -> None:
    source_url = (FIXTURES / "source.md").resolve().as_uri()
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(
        f"""version: 1
source:
  url: {source_url}
  title: Testing Hugging Face Spaces
translation:
  file_path: target_good.md
""",
        encoding="utf-8",
    )

    report = build_report(manifest, FIXTURES)

    assert report["status"] == "review_required"
    assert report["metadata"]["source_available"] is True
    assert report["metadata"]["source_format"] == "url_markdown"
    assert report["metadata"]["source_path"] == source_url
    assert report["segment_alignment"]


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

    assert report["status"] == "review_required"
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

    assert report["status"] == "review_required"
    assert report["metrics"]["summary"]["qe_metric"] == "cometkiwi"
    assert "qe_average" in report["metrics"]["summary"]
    assert report["metrics"]["summary"]["warnings"]


def write_mqm_fixture(tmp_path: Path) -> Path:
    fixture = tmp_path / "mqm-fixture.jsonl"
    fixture.write_text(
        json.dumps(
            {
                "segment_id": "p_002",
                "adequacy_score": 0.41,
                "fluency_score": 0.90,
                "technical_score": 0.80,
                "errors": [
                    {
                        "guide_rule": "modal_strength",
                        "guide_section": "4. 의미·조건·확신의 강도는 절대 바꾸지 않습니다",
                        "category": "accuracy",
                        "severity": "major",
                        "source_span": "can be used",
                        "target_span": "사용됩니다",
                        "explanation": "가능성을 단정으로 바꾸었습니다.",
                        "suggested_fix": "사용할 수 있습니다",
                    }
                ],
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return fixture


def test_fixture_mqm_judge_routes_feedback_into_report(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_good.md")
    fixture = write_mqm_fixture(tmp_path)
    config = MetricConfig(
        qe_metric="off",
        enable_embedding_similarity=False,
        llm_judge_provider="fixture",
        llm_judge_fixture_path=fixture,
        llm_judge_max_segments=3,
    )

    report = build_report(manifest, FIXTURES, source_path=FIXTURES / "source.md", metric_config=config)

    assert report["status"] == "review_required"
    assert report["mqm_judge"]["enabled"] is True
    assert report["mqm_judge"]["provider"] == "fixture"
    assert report["mqm_judge"]["requested_segment_count"] == 3
    assert report["mqm_judge"]["segment_count"] == 1
    assert report["mqm_judge"]["error_count"] == 1
    assert report["dimension_scores"]["adequacy"] == 41.0
    assert report["style_guide"]["issue_count"] == 0
    assert any(issue["message"] == "MQM judge reported accuracy issue." for issue in report["issues"])


def test_complete_clean_mqm_evaluation_allows_auto_pass(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_good.md")
    source = markdown_doc((FIXTURES / "source.md").read_text(encoding="utf-8"))
    target = markdown_doc((FIXTURES / "target_good.md").read_text(encoding="utf-8"))
    fixture = tmp_path / "complete-mqm-fixture.jsonl"
    fixture.write_text(
        "\n".join(
            json.dumps(
                {
                    "segment_id": item["target_id"],
                    "adequacy_score": 1.0,
                    "fluency_score": 1.0,
                    "technical_score": 1.0,
                    "errors": [],
                },
                ensure_ascii=False,
            )
            for item in align_segments(source, target)
        )
        + "\n",
        encoding="utf-8",
    )
    config = MetricConfig(
        qe_metric="off",
        enable_embedding_similarity=False,
        llm_judge_provider="fixture",
        llm_judge_fixture_path=fixture,
    )

    report = build_report(manifest, FIXTURES, source_path=FIXTURES / "source.md", metric_config=config)

    assert report["status"] == "auto_pass"
    assert report["metadata"]["semantic_evaluation_complete"] is True
    assert not any("Semantic adequacy evaluation is incomplete" in issue["message"] for issue in report["issues"])


def test_mqm_judge_downgrades_wording_only_accuracy_major(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_good.md")
    fixture = tmp_path / "mqm-wording-fixture.jsonl"
    fixture.write_text(
        json.dumps(
            {
                "segment_id": "p_002",
                "adequacy_score": 0.92,
                "fluency_score": 0.88,
                "technical_score": 0.95,
                "errors": [
                    {
                        "guide_rule": "preserve_meaning",
                        "guide_section": "MQM judge",
                        "category": "accuracy",
                        "severity": "major",
                        "source_span": "What you cannot profile",
                        "target_span": "프로파일링할 수 없는 것은",
                        "explanation": "의미는 유지되지만 직역이라 다소 어색한 표현입니다.",
                        "suggested_fix": "더 자연스럽게 다듬습니다.",
                    }
                ],
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    config = MetricConfig(
        qe_metric="off",
        enable_embedding_similarity=False,
        llm_judge_provider="fixture",
        llm_judge_fixture_path=fixture,
        llm_judge_max_segments=3,
    )

    report = build_report(manifest, FIXTURES, source_path=FIXTURES / "source.md", metric_config=config)

    [segment] = report["mqm_judge"]["segments"]
    [error] = segment["errors"]
    assert error["category"] == "fluency"
    assert error["severity"] == "minor"
    assert any("downgraded" in warning for warning in report["mqm_judge"]["warnings"])
    assert any(issue["message"] == "MQM judge reported fluency issue." for issue in report["issues"])


def test_mqm_judge_keeps_modal_strength_accuracy_major() -> None:
    warnings: list[str] = []

    result = normalize_mqm_result(
        {
            "segment_id": "p_002",
            "adequacy_score": 0.92,
            "fluency_score": 0.88,
            "technical_score": 1.0,
            "errors": [
                {
                    "guide_rule": "modal_strength",
                    "guide_section": "4. 의미·조건·확신의 강도는 절대 바꾸지 않습니다",
                    "category": "accuracy",
                    "severity": "major",
                    "source_span": "may improve throughput; must set the token",
                    "target_span": "처리량을 개선합니다; 토큰을 설정하는 것이 좋습니다",
                    "explanation": "가능성 표현과 의무 표현의 강도가 달라진 표현입니다.",
                    "suggested_fix": "개선할 수 있습니다. 반드시 토큰을 설정해야 합니다.",
                }
            ],
        },
        "p_002",
        warnings,
    )

    assert result is not None
    [error] = result["errors"]
    assert error["category"] == "accuracy"
    assert error["severity"] == "major"
    assert not warnings


def test_openai_mqm_judge_skips_without_api_key(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_good.md")
    config = MetricConfig(
        qe_metric="off",
        enable_embedding_similarity=False,
        llm_judge_provider="openai",
        llm_judge_api_key_env="HF_WORKFLOW_TEST_MISSING_OPENAI_KEY",
        llm_judge_max_segments=1,
    )

    report = build_report(manifest, FIXTURES, source_path=FIXTURES / "source.md", metric_config=config)

    assert report["status"] == "review_required"
    assert report["mqm_judge"]["enabled"] is True
    assert report["mqm_judge"]["provider"] == "openai"
    assert report["mqm_judge"]["reasoning_effort"] == "minimal"
    assert report["mqm_judge"]["segment_count"] == 0
    assert any("HF_WORKFLOW_TEST_MISSING_OPENAI_KEY" in warning for warning in report["mqm_judge"]["warnings"])


def test_openai_mqm_task_requests_json_object() -> None:
    task = openai_mqm_task(
        {
            "target_id": "p_001",
            "source_text": "The model can run locally.",
            "target_text": "모델은 로컬에서 실행할 수 있습니다.",
        }
    )

    assert "JSON object" in task
    assert "output_contract" in task


def test_mqm_prompt_embeds_translation_guide_digest() -> None:
    prompt = load_mqm_prompt(DEFAULT_MQM_PROMPT_PATH, DEFAULT_STYLE_GUIDE_PATH)
    digest, digest_hash = style_guide_digest(DEFAULT_STYLE_GUIDE_PATH)

    assert "Embedded Korean Translation Guide Digest" in prompt
    assert digest_hash in prompt
    assert "의미·조건·확신의 강도" in prompt
    assert "Hugging Face Space" in prompt
    assert "copied verbatim" in prompt
    assert "Return strict JSON only" in prompt
    assert digest


def test_openai_mqm_judge_reuses_cached_segments_without_api_key(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_good.md")
    cache_path = tmp_path / "metric-cache.json"
    source = markdown_doc((FIXTURES / "source.md").read_text(encoding="utf-8"))
    target = markdown_doc((FIXTURES / "target_good.md").read_text(encoding="utf-8"))
    first_alignment = align_segments(source, target)[0]
    prompt_hash = hashlib.sha256(load_mqm_prompt(DEFAULT_MQM_PROMPT_PATH, DEFAULT_STYLE_GUIDE_PATH).encode("utf-8")).hexdigest()
    cache_key = metric_cache_key(
        f"mqm:gpt-5-nano:{prompt_hash}",
        str(first_alignment["source_hash"]),
        str(first_alignment["target_hash"]),
    )
    cache_path.write_text(
        json.dumps(
            {
                cache_key: {
                    "segment_id": first_alignment["target_id"],
                    "adequacy_score": 1.0,
                    "fluency_score": 1.0,
                    "technical_score": 1.0,
                    "errors": [],
                }
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    config = MetricConfig(
        qe_metric="off",
        enable_embedding_similarity=False,
        metric_cache_path=cache_path,
        llm_judge_provider="openai",
        llm_judge_api_key_env="HF_WORKFLOW_TEST_MISSING_OPENAI_KEY",
        llm_judge_max_segments=1,
    )

    report = build_report(manifest, FIXTURES, source_path=FIXTURES / "source.md", metric_config=config)

    assert report["status"] == "review_required"
    assert report["mqm_judge"]["segment_count"] == 1
    assert report["mqm_judge"]["cache_hits"] == 1
    assert report["mqm_judge"]["cache_misses"] == 0
    assert report["mqm_judge"]["style_guide_hash"] == style_guide_digest(DEFAULT_STYLE_GUIDE_PATH)[1]
    assert not report["mqm_judge"]["warnings"]


def test_cli_writes_mqm_judge_outputs(tmp_path: Path) -> None:
    manifest = manifest_for(tmp_path, "target_good.md")
    fixture = write_mqm_fixture(tmp_path)
    output_json = tmp_path / "quality-report.json"
    output_md = tmp_path / "quality-report.md"
    output_mqm = tmp_path / "mqm-judge.jsonl"

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
            "--output-mqm-judge-jsonl",
            str(output_mqm),
            "--qe-metric",
            "off",
            "--disable-embedding-similarity",
            "--llm-judge-provider",
            "fixture",
            "--llm-judge-fixture",
            str(fixture),
            "--llm-judge-max-segments",
            "3",
        ]
    )

    assert exit_code == 0
    assert "## MQM Judge" in output_md.read_text(encoding="utf-8")
    assert output_mqm.read_text(encoding="utf-8").strip()
    loaded = json.loads(output_json.read_text(encoding="utf-8"))
    assert loaded["mqm_judge"]["segment_count"] == 1


def style_manifest_for(tmp_path: Path, target_name: str) -> Path:
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(
        f"""version: 1
source:
  url: https://huggingface.co/blog/style-guide
  title: A simple guide to fine-tuning
translation:
  file_path: {target_name}
handoff:
  quality:
    enabled: true
    checks:
      - style_guide
""",
        encoding="utf-8",
    )
    return manifest


def test_style_guide_good_translation_requires_semantic_review(tmp_path: Path) -> None:
    manifest = style_manifest_for(tmp_path, "style_target_good.md")

    report = build_report(manifest, FIXTURES, source_path=FIXTURES / "style_source.md")

    assert report["status"] == "review_required"
    assert report["style_guide"]["enabled"] is True
    assert report["style_guide"]["issue_count"] == 0
    assert report["dimension_scores"]["style_locale"] == 100.0
    assert report["metadata"]["style_guide_path"].endswith("hf-blog-ko-translation-guide.md")
    assert report["metadata"]["style_policy_version"] == 1


def test_style_guide_bad_translation_reports_guide_rules(tmp_path: Path) -> None:
    manifest = style_manifest_for(tmp_path, "style_target_bad.md")

    report = build_report(manifest, FIXTURES, source_path=FIXTURES / "style_source.md")

    assert report["status"] == "review_required"
    assert report["style_guide"]["issue_count"] >= 8
    assert report["dimension_scores"]["style_locale"] < 100.0
    rules = {issue["guide_rule"] for issue in report["issues"] if issue["guide_rule"]}
    assert {
        "modal_strength",
        "overstatement",
        "translationese",
        "emoji_delta",
        "list_consistency",
        "title_quality",
        "alt_text_caption",
        "link_text_translation",
        "first_mention_bilingual",
        "information_addition",
    }.issubset(rules)
    for issue in report["issues"]:
        if issue["guide_rule"]:
            assert issue["guide_section"]


def test_style_guide_can_be_disabled(tmp_path: Path) -> None:
    manifest = style_manifest_for(tmp_path, "style_target_bad.md")

    report = build_report(
        manifest,
        FIXTURES,
        source_path=FIXTURES / "style_source.md",
        metric_config=MetricConfig(enable_style_guide=False),
    )

    assert report["style_guide"]["enabled"] is False
    assert all(not issue["guide_rule"] for issue in report["issues"])


def test_cli_writes_style_guide_section(tmp_path: Path) -> None:
    manifest = style_manifest_for(tmp_path, "style_target_bad.md")
    output_md = tmp_path / "quality-report.md"
    output_json = tmp_path / "quality-report.json"
    output_pr_comment = tmp_path / "pr-comment.md"

    exit_code = main(
        [
            "--manifest",
            str(manifest),
            "--target-root",
            str(FIXTURES),
            "--source",
            str(FIXTURES / "style_source.md"),
            "--output-md",
            str(output_md),
            "--output-json",
            str(output_json),
            "--output-pr-comment",
            str(output_pr_comment),
        ]
    )

    assert exit_code == 0
    markdown = output_md.read_text(encoding="utf-8")
    assert "## Style Guide" in markdown
    assert "## Style Guide Findings" in markdown
    loaded = json.loads(output_json.read_text(encoding="utf-8"))
    assert loaded["style_guide"]["issue_count"] >= 8
    pr_comment = output_pr_comment.read_text(encoding="utf-8")
    assert "Top Style Guide Findings" in pr_comment
    assert "modal_strength" in pr_comment
