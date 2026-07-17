"""Lighthouse-equivalent SEO sub-audits.

These reproduce the Lighthouse SEO audits that the project's existing checkers
(frontmatter / content / images) do not already cover, so the heuristic
benchmark (Tier B) can mirror Lighthouse's rubric on local files.

Each function returns a single audit row:
    {name, label, status: 'pass'|'fail'|'na', message}

`name` matches the Lighthouse audit id so Tier A and Tier B render the same
table. Inputs are the rendered post HTML (BeautifulSoup) plus frontmatter /
manifest — never a live URL.
"""
from __future__ import annotations

from typing import Any, Dict, List
from urllib.parse import urlparse

from bs4 import BeautifulSoup

# Generic anchor text Lighthouse flags as non-descriptive (link-text audit),
# plus the Korean equivalents this blog actually produces.
_GENERIC_LINK_TEXT = {
    "click here", "click", "here", "link", "read more", "more", "learn more",
    "this", "this page", "여기", "여기를", "여기를 클릭", "클릭", "링크",
    "더보기", "더 보기", "자세히", "자세히 보기", "바로가기",
}


def _row(name: str, label: str, ok: bool, msg: str) -> Dict[str, Any]:
    return {"name": name, "label": label, "status": "pass" if ok else "fail",
            "message": msg}


def _na(name: str, label: str, msg: str) -> Dict[str, Any]:
    return {"name": name, "label": label, "status": "na", "message": msg}


def audit_link_text(soup: BeautifulSoup) -> Dict[str, Any]:
    """Anchors should have descriptive text, not 'here' / '여기'."""
    anchors = [a for a in soup.find_all("a") if a.get("href")]
    if not anchors:
        return _na("link-text", "Links have descriptive text", "No links on page")
    bad = [a.get_text(strip=True) for a in anchors
           if a.get_text(strip=True).lower() in _GENERIC_LINK_TEXT
           or not a.get_text(strip=True)]
    if bad:
        sample = ", ".join(repr(t) for t in bad[:3])
        return _row("link-text", "Links have descriptive text", False,
                    f"{len(bad)}/{len(anchors)} links have generic text ({sample})")
    return _row("link-text", "Links have descriptive text", True,
                f"All {len(anchors)} links have descriptive text")


def audit_crawlable_anchors(soup: BeautifulSoup) -> Dict[str, Any]:
    """Links must be crawlable: a real href, not javascript:/empty/fragment-only."""
    anchors = soup.find_all("a")
    if not anchors:
        return _na("crawlable-anchors", "Links are crawlable", "No links on page")
    uncrawlable: List[str] = []
    for a in anchors:
        href = (a.get("href") or "").strip()
        if not href or href.startswith(("javascript:", "#")):
            uncrawlable.append(a.get_text(strip=True) or href or "<empty>")
    if uncrawlable:
        sample = ", ".join(repr(t) for t in uncrawlable[:3])
        return _row("crawlable-anchors", "Links are crawlable", False,
                    f"{len(uncrawlable)}/{len(anchors)} links not crawlable ({sample})")
    return _row("crawlable-anchors", "Links are crawlable", True,
                f"All {len(anchors)} links crawlable")


def audit_canonical(frontmatter: Dict[str, Any]) -> Dict[str, Any]:
    """Lighthouse wants exactly one valid canonical. Pre-publish we can only
    assert intent: a `canonical` or a `permalink` in frontmatter (Jekyll/SEO
    plugins emit <link rel=canonical> from these)."""
    canonical = frontmatter.get("canonical") or frontmatter.get("permalink")
    if not canonical:
        return _row("canonical", "Valid canonical", False,
                    "No canonical/permalink in frontmatter")
    if isinstance(canonical, str) and canonical.startswith("http"):
        parsed = urlparse(canonical)
        if not parsed.scheme or not parsed.netloc:
            return _row("canonical", "Valid canonical", False,
                        f"Malformed canonical: {canonical!r}")
    return _row("canonical", "Valid canonical", True, f"canonical: {canonical}")


def audit_hreflang(manifest: Dict[str, Any], soup: BeautifulSoup) -> Dict[str, Any]:
    """Lighthouse checks <link rel=alternate hreflang>. This is a translation
    workflow: the localized post should link back to the source-language
    original so search engines can pair them. We assert that intent by
    requiring the source URL to appear as a link in the post body."""
    src_url = (manifest.get("source", {}) or {}).get("url", "")
    locale = (manifest.get("translation", {}) or {}).get("locale", "")
    if not src_url:
        return _na("hreflang", "Valid hreflang",
                   "No source.url in manifest — cross-language pairing N/A")
    hrefs = {(a.get("href") or "").rstrip("/") for a in soup.find_all("a")}
    if src_url.rstrip("/") in hrefs:
        return _row("hreflang", "Valid hreflang", True,
                    f"Localized ({locale or '?'}) post links to source original")
    return _row("hreflang", "Valid hreflang", False,
                f"Post does not link to source original ({src_url}) for "
                f"cross-language pairing")
