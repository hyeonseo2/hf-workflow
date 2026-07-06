# Quality Report

- Status: review_required
- Quality Score: 66.0
- Hard failures: 0
- Issues: 10
- Source available: True
- Source changed: False
- Source segments: 1
- Target segments: 25

## Scorecard

| Dimension | Score |
| --- | ---: |
| adequacy | 80.0 |
| technical_accuracy | 100.0 |
| completeness | 100.0 |
| terminology | 0.0 |
| fluency | 100.0 |
| publishing_integrity | 100.0 |
| style_locale | 60.0 |

## Metrics

- qe_metric: heuristic
- cache_hits: 0
- cache_misses: 0
- warning: Source was fetched as HTML text; structural hard gates, segment coverage, and segment metrics were skipped.

## Style Guide

- Enabled: True
- Guide: `/Users/harheem/hf-workflow/skills/quality/style/hf-blog-ko-translation-guide.md`
- Policy: `/Users/harheem/hf-workflow/skills/quality/configs/style_policy.yml`
- Style score: 60.0
- Rule hits: {'first_mention_bilingual': 1, 'modal_strength': 4}

## Style Guide Findings

| Rule | Severity | Segment | Current | Suggested |
| --- | --- | --- | --- | --- |
| modal_strength | major | h_001 | OlmoEarth v1.1: 더 효율적인 모델 패밀리 | Preserve the strength of `may` using: 수 있습니다, 일 수 있습니다. |
| modal_strength | major | h_001 | OlmoEarth v1.1: 더 효율적인 모델 패밀리 | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | h_001 | OlmoEarth v1.1: 더 효율적인 모델 패밀리 | Preserve the strength of `should` using: 좋습니다, 해야 합니다. |
| modal_strength | major | h_001 | OlmoEarth v1.1: 더 효율적인 모델 패밀리 | Preserve the strength of `up to` using: 최대. |
| first_mention_bilingual | minor |  | 미세 조정 | Use `미세 조정(fine-tuning)` on first mention, then `미세 조정` afterward. |

## Issues

### QL-001 terminology / major

- Message: Product or library name was not preserved.
- Source: `Hugging Face`
- Suggested fix: Preserve `Hugging Face` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-002 terminology / major

- Message: Product or library name was not preserved.
- Source: `Datasets`
- Suggested fix: Preserve `Datasets` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-003 terminology / major

- Message: Product or library name was not preserved.
- Source: `Spaces`
- Suggested fix: Preserve `Spaces` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-004 terminology / major

- Message: Product or library name was not preserved.
- Source: `Inference Endpoints`
- Suggested fix: Preserve `Inference Endpoints` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-005 terminology / major

- Message: Product or library name was not preserved.
- Source: `Inference Providers`
- Suggested fix: Preserve `Inference Providers` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-006 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `may`
- Target: `OlmoEarth v1.1: 더 효율적인 모델 패밀리`
- Suggested fix: Preserve the strength of `may` using: 수 있습니다, 일 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-007 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `OlmoEarth v1.1: 더 효율적인 모델 패밀리`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-008 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `OlmoEarth v1.1: 더 효율적인 모델 패밀리`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-009 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `up to`
- Target: `OlmoEarth v1.1: 더 효율적인 모델 패밀리`
- Suggested fix: Preserve the strength of `up to` using: 최대.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-010 terminology / minor

- Message: First mention is missing the recommended bilingual term.
- Source: `fine-tuning`
- Target: `미세 조정`
- Suggested fix: Use `미세 조정(fine-tuning)` on first mention, then `미세 조정` afterward.
- Reason: The style guide recommends preserving searchability by adding English in parentheses on first mention.
