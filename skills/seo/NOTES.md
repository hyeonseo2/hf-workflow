# SEO Skill — Stage-1 notes & stage-2 handoff

Stage 1 = Module 1 deterministic gate + repeatable test harness. The rubric
(R1–R6) and Module 2 (metadata writer) are interface skeletons
(`tools/rubric.py`, `tools/metadata.py`).

## Applied from the PR #8 review (v1 gate tuning)

The review ran the gate over 31 real KREW posts and found most failures came from
checker assumptions clashing with the Jekyll rendering, not bad content. Applied:

- **Structure checks are now advisory, not gating.** D1 H1 count, D2 heading
  hierarchy, D3 opening length, D4 citations were downgraded `required → recommended`
  so they're reported but don't block. The Jekyll layout renders frontmatter
  `title` as the page H1, so KREW bodies legitimately start at `##`.
- **Body H1 of 0 is allowed.** `h1_count` passes for 0 or 1; only *multiple* body
  H1s flag (e.g. `ai-agents-are-here`, 6 `#`). The post no longer fails the gate.
- **Opening extraction skips boilerplate.** `get_opening_paragraphs` now skips
  HTML comments / `<!--toc-->` / `{:toc}` / `* TOC` / Liquid tags and the italic
  source-attribution line, so the opening reflects the real lede.
- **Alt-less `<img>` is detected.** `extract_images` reads `src`/`alt`
  independently, so `<figure><img src=…>` with no alt is captured (alt='') and
  fails D6 alt-coverage. `rteb` correctly fails now (it previously passed on the
  bug).
- **Keyword gate no longer needs a body H1.** `primary_keyword` (D5) gates on the
  opening paragraph only; H1 placement is reported for the metadata writer.
- **Citation dedup stays strict (correct).** `extract_links` doesn't count
  embedded images, so `medium-post`'s only "citation" (an image URL) doesn't
  count; D4 is now advisory anyway.

## Deferred gate-policy work (from the PR #8 review)

The review proposes a richer state model than the current binary pass/fail:

- **A `BLOCKED` tier for hard publish-blockers** not yet implemented: `robots:
  noindex`, broken internal links (resolved against the repo root), frontmatter
  parse failure, unreadable file. These should block regardless of body quality.
- **A `NEEDS_CHANGES` vs `ADVISORY` split** instead of one advisory bucket:
  description/alt/empty-body → NEEDS_CHANGES (comment, optionally block by team
  policy); H1/heading/opening/citations → ADVISORY.
- **Render-based structure checks.** Re-base D1/D2 on the rendered HTML (post
  Jekyll layout) rather than raw markdown, then promote back to a hard gate.

### Synthetic negative fixtures ready for the BLOCKED tier

`tests/fixtures/mutated/` (+ `generated/blocked-post.md`) hold one-mutation
negative samples, wired into the golden set and asserted in
`tests/test_mutated_fixtures.py`. Their current vs intended outcomes:

| Fixture | Current | Intended | Note |
|---|---|---|---|
| `mutated/missing-alt` | FAIL | FAIL | already gated (D6) ✅ |
| `mutated/missing-description` | PASS | PASS | metadata advisory ✅ |
| `mutated/short-opening` | PASS | PASS* | *short lede masked by 3-paragraph window — calibration gap |
| `mutated/noindex` | PASS | BLOCKED | needs BLOCKED tier |
| `generated/blocked-post` | PASS | BLOCKED | needs BLOCKED tier |
| `mutated/broken-internal-link` | PASS | BLOCKED | needs link resolution w/ `target_root` |

When the BLOCKED tier lands, flip the `TODO(BLOCKED tier)` asserts and
re-baseline the affected golden files.

## Deferred (out of stage-1 scope)

- Rubric R1–R6 LLM scoring + `deterministic AND rubric` integration.
- Module 2 metadata writer (frontmatter write-back, JSON-LD via `jekyll-seo-tag`,
  manifest `handoff.seo` record, canonical/hreflang).
- Realistic/harder golden fixtures + whether to keep the golden approach
  (provisional, agreed 2026-06-14).
- Activation trigger (manual / PR label / CI step) — stage 1 is trigger-agnostic.
- `tools/simple_seo_report.py` (legacy minimal checker) + its test can be removed
  once nothing references them.
