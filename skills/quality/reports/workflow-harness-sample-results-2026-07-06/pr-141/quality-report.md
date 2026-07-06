# Quality Report

- Status: reject
- Quality Score: 0.0
- Hard failures: 3
- Issues: 110
- Source available: True
- Source changed: False
- Source segments: 253
- Target segments: 252

## Scorecard

| Dimension | Score |
| --- | ---: |
| adequacy | 0.0 |
| technical_accuracy | 40.0 |
| completeness | 0.0 |
| terminology | 40.0 |
| fluency | 0.0 |
| publishing_integrity | 40.0 |
| style_locale | 60.0 |

## Metrics

- qe_metric: heuristic
- qe_average: 0.8639
- qe_min: 0.0
- embedding_similarity_average: 0.7743
- embedding_similarity_min: 0.0189
- cache_hits: 50
- cache_misses: 454

## Style Guide

- Enabled: True
- Guide: `/Users/harheem/hf-workflow/skills/quality/style/hf-blog-ko-translation-guide.md`
- Policy: `/Users/harheem/hf-workflow/skills/quality/configs/style_policy.yml`
- Style score: 60.0
- Rule hits: {'alt_text_caption': 22, 'information_addition': 2, 'link_text_translation': 22, 'list_consistency': 1, 'modal_strength': 15, 'translationese': 1}

## Style Guide Findings

| Rule | Severity | Segment | Current | Suggested |
| --- | --- | --- | --- | --- |
| translationese | minor |  | 에 의해 | Rewrite the sentence in natural Korean. |
| list_consistency | minor |  | sentence, sentence, sentence, phrase, phrase, phrase, phrase, sentence, sentence, phrase, phrase, sentence, sentence, sentence, sentence, phrase, phrase, phrase, phrase, phrase, phrase, phrase, phrase, sentence, phrase, phrase, phrase, phrase | Use either sentence-style endings or phrase-style endings consistently within one list. |
| modal_strength | major | b_003 | *프로파일링할 수 없는 것은 최적화할 수 없다.* | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_005 | 문제는 프로파일링에 가파른 온-램프가 있다는 점이다. 추적은 다채로운 색상의 직사각형으로 가득 찬 벽처럼 보인다. 이벤트는 위협적으로 보이는 이름을 담고 있다. 대부분의 튜토리얼은 이미 그것들을 읽을 수 있다고 가정한다. 그래서 우리가 *프로파일링을 해야 한다고 해도*, 추적을 여는 것은 나중에(또는 다른 사람에게) 맡겨두는 일이 되기 쉽다. 이 글과 시리즈는 그 온-램프를 낮추려는 시도다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_005 | 문제는 프로파일링에 가파른 온-램프가 있다는 점이다. 추적은 다채로운 색상의 직사각형으로 가득 찬 벽처럼 보인다. 이벤트는 위협적으로 보이는 이름을 담고 있다. 대부분의 튜토리얼은 이미 그것들을 읽을 수 있다고 가정한다. 그래서 우리가 *프로파일링을 해야 한다고 해도*, 추적을 여는 것은 나중에(또는 다른 사람에게) 맡겨두는 일이 되기 쉽다. 이 글과 시리즈는 그 온-램프를 낮추려는 시도다. | Preserve the strength of `should` using: 좋습니다, 해야 합니다. |
| modal_strength | major | p_010 | 우리는 초보자의 시각에서 여정을 기록합니다. 기본적인 PyTorch 이외의 전제 조건은 없습니다. 이를 천천히 읽되 "아하!" 모멘트를 즐깁니다. 글의 구성은 의도적으로 질문 중심으로 구성되어 있습니다: 추적을 열고 "잠깐, 왜 *그 일이* 일어나지?"라고 묻고, 무언가가 이해될 때까지 그 이유를 쫓습니다. 끝에 가면 여러분은 다음을 알게 될 것입니다: | Preserve the strength of `should` using: 좋습니다, 해야 합니다. |
| modal_strength | major | l_011 | torch.profiler를 설정하는 방법과 그것이 실제로 반환하는 내용, | Preserve the strength of `up to` using: 최대. |
| modal_strength | major | p_041 | 다른 열은 activities 내 torch.profiler.profile에서 CPU 또는 GPU 또는 다른 장치들에서 이벤트가 차지하는 시간과 관련이 있습니다. 어떤 이벤트가 가장 많은 시간인지를 살펴보고, 그 이벤트가 실제로 그 시간만큼 걸리는지 직관적으로 이해해 보세요. 또한 "호출 수(# of Calls)" 열은 이벤트가 얼마나 자주 트리거되었는지를 나타냅니다. | Preserve the strength of `should` using: 좋습니다, 해야 합니다. |
| modal_strength | major | p_044 | CPU 시간은 ms에서, GPU 시간은 us에서 나타납니다. 관점으로 보면 GPU에서 소요된 시간(커널 ampere_bf16_s16816gemm...)은 CPU에서 소요된 시간(matmul_add 연산)보다 1% 미만입니다. GPU는 대부분의 시간 동안 대기 상태이며, 이는 즉시 나타나는 적신호입니다. 이러한 현상은 GPU가 아주 작은 행렬 곱을 아주 빠르게 계산할 수 있기 때문이며, 우리의 코드는 커널을 준비하고, GPU에서 실행을 시작하고, 곱하기를 위해 데이터를 보내고 결과를 모으는 데 대부분의 시간을 소비합니다. 이 개념은 오버헤드-바운드(overhead-bound) 알고리즘으로 알려져 있습니다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_093 | 그림 8에서 CPU 레인과 GPU 레인 사이에 약 2.5 ms의 오프설정이 존재함을 확인할 수 있습니다. 이는 CPU가 CUDA 커널을 제출하고 실제로 실행되기까지의 지연 시간입니다. 워밍업 단계와 스케줄의 wait 및 warmup이 합쳐져 GPU를 바쁘게 유지시켜 오프셋을 줄여줄 거라고 생각할 수 있습니다. | Preserve the strength of `should` using: 좋습니다, 해야 합니다. |

## Issues

### QL-001 technical / critical

- Message: inline code mismatch.
- Source: `/tmp/torchinductor_<user>/fxgraph, addmm, torch.compile, torch.compile`
- Target: `kernels, nn.Linear, transformers`
- Suggested fix: Preserve source inline code exactly.
- Reason: Hard gate exact-match validator failed: missing=['/tmp/torchinductor_<user>/fxgraph', 'addmm', 'torch.compile', 'torch.compile']; extra=['kernels', 'nn.Linear', 'transformers']

### QL-002 formatting / critical

- Message: link target mismatch.
- Source: `https://developer.nvidia.com/cublas, https://huggingface.co/blog/torch-mlp-fusion, https://huggingface.co/docs/hub/spaces-dev-mode, https://huggingface.co/docs/huggingface_hub/en/guides/jobs`
- Suggested fix: Preserve source link target exactly.
- Reason: Hard gate exact-match validator failed: missing=['https://developer.nvidia.com/cublas', 'https://huggingface.co/blog/torch-mlp-fusion', 'https://huggingface.co/docs/hub/spaces-dev-mode', 'https://huggingface.co/docs/huggingface_hub/en/guides/jobs']

### QL-003 formatting / major

- Message: bare URL mismatch.
- Source: `https://huggingface.co/blog/torch-mlp-fusion, https://huggingface.co/blog/torch-profiler`
- Suggested fix: Preserve source bare URL exactly.
- Reason: Review gate exact-match validator failed: missing=['https://huggingface.co/blog/torch-mlp-fusion', 'https://huggingface.co/blog/torch-profiler']

### QL-004 technical / major

- Message: Python/API identifier mismatch.
- Source: `torch.compile, torch.compile, torch.compile, torch.compile, torch.profiler, torch.profiler`
- Suggested fix: Preserve source Python/API identifier exactly.
- Reason: Review gate exact-match validator failed: missing=['torch.compile', 'torch.compile', 'torch.compile', 'torch.compile', 'torch.profiler', 'torch.profiler']

### QL-005 technical / major

- Message: number/unit token mismatch.
- Source: `2`
- Target: `0`
- Suggested fix: Preserve source number/unit token exactly.
- Reason: Review gate exact-match validator failed: missing=['2']; extra=['0']

### QL-006 formatting / critical

- Message: Markdown table shape mismatch.
- Source: `[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [4, 4, 4, 4, 4], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [2, 2, 2], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [3, 3, 3, 3, 3], [2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2]]`
- Target: `[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [4, 4, 4, 4, 4], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [2, 2, 2], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [3, 3, 3, 3, 3], [2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2]]`
- Suggested fix: Preserve source table row and column counts.

### QL-007 accuracy / major

- Message: Source segment coverage is low.
- Source: `source_segments=253`
- Target: `target_segments=252`
- Suggested fix: Check for omitted paragraphs, headings, list items, or table cells.
- Reason: Segment count validator found fewer target text segments than source text segments.

### QL-008 accuracy / major

- Message: Duplicate target segments detected.
- Target: `what you see | what it usually means`
- Suggested fix: Remove repeated translated segments unless the source intentionally repeats them.
- Reason: Duplicate detector found repeated normalized target segments.

### QL-009 accuracy / major

- Message: QE metric score is low.
- Target: `0.4149`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-010 accuracy / major

- Message: QE metric score is low.
- Target: `0.4727`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-011 accuracy / major

- Message: QE metric score is low.
- Target: `0.3625`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-012 accuracy / major

- Message: QE metric score is low.
- Target: `0.0000`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-013 accuracy / minor

- Message: Embedding similarity is an outlier.
- Target: `0.0271`
- Suggested fix: Review whether the segment still corresponds to the source.
- Reason: Embedding similarity is below threshold 0.08.

### QL-014 accuracy / major

- Message: QE metric score is low.
- Target: `0.4226`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-015 accuracy / major

- Message: QE metric score is low.
- Target: `0.5375`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-016 accuracy / major

- Message: QE metric score is low.
- Target: `0.1330`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-017 accuracy / minor

- Message: Embedding similarity is an outlier.
- Target: `0.0253`
- Suggested fix: Review whether the segment still corresponds to the source.
- Reason: Embedding similarity is below threshold 0.08.

### QL-018 accuracy / major

- Message: QE metric score is low.
- Target: `0.5285`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-019 accuracy / major

- Message: QE metric score is low.
- Target: `0.1216`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-020 accuracy / minor

- Message: Embedding similarity is an outlier.
- Target: `0.0189`
- Suggested fix: Review whether the segment still corresponds to the source.
- Reason: Embedding similarity is below threshold 0.08.

### QL-021 accuracy / major

- Message: QE metric score is low.
- Target: `0.2295`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-022 accuracy / major

- Message: QE metric score is low.
- Target: `0.4264`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-023 accuracy / major

- Message: QE metric score is low.
- Target: `0.3900`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-024 accuracy / major

- Message: QE metric score is low.
- Target: `0.4288`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-025 accuracy / major

- Message: QE metric score is low.
- Target: `0.4347`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-026 accuracy / major

- Message: QE metric score is low.
- Target: `0.3900`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-027 accuracy / major

- Message: QE metric score is low.
- Target: `0.1354`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-028 accuracy / minor

- Message: Embedding similarity is an outlier.
- Target: `0.0311`
- Suggested fix: Review whether the segment still corresponds to the source.
- Reason: Embedding similarity is below threshold 0.08.

### QL-029 accuracy / major

- Message: QE metric score is low.
- Target: `0.4347`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-030 accuracy / major

- Message: QE metric score is low.
- Target: `0.3900`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-031 accuracy / major

- Message: QE metric score is low.
- Target: `0.1411`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-032 accuracy / minor

- Message: Embedding similarity is an outlier.
- Target: `0.0340`
- Suggested fix: Review whether the segment still corresponds to the source.
- Reason: Embedding similarity is below threshold 0.08.

### QL-033 accuracy / major

- Message: QE metric score is low.
- Target: `0.4264`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-034 accuracy / major

- Message: QE metric score is low.
- Target: `0.3900`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-035 accuracy / major

- Message: QE metric score is low.
- Target: `0.4383`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-036 accuracy / major

- Message: QE metric score is low.
- Target: `0.4427`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-037 accuracy / major

- Message: QE metric score is low.
- Target: `0.4479`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-038 accuracy / major

- Message: QE metric score is low.
- Target: `0.2715`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-039 accuracy / minor

- Message: Embedding similarity is an outlier.
- Target: `0.0528`
- Suggested fix: Review whether the segment still corresponds to the source.
- Reason: Embedding similarity is below threshold 0.08.

### QL-040 accuracy / major

- Message: QE metric score is low.
- Target: `0.3986`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-041 accuracy / major

- Message: QE metric score is low.
- Target: `0.3900`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-042 accuracy / major

- Message: QE metric score is low.
- Target: `0.1934`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-043 accuracy / minor

- Message: Embedding similarity is an outlier.
- Target: `0.0655`
- Suggested fix: Review whether the segment still corresponds to the source.
- Reason: Embedding similarity is below threshold 0.08.

### QL-044 accuracy / major

- Message: QE metric score is low.
- Target: `0.5123`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-045 terminology / major

- Message: Product or library name was not preserved.
- Source: `Hugging Face`
- Suggested fix: Preserve `Hugging Face` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-046 terminology / major

- Message: Product or library name was not preserved.
- Source: `Transformers`
- Suggested fix: Preserve `Transformers` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-047 terminology / major

- Message: Product or library name was not preserved.
- Source: `Spaces`
- Suggested fix: Preserve `Spaces` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-048 fluency / minor

- Message: Translationese expression found.
- Target: `에 의해`
- Suggested fix: Rewrite the sentence in natural Korean.
- Reason: The style guide lists this expression as translationese to avoid.

### QL-049 style_locale / minor

- Message: List mixes sentence-style and phrase-style endings.
- Target: `sentence, sentence, sentence, phrase, phrase, phrase, phrase, sentence, sentence, phrase, phrase, sentence, sentence, sentence, sentence, phrase, phrase, phrase, phrase, phrase, phrase, phrase, phrase, sentence, phrase, phrase, phrase, phrase`
- Suggested fix: Use either sentence-style endings or phrase-style endings consistently within one list.
- Reason: The style guide requires consistent list item endings.

### QL-050 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `*프로파일링할 수 없는 것은 최적화할 수 없다.*`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-051 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `문제는 프로파일링에 가파른 온-램프가 있다는 점이다. 추적은 다채로운 색상의 직사각형으로 가득 찬 벽처럼 보인다. 이벤트는 위협적으로 보이는 이름을 담고 있다. 대부분의 튜토리얼은 이미 그것들을 읽을 수 있다고 가정한다. 그래서 우리가 *프로파일링을 해야 한다고 해도*, 추적을 여는 것은 나중에(또는 다른 사람에게) 맡겨두는 일이 되기 쉽다. 이 글과 시리즈는 그 온-램프를 낮추려는 시도다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-052 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `문제는 프로파일링에 가파른 온-램프가 있다는 점이다. 추적은 다채로운 색상의 직사각형으로 가득 찬 벽처럼 보인다. 이벤트는 위협적으로 보이는 이름을 담고 있다. 대부분의 튜토리얼은 이미 그것들을 읽을 수 있다고 가정한다. 그래서 우리가 *프로파일링을 해야 한다고 해도*, 추적을 여는 것은 나중에(또는 다른 사람에게) 맡겨두는 일이 되기 쉽다. 이 글과 시리즈는 그 온-램프를 낮추려는 시도다.`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-053 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `우리는 초보자의 시각에서 여정을 기록합니다. 기본적인 PyTorch 이외의 전제 조건은 없습니다. 이를 천천히 읽되 "아하!" 모멘트를 즐깁니다. 글의 구성은 의도적으로 질문 중심으로 구성되어 있습니다: 추적을 열고 "잠깐, 왜 *그 일이* 일어나지?"라고 묻고, 무언가가 이해될 때까지 그 이유를 쫓습니다. 끝에 가면 여러분은 다음을 알게 될 것입니다:`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-054 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `up to`
- Target: `torch.profiler를 설정하는 방법과 그것이 실제로 반환하는 내용,`
- Suggested fix: Preserve the strength of `up to` using: 최대.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-055 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `다른 열은 activities 내 torch.profiler.profile에서 CPU 또는 GPU 또는 다른 장치들에서 이벤트가 차지하는 시간과 관련이 있습니다. 어떤 이벤트가 가장 많은 시간인지를 살펴보고, 그 이벤트가 실제로 그 시간만큼 걸리는지 직관적으로 이해해 보세요. 또한 "호출 수(# of Calls)" 열은 이벤트가 얼마나 자주 트리거되었는지를 나타냅니다.`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-056 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `CPU 시간은 ms에서, GPU 시간은 us에서 나타납니다. 관점으로 보면 GPU에서 소요된 시간(커널 ampere_bf16_s16816gemm...)은 CPU에서 소요된 시간(matmul_add 연산)보다 1% 미만입니다. GPU는 대부분의 시간 동안 대기 상태이며, 이는 즉시 나타나는 적신호입니다. 이러한 현상은 GPU가 아주 작은 행렬 곱을 아주 빠르게 계산할 수 있기 때문이며, 우리의 코드는 커널을 준비하고, GPU에서 실행을 시작하고, 곱하기를 위해 데이터를 보내고 결과를 모으는 데 대부분의 시간을 소비합니다. 이 개념은 오버헤드-바운드(overhead-bound) 알고리즘으로 알려져 있습니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-057 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `그림 8에서 CPU 레인과 GPU 레인 사이에 약 2.5 ms의 오프설정이 존재함을 확인할 수 있습니다. 이는 CPU가 CUDA 커널을 제출하고 실제로 실행되기까지의 지연 시간입니다. 워밍업 단계와 스케줄의 wait 및 warmup이 합쳐져 GPU를 바쁘게 유지시켜 오프셋을 줄여줄 거라고 생각할 수 있습니다.`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-058 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `cudaOccupancyMaxActiveBlocksPerMultiprocessor은 계획(plan) 호출이며 순수하게 CPU 측에 있습니다. "주어진 커널 함수, 선택된 블록 크기, 선택된 동적 공유 메모리 크기"를 바탕으로 이 커널의 블록이 한 SM에 얼마나 동시에 존재할 수 있는지 묻습니다."`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-059 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `이 해시로 키가 부여된 디스크상의 생성된 코드를 찾아볼 수 있으며, Inductor가 실제로 생성한 Triton/C++를 읽고 싶을 때 유용합니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-060 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `[!NOTE]`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-061 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `정말로 원하던 융합은 x·w + b(여기서는 out = α·A·B + β·C가) 추가 메모리 트래픽 없이 단일 커널로 축소되는 것이었지만 그렇지 않았습니다. Inductor는 두 개의 메모리 접촉 작업을 보존했으며, 바이어스 복사를 memcpy로, 덧셈을 GEMM 에필로그로 라벨링만 바꿨습니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-062 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `한 이벤트가 CUDA total를 지배 | 핫스팟입니다. 최적화 시작점으로 삼으세요.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-063 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `record_function("...") 시작과 내부의 첫 번째 aten::* 사이의 큰 간격 | 같은 콜드 스타트 비용, 확대해 본 것일 뿐. 주석이 들어갔지만 디스패치는 아직 일어나지 않았습니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-064 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `:-- | :--`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

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

### QL-067 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `Thumbnail of the blog post`
- Target: `Thumbnail of the blog post`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-068 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `Profiler table for matmul add on 64 sized matrices`
- Target: `Profiler table for matmul add on 64 sized matrices`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-069 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `Profiler table for matmul add algorithm on 4096 sized matrices`
- Target: `Profiler table for matmul add algorithm on 4096 sized matrices`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-070 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `PyTorch profiler trace of a 64×64 bf16 matmul followed by an add on a CUDA GPU`
- Target: `PyTorch profiler trace of a 64×64 bf16 matmul followed by an add on a CUDA GPU`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-071 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `PyTorch profiler trace with the CPU lane and GPU lane labelled side by side in Perfetto`
- Target: `PyTorch profiler trace with the CPU lane and GPU lane labelled side by side in Perfetto`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-072 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `ProfileStep#2 in a PyTorch profiler trace appears wider than ProfileStep#3 and ProfileStep#4`
- Target: `ProfileStep#2 in a PyTorch profiler trace appears wider than ProfileStep#3 and ProfileStep#4`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-073 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `228 microsecond gap between record_function matmul_add and the aten::matmul dispatch in profile step 2`
- Target: `228 microsecond gap between record_function matmul_add and the aten::matmul dispatch in profile step 2`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-074 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `PyTorch profiler trace after warmup steps where ProfileStep#2 no longer shows cold-start overhead`
- Target: `PyTorch profiler trace after warmup steps where ProfileStep#2 no longer shows cold-start overhead`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-075 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `2.32 millisecond offset between the CPU lane and the GPU lane in a PyTorch profiler trace`
- Target: `2.32 millisecond offset between the CPU lane and the GPU lane in a PyTorch profiler trace`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-076 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `PyTorch profiler trace with wait=0 warmup=0 showing an Activity Buffer Request between steps`
- Target: `PyTorch profiler trace with wait=0 warmup=0 showing an Activity Buffer Request between steps`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-077 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `gap between matmul and add CUDA kernels caused by profiler buffer request`
- Target: `gap between matmul and add CUDA kernels caused by profiler buffer request`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-078 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `PyTorch profiler trace of 20 active iterations confirming the buffer-request gap only appears once`
- Target: `PyTorch profiler trace of 20 active iterations confirming the buffer-request gap only appears once`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-079 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `nested CPU dispatch chain in PyTorch profiler: ProfileStep, matmul_add, aten::matmul, aten::mm`
- Target: `nested CPU dispatch chain in PyTorch profiler: ProfileStep, matmul_add, aten::matmul, aten::mm`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-080 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `PyTorch profiler trace showing aten::matmul dispatching aten::bmm for 3D batched tensors`
- Target: `PyTorch profiler trace showing aten::matmul dispatching aten::bmm for 3D batched tensors`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-081 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `CPU lane showing cudaOccupancyMaxActiveBlocksPerMultiprocessor preceding the matmul cudaLaunchKernel`
- Target: `CPU lane showing cudaOccupancyMaxActiveBlocksPerMultiprocessor preceding the matmul cudaLaunchKernel`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-082 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `cuBLAS matmul kernel resource footprint: registers, shared memory and block size in Perfetto`
- Target: `cuBLAS matmul kernel resource footprint: registers, shared memory and block size in Perfetto`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-083 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `elementwise add CUDA kernel resource footprint with 32 registers and zero shared memory`
- Target: `elementwise add CUDA kernel resource footprint with 32 registers and zero shared memory`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-084 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `4096x4096 bf16 matmul kernel timings varying across profiler steps on the same GPU`
- Target: `4096x4096 bf16 matmul kernel timings varying across profiler steps on the same GPU`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-085 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `PyTorch profiler trace of 20 matmul iterations showing kernel runtime variance`
- Target: `PyTorch profiler trace of 20 matmul iterations showing kernel runtime variance`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-086 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `torch.compile region highlighted in a PyTorch profiler trace, showing TorchDynamo and Inductor frames`
- Target: `torch.compile region highlighted in a PyTorch profiler trace, showing TorchDynamo and Inductor frames`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-087 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `Compiled trace showing aten::addmm replacing the eager aten::add and aten::mm pair`
- Target: `Compiled trace showing aten::addmm replacing the eager aten::add and aten::mm pair`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-088 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `compiled matmul trace showing Memcpy DtoD and GEMM kernels launched per step`
- Target: `compiled matmul trace showing Memcpy DtoD and GEMM kernels launched per step`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-089 fluency / minor

- Message: Link text appears untranslated.
- Source: `Here is the entire `01_matmul_add.py` script`
- Target: `Here is the entire `01_matmul_add.py` script`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-090 fluency / minor

- Message: Link text appears untranslated.
- Source: `Dev Mode with Spaces`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-091 fluency / minor

- Message: Link text appears untranslated.
- Source: `Hugging Face Jobs pipeline`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-092 fluency / minor

- Message: Link text appears untranslated.
- Source: `quipped by Dr. Sara Hooker`
- Target: `quipped by Dr. Sara Hooker`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-093 fluency / minor

- Message: Link text appears untranslated.
- Source: `later in the post`
- Target: `later in the post`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-094 fluency / minor

- Message: Link text appears untranslated.
- Source: `code to profile ready`
- Target: `code to profile ready`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-095 fluency / minor

- Message: Link text appears untranslated.
- Source: `Annotate`
- Target: `Annotate`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-096 fluency / minor

- Message: Link text appears untranslated.
- Source: `context manager`
- Target: `context manager`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-097 fluency / minor

- Message: Link text appears untranslated.
- Source: `profile`
- Target: `profile`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-098 fluency / minor

- Message: Link text appears untranslated.
- Source: `Perfetto UI`
- Target: `Perfetto UI`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-099 fluency / minor

- Message: Link text appears untranslated.
- Source: `script here`
- Target: `script here`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-100 fluency / minor

- Message: Link text appears untranslated.
- Source: `cuBLAS`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-101 fluency / minor

- Message: Link text appears untranslated.
- Source: `some more warmup steps`
- Target: `some more warmup steps`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-102 fluency / minor

- Message: Link text appears untranslated.
- Source: `Perfetto Trace for 64x64 with Warmup`
- Target: `Perfetto Trace for 64x64 with Warmup`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-103 fluency / minor

- Message: Link text appears untranslated.
- Source: `link`
- Target: `link`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-104 fluency / minor

- Message: Link text appears untranslated.
- Source: `ATen-level`
- Target: `ATen-level`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-105 fluency / minor

- Message: Link text appears untranslated.
- Source: `working on independent tiles`
- Target: `working on independent tiles`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-106 fluency / minor

- Message: Link text appears untranslated.
- Source: ``torch.addmm``
- Target: ``torch.addmm``
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-107 fluency / minor

- Message: Link text appears untranslated.
- Source: `In the posts`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-108 fluency / minor

- Message: Link text appears untranslated.
- Source: `Noe Flandre`
- Target: `Noe Flandre`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-109 fluency / minor

- Message: Link text appears untranslated.
- Source: `Suvaditya Mukherjee`
- Target: `Suvaditya Mukherjee`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-110 fluency / minor

- Message: Link text appears untranslated.
- Source: `Vidit Ostwal`
- Target: `Vidit Ostwal`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.
