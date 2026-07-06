# Quality Report

- Status: review_required
- Quality Score: 63.0
- Hard failures: 0
- Issues: 12
- Source available: True
- Source changed: False
- Source segments: 6
- Target segments: 51

## Scorecard

| Dimension | Score |
| --- | ---: |
| adequacy | 75.0 |
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

## MQM Judge

- Enabled: False
- Provider: `off`
- Requested segments: 0
- Evaluated segments: 0
- MQM errors: 0
- Cache hits: 0
- Cache misses: 0

## Style Guide

- Enabled: True
- Guide: `/Users/harheem/hf-workflow/skills/quality/style/hf-blog-ko-translation-guide.md`
- Policy: `/Users/harheem/hf-workflow/skills/quality/configs/style_policy.yml`
- Style score: 60.0
- Rule hits: {'first_mention_bilingual': 1, 'list_consistency': 1, 'modal_strength': 5}

## Style Guide Findings

| Rule | Severity | Segment | Current | Suggested |
| --- | --- | --- | --- | --- |
| list_consistency | minor |  | sentence, sentence, sentence, phrase, phrase, phrase, phrase, phrase, phrase, phrase | Use either sentence-style endings or phrase-style endings consistently within one list. |
| modal_strength | major | h_001 | PaddleOCR 3.5: Transformers 백엔드를 활용한 OCR 및 문서 파싱 작업 실행 | Preserve the strength of `may` using: 수 있습니다, 일 수 있습니다. |
| modal_strength | major | h_001 | PaddleOCR 3.5: Transformers 백엔드를 활용한 OCR 및 문서 파싱 작업 실행 | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | h_001 | PaddleOCR 3.5: Transformers 백엔드를 활용한 OCR 및 문서 파싱 작업 실행 | Preserve the strength of `should` using: 좋습니다, 해야 합니다. |
| modal_strength | major | h_005 | What changed? | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_006 | PaddleOCR 3.5는 더 유연한 추론 엔진 인터페이스를 도입합니다. 개발자는 engine 파라미터를 통해 백엔드를 선택하고, engine_config를 통해 백엔드별 옵션을 전달할 수 있습니다. | Preserve the strength of `should` using: 좋습니다, 해야 합니다. |
| first_mention_bilingual | minor |  | 처리량 | Use `처리량(throughput)` on first mention, then `처리량` afterward. |

## Issues

### QL-001 terminology / major

- Message: Product or library name was not preserved.
- Source: `Datasets`
- Suggested fix: Preserve `Datasets` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-002 terminology / major

- Message: Product or library name was not preserved.
- Source: `Spaces`
- Suggested fix: Preserve `Spaces` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-003 terminology / major

- Message: Product or library name was not preserved.
- Source: `Space`
- Suggested fix: Preserve `Space` exactly.
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

### QL-006 style_locale / minor

- Message: List mixes sentence-style and phrase-style endings.
- Target: `sentence, sentence, sentence, phrase, phrase, phrase, phrase, phrase, phrase, phrase`
- Suggested fix: Use either sentence-style endings or phrase-style endings consistently within one list.
- Reason: The style guide requires consistent list item endings.

### QL-007 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `may`
- Target: `PaddleOCR 3.5: Transformers 백엔드를 활용한 OCR 및 문서 파싱 작업 실행`
- Suggested fix: Preserve the strength of `may` using: 수 있습니다, 일 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-008 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `PaddleOCR 3.5: Transformers 백엔드를 활용한 OCR 및 문서 파싱 작업 실행`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-009 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `PaddleOCR 3.5: Transformers 백엔드를 활용한 OCR 및 문서 파싱 작업 실행`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-010 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `What changed?`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-011 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `PaddleOCR 3.5는 더 유연한 추론 엔진 인터페이스를 도입합니다. 개발자는 engine 파라미터를 통해 백엔드를 선택하고, engine_config를 통해 백엔드별 옵션을 전달할 수 있습니다.`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-012 terminology / minor

- Message: First mention is missing the recommended bilingual term.
- Source: `throughput`
- Target: `처리량`
- Suggested fix: Use `처리량(throughput)` on first mention, then `처리량` afterward.
- Reason: The style guide recommends preserving searchability by adding English in parentheses on first mention.
