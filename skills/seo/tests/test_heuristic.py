"""Tests for the Tier-B Lighthouse heuristic score (requires markdown + bs4)."""
import pytest

pytest.importorskip("markdown")
pytest.importorskip("bs4")
from heuristic import compute_heuristic_seo  # noqa: E402


def test_heuristic_deterministic_and_scored():
    manifest = {"source": {"url": "https://huggingface.co/blog/x"},
                "translation": {"locale": "ko"}}
    body = "# 제목\n\n본문 [원문](https://huggingface.co/blog/x) 링크입니다."
    fm = {"title": "제목", "description": "설명", "permalink": "/p/"}

    a = compute_heuristic_seo(manifest, body, fm)
    b = compute_heuristic_seo(manifest, body, fm)
    assert a == b                       # deterministic
    assert 0 <= a["score"] <= 100
    assert a["mode"] == "heuristic"
    names = {x["name"] for x in a["audits"]}
    assert {"document-title", "meta-description", "hreflang", "canonical"} <= names
