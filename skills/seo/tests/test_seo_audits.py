"""Tests for Lighthouse-equivalent sub-audits (requires beautifulsoup4)."""
import pytest

pytest.importorskip("bs4")
from bs4 import BeautifulSoup  # noqa: E402
from checkers.seo_audits import (  # noqa: E402
    audit_link_text,
    audit_crawlable_anchors,
    audit_canonical,
    audit_hreflang,
)


def _soup(html):
    return BeautifulSoup(html, "html.parser")


def test_link_text_flags_generic_korean():
    assert audit_link_text(_soup('<a href="/x">여기</a>'))["status"] == "fail"
    assert audit_link_text(_soup('<a href="/x">검색 임베딩 벤치마크</a>'))["status"] == "pass"


def test_crawlable_anchors():
    assert audit_crawlable_anchors(_soup('<a href="#">x</a>'))["status"] == "fail"
    assert audit_crawlable_anchors(_soup('<a href="/real">x</a>'))["status"] == "pass"


def test_canonical_from_frontmatter():
    assert audit_canonical({"permalink": "/p/"})["status"] == "pass"
    assert audit_canonical({})["status"] == "fail"


def test_hreflang_requires_source_link():
    manifest = {"source": {"url": "https://huggingface.co/blog/x"},
                "translation": {"locale": "ko"}}
    assert audit_hreflang(
        manifest, _soup('<a href="https://huggingface.co/blog/x">원문</a>')
    )["status"] == "pass"
    assert audit_hreflang(manifest, _soup('<p>no link</p>'))["status"] == "fail"
