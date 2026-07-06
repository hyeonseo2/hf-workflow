# Quality Report

- Status: review_required
- Quality Score: 81.0
- Hard failures: 0
- Issues: 7
- Source available: True
- Source changed: False
- Source segments: 3
- Target segments: 3

## Scorecard

| Dimension | Score |
| --- | ---: |
| adequacy | 26.5 |
| technical_accuracy | 100.0 |
| completeness | 60.0 |
| terminology | 80.0 |
| fluency | 91.7 |
| publishing_integrity | 100.0 |
| style_locale | 60.0 |

## Metrics

- qe_metric: heuristic
- qe_average: 0.8145
- qe_min: 0.6434
- embedding_similarity_average: 0.8241
- embedding_similarity_min: 0.7552
- cache_hits: 0
- cache_misses: 6

## MQM Judge

- Enabled: True
- Provider: `openai`
- Model: `gpt-5-nano`
- Reasoning effort: `minimal`
- Prompt: `/Users/harheem/hf-workflow/skills/quality/judges/mqm_prompt.md`
- Prompt hash: `10923aaf9e56e0a8e9503592b287e1d477372d1167530621d8206c31498292b6`
- Style guide hash: `937d8cd893578d30e716a3eb513cdf5f10d6fd3ad8f5e77068b57f96e160de12`
- Requested segments: 3
- Evaluated segments: 3
- MQM errors: 2
- Cache hits: 0
- Cache misses: 3
- Severity counts: {'major': 2}
- adequacy_average: 0.93
- technical_average: 1.0
- fluency_average: 0.9167

## Style Guide

- Enabled: True
- Guide: `/Users/harheem/hf-workflow/skills/quality/style/hf-blog-ko-translation-guide.md`
- Policy: `/Users/harheem/hf-workflow/skills/quality/configs/style_policy.yml`
- Style score: 60.0
- Rule hits: {'first_mention_bilingual': 1, 'modal_strength': 3, 'overstatement': 1}

## Style Guide Findings

| Rule | Severity | Segment | Current | Suggested |
| --- | --- | --- | --- | --- |
| modal_strength | major | p_002 | 이 접근법은 처리량을 30% 개선합니다. 스크립트를 실행하기 전에 HF_TOKEN 환경 변수를 설정하는 것이 좋습니다. | Preserve the strength of `may` using: 수 있습니다, 일 수 있습니다. |
| modal_strength | major | p_002 | 이 접근법은 처리량을 30% 개선합니다. 스크립트를 실행하기 전에 HF_TOKEN 환경 변수를 설정하는 것이 좋습니다. | Preserve the strength of `must` using: 반드시, 해야 합니다. |
| modal_strength | major | p_002 | 이 접근법은 처리량을 30% 개선합니다. 스크립트를 실행하기 전에 HF_TOKEN 환경 변수를 설정하는 것이 좋습니다. | Preserve the strength of `up to` using: 최대. |
| overstatement | major | p_002 | 개선합니다 | Use a weaker expression that preserves the source claim strength. |
| first_mention_bilingual | minor |  | 처리량 | Use `처리량(throughput)` on first mention, then `처리량` afterward. |

## Issues

### QL-001 accuracy / major

- Message: MQM judge reported accuracy issue.
- Source: `This approach may improve throughput by up to 30% in our experiments.`
- Target: `이 접근법은 처리량을 30% 개선합니다.`
- Suggested fix: 이 접근법은 실험에서 처리량을 최대 30% 향상시킬 수 있습니다.
- Reason: 영문 원문에서의 가능성(marked by 'may')가 한국어 번역에서 확정적 진술('개선합니다')으로 바뀌어 확신 강도가 강화되었습니다.

### QL-002 accuracy / major

- Message: MQM judge reported accuracy issue.
- Source: `You must set the HF_TOKEN environment variable before running the script.`
- Target: `스크립트를 실행하기 전에 HF_TOKEN 환경 변수를 설정하는 것이 좋습니다.`
- Suggested fix: 스크립트를 실행하기 전에 HF_TOKEN 환경 변수를 반드시 설정해야 합니다.
- Reason: 원문에서 강제적 필수 요건('must')을 한국어에서 권장('좋습니다')으로 바꿔 확신 강도가 약화되거나 다르게 전달되었습니다.

### QL-003 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `may`
- Target: `이 접근법은 처리량을 30% 개선합니다. 스크립트를 실행하기 전에 HF_TOKEN 환경 변수를 설정하는 것이 좋습니다.`
- Suggested fix: Preserve the strength of `may` using: 수 있습니다, 일 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-004 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `must`
- Target: `이 접근법은 처리량을 30% 개선합니다. 스크립트를 실행하기 전에 HF_TOKEN 환경 변수를 설정하는 것이 좋습니다.`
- Suggested fix: Preserve the strength of `must` using: 반드시, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-005 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `up to`
- Target: `이 접근법은 처리량을 30% 개선합니다. 스크립트를 실행하기 전에 HF_TOKEN 환경 변수를 설정하는 것이 좋습니다.`
- Suggested fix: Preserve the strength of `up to` using: 최대.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-006 style_locale / major

- Message: Translation appears stronger or more promotional than the source.
- Source: `may improve`
- Target: `개선합니다`
- Suggested fix: Use a weaker expression that preserves the source claim strength.
- Reason: The style guide forbids strengthening performance, certainty, or marketing claims.

### QL-007 terminology / minor

- Message: First mention is missing the recommended bilingual term.
- Source: `throughput`
- Target: `처리량`
- Suggested fix: Use `처리량(throughput)` on first mention, then `처리량` afterward.
- Reason: The style guide recommends preserving searchability by adding English in parentheses on first mention.
