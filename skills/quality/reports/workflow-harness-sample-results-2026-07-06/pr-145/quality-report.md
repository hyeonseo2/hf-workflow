# Quality Report

- Status: reject
- Quality Score: 0.0
- Hard failures: 0
- Issues: 71
- Source available: True
- Source changed: False
- Source segments: 63
- Target segments: 62

## Scorecard

| Dimension | Score |
| --- | ---: |
| adequacy | 0.0 |
| technical_accuracy | 100.0 |
| completeness | 0.0 |
| terminology | 0.0 |
| fluency | 0.0 |
| publishing_integrity | 80.0 |
| style_locale | 60.0 |

## Metrics

- qe_metric: heuristic
- qe_average: 0.858
- qe_min: 0.192
- embedding_similarity_average: 0.752
- embedding_similarity_min: 0.0427
- cache_hits: 0
- cache_misses: 124

## Style Guide

- Enabled: True
- Guide: `/Users/harheem/hf-workflow/skills/quality/style/hf-blog-ko-translation-guide.md`
- Policy: `/Users/harheem/hf-workflow/skills/quality/configs/style_policy.yml`
- Style score: 60.0
- Rule hits: {'first_mention_bilingual': 3, 'information_addition': 7, 'link_text_translation': 22, 'list_consistency': 1, 'modal_strength': 23, 'translationese': 1}

## Style Guide Findings

| Rule | Severity | Segment | Current | Suggested |
| --- | --- | --- | --- | --- |
| translationese | minor |  | 에 의해 | Rewrite the sentence in natural Korean. |
| list_consistency | minor |  | phrase, sentence, sentence, sentence, phrase, sentence | Use either sentence-style endings or phrase-style endings consistently within one list. |
| modal_strength | major | h_001 | Beyond LoRA: 가장 인기 있는 미세조정 기법을 이길 수 있을까? | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_004 | 오픈 모델을 자신의 데이터로 미세조정하고자 한다면, 아마도 소위 매개변수 효율적 미세조정, 간단히 *PEFT*에 관심이 있을 것입니다. 이 용어는 모델을 미세조정하는 데 필요한 메모리 요구량을 크게 줄여주는 기술들을 설명합니다. 이러한 기법은 수십 가지가 있지만, 거의 모두 "LoRA"라는 것을 선택합니다. 이 블로그 글에서 LoRA가 정말 최선의 선택인지, 정보에 기반한 의사결정을 내리기 위해 어떤 도구들이 있는지, 그리고 LoRA를 넘어 시야를 넓힘으로써 어떻게 이익을 얻을 수 있는지 살펴봅니다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_006 | 수많은 오픈 모델이 있지만, 그것들이 자주 당신의 사용 사례에 충분하지는 않습니다. 프롬프트 엔지니어링이 도움이 될 수는 있지만 보통은 충분하지 않습니다. 처음부터 새 모델을 학습시키기보다는 기존 모델을 미세조정하는 것을 고려해야 합니다. | Preserve the strength of `may` using: 수 있습니다, 일 수 있습니다. |
| modal_strength | major | p_007 | 하지만 미세조정은 메모리를 많이 요구합니다: 일반적으로 전체 모델을 여러 번 적합시키려면 충분한 메모리가 필요합니다. 양자화는 모델의 메모리 footprint를 줄여주지만 양자화된 모델은 직접 미세조정할 수 없습니다. 그래서 미세조정에 필요한 메모리를 줄이기 위해 여러 기법이 등장했고 이를 "매개변수 효율적 미세조정"(PEFT)이라고 부릅니다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_018 | 이 모든 것은 다음과 같은 질문으로 이어집니다: *더 나은 기법을 배제함으로써 성능을 놓치고 있는 걸까요?* 결국 LoRA를 이겼다고 주장하는 논문들이 무수히 있습니다. 그것이 LoRA를 넘어 새로운 기술로 가야 한다는 충분한 증거가 아닐까요? | Preserve the strength of `should` using: 좋습니다, 해야 합니다. |
| modal_strength | major | p_025 | 허깅페이스에서 사용자가 어떤 PEFT 기법을 사용할지에 대해 정보에 입각한 결정을 내릴 수 있도록 어떻게 도울 수 있을지 고민했습니다. PEFT 라이브러리를 통해 이미 많은 PEFT 기법을 구현하고 동일한 API로 노출하는 패키지를 제공하고 있습니다. 다음 단계는 논의된 이슈에 대해 더 많은 정보를 제공하는 벤치마크를 제공하는 것입니다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_026 | 이미 checks fine-tuning of LLMs on a math dataset를 한동안 보유하고 있었습니다. 이 벤치마크는 LLM을 가져와 사고 체인 추론(chain-of-thought reasoning)으로 미세조정하여 수학 문제에 대한 결과를 생성하도록 하며, 지시문으로 미세조정되지 않은 기본 모델을 사용합니다. 벤치마크는 따라서 모델이 수학적 추론을 학습하고 생성된 출력을 기대 형식에 맞추어 조정할 수 있는지 여부를 검사합니다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_027 | 다른 모달리티에 대한 우리의 발견을 확장하기 위해 또 하나의 image generation benchmark를 추가했습니다. 이 벤치마크는 모델이 새로운 개념인 cat plushy을 학습하도록 미세조정할 수 있는지, 그리고 기존 개념을 잊지 않고 새로운 맥락에서 이를 생성할 수 있는지 테스트합니다. | Preserve the strength of `can` using: 수 있습니다. |

## Issues

### QL-001 formatting / major

- Message: bare URL mismatch.
- Target: `https://arxiv.org/abs/2602.04998, https://huggingface.co/docs/peft/package_reference/cartridges`
- Suggested fix: Preserve source bare URL exactly.
- Reason: Review gate exact-match validator failed: extra=['https://arxiv.org/abs/2602.04998', 'https://huggingface.co/docs/peft/package_reference/cartridges']

### QL-002 accuracy / major

- Message: Source segment coverage is low.
- Source: `source_segments=63`
- Target: `target_segments=62`
- Suggested fix: Check for omitted paragraphs, headings, list items, or table cells.
- Reason: Segment count validator found fewer target text segments than source text segments.

### QL-003 accuracy / major

- Message: QE metric score is low.
- Target: `0.3573`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-004 accuracy / major

- Message: QE metric score is low.
- Target: `0.2359`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-005 accuracy / minor

- Message: Embedding similarity is an outlier.
- Target: `0.0427`
- Suggested fix: Review whether the segment still corresponds to the source.
- Reason: Embedding similarity is below threshold 0.08.

### QL-006 accuracy / major

- Message: QE metric score is low.
- Target: `0.3813`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-007 accuracy / major

- Message: QE metric score is low.
- Target: `0.1920`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-008 accuracy / major

- Message: QE metric score is low.
- Target: `0.3120`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-009 accuracy / minor

- Message: Embedding similarity is an outlier.
- Target: `0.0566`
- Suggested fix: Review whether the segment still corresponds to the source.
- Reason: Embedding similarity is below threshold 0.08.

### QL-010 accuracy / major

- Message: QE metric score is low.
- Target: `0.5268`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-011 accuracy / major

- Message: QE metric score is low.
- Target: `0.3478`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-012 terminology / minor

- Message: Preferred glossary term is not used.
- Source: `fine-tuning`
- Target: `미세 조정`
- Suggested fix: Prefer `미세 조정` for `fine-tuning`.
- Reason: Glossary policy marked this Korean term as preferred.

### QL-013 terminology / major

- Message: Product or library name was not preserved.
- Source: `Transformers`
- Suggested fix: Preserve `Transformers` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-014 terminology / major

- Message: Product or library name was not preserved.
- Source: `Diffusers`
- Suggested fix: Preserve `Diffusers` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-015 fluency / minor

- Message: Translationese expression found.
- Target: `에 의해`
- Suggested fix: Rewrite the sentence in natural Korean.
- Reason: The style guide lists this expression as translationese to avoid.

### QL-016 style_locale / minor

- Message: List mixes sentence-style and phrase-style endings.
- Target: `phrase, sentence, sentence, sentence, phrase, sentence`
- Suggested fix: Use either sentence-style endings or phrase-style endings consistently within one list.
- Reason: The style guide requires consistent list item endings.

### QL-017 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `Beyond LoRA: 가장 인기 있는 미세조정 기법을 이길 수 있을까?`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-018 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `오픈 모델을 자신의 데이터로 미세조정하고자 한다면, 아마도 소위 매개변수 효율적 미세조정, 간단히 *PEFT*에 관심이 있을 것입니다. 이 용어는 모델을 미세조정하는 데 필요한 메모리 요구량을 크게 줄여주는 기술들을 설명합니다. 이러한 기법은 수십 가지가 있지만, 거의 모두 "LoRA"라는 것을 선택합니다. 이 블로그 글에서 LoRA가 정말 최선의 선택인지, 정보에 기반한 의사결정을 내리기 위해 어떤 도구들이 있는지, 그리고 LoRA를 넘어 시야를 넓힘으로써 어떻게 이익을 얻을 수 있는지 살펴봅니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-019 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `may`
- Target: `수많은 오픈 모델이 있지만, 그것들이 자주 당신의 사용 사례에 충분하지는 않습니다. 프롬프트 엔지니어링이 도움이 될 수는 있지만 보통은 충분하지 않습니다. 처음부터 새 모델을 학습시키기보다는 기존 모델을 미세조정하는 것을 고려해야 합니다.`
- Suggested fix: Preserve the strength of `may` using: 수 있습니다, 일 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-020 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `하지만 미세조정은 메모리를 많이 요구합니다: 일반적으로 전체 모델을 여러 번 적합시키려면 충분한 메모리가 필요합니다. 양자화는 모델의 메모리 footprint를 줄여주지만 양자화된 모델은 직접 미세조정할 수 없습니다. 그래서 미세조정에 필요한 메모리를 줄이기 위해 여러 기법이 등장했고 이를 "매개변수 효율적 미세조정"(PEFT)이라고 부릅니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-021 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `이 모든 것은 다음과 같은 질문으로 이어집니다: *더 나은 기법을 배제함으로써 성능을 놓치고 있는 걸까요?* 결국 LoRA를 이겼다고 주장하는 논문들이 무수히 있습니다. 그것이 LoRA를 넘어 새로운 기술로 가야 한다는 충분한 증거가 아닐까요?`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-022 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `허깅페이스에서 사용자가 어떤 PEFT 기법을 사용할지에 대해 정보에 입각한 결정을 내릴 수 있도록 어떻게 도울 수 있을지 고민했습니다. PEFT 라이브러리를 통해 이미 많은 PEFT 기법을 구현하고 동일한 API로 노출하는 패키지를 제공하고 있습니다. 다음 단계는 논의된 이슈에 대해 더 많은 정보를 제공하는 벤치마크를 제공하는 것입니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-023 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `이미 checks fine-tuning of LLMs on a math dataset를 한동안 보유하고 있었습니다. 이 벤치마크는 LLM을 가져와 사고 체인 추론(chain-of-thought reasoning)으로 미세조정하여 수학 문제에 대한 결과를 생성하도록 하며, 지시문으로 미세조정되지 않은 기본 모델을 사용합니다. 벤치마크는 따라서 모델이 수학적 추론을 학습하고 생성된 출력을 기대 형식에 맞추어 조정할 수 있는지 여부를 검사합니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-024 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `다른 모달리티에 대한 우리의 발견을 확장하기 위해 또 하나의 image generation benchmark를 추가했습니다. 이 벤치마크는 모델이 새로운 개념인 cat plushy을 학습하도록 미세조정할 수 있는지, 그리고 기존 개념을 잊지 않고 새로운 맥락에서 이를 생성할 수 있는지 테스트합니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-025 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `모든 PEFT 기법을 동등한 조건에서 비교하고 특정 기법을 편들지 않기 때문에, 이 벤치마크가 서로 다른 PEFT 기법들이 얼마나 잘 작동하는지에 대한 객관적인 그림을 제시한다고 믿습니다. 귀하의 데이터세트가 있다면 비슷한 접근법을 취하고 PEFT 라이브러리를 활용해 여러 PEFT 기법을 평가해 보시길 권합니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-026 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `벤치마크를 마친 뒤, LoRA가 잘 작동하더라도 다른 PEFT 기법들이 한 가지 혹은 여러 축에서 이를 능가할 수 있으며 따라서 고려되어야 한다는 것을 발견했습니다. 아래 이미지는 LoRA와 다섯 가지 다른 PEFT 기법의 성능을 비교합니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-027 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `벤치마크를 마친 뒤, LoRA가 잘 작동하더라도 다른 PEFT 기법들이 한 가지 혹은 여러 축에서 이를 능가할 수 있으며 따라서 고려되어야 한다는 것을 발견했습니다. 아래 이미지는 LoRA와 다섯 가지 다른 PEFT 기법의 성능을 비교합니다.`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-028 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `위의 결과를 해석하는 한 가지 방법은 트레이드오프 관점에서 생각하는 것입니다. 예를 들어: 모델이 테스트 데이터에서 얼마나 잘 작동하는지와 이를 학습하는 데 필요한 메모리가 얼마나 되는지 사이의 trade-off는 어떤가요? 어떤 PEFT 기법도 이 두 지표를 동시에 다른 어떤 기법보다 더 잘 이길 수 없다면, 그것은 *파레토 프런티어*에 속합니다. 다시 말해: 더 나은 테스트 정확도를 원한다면 더 많은 메모리가 필요하고, 메모리 효율성을 더 원한다면 정확도를 포기해야 한다는 뜻입니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-029 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `may`
- Target: `LLM 수학 데이터셋 벤치마크의 결과를 좀 더 자세히 살펴보겠습니다. 테스트 정확도와 메모리 측면에서 보자면 LoRA는 실제로 파레토 프런티어에 속합니다. 최고점에서 53.2%의 테스트 정확도와 22.6 GB의 VRAM이 필요합니다. 그러나 파레토 프런티어에 속하는 다른 PEFT 기법도 있습니다. 예를 들어, BEFT은 32.9%의 테스트 정확도를 달성하고 최대 메모리는 20.2 GB에 불과합니다. 반대편 끝에는 Lily이 있는데, 54.9%의 테스트 정확도를 달성하지만 25.6 GB의 메모리가 필요합니다. 무엇이 더 중요한지에 따라 LoRA가 최적의 트레이드오프를 제시하지 않는다고 결론지을 수도 있습니다.`
- Suggested fix: Preserve the strength of `may` using: 수 있습니다, 일 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-030 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `may`
- Target: `벤치마크의 또 다른 문제는 특정 PEFT 기법의 능력을 완전히 반영하지 못할 수 있다는 점입니다. 우리는 다양한 차원에서 기법들을 비교하고 이러한 트레이드오프에 따라 최상위를 발견할 수 있도록 했습니다. 그러나 이렇게 해서 모든 면모를 포착하는 것은 불가능합니다. 예를 들어, Cartridges (https://huggingface.co/docs/peft/package_reference/cartridges)라는 PEFT 기법은 긴 프롬프트를 압축하기 위해 개발되었지만 벤치마크에는 측정되지 않았습니다. 선택에 영향을 줄 수 있는 다른 요인들도 있습니다. 예를 들면:`
- Suggested fix: Preserve the strength of `may` using: 수 있습니다, 일 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-031 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `벤치마크의 또 다른 문제는 특정 PEFT 기법의 능력을 완전히 반영하지 못할 수 있다는 점입니다. 우리는 다양한 차원에서 기법들을 비교하고 이러한 트레이드오프에 따라 최상위를 발견할 수 있도록 했습니다. 그러나 이렇게 해서 모든 면모를 포착하는 것은 불가능합니다. 예를 들어, Cartridges (https://huggingface.co/docs/peft/package_reference/cartridges)라는 PEFT 기법은 긴 프롬프트를 압축하기 위해 개발되었지만 벤치마크에는 측정되지 않았습니다. 선택에 영향을 줄 수 있는 다른 요인들도 있습니다. 예를 들면:`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-032 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `may`
- Target: `PEFT 기법에 따라 수정할 수 있는 특정 레이어 유형만 있습니다.`
- Suggested fix: Preserve the strength of `may` using: 수 있습니다, 일 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-033 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `PEFT 기법에 따라 수정할 수 있는 특정 레이어 유형만 있습니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-034 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `모든 PEFT 기법이 양자화된 기본 모델을 지원하는 것은 아니지만(하지만 PEFT에서 지원을 활발히 확장하고 있습니다).`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-035 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `<table align="center"> <tr> <td align="center"><a href="https://huggingface.co/spaces/peft-internal-testing/PEFT-shop"><img src="https://huggingface.co/datasets/peft-internal-testing/peft-blog-assets/resolve/main/peft-beyond-lora/peft-shop.png" width="100%"/></a></td> </tr> <tr> <td align="center"><em>Click on the image to peruse the PEFT shop to find the best PEFT technique for you. It allows you to browse not only by benchmark metrics but also by capabilities, like quantization support.</em></td> </tr> </table>`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-036 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `이를 테스트하기 위해 GraLoRA 기법을 사용한 이미지 어댑터를 LoRA 체크포인트로 변환했습니다. 변환 후 테스트 점수는 사실상 동일했습니다(유사도 0.702 → 0.694, 0.260 → 0.269). 아래는 프롬프트 “sks 해변의 고양이”에 대한 테스트 이미지입니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-037 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `저희의 여정은 아직 끝나지 않았습니다. 기존 벤치마크를 확장하고 개선하며 앞으로 더 많은 벤치마크를 추가할 계획도 있습니다. 커뮤니티의 기여를 쉽게 할 수 있도록 보장했으며, 이것에 기여하고 싶다면 issue on the PEFT repository를 열고 기여 방법을 알려 주세요.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-038 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `must`
- Target: `저희의 여정은 아직 끝나지 않았습니다. 기존 벤치마크를 확장하고 개선하며 앞으로 더 많은 벤치마크를 추가할 계획도 있습니다. 커뮤니티의 기여를 쉽게 할 수 있도록 보장했으며, 이것에 기여하고 싶다면 issue on the PEFT repository를 열고 기여 방법을 알려 주세요.`
- Suggested fix: Preserve the strength of `must` using: 반드시, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-039 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `<p align="left"> <em>Example: Changing from LoRA to OFT using PEFT</em> </p>`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-040 accuracy / major

- Message: Translation may add a causal explanation that is not in the source.
- Target: `따라서`
- Suggested fix: Remove invented causal explanation unless the source explicitly states it.
- Reason: The style guide forbids adding technical explanations, reasons, examples, or conclusions.

### QL-041 accuracy / major

- Message: Translation may add a causal explanation that is not in the source.
- Target: `때문에`
- Suggested fix: Remove invented causal explanation unless the source explicitly states it.
- Reason: The style guide forbids adding technical explanations, reasons, examples, or conclusions.

### QL-042 accuracy / major

- Message: Translation may add a causal explanation that is not in the source.
- Target: `때문에`
- Suggested fix: Remove invented causal explanation unless the source explicitly states it.
- Reason: The style guide forbids adding technical explanations, reasons, examples, or conclusions.

### QL-043 accuracy / major

- Message: Translation may add a causal explanation that is not in the source.
- Target: `따라서`
- Suggested fix: Remove invented causal explanation unless the source explicitly states it.
- Reason: The style guide forbids adding technical explanations, reasons, examples, or conclusions.

### QL-044 accuracy / major

- Message: Translation may add a causal explanation that is not in the source.
- Target: `따라서`
- Suggested fix: Remove invented causal explanation unless the source explicitly states it.
- Reason: The style guide forbids adding technical explanations, reasons, examples, or conclusions.

### QL-045 accuracy / major

- Message: Translation may add a causal explanation that is not in the source.
- Target: `따라서`
- Suggested fix: Remove invented causal explanation unless the source explicitly states it.
- Reason: The style guide forbids adding technical explanations, reasons, examples, or conclusions.

### QL-046 accuracy / major

- Message: Translation may add a causal explanation that is not in the source.
- Target: `덕분에`
- Suggested fix: Remove invented causal explanation unless the source explicitly states it.
- Reason: The style guide forbids adding technical explanations, reasons, examples, or conclusions.

### QL-047 fluency / minor

- Message: Link text appears untranslated.
- Source: ``PEFT` library`
- Target: ``PEFT` library`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-048 fluency / minor

- Message: Link text appears untranslated.
- Source: ``Transformers``
- Target: ``Transformers``
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-049 fluency / minor

- Message: Link text appears untranslated.
- Source: ``Diffusers``
- Target: ``Diffusers``
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-050 fluency / minor

- Message: Link text appears untranslated.
- Source: `multiple quantization methods`
- Target: `multiple quantization methods`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-051 fluency / minor

- Message: Link text appears untranslated.
- Source: `“LoRA”`
- Target: `“LoRA”`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-052 fluency / minor

- Message: Link text appears untranslated.
- Source: `model cards on Hugging Face Hub`
- Target: `model cards on Hugging Face Hub`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-053 fluency / minor

- Message: Link text appears untranslated.
- Source: `example GH query`
- Target: `example GH query`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-054 fluency / minor

- Message: Link text appears untranslated.
- Source: `One study`
- Target: `https://arxiv.org/abs/2602.04998`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-055 fluency / minor

- Message: Link text appears untranslated.
- Source: `checks fine-tuning of LLMs on a math dataset`
- Target: `checks fine-tuning of LLMs on a math dataset`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-056 fluency / minor

- Message: Link text appears untranslated.
- Source: `image generation benchmark`
- Target: `image generation benchmark`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-057 fluency / minor

- Message: Link text appears untranslated.
- Source: `cat plushy`
- Target: `cat plushy`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-058 fluency / minor

- Message: Link text appears untranslated.
- Source: `BEFT`
- Target: `BEFT`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-059 fluency / minor

- Message: Link text appears untranslated.
- Source: `Lily`
- Target: `Lily`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-060 fluency / minor

- Message: Link text appears untranslated.
- Source: `rank stabilized initialization`
- Target: `rank stabilized initialization`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-061 fluency / minor

- Message: Link text appears untranslated.
- Source: `LoRA-FA`
- Target: `LoRA-FA`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-062 fluency / minor

- Message: Link text appears untranslated.
- Source: `Hugging Face Space`
- Target: `Hugging Face Space`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-063 fluency / minor

- Message: Link text appears untranslated.
- Source: `OFT`
- Target: `OFT`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-064 fluency / minor

- Message: Link text appears untranslated.
- Source: `instructions on how to do that`
- Target: `instructions on how to do that`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-065 fluency / minor

- Message: Link text appears untranslated.
- Source: `Cartridges`
- Target: `https://huggingface.co/docs/peft/package_reference/cartridges`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-066 fluency / minor

- Message: Link text appears untranslated.
- Source: `merging of the adapter`
- Target: `merging of the adapter`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-067 fluency / minor

- Message: Link text appears untranslated.
- Source: `converting other adapters into LoRA`
- Target: `converting other adapters into LoRA`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-068 fluency / minor

- Message: Link text appears untranslated.
- Source: `issue on the `PEFT` repository`
- Target: `issue on the `PEFT` repository`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-069 terminology / minor

- Message: First mention is missing the recommended bilingual term.
- Source: `fine-tuning`
- Target: `미세 조정`
- Suggested fix: Use `미세 조정(fine-tuning)` on first mention, then `미세 조정` afterward.
- Reason: The style guide recommends preserving searchability by adding English in parentheses on first mention.

### QL-070 terminology / minor

- Message: First mention is missing the recommended bilingual term.
- Source: `checkpoint`
- Target: `체크포인트`
- Suggested fix: Use `체크포인트(checkpoint)` on first mention, then `체크포인트` afterward.
- Reason: The style guide recommends preserving searchability by adding English in parentheses on first mention.

### QL-071 terminology / minor

- Message: First mention is missing the recommended bilingual term.
- Source: `quantization`
- Target: `양자화`
- Suggested fix: Use `양자화(quantization)` on first mention, then `양자화` afterward.
- Reason: The style guide recommends preserving searchability by adding English in parentheses on first mention.
