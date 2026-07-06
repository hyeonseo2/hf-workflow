# Quality Report

- Status: reject
- Quality Score: 0.0
- Hard failures: 3
- Issues: 93
- Source available: True
- Source changed: False
- Source segments: 64
- Target segments: 63

## Scorecard

| Dimension | Score |
| --- | ---: |
| adequacy | 0.0 |
| technical_accuracy | 40.0 |
| completeness | 0.0 |
| terminology | 40.0 |
| fluency | 0.0 |
| publishing_integrity | 60.0 |
| style_locale | 60.0 |

## Metrics

- qe_metric: heuristic
- qe_average: 0.8295
- qe_min: 0.0
- embedding_similarity_average: 0.7235
- embedding_similarity_min: 0.0072
- cache_hits: 0
- cache_misses: 126

## Style Guide

- Enabled: True
- Guide: `/Users/harheem/hf-workflow/skills/quality/style/hf-blog-ko-translation-guide.md`
- Policy: `/Users/harheem/hf-workflow/skills/quality/configs/style_policy.yml`
- Style score: 60.0
- Rule hits: {'alt_text_caption': 7, 'information_addition': 2, 'link_text_translation': 49, 'list_consistency': 1, 'modal_strength': 15, 'translationese': 2}

## Style Guide Findings

| Rule | Severity | Segment | Current | Suggested |
| --- | --- | --- | --- | --- |
| translationese | minor |  | 에 의해 | Rewrite the sentence in natural Korean. |
| translationese | minor |  | 를 가지 | Rewrite the sentence in natural Korean. |
| list_consistency | minor |  | sentence, phrase, sentence, sentence, sentence | Use either sentence-style endings or phrase-style endings consistently within one list. |
| modal_strength | major | p_010 | 그러나 Xenova/whisper-tiny.en은(는) 인기 있는 모델이며(앞에서 언급했듯이 Transformer.js의 기본 ASR 모델이기도 합니다), 이를 사용하는 앱이 여러 개일 수 있음을 쉽게 상상할 수 있습니다. 이 상황을 시뮬레이션하기 위해, 이전의 동일한 예제 앱을 different origin에서 제공하는 것으로 가정합니다. 이 다른 원본(origin) 애플리케이션을 방문하면, 거의 즉시 사용할 수 있도록 하는 대신 브라우저는 모든 모델 리소스를 다시 다운로드하고 캐시해야 하므로 바이트 단위로 동일하더라도 중복 다운로드 및 저장이 발생합니다. 이 toy 예제에서도 이는 누적되어 177 MB의 중복 다운로드 및 저장으로 이어진다는 점을 Chrome DevTools의 Storage 섹션에서 확인할 수 있습니다 Application panel. 이를 상상해 보실 수 있습니다. | Preserve the strength of `up to` using: 최대. |
| modal_strength | major | p_023 | 다양한 앱이 서로 다른 오리진에서 실행되더라도 결국 동일한 CDN URL에서 리소스를 제공한다면 캐싱 문제는 없을 것이라고 생각할 수 있습니다. 하지만 오랜 기간 브라우저에서의 캐싱 방식은 그렇지 않습니다. 기사 Gaining security and privacy by partitioning the cache가 모든 세부 정보를 다룹니다. 본질적으로, 캐시가 오리진별로 분리되어 있어 타이밍 공격을 방지합니다: 웹사이트가 HTTP 요청에 응답하는 데 걸리는 시간은 브라우저가 과거에 같은 리소스에 접근했다는 것을 암시할 수 있어 보안 및 개인정보 유출 취약점을 만들 수 있습니다. | Preserve the strength of `should` using: 좋습니다, 해야 합니다. |
| modal_strength | major | p_025 | 구체적인 구현은 브라우저에 따라 다를 수 있지만 Chrome에서는 캐시된 리소스가 **리소스 URL** 외에 네트워크 격리 키(Network Isolation Key)로도 키가 부여됩니다. 네트워크 격리 키는 **최상위 사이트**와 **현재 프레임 사이트**로 구성됩니다. 앞의 toy 예제가 https://googlechrome.github.io와 https://rawcdn.rawgit.net에서 호스팅되었다고 가정하고, 둘 다 https://cdn.jsdelivr.net/npm/onnxruntime-web@1.26.0-dev.20260416-b7804b056c/dist/ort-wasm-simd-threaded.asyncify.wasm의 Wasm 런타임을 사용한다면, 캐시 키는 아래 표와 같이 보일 것입니다. | Preserve the strength of `may` using: 수 있습니다, 일 수 있습니다. |
| modal_strength | major | p_030 | 제안된 **Cross-Origin Storage (COS) API**는 웹 앱이 원점 경계를 넘어 큰 파일을 저장하고 검색할 수 있도록 하는 전용 navigator.crossOriginStorage 인터페이스를 도입합니다. 이는 URL이 아니라 암호학적 해시로 식별됩니다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | h_035 | 누가 무엇을 읽을 수 있는지 제어 | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_036 | 모든 리소스를 전역적으로 공유해서는 안됩니다. COS는 파일 저장 시 가시성을 제어하기 위해 origins 옵션을 통해 개발자에게 정밀한 제어를 제공합니다. | Preserve the strength of `should` using: 좋습니다, 해야 합니다. |
| modal_strength | major | l_038 | 특정 오리진 목록, 예를 들어 origins: ['https://write.example.com', 'https://calculate.example.com']과 같은 목록은 이 사이트들에 대한 접근을 **제한**합니다. 이는 서로의 소유 자산 간에 공유되지만 다른 누구도 검색될 필요가 없는 리소스와 같은 사례에 잘 맞습니다. 예: 상업용 오피스 도구에서 사용되는 독점 교정 AI 모델. | Preserve the strength of `should` using: 좋습니다, 해야 합니다. |

## Issues

### QL-001 formatting / critical

- Message: code block hash mismatch.
- Source: `548f672b2b8aecdef3cdcb59fafc37a7cd4b29d4fe401eede3c720bced4bec51, f64356711b2f17030d4fd9c5d941da88a556df4420f41c7116e7cf62aefdb8b9`
- Target: `f2b53469c9e34443842f1a6189e0dd9c523766d990f267e4a17d062cdcc03921, f389353c5c05ff7207b72a892073823bba1da9f398e370b1124f1377224144dd`
- Suggested fix: Preserve source code block hash exactly.
- Reason: Hard gate exact-match validator failed: missing=['548f672b2b8aecdef3cdcb59fafc37a7cd4b29d4fe401eede3c720bced4bec51', 'f64356711b2f17030d4fd9c5d941da88a556df4420f41c7116e7cf62aefdb8b9']; extra=['f2b53469c9e34443842f1a6189e0dd9c523766d990f267e4a17d062cdcc03921', 'f389353c5c05ff7207b72a892073823bba1da9f398e370b1124f1377224144dd']

### QL-002 technical / critical

- Message: inline code mismatch.
- Source: `ModelRegistry.is_pipeline_cached(), Xenova/whisper-large-v3, Xenova/whisper-large-v3, Xenova/whisper-tiny.en, Xenova/whisper-tiny.en, create: true, whisper-medium.en`
- Suggested fix: Preserve source inline code exactly.
- Reason: Hard gate exact-match validator failed: missing=['ModelRegistry.is_pipeline_cached()', 'Xenova/whisper-large-v3', 'Xenova/whisper-large-v3', 'Xenova/whisper-tiny.en', 'Xenova/whisper-tiny.en', 'create: true', 'whisper-medium.en']

### QL-003 formatting / critical

- Message: link target mismatch.
- Source: `https://huggingface.co/Xenova/models?search=whisper, https://huggingface.co/Xenova/whisper-large-v3, https://huggingface.co/docs/transformers.js/en/api/utils/model_registry, https://huggingface.co/docs/transformers.js/en/api/utils/model_registry#modelregistryispipelinecachedtask-modelid-options--promise--boolean-`
- Suggested fix: Preserve source link target exactly.
- Reason: Hard gate exact-match validator failed: missing=['https://huggingface.co/Xenova/models?search=whisper', 'https://huggingface.co/Xenova/whisper-large-v3', 'https://huggingface.co/docs/transformers.js/en/api/utils/model_registry', 'https://huggingface.co/docs/transformers.js/en/api/utils/model_registry#modelregistryispipelinecachedtask-modelid-options--promise--boolean-']

### QL-004 technical / major

- Message: model or dataset id mismatch.
- Source: `Xenova/whisper-large-v3, Xenova/whisper-large-v3, Xenova/whisper-tiny.en, Xenova/whisper-tiny.en`
- Suggested fix: Preserve source model or dataset id exactly.
- Reason: Review gate exact-match validator failed: missing=['Xenova/whisper-large-v3', 'Xenova/whisper-large-v3', 'Xenova/whisper-tiny.en', 'Xenova/whisper-tiny.en']

### QL-005 technical / major

- Message: Python/API identifier mismatch.
- Source: `ModelRegistry.is_pipeline_cached, Transformers.js, Transformers.js, Transformers.js, Transformers.js, Transformers.js, Transformers.js, Transformers.js`
- Suggested fix: Preserve source Python/API identifier exactly.
- Reason: Review gate exact-match validator failed: missing=['ModelRegistry.is_pipeline_cached', 'Transformers.js', 'Transformers.js', 'Transformers.js', 'Transformers.js', 'Transformers.js', 'Transformers.js', 'Transformers.js']

### QL-006 accuracy / major

- Message: Source segment coverage is low.
- Source: `source_segments=64`
- Target: `target_segments=63`
- Suggested fix: Check for omitted paragraphs, headings, list items, or table cells.
- Reason: Segment count validator found fewer target text segments than source text segments.

### QL-007 accuracy / major

- Message: QE metric score is low.
- Target: `0.4461`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-008 accuracy / major

- Message: QE metric score is low.
- Target: `0.2630`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-009 accuracy / minor

- Message: Embedding similarity is an outlier.
- Target: `0.0072`
- Suggested fix: Review whether the segment still corresponds to the source.
- Reason: Embedding similarity is below threshold 0.08.

### QL-010 accuracy / major

- Message: QE metric score is low.
- Target: `0.5313`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-011 accuracy / major

- Message: QE metric score is low.
- Target: `0.0346`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-012 accuracy / major

- Message: QE metric score is low.
- Target: `0.5446`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-013 accuracy / major

- Message: QE metric score is low.
- Target: `0.0000`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-014 accuracy / major

- Message: QE metric score is low.
- Target: `0.4620`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-015 terminology / minor

- Message: Preferred glossary term is not used.
- Source: `serving`
- Target: `서빙`
- Suggested fix: Prefer `서빙` for `serving`.
- Reason: Glossary policy marked this Korean term as preferred.

### QL-016 terminology / major

- Message: Product or library name was not preserved.
- Source: `Hugging Face Hub`
- Suggested fix: Preserve `Hugging Face Hub` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-017 terminology / major

- Message: Product or library name was not preserved.
- Source: `Space`
- Suggested fix: Preserve `Space` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-018 fluency / minor

- Message: Translationese expression found.
- Target: `에 의해`
- Suggested fix: Rewrite the sentence in natural Korean.
- Reason: The style guide lists this expression as translationese to avoid.

### QL-019 fluency / minor

- Message: Translationese expression found.
- Target: `를 가지`
- Suggested fix: Rewrite the sentence in natural Korean.
- Reason: The style guide lists this expression as translationese to avoid.

### QL-020 style_locale / minor

- Message: List mixes sentence-style and phrase-style endings.
- Target: `sentence, phrase, sentence, sentence, sentence`
- Suggested fix: Use either sentence-style endings or phrase-style endings consistently within one list.
- Reason: The style guide requires consistent list item endings.

### QL-021 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `up to`
- Target: `그러나 Xenova/whisper-tiny.en은(는) 인기 있는 모델이며(앞에서 언급했듯이 Transformer.js의 기본 ASR 모델이기도 합니다), 이를 사용하는 앱이 여러 개일 수 있음을 쉽게 상상할 수 있습니다. 이 상황을 시뮬레이션하기 위해, 이전의 동일한 예제 앱을 different origin에서 제공하는 것으로 가정합니다. 이 다른 원본(origin) 애플리케이션을 방문하면, 거의 즉시 사용할 수 있도록 하는 대신 브라우저는 모든 모델 리소스를 다시 다운로드하고 캐시해야 하므로 바이트 단위로 동일하더라도 중복 다운로드 및 저장이 발생합니다. 이 toy 예제에서도 이는 누적되어 177 MB의 중복 다운로드 및 저장으로 이어진다는 점을 Chrome DevTools의 Storage 섹션에서 확인할 수 있습니다 Application panel. 이를 상상해 보실 수 있습니다.`
- Suggested fix: Preserve the strength of `up to` using: 최대.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-022 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `다양한 앱이 서로 다른 오리진에서 실행되더라도 결국 동일한 CDN URL에서 리소스를 제공한다면 캐싱 문제는 없을 것이라고 생각할 수 있습니다. 하지만 오랜 기간 브라우저에서의 캐싱 방식은 그렇지 않습니다. 기사 Gaining security and privacy by partitioning the cache가 모든 세부 정보를 다룹니다. 본질적으로, 캐시가 오리진별로 분리되어 있어 타이밍 공격을 방지합니다: 웹사이트가 HTTP 요청에 응답하는 데 걸리는 시간은 브라우저가 과거에 같은 리소스에 접근했다는 것을 암시할 수 있어 보안 및 개인정보 유출 취약점을 만들 수 있습니다.`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-023 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `may`
- Target: `구체적인 구현은 브라우저에 따라 다를 수 있지만 Chrome에서는 캐시된 리소스가 **리소스 URL** 외에 네트워크 격리 키(Network Isolation Key)로도 키가 부여됩니다. 네트워크 격리 키는 **최상위 사이트**와 **현재 프레임 사이트**로 구성됩니다. 앞의 toy 예제가 https://googlechrome.github.io와 https://rawcdn.rawgit.net에서 호스팅되었다고 가정하고, 둘 다 https://cdn.jsdelivr.net/npm/onnxruntime-web@1.26.0-dev.20260416-b7804b056c/dist/ort-wasm-simd-threaded.asyncify.wasm의 Wasm 런타임을 사용한다면, 캐시 키는 아래 표와 같이 보일 것입니다.`
- Suggested fix: Preserve the strength of `may` using: 수 있습니다, 일 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-024 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `제안된 **Cross-Origin Storage (COS) API**는 웹 앱이 원점 경계를 넘어 큰 파일을 저장하고 검색할 수 있도록 하는 전용 navigator.crossOriginStorage 인터페이스를 도입합니다. 이는 URL이 아니라 암호학적 해시로 식별됩니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-025 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `누가 무엇을 읽을 수 있는지 제어`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-026 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `모든 리소스를 전역적으로 공유해서는 안됩니다. COS는 파일 저장 시 가시성을 제어하기 위해 origins 옵션을 통해 개발자에게 정밀한 제어를 제공합니다.`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-027 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `특정 오리진 목록, 예를 들어 origins: ['https://write.example.com', 'https://calculate.example.com']과 같은 목록은 이 사이트들에 대한 접근을 **제한**합니다. 이는 서로의 소유 자산 간에 공유되지만 다른 누구도 검색될 필요가 없는 리소스와 같은 사례에 잘 맞습니다. 예: 상업용 오피스 도구에서 사용되는 독점 교정 AI 모델.`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-028 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `must`
- Target: `하나 중요한 규칙: 가시성은 상향은 가능하지만 하향은 불가능합니다. 파일이 이미 전역적으로 공유 가능하면, 나중에 제한된 origins 목록으로 저장하려는 시도는 묵시적으로 무시됩니다. 이는 악의적인 행위자가 공개 리소스를 재저장하고 가용성을 축소하는 것을 방지합니다. 반대로도 가능합니다: 처음에 제한된 origins 목록으로 저장된 파일은 나중에 더 관대하게 설정될 수 있습니다. 어떤 사이트든, 원래 저장자뿐 아니라, 같은 해시(requestFileHandle())에 대해 같은 해시를 가진 리소스에 대해 더 넓은 origins 값을 갖고 호출할 수 있으며, 브라우저가 해시가 일치하는지 확인하면 그 리소스는 그 시점부터 더 넓은 대중에게 제공됩니다. 업그레이드가 이루어져도 반환된 핸들을 통해 전체 파일을 여전히 써야 한다는 점에 주의하십시오. 이 요건은 COS에 특정 파일이 이미 저장되어 있는지 여부를 악용하려는 사이드 채널을 방지하기 위해 존재합니다.`
- Suggested fix: Preserve the strength of `must` using: 반드시, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-029 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `물론 교차 출처 공유 캐시는 분할된 HTTP 캐시와 같은 문제를 역으로 제기합니다: 어떤 사이트든 해시로 파일의 존재 여부를 확인할 수 있다면, 예를 들어 게임 엔진 Wasm 모듈이 캐시되어 있는지 확인함으로써 사용자의 브라우징 이력에 대해 뭔가를 알아낼 수 있지 않을까요?`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-030 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `먼저, origins 필드: 전역적으로 탐지 가능하지 않는 독점 리소스는 단순히 origins: '*'로 저장해서는 안 됩니다. 필요할 때마다 개발자 교육을 통해 고려되도록 권장됩니다.`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-031 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `may`
- Target: `해당 플래그를 설정하면, 각 Xet-tracked 모델 파일(대형 ONNX 가중치 파일)의 SHA-256 해시를 원시 포인터 example raw pointer file를 가져와서 oid sha256: 필드를 추출해 얻은 해시를 navigator.crossOriginStorage의 키로 사용합니다. 만약 다른 사이트가 먼저 COS에 저장해 두었다면 네트워크 왕복 없이 즉시 제공됩니다. 그렇지 않으면 일반 다운로드로 폴백하고 다음 호출자를 위해 COS에 결과를 저장합니다. 토이 예제에서 실제 이점은 Xenova/whisper-tiny.en와 Xenova/distilbert-base-uncased-finetuned-sst-2-english(그리고 물론 ort-wasm-simd-threaded.asyncify.wasm)가 서로 다른 오리진에서 요청하더라도 한 번만 교차하면 된다는 점입니다.`
- Suggested fix: Preserve the strength of `may` using: 수 있습니다, 일 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-032 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `may`
- Target: `지금 바로 시도해 보기`
- Suggested fix: Preserve the strength of `may` using: 수 있습니다, 일 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-033 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `지금 바로 시도해 보기`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-034 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `may`
- Target: `A resource seen in the Cross-Origin Storage extension, showing it's shared between two origins.`
- Suggested fix: Preserve the strength of `may` using: 수 있습니다, 일 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-035 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `A resource seen in the Cross-Origin Storage extension, showing it's shared between two origins.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-036 accuracy / major

- Message: Translation may add a causal explanation that is not in the source.
- Target: `따라서`
- Suggested fix: Remove invented causal explanation unless the source explicitly states it.
- Reason: The style guide forbids adding technical explanations, reasons, examples, or conclusions.

### QL-037 accuracy / major

- Message: Translation may add a causal explanation that is not in the source.
- Target: `때문에`
- Suggested fix: Remove invented causal explanation unless the source explicitly states it.
- Reason: The style guide forbids adding technical explanations, reasons, examples, or conclusions.

### QL-038 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `A minimalistic example of the automatic speech recognition pipeline.`
- Target: `A minimalistic example of the automatic speech recognition pipeline.`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-039 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `The Chrome DevTools Cache storage section showing Whisper AI model resources and Wasm runtime files after visiting the app.`
- Target: `The Chrome DevTools Cache storage section showing Whisper AI model resources and Wasm runtime files after visiting the app.`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-040 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `The Chrome DevTools Storage overview showing 177 MB of used storage.`
- Target: `The Chrome DevTools Storage overview showing 177 MB of used storage.`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-041 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `image`
- Target: `image`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-042 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `Chrome DevTools Network panel showing the download of the Wasm runtime resource.`
- Target: `Chrome DevTools Network panel showing the download of the Wasm runtime resource.`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-043 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `Chrome Web Store page for the Cross-Origin Storage extension.`
- Target: `Chrome Web Store page for the Cross-Origin Storage extension.`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-044 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `A resource seen in the Cross-Origin Storage extension, showing it's shared between two origins.`
- Target: `A resource seen in the Cross-Origin Storage extension, showing it's shared between two origins.`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-045 fluency / minor

- Message: Link text appears untranslated.
- Source: `Thomas Steiner`
- Target: `Thomas Steiner`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-046 fluency / minor

- Message: Link text appears untranslated.
- Source: ``pipeline()``
- Target: ``pipeline()``
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-047 fluency / minor

- Message: Link text appears untranslated.
- Source: ``Xenova/whisper-tiny.en``
- Target: ``Xenova/whisper-tiny.en``
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-048 fluency / minor

- Message: Link text appears untranslated.
- Source: `default model resolution`
- Target: `default model resolution`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-049 fluency / minor

- Message: Link text appears untranslated.
- Source: `excerpt`
- Target: `excerpt`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-050 fluency / minor

- Message: Link text appears untranslated.
- Source: `run this example in the browser`
- Target: `run this example in the browser`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-051 fluency / minor

- Message: Link text appears untranslated.
- Source: `Cache storage`
- Target: `Cache storage`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-052 fluency / minor

- Message: Link text appears untranslated.
- Source: `Cache`
- Target: `Web Cache`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-053 fluency / minor

- Message: Link text appears untranslated.
- Source: `different origin`
- Target: `different origin`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-054 fluency / minor

- Message: Link text appears untranslated.
- Source: `Application panel`
- Target: `Application panel`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-055 fluency / minor

- Message: Link text appears untranslated.
- Source: `by default`
- Target: `by default`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-056 fluency / minor

- Message: Link text appears untranslated.
- Source: ``Xenova/distilbert-base-uncased-finetuned-sst-2-english``
- Target: ``Xenova/distilbert-base-uncased-finetuned-sst-2-english``
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-057 fluency / minor

- Message: Link text appears untranslated.
- Source: `from the underlying ONNX Runtime library`
- Target: `from the underlying ONNX Runtime library`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-058 fluency / minor

- Message: Link text appears untranslated.
- Source: `extended demo on a different origin`
- Target: `extended demo on a different origin`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-059 fluency / minor

- Message: Link text appears untranslated.
- Source: `**Network** tab`
- Target: `**Network** tab`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-060 fluency / minor

- Message: Link text appears untranslated.
- Source: `Hugging Face Hub`
- Target: `Hugging Face Hub`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-061 fluency / minor

- Message: Link text appears untranslated.
- Source: ``https://huggingface.co/Xenova/distilbert-base-uncased-finetuned-sst-2-english/resolve/main/config.json``
- Target: ``https://huggingface.co/Xenova/distilbert-base-uncased-finetuned-sst-2-english/resolve/main/config.json``
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-062 fluency / minor

- Message: Link text appears untranslated.
- Source: ``https://huggingface.co/api/resolve-cache/models/Xenova/distilbert-base-uncased-finetuned-sst-2-english/0b6928efcb76139cae2c6881d49cda67fe119f42/config.json?%2FXenova%2Fdistilbert-base-uncased-finetuned-sst-2-english%2Fresolve%2Fmain%2Fconfig.json=&etag=%223c36342ef1f74de2797d667c68c6b7b988d0b87c%22``
- Target: ``https://huggingface.co/api/resolve-cache/models/Xenova/distilbert-base-uncased-finetuned-sst-2-english/0b6928efcb76139cae2c6881d49cda67fe119f42/config.json?%2FXenova%2Fdistilbert-base-uncased-finetuned-sst-2-english%2Fresolve%2Fmain%2Fconfig.json=&etag=%223c36342ef1f74de2797d667c68c6b7b988d0b87c%22``
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-063 fluency / minor

- Message: Link text appears untranslated.
- Source: `jsDelivr CDN`
- Target: `jsDelivr CDN`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-064 fluency / minor

- Message: Link text appears untranslated.
- Source: ``https://cdn.jsdelivr.net/npm/onnxruntime-web@1.26.0-dev.20260416-b7804b056c/dist/ort-wasm-simd-threaded.asyncify.wasm``
- Target: ``https://cdn.jsdelivr.net/npm/onnxruntime-web@1.26.0-dev.20260416-b7804b056c/dist/ort-wasm-simd-threaded.asyncify.wasm``
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-065 fluency / minor

- Message: Link text appears untranslated.
- Source: `Gaining security and privacy by partitioning the cache`
- Target: `Gaining security and privacy by partitioning the cache`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-066 fluency / minor

- Message: Link text appears untranslated.
- Source: `Cross-Origin Storage extension`
- Target: `Cross-Origin Storage extension`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-067 fluency / minor

- Message: Link text appears untranslated.
- Source: `Cross-Origin Storage repository`
- Target: `Cross-Origin Storage repository`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-068 fluency / minor

- Message: Link text appears untranslated.
- Source: ``FileSystemFileHandle``
- Target: ``FileSystemFileHandle``
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-069 fluency / minor

- Message: Link text appears untranslated.
- Source: ``getFile()``
- Target: ``getFile()``
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-070 fluency / minor

- Message: Link text appears untranslated.
- Source: ``File``
- Target: ``File``
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-071 fluency / minor

- Message: Link text appears untranslated.
- Source: ``Blob``
- Target: ``Blob``
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-072 fluency / minor

- Message: Link text appears untranslated.
- Source: `File System Standard`
- Target: `File System Standard`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-073 fluency / minor

- Message: Link text appears untranslated.
- Source: ``FileSystemDirectoryHandle.getFileHandle()``
- Target: ``FileSystemDirectoryHandle.getFileHandle()``
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-074 fluency / minor

- Message: Link text appears untranslated.
- Source: `Origin Private File System`
- Target: `Origin Private File System`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-075 fluency / minor

- Message: Link text appears untranslated.
- Source: `same-site`
- Target: `same-site`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-076 fluency / minor

- Message: Link text appears untranslated.
- Source: `Pull request #1549`
- Target: `Pull request #1549`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-077 fluency / minor

- Message: Link text appears untranslated.
- Source: `Xet-tracked`
- Target: `Xet-tracked`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-078 fluency / minor

- Message: Link text appears untranslated.
- Source: `example raw pointer file`
- Target: `example raw pointer file`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-079 fluency / minor

- Message: Link text appears untranslated.
- Source: `any of the other Whisper variants`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-080 fluency / minor

- Message: Link text appears untranslated.
- Source: ``Xenova/whisper-large-v3``
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-081 fluency / minor

- Message: Link text appears untranslated.
- Source: `Model Registry`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-082 fluency / minor

- Message: Link text appears untranslated.
- Source: ``ModelRegistry.is_pipeline_cached()``
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-083 fluency / minor

- Message: Link text appears untranslated.
- Source: `source code of the extension`
- Target: `source code of the extension`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-084 fluency / minor

- Message: Link text appears untranslated.
- Source: `usage instructions`
- Target: `usage instructions`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-085 fluency / minor

- Message: Link text appears untranslated.
- Source: `toy example with COS enabled`
- Target: `toy example with COS enabled`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-086 fluency / minor

- Message: Link text appears untranslated.
- Source: `toy example with COS enabled from the second origin`
- Target: `toy example with COS enabled from the second origin`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-087 fluency / minor

- Message: Link text appears untranslated.
- Source: ``https://huggingface.co/Xenova/whisper-tiny.en/blob/main/onnx/decoder_model_merged.onnx``
- Target: ``https://huggingface.co/Xenova/whisper-tiny.en/blob/main/onnx/decoder_model_merged.onnx``
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-088 fluency / minor

- Message: Link text appears untranslated.
- Source: `WebLLM`
- Target: `WebLLM`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-089 fluency / minor

- Message: Link text appears untranslated.
- Source: `documentation`
- Target: `documentation`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-090 fluency / minor

- Message: Link text appears untranslated.
- Source: `wllama`
- Target: `wllama`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-091 fluency / minor

- Message: Link text appears untranslated.
- Source: `PR`
- Target: `PR`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-092 fluency / minor

- Message: Link text appears untranslated.
- Source: `considering implementing the COS API`
- Target: `considering implementing the COS API`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-093 fluency / minor

- Message: Link text appears untranslated.
- Source: `express support`
- Target: `express support`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.
