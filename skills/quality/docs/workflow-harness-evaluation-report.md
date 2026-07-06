# Workflow Harness Evaluation Report

Date: 2026-07-06

## What The Pipeline Emits

Running `translation_quality_harness.py` for a translated post produces these files:

| Output | Purpose | Intended Consumer |
| --- | --- | --- |
| `quality-report.md` | Human-readable review report with status, scorecard, metric summary, style guide summary, and issue details. | Translator, reviewer, PR reviewer |
| `quality-report.json` | Machine-readable report matching `schemas/quality_report.schema.json`. | CI gate, dashboard, later automation |
| `pr-comment.md` | Short PR comment summary with status, quality score, style score, hard failure count, and top style findings. | GitHub PR comment bot |
| `source-segments.jsonl` | Source text segments with ids, hashes, kinds, and paths. | Debugging, audit, regression tracking |
| `target-segments.jsonl` | Target text segments with ids, hashes, kinds, and paths. | Debugging, audit, regression tracking |
| `metric-cache.json` | Cached metric results keyed by segment hashes. | Repeat runs and CI cost control |

The top-level status is one of:

- `auto_pass`: no hard failures, no major review blockers, high score.
- `review_required`: publishable only after human review; typically style, terminology, or low-confidence metric findings.
- `reject`: hard publishing/technical failures or score below threshold.
- `source_changed`: manifest source hash exists and no longer matches the current source.

## Harness Changes Made For Current Workflow Outputs

The current translation workflow outputs did not include a local `source.file_path`; most manifests only contained `source.url`. The harness was adjusted to match that shape:

- Fetches `source.url` automatically when `--source` and `source.file_path` are absent.
- For Hugging Face Blog URLs, tries public raw Markdown in `huggingface/blog` before falling back to rendered HTML.
- Records `metadata.source_format` as `url_markdown` or `url_html_text`.
- Skips structural Markdown hard gates when only HTML text is available.
- Normalizes workflow-only target scaffolding before source/target comparison:
  `> Source:`, generated TOC, Korean translation notice, review-instruction comment, and heading anchors like `{#section-1}`.
- Tightened protected-token extraction to reduce false positives from ordinary acronyms, domains, `e.g`, K/M/B/T localized number units, generic slash expressions, Markdown link URLs, inline code duplication, and HTML style attributes.
- Treats noisy but useful checks such as prose numbers, bare URLs, model IDs, and Python/API identifiers as review gates instead of deterministic hard failures.

Unit verification after these changes:

```text
PYTHONPATH=skills/quality python3 -m pytest -q skills/quality/tests
27 passed
```

## Sample Run

The harness was run against 14 current translation PR outputs. Six runs used real workflow manifests from `reports/pr-*`; eight additional open PR files used temporary manifests synthesized from target front matter so the same harness path could be exercised.

| PR | Manifest | Slug | Status | Score | Hard | Issues | Style | Source |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| #137 | workflow manifest | `paddleocr-transformers` | `review_required` | 63.0 | 0 | 12 | 60.0 | `url_html_text` |
| #138 | workflow manifest | `olmoearth-v1-1` | `review_required` | 66.0 | 0 | 10 | 60.0 | `url_html_text` |
| #141 | workflow manifest | `torch-profiler` | `reject` | 0.0 | 3 | 110 | 60.0 | `url_markdown` |
| #142 | workflow manifest | `openenv-agentic-rl` | `reject` | 39.0 | 2 | 17 | 60.0 | `url_markdown` |
| #143 | workflow manifest | `github-ci-hf-jobs` | `reject` | 49.0 | 0 | 24 | 60.0 | `url_markdown` |
| #144 | workflow manifest | `agentic-resource-discovery-launch` | `reject` | 64.0 | 1 | 14 | 60.0 | `url_markdown` |
| #145 | frontmatter manifest | `peft-beyond-lora` | `reject` | 0.0 | 0 | 71 | 60.0 | `url_markdown` |
| #146 | frontmatter manifest | `is-it-agentic-enough` | `reject` | 0.0 | 0 | 78 | 60.0 | `url_markdown` |
| #153 | frontmatter manifest | `huggingface-hub-release-ci` | `reject` | 36.0 | 1 | 25 | 60.0 | `url_markdown` |
| #154 | frontmatter manifest | `cross-origin-storage` | `reject` | 0.0 | 3 | 93 | 60.0 | `url_markdown` |
| #155 | frontmatter manifest | `ffasr-leaderboard` | `reject` | 47.0 | 0 | 24 | 60.0 | `url_markdown` |
| #156 | frontmatter manifest | `vllm-jobs` | `review_required` | 66.0 | 0 | 16 | 60.0 | `url_markdown` |
| #161 | frontmatter manifest | `eee-community-evals` | `reject` | 58.0 | 0 | 24 | 60.0 | `url_markdown` |
| #163 | frontmatter manifest | `cerebras-gemma4-voice-ai` | `review_required` | 94.0 | 0 | 5 | 83.0 | `url_markdown` |

Summary:

- `review_required`: 4
- `reject`: 10
- `url_markdown` source: 12
- `url_html_text` source: 2

Most common hard failures:

| Hard Failure | Count | Interpretation |
| --- | ---: | --- |
| `link target mismatch` | 3 | Markdown link destinations differ. |
| `inline code mismatch` | 3 | Inline code tokens changed or disappeared. |
| `thumbnail` front matter mismatch | 2 | Source thumbnail metadata differs from target. |
| `Markdown table shape mismatch` | 1 | Table row or column shape differs. |
| `code block hash mismatch` | 1 | A fenced code block changed. |

Most common style-guide findings:

| Rule | Count |
| --- | ---: |
| `link_text_translation` | 157 |
| `modal_strength` | 124 |
| `alt_text_caption` | 37 |
| `information_addition` | 20 |
| `first_mention_bilingual` | 12 |
| `translationese` | 10 |
| `list_consistency` | 8 |
| `intro_closing_style` | 1 |

## Findings

The harness now attaches to current workflow outputs without requiring a local source Markdown file. For official Hugging Face Blog posts present in `huggingface/blog`, it can run full structural hard gates. For organization/community posts that are not available as raw Markdown, it falls back to HTML text and intentionally avoids structural Markdown comparisons.

The current translations would not be safe to auto-merge under this gate. Several rejects are caused by real publishing-risk signals: changed code blocks, missing inline code, changed links, and stale front matter. Numeric, bare URL, model-id, and API-identifier differences are still reported, but they are review gates rather than hard failures because the real samples showed too many legitimate localization and formatting variants.

There is also a workflow-level gap: existing manifests do not pin `source.hash` or a source snapshot. When the upstream blog post changes after translation, the harness can detect mismatches but cannot always distinguish "translation error" from "source drift". Future workflow runs should store the source hash and preferably the source snapshot artifact.

## Remaining Work

- Wire `translation_quality_harness.py` into `.github/workflows/daily-translation.yml` after `run_local_review.py` or replace the old `simple_quality_report.py` path.
- Upload the full harness artifacts per PR: Markdown report, JSON report, PR comment, segment JSONL files, and metric cache.
- Add `source.hash` and source snapshot storage to translation-flow manifests.
- Decide whether `reject` should fail the workflow immediately or only block PR auto-merge.
- Calibrate style thresholds after reviewer feedback, especially `modal_strength` and `link_text_translation`, which are intentionally broad review gates.
- Add a PR comment posting step that uses `pr-comment.md`.
