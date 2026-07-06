# Quality Report

- Status: reject
- Quality Score: 0.0
- Hard failures: 0
- Issues: 78
- Source available: True
- Source changed: False
- Source segments: 118
- Target segments: 109

## Scorecard

| Dimension | Score |
| --- | ---: |
| adequacy | 0.0 |
| technical_accuracy | 60.0 |
| completeness | 0.0 |
| terminology | 40.0 |
| fluency | 0.0 |
| publishing_integrity | 100.0 |
| style_locale | 60.0 |

## Metrics

- qe_metric: heuristic
- qe_average: 0.738
- qe_min: 0.1846
- embedding_similarity_average: 0.6155
- embedding_similarity_min: 0.0098
- cache_hits: 0
- cache_misses: 218

## Style Guide

- Enabled: True
- Guide: `/Users/harheem/hf-workflow/skills/quality/style/hf-blog-ko-translation-guide.md`
- Policy: `/Users/harheem/hf-workflow/skills/quality/configs/style_policy.yml`
- Style score: 60.0
- Rule hits: {'alt_text_caption': 1, 'first_mention_bilingual': 2, 'information_addition': 6, 'link_text_translation': 7, 'list_consistency': 1, 'modal_strength': 27, 'translationese': 2}

## Style Guide Findings

| Rule | Severity | Segment | Current | Suggested |
| --- | --- | --- | --- | --- |
| translationese | minor |  | 에 의해 | Rewrite the sentence in natural Korean. |
| translationese | minor |  | 을 가지 | Rewrite the sentence in natural Korean. |
| list_consistency | minor |  | sentence, sentence, phrase, sentence, sentence, sentence, sentence, phrase, phrase, phrase, sentence, phrase, sentence | Use either sentence-style endings or phrase-style endings consistently within one list. |
| modal_strength | major | b_004 | 이것은 인간이 만든, 에이전트 중심의 블로그 글입니다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | b_004 | 이것은 인간이 만든, 에이전트 중심의 블로그 글입니다. | Preserve the strength of `should` using: 좋습니다, 해야 합니다. |
| modal_strength | major | p_012 | 에이전트적 최적화 도구의 영역에서도 이것은 여전히 동일하며, 이번에는 두 가지가 서로 직접 연결되어 있습니다. | Preserve the strength of `should` using: 좋습니다, 해야 합니다. |
| modal_strength | major | h_014 | 에이전트적 사용을 위한 소프트웨어 테스트 | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_015 | 본 블로그 포스트 전반에 걸쳐 transformers를 예로 사용할 것이다: 이를 *사용하는* 에이전트가 ML 작업을 해결하도록 하는 것이며, 코드를 기여하지는 않지만, 해처스는 명령줄에서 작동할 수 있는 어떤 도구와도 작동하도록 설계되었다. | Preserve the strength of `up to` using: 최대. |
| modal_strength | major | h_018 | 모든 성공이 동등하지는 않다 | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_029 | 여기에서 에이전트를 평가하는 방식에 대해 간단히 설명합니다. | Preserve the strength of `can` using: 수 있습니다. |

## Issues

### QL-001 technical / major

- Message: Python/API identifier mismatch.
- Source: `SECURITY.md`
- Suggested fix: Preserve source Python/API identifier exactly.
- Reason: Review gate exact-match validator failed: missing=['SECURITY.md']

### QL-002 technical / major

- Message: number/unit token mismatch.
- Target: `1, 1, 3`
- Suggested fix: Preserve source number/unit token exactly.
- Reason: Review gate exact-match validator failed: extra=['1', '1', '3']

### QL-003 accuracy / major

- Message: Source segment coverage is low.
- Source: `source_segments=118`
- Target: `target_segments=109`
- Suggested fix: Check for omitted paragraphs, headings, list items, or table cells.
- Reason: Segment count validator found fewer target text segments than source text segments.

### QL-004 accuracy / major

- Message: QE metric score is low.
- Target: `0.4125`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-005 accuracy / major

- Message: QE metric score is low.
- Target: `0.5403`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-006 accuracy / major

- Message: QE metric score is low.
- Target: `0.2890`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-007 accuracy / minor

- Message: Embedding similarity is an outlier.
- Target: `0.0216`
- Suggested fix: Review whether the segment still corresponds to the source.
- Reason: Embedding similarity is below threshold 0.08.

### QL-008 accuracy / major

- Message: QE metric score is low.
- Target: `0.5426`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-009 accuracy / major

- Message: QE metric score is low.
- Target: `0.2749`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-010 accuracy / minor

- Message: Embedding similarity is an outlier.
- Target: `0.0138`
- Suggested fix: Review whether the segment still corresponds to the source.
- Reason: Embedding similarity is below threshold 0.08.

### QL-011 accuracy / major

- Message: QE metric score is low.
- Target: `0.2677`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-012 accuracy / minor

- Message: Embedding similarity is an outlier.
- Target: `0.0098`
- Suggested fix: Review whether the segment still corresponds to the source.
- Reason: Embedding similarity is below threshold 0.08.

### QL-013 accuracy / major

- Message: QE metric score is low.
- Target: `0.1846`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-014 accuracy / major

- Message: QE metric score is low.
- Target: `0.2073`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-015 accuracy / major

- Message: QE metric score is low.
- Target: `0.3760`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-016 accuracy / major

- Message: QE metric score is low.
- Target: `0.3205`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-017 accuracy / major

- Message: QE metric score is low.
- Target: `0.2978`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-018 accuracy / minor

- Message: Embedding similarity is an outlier.
- Target: `0.0265`
- Suggested fix: Review whether the segment still corresponds to the source.
- Reason: Embedding similarity is below threshold 0.08.

### QL-019 accuracy / major

- Message: QE metric score is low.
- Target: `0.3106`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-020 accuracy / minor

- Message: Embedding similarity is an outlier.
- Target: `0.0337`
- Suggested fix: Review whether the segment still corresponds to the source.
- Reason: Embedding similarity is below threshold 0.08.

### QL-021 accuracy / major

- Message: QE metric score is low.
- Target: `0.5356`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-022 accuracy / major

- Message: QE metric score is low.
- Target: `0.3109`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-023 accuracy / major

- Message: QE metric score is low.
- Target: `0.5360`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-024 accuracy / major

- Message: QE metric score is low.
- Target: `0.2378`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-025 accuracy / major

- Message: QE metric score is low.
- Target: `0.3680`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-026 accuracy / minor

- Message: Embedding similarity is an outlier.
- Target: `0.0678`
- Suggested fix: Review whether the segment still corresponds to the source.
- Reason: Embedding similarity is below threshold 0.08.

### QL-027 accuracy / major

- Message: QE metric score is low.
- Target: `0.2687`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-028 accuracy / minor

- Message: Embedding similarity is an outlier.
- Target: `0.0104`
- Suggested fix: Review whether the segment still corresponds to the source.
- Reason: Embedding similarity is below threshold 0.08.

### QL-029 accuracy / major

- Message: QE metric score is low.
- Target: `0.4959`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-030 accuracy / major

- Message: QE metric score is low.
- Target: `0.3432`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-031 accuracy / minor

- Message: Embedding similarity is an outlier.
- Target: `0.0593`
- Suggested fix: Review whether the segment still corresponds to the source.
- Reason: Embedding similarity is below threshold 0.08.

### QL-032 terminology / major

- Message: Product or library name was not preserved.
- Source: `Inference Providers`
- Suggested fix: Preserve `Inference Providers` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-033 fluency / minor

- Message: Translationese expression found.
- Target: `에 의해`
- Suggested fix: Rewrite the sentence in natural Korean.
- Reason: The style guide lists this expression as translationese to avoid.

### QL-034 fluency / minor

- Message: Translationese expression found.
- Target: `을 가지`
- Suggested fix: Rewrite the sentence in natural Korean.
- Reason: The style guide lists this expression as translationese to avoid.

### QL-035 style_locale / minor

- Message: List mixes sentence-style and phrase-style endings.
- Target: `sentence, sentence, phrase, sentence, sentence, sentence, sentence, phrase, phrase, phrase, sentence, phrase, sentence`
- Suggested fix: Use either sentence-style endings or phrase-style endings consistently within one list.
- Reason: The style guide requires consistent list item endings.

### QL-036 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `이것은 인간이 만든, 에이전트 중심의 블로그 글입니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-037 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `이것은 인간이 만든, 에이전트 중심의 블로그 글입니다.`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-038 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `에이전트적 최적화 도구의 영역에서도 이것은 여전히 동일하며, 이번에는 두 가지가 서로 직접 연결되어 있습니다.`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-039 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `에이전트적 사용을 위한 소프트웨어 테스트`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-040 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `up to`
- Target: `본 블로그 포스트 전반에 걸쳐 transformers를 예로 사용할 것이다: 이를 *사용하는* 에이전트가 ML 작업을 해결하도록 하는 것이며, 코드를 기여하지는 않지만, 해처스는 명령줄에서 작동할 수 있는 어떤 도구와도 작동하도록 설계되었다.`
- Suggested fix: Preserve the strength of `up to` using: 최대.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-041 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `모든 성공이 동등하지는 않다`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-042 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `여기에서 에이전트를 평가하는 방식에 대해 간단히 설명합니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-043 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `우리는 모든 과제를 세 가지 변형(또는 '계층')으로 실행합니다; transformers에 에이전트가 접근하는 세 가지 서로 다른 방식:`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-044 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `추가 선택 사항:`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-045 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `어떤 모델을 벤치마크 대상으로 삼을까요?`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-046 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `*대형 오픈 모델*`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-047 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `*로컬*`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-048 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `이 해처스는 에이전트 간의 상호작용에 대한 저장소 개선 방법에 대해 라이브러리 유지관리자에게 지침을 제공하는 데 그치지 않고, 사용자가 관심을 가지는 작업에서 서로 다른 에이전트와 모델이 어떻게 수행하는지 평가하는 데에도 도움을 줍니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-049 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `</iframe>`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-050 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `결과를 보기 전에 설정에 대한 간단한 요약입니다. 각 실행은 네 가지를 다릅니다: 에이전트를 구동하는 **모델**, 실행 대상인 **transformers 개정판**, **과제**, 그리고 **계층**( bare / clone / skill ). 다루었던 바와 같이, 두 가지 다른 모델 범주에 대해 서로 다른 지표를 살펴봅니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-051 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `복제 변형의 추적을 읽어보면 이유를 설명합니다. 이 커밋은 명령을 추가하지만, 동시에 CLI의 구현과 cli/agentic/*.py 사용 예제 모음을 저장소에 직접 포함합니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-052 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `may`
- Target: `<p align="center"> <img src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/is-it-agentic-enough/img_14.png" alt="Match % across models, by tier" width="85%"><br> <em>Match % across models, by tier: the skill tier lifts the larger models but drops the smaller ones.</em> </p>`
- Suggested fix: Preserve the strength of `may` using: 수 있습니다, 일 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-053 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `<p align="center"> <img src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/is-it-agentic-enough/img_14.png" alt="Match % across models, by tier" width="85%"><br> <em>Match % across models, by tier: the skill tier lifts the larger models but drops the smaller ones.</em> </p>`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-054 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `이는 또한 투입된 토큰 수와 상관관계가 있는 것으로 보입니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-055 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `이것이 우리가 마커의 개념을 도입한 이유입니다. 마커는 프로필(해처스가 특정 라이브러리를 구성하고 구동하는 방법을 가르쳐 주는 도구별 플러그인)에 의해 실행과 매칭되는 이름 있는 패턴입니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-056 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `CLI 도입은 새롭습니다: CLI는 단일 커밋에 도입되었고 어떤 모델의 학습 데이터에도 포함되지 않았으며, 문서는 간략하게만 남아 있습니다. 효과는 명확합니다: CLI의 문서를 포함하는 스킬 변형이 실제로 그것을 활용하는 경향이 가장 뚜렷하며, 그 비율은 55.3%입니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-057 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `<p align="center"> <img src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/is-it-agentic-enough/img_10.png" alt="Qwen3-14B gives up on classify-sentiment under the Skill variant" width="85%"><br> <em>Qwen3-14B on classify-sentiment (Skill variant): it reasons that read/bash/edit/write can't run a model, and gives up.</em> </p>`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-058 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `[경고]`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-059 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `전체이고 최신의 설정 및 사용 지침은 README에 있습니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-060 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `마무리`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-061 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `마무리`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-062 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `우리가 훑어본 모델 뒤에 있는 모델 제작자들과 추론 제공자들에게 감사드립니다. 전반적으로 그들은 bare 기준선이 제시하는 것보다 훨씬 뛰어난 성능을 보였습니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-063 accuracy / major

- Message: Translation may add a causal explanation that is not in the source.
- Target: `때문에`
- Suggested fix: Remove invented causal explanation unless the source explicitly states it.
- Reason: The style guide forbids adding technical explanations, reasons, examples, or conclusions.

### QL-064 accuracy / major

- Message: Translation may add a causal explanation that is not in the source.
- Target: `으로 인해`
- Suggested fix: Remove invented causal explanation unless the source explicitly states it.
- Reason: The style guide forbids adding technical explanations, reasons, examples, or conclusions.

### QL-065 accuracy / major

- Message: Translation may add a causal explanation that is not in the source.
- Target: `따라서`
- Suggested fix: Remove invented causal explanation unless the source explicitly states it.
- Reason: The style guide forbids adding technical explanations, reasons, examples, or conclusions.

### QL-066 accuracy / major

- Message: Translation may add a causal explanation that is not in the source.
- Target: `따라서`
- Suggested fix: Remove invented causal explanation unless the source explicitly states it.
- Reason: The style guide forbids adding technical explanations, reasons, examples, or conclusions.

### QL-067 accuracy / major

- Message: Translation may add a causal explanation that is not in the source.
- Target: `따라서`
- Suggested fix: Remove invented causal explanation unless the source explicitly states it.
- Reason: The style guide forbids adding technical explanations, reasons, examples, or conclusions.

### QL-068 accuracy / major

- Message: Translation may add a causal explanation that is not in the source.
- Target: `따라서`
- Suggested fix: Remove invented causal explanation unless the source explicitly states it.
- Reason: The style guide forbids adding technical explanations, reasons, examples, or conclusions.

### QL-069 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `Benchmarking transformers revisions across different metrics`
- Target: `Benchmarking transformers revisions across different metrics`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-070 fluency / minor

- Message: Link text appears untranslated.
- Source: `pi`
- Target: `pi`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-071 fluency / minor

- Message: Link text appears untranslated.
- Source: `Hugging Face Jobs`
- Target: `Hugging Face Jobs`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-072 fluency / minor

- Message: Link text appears untranslated.
- Source: ``hf` CLI, redesigned to be agent-optimized`
- Target: ``hf` CLI, redesigned to be agent-optimized`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-073 fluency / minor

- Message: Link text appears untranslated.
- Source: `agent-traces viewer`
- Target: `agent-traces viewer`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-074 fluency / minor

- Message: Link text appears untranslated.
- Source: `Upskill`
- Target: `Upskill`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-075 fluency / minor

- Message: Link text appears untranslated.
- Source: `SECURITY.md`
- Target: `SECURITY.md`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-076 fluency / minor

- Message: Link text appears untranslated.
- Source: `repo`
- Target: `repo`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-077 terminology / minor

- Message: First mention is missing the recommended bilingual term.
- Source: `quantization`
- Target: `양자화`
- Suggested fix: Use `양자화(quantization)` on first mention, then `양자화` afterward.
- Reason: The style guide recommends preserving searchability by adding English in parentheses on first mention.

### QL-078 terminology / minor

- Message: First mention is missing the recommended bilingual term.
- Source: `latency`
- Target: `지연 시간`
- Suggested fix: Use `지연 시간(latency)` on first mention, then `지연 시간` afterward.
- Reason: The style guide recommends preserving searchability by adding English in parentheses on first mention.
