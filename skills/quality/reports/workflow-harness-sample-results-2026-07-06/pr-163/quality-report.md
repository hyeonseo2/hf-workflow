# Quality Report

- Status: review_required
- Quality Score: 94.0
- Hard failures: 0
- Issues: 5
- Source available: True
- Source changed: False
- Source segments: 21
- Target segments: 21

## Scorecard

| Dimension | Score |
| --- | ---: |
| adequacy | 88.6 |
| technical_accuracy | 100.0 |
| completeness | 100.0 |
| terminology | 80.0 |
| fluency | 55.0 |
| publishing_integrity | 100.0 |
| style_locale | 83.0 |

## Metrics

- qe_metric: heuristic
- qe_average: 0.9357
- qe_min: 0.5669
- embedding_similarity_average: 0.8596
- embedding_similarity_min: 0.7763
- cache_hits: 0
- cache_misses: 42

## Style Guide

- Enabled: True
- Guide: `/Users/harheem/hf-workflow/skills/quality/style/hf-blog-ko-translation-guide.md`
- Policy: `/Users/harheem/hf-workflow/skills/quality/configs/style_policy.yml`
- Style score: 83.0
- Rule hits: {'first_mention_bilingual': 1, 'link_text_translation': 2, 'modal_strength': 1, 'translationese': 1}

## Style Guide Findings

| Rule | Severity | Segment | Current | Suggested |
| --- | --- | --- | --- | --- |
| translationese | minor |  | 에 의해 | Rewrite the sentence in natural Korean. |
| modal_strength | major | p_014 | 그 안정성은 특히 롱테일에서 중요합니다. 많은 시스템이 합리적인 중앙값 응답 시간을 제공할 수 있지만, 간헐적으로 발생하는 느린 응답은 대화를 여전히 불안정하게 만듭니다. | Preserve the strength of `can` using: 수 있습니다. |
| link_text_translation | minor |  | Hugging Face Space | Translate link text while preserving the URL target. |
| link_text_translation | minor |  | huggingface/speech-to-speech | Translate link text while preserving the URL target. |
| first_mention_bilingual | minor |  | 지연 시간 | Use `지연 시간(latency)` on first mention, then `지연 시간` afterward. |

## Issues

### QL-001 fluency / minor

- Message: Translationese expression found.
- Target: `에 의해`
- Suggested fix: Rewrite the sentence in natural Korean.
- Reason: The style guide lists this expression as translationese to avoid.

### QL-002 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `그 안정성은 특히 롱테일에서 중요합니다. 많은 시스템이 합리적인 중앙값 응답 시간을 제공할 수 있지만, 간헐적으로 발생하는 느린 응답은 대화를 여전히 불안정하게 만듭니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-003 fluency / minor

- Message: Link text appears untranslated.
- Source: `Hugging Face Space`
- Target: `Hugging Face Space`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-004 fluency / minor

- Message: Link text appears untranslated.
- Source: `huggingface/speech-to-speech`
- Target: `huggingface/speech-to-speech`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-005 terminology / minor

- Message: First mention is missing the recommended bilingual term.
- Source: `latency`
- Target: `지연 시간`
- Suggested fix: Use `지연 시간(latency)` on first mention, then `지연 시간` afterward.
- Reason: The style guide recommends preserving searchability by adding English in parentheses on first mention.
