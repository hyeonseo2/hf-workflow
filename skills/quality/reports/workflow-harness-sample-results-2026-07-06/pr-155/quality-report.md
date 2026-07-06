# Quality Report

- Status: reject
- Quality Score: 47.0
- Hard failures: 0
- Issues: 24
- Source available: True
- Source changed: False
- Source segments: 43
- Target segments: 43

## Scorecard

| Dimension | Score |
| --- | ---: |
| adequacy | 73.0 |
| technical_accuracy | 80.0 |
| completeness | 100.0 |
| terminology | 0.0 |
| fluency | 0.0 |
| publishing_integrity | 80.0 |
| style_locale | 60.0 |

## Metrics

- qe_metric: heuristic
- qe_average: 0.9803
- qe_min: 0.8625
- embedding_similarity_average: 0.8458
- embedding_similarity_min: 0.7236
- cache_hits: 86
- cache_misses: 0

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
- Rule hits: {'alt_text_caption': 2, 'first_mention_bilingual': 3, 'link_text_translation': 8, 'modal_strength': 5}

## Style Guide Findings

| Rule | Severity | Segment | Current | Suggested |
| --- | --- | --- | --- | --- |
| modal_strength | major | p_004 | 🔬 **신뢰할 수 있는 방법론:** 하이브리드 파형 기반 시뮬레이션, sim-to-real 검증, 베타 단계의 이동 소스 분할, 보유 오디오, 그리고 모든 제출에서 표준화된 평가 하드웨어를 포함합니다 | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_006 | 👀 **더 많은 소식이 곧 옵니다:** 다중 화자 시나리오, 마이크로폰 어레이 지원, 그리고 에코 제거가 로드맵에 포함되어 있습니다 | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_030 | 이 벤치마크는 Treble Technologies의 독점 시뮬레이션 엔진을 통해 시뮬레이션된 음향 공간 위에 구축됩니다. 작년 발표된 Treble10 dataset의 예시는 시뮬레이션 파이프라인을 확립하고 훈련 및 연구를 위한 원거리 RIR을 가능하게 했습니다. FFASR은 이를 확장하여 고정된 테스트 세트, 일관된 정규화 및 자동 스코어링이 포함된 표준화된 평가 프레임워크로 발전시켰습니다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_032 | 리더보드가 활성화되면서 제출된 모든 모델에서 일관된 패턴이 나타나고 있습니다: 근거리와 원거리 간의 성능 차이가 크고, SNR이 낮아질수록 그 차이가 크게 커집니다. 깨끗하고 건조한 음성에서의 근거리 WER 값은 같은 모델이 기존 벤치마크에서 달성하는 것과 비슷해 보입니다. 낮은 SNR의 원거리 WER는 다른 이야기를 들려주며, 종종 여러 배 더 높습니다. 이 벤치마크는 이러한 저하를 가시화하고 비교 가능하게 만들어주어, 이전에는 독점적인 평가 파이프라인 밖에서 이를 비교하기 어렵던 점을 해결합니다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_041 | 향후 트랙에서 적극적으로 검토 중인 조건에는 다중 화자 시나리오(동시 다발적으로 화자 2인 이상), 마이크로폰 어레이 평가(빔포밍 및 공간 필터링 접근법 포함), 그리고 에코 제거가 포함됩니다. 이는 소리를 재생하면서 듣는 모든 디바이스에 관련된 내용입니다. | Preserve the strength of `can` using: 수 있습니다. |
| alt_text_caption | minor |  | Pareto front of average WER vs RTFx across submitted models | Translate image alt text while preserving the image path. |
| alt_text_caption | minor |  | Custom evaluate method | Translate image alt text while preserving the image path. |
| link_text_translation | minor |  | Treble Technologies | Translate link text while preserving the URL target. |
| link_text_translation | minor |  | CHiME | Translate link text while preserving the URL target. |
| link_text_translation | minor |  | URGENT | Translate link text while preserving the URL target. |

## Issues

### QL-001 formatting / major

- Message: Front matter key `authors` changed or is missing.
- Source: `user: bezzam`
- Target: `user: daniel-treble`
- Suggested fix: Preserve front matter `authors` exactly.

### QL-002 technical / major

- Message: number/unit token mismatch.
- Target: `1, 14, 2, 3, 6, 9`
- Suggested fix: Preserve source number/unit token exactly.
- Reason: Review gate exact-match validator failed: extra=['1', '14', '2', '3', '6', '9']

### QL-003 terminology / major

- Message: Required glossary term is not used.
- Source: `training`
- Target: `학습`
- Suggested fix: Use `학습` for `training`.
- Reason: Glossary policy required the Korean term.

### QL-004 terminology / major

- Message: Product or library name was not preserved.
- Source: `Hugging Face`
- Suggested fix: Preserve `Hugging Face` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-005 terminology / major

- Message: Product or library name was not preserved.
- Source: `Spaces`
- Suggested fix: Preserve `Spaces` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-006 terminology / major

- Message: Product or library name was not preserved.
- Source: `Space`
- Suggested fix: Preserve `Space` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-007 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `🔬 **신뢰할 수 있는 방법론:** 하이브리드 파형 기반 시뮬레이션, sim-to-real 검증, 베타 단계의 이동 소스 분할, 보유 오디오, 그리고 모든 제출에서 표준화된 평가 하드웨어를 포함합니다`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-008 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `👀 **더 많은 소식이 곧 옵니다:** 다중 화자 시나리오, 마이크로폰 어레이 지원, 그리고 에코 제거가 로드맵에 포함되어 있습니다`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-009 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `이 벤치마크는 Treble Technologies의 독점 시뮬레이션 엔진을 통해 시뮬레이션된 음향 공간 위에 구축됩니다. 작년 발표된 Treble10 dataset의 예시는 시뮬레이션 파이프라인을 확립하고 훈련 및 연구를 위한 원거리 RIR을 가능하게 했습니다. FFASR은 이를 확장하여 고정된 테스트 세트, 일관된 정규화 및 자동 스코어링이 포함된 표준화된 평가 프레임워크로 발전시켰습니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-010 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `리더보드가 활성화되면서 제출된 모든 모델에서 일관된 패턴이 나타나고 있습니다: 근거리와 원거리 간의 성능 차이가 크고, SNR이 낮아질수록 그 차이가 크게 커집니다. 깨끗하고 건조한 음성에서의 근거리 WER 값은 같은 모델이 기존 벤치마크에서 달성하는 것과 비슷해 보입니다. 낮은 SNR의 원거리 WER는 다른 이야기를 들려주며, 종종 여러 배 더 높습니다. 이 벤치마크는 이러한 저하를 가시화하고 비교 가능하게 만들어주어, 이전에는 독점적인 평가 파이프라인 밖에서 이를 비교하기 어렵던 점을 해결합니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-011 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `향후 트랙에서 적극적으로 검토 중인 조건에는 다중 화자 시나리오(동시 다발적으로 화자 2인 이상), 마이크로폰 어레이 평가(빔포밍 및 공간 필터링 접근법 포함), 그리고 에코 제거가 포함됩니다. 이는 소리를 재생하면서 듣는 모든 디바이스에 관련된 내용입니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-012 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `Pareto front of average WER vs RTFx across submitted models`
- Target: `Pareto front of average WER vs RTFx across submitted models`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-013 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `Custom evaluate method`
- Target: `Custom evaluate method`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-014 fluency / minor

- Message: Link text appears untranslated.
- Source: `Treble Technologies`
- Target: `Treble Technologies`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-015 fluency / minor

- Message: Link text appears untranslated.
- Source: `CHiME`
- Target: `CHiME`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-016 fluency / minor

- Message: Link text appears untranslated.
- Source: `URGENT`
- Target: `URGENT`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-017 fluency / minor

- Message: Link text appears untranslated.
- Source: `NOIZEUS`
- Target: `NOIZEUS`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-018 fluency / minor

- Message: Link text appears untranslated.
- Source: `Treble's hybrid simulation engine`
- Target: `Treble's hybrid simulation engine`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-019 fluency / minor

- Message: Link text appears untranslated.
- Source: `Treble10 dataset`
- Target: `Treble10 dataset`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-020 fluency / minor

- Message: Link text appears untranslated.
- Source: `FFASR Leaderboard`
- Target: `FFASR Leaderboard`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-021 fluency / minor

- Message: Link text appears untranslated.
- Source: `FFASR forum`
- Target: `FFASR forum`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-022 terminology / minor

- Message: First mention is missing the recommended bilingual term.
- Source: `fine-tuning`
- Target: `미세 조정`
- Suggested fix: Use `미세 조정(fine-tuning)` on first mention, then `미세 조정` afterward.
- Reason: The style guide recommends preserving searchability by adding English in parentheses on first mention.

### QL-023 terminology / minor

- Message: First mention is missing the recommended bilingual term.
- Source: `latency`
- Target: `지연 시간`
- Suggested fix: Use `지연 시간(latency)` on first mention, then `지연 시간` afterward.
- Reason: The style guide recommends preserving searchability by adding English in parentheses on first mention.

### QL-024 terminology / minor

- Message: First mention is missing the recommended bilingual term.
- Source: `throughput`
- Target: `처리량`
- Suggested fix: Use `처리량(throughput)` on first mention, then `처리량` afterward.
- Reason: The style guide recommends preserving searchability by adding English in parentheses on first mention.
