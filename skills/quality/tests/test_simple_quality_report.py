from __future__ import annotations

from pathlib import Path

from tools.simple_quality_report import build_report


def test_build_report(tmp_path: Path) -> None:
    target = tmp_path / "target"
    post = target / "_posts" / "post.md"
    post.parent.mkdir(parents=True)
    post.write_text(
        """---
title: "테스트"
source_url: "https://huggingface.co/blog/test"
---
> Source: https://huggingface.co/blog/test

# 테스트

한국어 본문입니다. 충분한 길이의 한국어 문장을 포함합니다.

```
print("hello")
```
"""
    )
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(
        """source:
  url: https://huggingface.co/blog/test
translation:
  file_path: _posts/post.md
"""
    )

    report = build_report(manifest, target)

    assert "PASS: code fences are balanced" in report
    assert "PASS: source attribution exists" in report
