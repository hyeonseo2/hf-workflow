# SEO Skill — Agent Guide

Evaluate/improve one HF KREW blog post for SEO/GEO. Translation quality is out of
scope (separate quality skill).

**Entry point:** `tools/seo_eval.py` — body-only deterministic gate (D1–D7) plus a
rubric seam (`tools/rubric.py`, stage-2 skeleton). Metadata writing lives in
`tools/metadata.py` (stage-2 skeleton).

Workflow:
1. Get inputs — a `translation-flow` manifest (`--manifest`, PR flow) or a post
   path (`--file --target-root`, published flow).
2. Run the eval: `python tools/seo_eval.py ...` → markdown report + JSON, exit 0/1.
3. On fail, return the feedback (the failing REQUIRED checks).
4. On pass, the metadata writer (Module 2) generates frontmatter / JSON-LD.

Rules:
- Eval gates the **body** only (structure / keyword / images). Frontmatter is
  written after a pass, never gated.
- v1 gate is conservative: only image alt/file (D6/D7) and keyword-in-opening
  (D5) block; structure checks (D1–D4) are advisory (see `NOTES.md`, PR #8).
- Do not create translation files here — that belongs to `translation-flow`.
- Keep everything deterministic and offline-testable: `python -m pytest tests`.
