"""Behavioral assertions for the synthetic negative ("mutated") fixtures.

Each fixture mutates one thing on an otherwise-clean post. This pins what the
**current v1 gate** does with each — distinct from the golden snapshot (which
only verifies stability). Intended-but-not-yet-implemented outcomes (the BLOCKED
tier: noindex / broken internal links) are asserted at their *current* behavior
and flagged here so they re-baseline when that tier lands (see NOTES.md).
"""
import pytest

from seo_eval import evaluate_path
from utils import parse_frontmatter

MUTATED = "mutated"


def _eval(fixtures_dir, rel, **kw):
    return evaluate_path(fixtures_dir / f"{rel}.md", **kw)


def test_missing_alt_fails_body_gate(fixtures_dir):
    # Empty image alt is a real body-quality failure and DOES block (D6).
    r = _eval(fixtures_dir, f"{MUTATED}/missing-alt")
    assert r["gate"]["passed"] is False
    failed = {c["name"] for c in r["deterministic"]["required"]["checks"] if not c["passed"]}
    assert "alt_text_coverage" in failed


def test_missing_description_passes_body_gate(fixtures_dir):
    # Metadata is advisory and written after a pass, so a missing description
    # must NOT block the body gate; it surfaces as frontmatter advisory.
    r = _eval(fixtures_dir, f"{MUTATED}/missing-description")
    assert r["gate"]["passed"] is True
    fm = {c["name"]: c for c in r["frontmatter_advisory"]["checks"]}
    assert fm["description"]["passed"] is False


def test_short_opening_not_caught_needs_calibration(fixtures_dir):
    # KNOWN GAP (rule needs calibration): a very short *first* paragraph is masked
    # because opening_summary measures the first 3 paragraphs combined, so the
    # later paragraphs push it over the threshold and it passes. Pinned here so
    # the calibration work has a regression anchor. opening_summary is advisory
    # in v1 regardless, so the gate also passes.
    r = _eval(fixtures_dir, f"{MUTATED}/short-opening")
    assert r["gate"]["passed"] is True
    opening = next(c for c in r["deterministic"]["advisory"]["checks"]
                   if c["name"] == "opening_summary")
    assert opening["passed"] is True  # TODO(calibration): should detect short lede


@pytest.mark.parametrize("rel", ["mutated/noindex", "generated/blocked-post"])
def test_noindex_not_yet_blocked(fixtures_dir, rel):
    # INTENDED: BLOCKED. The v1 gate has no BLOCKED tier yet and does not gate on
    # frontmatter, so `robots: noindex` currently passes the body gate. When the
    # BLOCKED tier lands this assertion flips (see NOTES.md).
    fm, _ = parse_frontmatter((fixtures_dir / f"{rel}.md").read_text(encoding="utf-8"))
    assert fm.get("robots") == "noindex"  # the fixture really carries the blocker
    r = _eval(fixtures_dir, rel)
    assert r["gate"]["passed"] is True  # TODO(BLOCKED tier): expect blocked


def test_broken_internal_link_not_yet_blocked(fixtures_dir):
    # INTENDED: BLOCKED when evaluated with a target_root (link must resolve to a
    # real file/page). Link resolution isn't implemented yet, so it passes today.
    r = _eval(fixtures_dir, f"{MUTATED}/broken-internal-link")
    assert r["gate"]["passed"] is True  # TODO(BLOCKED tier): expect blocked w/ target_root
