"""Tier B: Lighthouse-SEO-equivalent heuristic score.

Computes a 0-100 SEO score from local files only (rendered HTML + frontmatter
+ manifest), mirroring Lighthouse's SEO audit set. Used when the Lighthouse
toolchain is unavailable.

Scoring matches Lighthouse: every scored content audit carries equal weight,
so the score is the share of *applicable* audits that pass. Audits that
genuinely cannot be determined from local files (server status, robots,
structured data, rendered font/tap sizing) are reported as N/A and excluded
from the denominator — keeping the scale comparable to Tier A.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List

import markdown
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))
from checkers.seo_audits import (  # noqa: E402
    audit_canonical,
    audit_crawlable_anchors,
    audit_hreflang,
    audit_link_text,
)
from utils import extract_images  # noqa: E402

# Lighthouse calls >= 0.90 "good". Mirror it (kept local to avoid a circular
# import with benchmark.py).
GOOD_SCORE = 90

# Lighthouse SEO audits that depend on the live server, robots directives, or
# real rendered geometry — not derivable from a pre-publish markdown file.
_NA_AUDITS = [
    ("is-crawlable", "Page is indexable (robots)"),
    ("http-status-code", "Page has successful HTTP status"),
    ("robots-txt", "robots.txt is valid"),
    ("structured-data", "Structured data is valid"),
    ("font-legibility", "Legible font sizes"),
    ("tap-targets", "Tap targets sized correctly"),
]


def _audit_title(frontmatter: Dict[str, Any]) -> Dict[str, Any]:
    title = str(frontmatter.get("title", "")).strip()
    ok = bool(title)
    return {"name": "document-title", "label": "Document has a <title>",
            "status": "pass" if ok else "fail",
            "message": f"title: {title!r}" if ok else "Missing frontmatter title"}


def _audit_meta_description(frontmatter: Dict[str, Any]) -> Dict[str, Any]:
    desc = str(frontmatter.get("description", "")).strip()
    ok = bool(desc)
    return {"name": "meta-description", "label": "Has a meta description",
            "status": "pass" if ok else "fail",
            "message": (f"description present ({len(desc)} chars)" if ok
                        else "Missing frontmatter description")}


def _audit_image_alt(body: str) -> Dict[str, Any]:
    images = extract_images(body)
    if not images:
        return {"name": "image-alt", "label": "Images have alt text",
                "status": "na", "message": "No images on page"}
    missing = [i["src"] for i in images if not i.get("alt", "").strip()]
    ok = not missing
    return {"name": "image-alt", "label": "Images have alt text",
            "status": "pass" if ok else "fail",
            "message": (f"All {len(images)} images have alt text" if ok
                        else f"{len(missing)}/{len(images)} images missing alt text")}


def compute_heuristic_seo(
    manifest: Dict[str, Any], body: str, frontmatter: Dict[str, Any]
) -> Dict[str, Any]:
    """Return {mode, score, audits[], passed} — `fallback_reason` is set by
    the caller (benchmark.run_benchmark)."""
    html = markdown.markdown(body, extensions=["extra"])
    soup = BeautifulSoup(html, "html.parser")

    audits: List[Dict[str, Any]] = [
        _audit_title(frontmatter),
        _audit_meta_description(frontmatter),
        _audit_image_alt(body),
        audit_link_text(soup),
        audit_crawlable_anchors(soup),
        audit_canonical(frontmatter),
        audit_hreflang(manifest, soup),
    ]
    audits += [
        {"name": n, "label": label, "status": "na",
         "message": "Not determinable pre-publish (heuristic mode)"}
        for n, label in _NA_AUDITS
    ]

    scorable = [a for a in audits if a["status"] in ("pass", "fail")]
    passed_n = sum(1 for a in scorable if a["status"] == "pass")
    score = round(100 * passed_n / len(scorable)) if scorable else 0

    return {
        "mode": "heuristic",
        "score": score,
        "fallback_reason": None,
        "audits": audits,
        "passed": score >= GOOD_SCORE,
    }
