"""Metadata writer — Module 2.

STAGE-1 SKELETON. Runs only after the eval gate passes (design §2). It generates
SEO metadata and writes it back. Stage 1 ships the interface only;
``build_plan`` / ``apply`` raise ``NotImplementedError``.

Write-back targets (design §4):
  1. post ``.md`` frontmatter (yaml round-trip) — title / description / categories / image
  2. ``manifest.yaml`` ``handoff.seo`` — generated meta + eval result + rubric scores
  3. Schema.org JSON-LD — prefer the target's ``jekyll-seo-tag`` frontmatter fields
     (it already emits BlogPosting); inline only the fields the plugin omits
Plus, for this translation workflow (design §8):
  - canonical: language self-canonical
  - hreflang: ko ↔ en source bidirectional
  - visible date ↔ datePublished / dateModified consistency
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


@dataclass
class MetadataPlan:
    """The metadata the writer intends to apply to a passing post."""

    title: str = ""
    description: str = ""
    categories: list[str] = field(default_factory=list)
    image: str = ""
    canonical: str = ""
    hreflang: dict[str, str] = field(default_factory=dict)  # {"ko": url, "en": url}
    json_ld: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "description": self.description,
            "categories": self.categories,
            "image": self.image,
            "canonical": self.canonical,
            "hreflang": self.hreflang,
            "json_ld": self.json_ld,
        }


def build_plan(
    body: str,
    frontmatter: dict[str, Any],
    manifest: dict[str, Any],
    *,
    source_url: str = "",
    primary_keyword: str = "",
) -> MetadataPlan:
    """SKELETON: derive a MetadataPlan from a passing post. Lands in stage 2."""
    raise NotImplementedError("metadata writer lands in stage 2")


def apply(
    plan: MetadataPlan,
    post_path: Path,
    manifest_path: Optional[Path] = None,
) -> None:
    """SKELETON: write the plan back to the post (and manifest). Lands in stage 2."""
    raise NotImplementedError("metadata writer lands in stage 2")
