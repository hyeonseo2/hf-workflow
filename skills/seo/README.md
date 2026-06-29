# SEO Skill

Reusable SEO/GEO review for a single Korean Hugging Face Blog translation in
`Hugging-Face-KREW/hugging-face-krew.github.io`. See `SKILL.md` for the full
spec; this is the quick reference.

## Modules

- **Module 1 — Eval (this stage):** body-only deterministic gate (D1–D7) +
  rubric seam. Produces a pass/fail gate, a markdown report, and a JSON result.
- **Module 2 — Metadata writer (stage 2):** generates and writes back
  frontmatter / JSON-LD after a pass. Interface only for now (`tools/metadata.py`).

Translation quality is **out of scope** (separate quality skill).

## Usage

```bash
# PR / pre-publish flow (from a translation-flow manifest)
python tools/seo_eval.py --manifest <manifest.yaml> \
  --target-root <cloned target repo> --output <report.md>

# Published flow (direct file)
python tools/seo_eval.py --file _posts/2025-12-01-rteb.md \
  --target-root ../hugging-face-krew.github.io --output /tmp/seo.md
```

Outputs `<report.md>` and `<report>.json`. Exit code: `0` gate pass, `1` fail.
Add `--primary-keyword` to enable the keyword checks (D5/D10); the manifest's
`handoff.seo.primary_keyword` is empty in practice. `--benchmark heuristic` adds
an informational Lighthouse-SEO score (never affects the gate).

## Tests

```bash
pip install -e .[dev]          # pyyaml + pytest + markdown + beautifulsoup4
python -m pytest tests          # functional unit tests + golden regression, offline
UPDATE_GOLDEN=1 python -m pytest tests/test_golden_regression.py   # re-baseline golden
```

## Layout

```
tools/
  seo_eval.py        # orchestrator: body-only AND gate, manifest|--file input
  report.py          # markdown renderer over the result dict
  rubric.py          # R1–R6 rubric interface (stage-2 skeleton)
  metadata.py        # Module 2 metadata writer interface (stage-2 skeleton)
  checkers/          # content / keywords / images / frontmatter / seo_audits
  utils.py           # frontmatter parse + text metrics
  heuristic.py       # Lighthouse Tier-B heuristic
  benchmark.py       # Lighthouse Tier-A/B orchestrator (informational)
tests/               # pytest harness + fixtures/ + golden/
```

> `tools/simple_seo_report.py` is the legacy minimal checker, kept only for the
> old `tests/test_simple_seo_report.py`. `seo_eval.py` supersedes it.
