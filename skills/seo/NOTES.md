# SEO Skill — Stage-1 notes & stage-2 handoff

Stage 1 = Module 1 deterministic gate + repeatable test harness. The rubric
(R1–R6) and Module 2 (metadata writer) are interface skeletons
(`tools/rubric.py`, `tools/metadata.py`).

## Observations from verifying real KREW posts (for stage 2)

Found while baselining `tests/fixtures/real/*`. None are blockers; they inform
stage-2 tuning and were recorded so they aren't re-discovered later.

- **Citation dedup is now strict (correct).** `utils.extract_links` no longer
  counts embedded images, so `medium-post` (whose only "citation" was its image
  URL) correctly fails D4 with 0 real citations. The old design-doc baseline
  (medium = PASS) rode on the buggy count.
- **Opening extraction is boilerplate-sensitive.** `get_opening_paragraphs`
  takes the first non-heading paragraphs, which on KREW posts can be the `* TOC`
  / `_이 글은 … 번역한 글입니다._` lines rather than the real lede — e.g.
  `smolvla` reads as 24 *English* words and fails D3. Stage 2: skip the TOC and
  the source-attribution line before measuring the opening.
- **`<img>` without `alt` is not detected.** `utils.extract_images` only matches
  `<img>` tags that have BOTH `src` and `alt`. `rteb` uses `<figure><img src=…>`
  with no `alt`, so D6 alt-coverage is silently skipped and the post passes.
  Stage 2: detect alt-less `<img>` and fail D6.
- **Multiple H1s correctly fail.** `ai-agents-are-here` has 6 `#` headings →
  D1/D2 fail (genuinely poor structure).

## Deferred (out of stage-1 scope)

- Rubric R1–R6 LLM scoring + `deterministic AND rubric` integration.
- Module 2 metadata writer (frontmatter write-back, JSON-LD via `jekyll-seo-tag`,
  manifest `handoff.seo` record, canonical/hreflang).
- Realistic/harder golden fixtures + whether to keep the golden approach
  (provisional, agreed 2026-06-14).
- Activation trigger (manual / PR label / CI step) — stage 1 is trigger-agnostic.
- `tools/simple_seo_report.py` (legacy minimal checker) + its test can be removed
  once nothing references them.
