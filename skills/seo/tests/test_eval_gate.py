"""Tests for the orchestrator's body-only AND gate composition."""
from seo_eval import evaluate_path

GOOD_KO = (
    "---\ntitle: x\n---\n"
    "# 검색 임베딩 벤치마크 입문\n\n"
    "검색 임베딩 벤치마크는 임베딩 모델의 실제 검색 정확도를 신뢰성 있게 측정하기 위한 평가 "
    "도구입니다. 공개 데이터셋과 비공개 데이터셋을 함께 사용하면 모델이 학습하지 않은 데이터에 "
    "대한 일반화 능력을 더 공정하게 측정할 수 있습니다. 자세한 내용은 원문 "
    "[블로그](https://huggingface.co/blog/rteb)에서 확인하세요.\n\n"
    "## 무엇을 측정하는가?\n\n측정 내용을 설명합니다."
)


def _write(tmp_path, text):
    p = tmp_path / "post.md"
    p.write_text(text, encoding="utf-8")
    return p


def test_gate_passes_on_good_post(tmp_path):
    r = evaluate_path(_write(tmp_path, GOOD_KO))
    assert r["gate"]["deterministic_passed"]
    assert r["gate"]["passed"]


def test_gate_passes_without_body_h1(tmp_path):
    # KREW posts start at `##` (Jekyll renders the frontmatter title as the H1),
    # so a body with no H1 must NOT block the gate (PR #8 review). h1_count is now
    # advisory and a body H1 of 0 passes.
    body = "---\ntitle: x\n---\n## 소제목만\n\n" + "본문 문장입니다. " * 20
    r = evaluate_path(_write(tmp_path, body))
    assert r["gate"]["passed"]
    h1 = next(c for c in r["deterministic"]["advisory"]["checks"] if c["name"] == "h1_count")
    assert h1["passed"] and h1["value"] == 0


def test_structure_checks_are_advisory_not_gated(tmp_path):
    # D1–D4 (h1/heading/opening/citations) were downgraded to advisory in v1 so
    # the gate no longer over-blocks on raw-markdown structure assumptions.
    r = evaluate_path(_write(tmp_path, GOOD_KO))
    required = {c["name"] for c in r["deterministic"]["required"]["checks"]}
    advisory = {c["name"] for c in r["deterministic"]["advisory"]["checks"]}
    downgraded = {"h1_count", "heading_hierarchy", "opening_summary", "citations"}
    assert downgraded.isdisjoint(required)
    assert downgraded <= advisory
    assert "word_count" not in required           # optional (D11)
    assert "internal_links" not in required        # recommended (D9)


def test_rubric_is_skeleton_and_gate_falls_back(tmp_path):
    r = evaluate_path(_write(tmp_path, GOOD_KO))
    assert r["rubric"]["available"] is False
    assert r["rubric"]["passed"] is None
    assert r["gate"]["rubric_passed"] is None
    assert r["gate"]["passed"] == r["gate"]["deterministic_passed"]
