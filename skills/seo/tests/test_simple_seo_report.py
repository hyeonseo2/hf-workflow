from __future__ import annotations

from pathlib import Path

from tools.simple_seo_report import build_report


def test_build_report(tmp_path: Path) -> None:
    target = tmp_path / "target"
    post = target / "_posts" / "post.md"
    post.parent.mkdir(parents=True)
    post.write_text(
        """---
layout: post
title: "테스트"
categories: [Translation]
slug: "test"
source_url: "https://huggingface.co/blog/test"
---
_이 글은 Hugging Face 블로그의 원문을 한국어로 번역한 글입니다._
# 테스트
## 하나
## 둘
## 셋
"""
    )
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(
        """source:
  url: https://huggingface.co/blog/test
  title: "Test"
translation:
  file_path: _posts/post.md
"""
    )

    report = build_report(manifest, target)

    assert "PASS: frontmatter title exists" in report
    assert "PASS: has at least three section headings" in report
