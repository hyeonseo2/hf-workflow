# Quality Report

- Status: reject
- Quality Score: 49.0
- Hard failures: 0
- Issues: 24
- Source available: True
- Source changed: False
- Source segments: 81
- Target segments: 81

## Scorecard

| Dimension | Score |
| --- | ---: |
| adequacy | 0.0 |
| technical_accuracy | 80.0 |
| completeness | 60.0 |
| terminology | 80.0 |
| fluency | 0.0 |
| publishing_integrity | 100.0 |
| style_locale | 60.0 |

## Metrics

- qe_metric: heuristic
- qe_average: 0.9237
- qe_min: 0.4664
- embedding_similarity_average: 0.802
- embedding_similarity_min: 0.2905
- cache_hits: 162
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
- Rule hits: {'information_addition': 1, 'link_text_translation': 8, 'list_consistency': 1, 'modal_strength': 10}

## Style Guide Findings

| Rule | Severity | Segment | Current | Suggested |
| --- | --- | --- | --- | --- |
| list_consistency | minor |  | phrase, phrase, phrase, phrase, sentence, sentence, sentence, sentence, sentence | Use either sentence-style endings or phrase-style endings consistently within one list. |
| modal_strength | major | p_003 | 그 기본 설정은 편리하지만 한계도 있습니다. GitHub Actions는 느려지거나 유지 보수로 다운될 수 있고, 호스팅 머신은 일반적이며, GPU 접근은 대부분의 오픈 소스 프로젝트에서 바로 활성화하기 어렵습니다. Trackio의 경우 이러한 한계가 점점 문제로 다가왔습니다. 기본 단위 테스트와 프런트엔드 확인을 위한 안정적인 CPU CI는 물론 실제 CUDA 하드웨어에서 실행해야 하는 테스트를 위한 GPU CI도 원했습니다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_006 | 이 글에서는 GitHub 저장소에 대해 동일한 설정을 단계별로 재현하는 방법을 설명합니다. 에이전트를 사용 중이라면 이 글을 참고하실 수 있는데, 인간용으로 브라우저 기반 지침과 함께 CLI 지침이 함께 제공되기 때문입니다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_029 | 이 Space를 먼저 만드는 이유는 GitHub App에 웹훅 URL이 필요하고 그 URL이 Space에서 나오기 때문입니다. 이 Space는 당신의 고유 네임스페이스 아래에 있거나 쓰기 권한이 있는 허깅페이스 org 아래에 있어야 합니다. | Preserve the strength of `should` using: 좋습니다, 해야 합니다. |
| modal_strength | major | p_035 | 빌드가 완료되면 복제된 Space를 엽니다. 현재는 무시해도 되는 "Required Space secrets" 섹션이 보일 것입니다. 다음 단계에서 필요한 GitHub App 웹훅 URL이 랜딩 페이지에 표시되어야 하며, 아래와 같은 형태일 것입니다: | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_035 | 빌드가 완료되면 복제된 Space를 엽니다. 현재는 무시해도 되는 "Required Space secrets" 섹션이 보일 것입니다. 다음 단계에서 필요한 GitHub App 웹훅 URL이 랜딩 페이지에 표시되어야 하며, 아래와 같은 형태일 것입니다: | Preserve the strength of `should` using: 좋습니다, 해야 합니다. |
| modal_strength | major | p_043 | 설정 양식에서 허깅페이스 Jobs에서 CI가 실행되도록 하는 GitHub 리포를 입력합니다: | Preserve the strength of `should` using: 좋습니다, 해야 합니다. |
| modal_strength | major | p_044 | 그런 다음 GitHub App 생성을 위한 버튼을 클릭합니다. GitHub은 App의 이름을 선택하라고 묻습니다. 이름은 GitHub 계정이나 조직에서 사용 가능하면 무엇이든 상관없습니다. 제출하면 최종 화면에 hf CLI를 사용해 dispatcher Space에 App 자격 증명을 업로드하는 정확한 방법이 표시됩니다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_052 | 이 시점에서 dispatcher Space가 구성되어 있어야 합니다. GitHub App 설정 흐름은 Space에 App 자격 증명, 웹훅 시크릿 및 허깅페이스 토큰을 업로드하는 명령을 생성합니다. | Preserve the strength of `should` using: 좋습니다, 해야 합니다. |
| modal_strength | major | p_064 | 일반적인 GitHub Action처럼 로그를 확인할 수 있어야 합니다—예를 들어 이 Trackio PR #565에서. | Preserve the strength of `should` using: 좋습니다, 해야 합니다. |

## Issues

### QL-001 technical / major

- Message: number/unit token mismatch.
- Source: `1`
- Suggested fix: Preserve source number/unit token exactly.
- Reason: Review gate exact-match validator failed: missing=['1']

### QL-002 accuracy / major

- Message: Duplicate target segments detected.
- Target: `다음으로, dispatcher space 자체에서 github app을 생성하고 설치합니다. 이 app은 대기 중인 워크플로우 작업을 수신하고 임시 셀프호스드 러너 등록 토큰을 생성할 수 있는 권한이 필요합니다.`
- Suggested fix: Remove repeated translated segments unless the source intentionally repeats them.
- Reason: Duplicate detector found repeated normalized target segments.

### QL-003 accuracy / major

- Message: QE metric score is low.
- Target: `0.4664`
- Suggested fix: Review this segment for omission, unrelated translation, or over-compression.
- Reason: QE score is below threshold 0.55.

### QL-004 terminology / major

- Message: Product or library name was not preserved.
- Source: `Datasets`
- Suggested fix: Preserve `Datasets` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-005 style_locale / minor

- Message: List mixes sentence-style and phrase-style endings.
- Target: `phrase, phrase, phrase, phrase, sentence, sentence, sentence, sentence, sentence`
- Suggested fix: Use either sentence-style endings or phrase-style endings consistently within one list.
- Reason: The style guide requires consistent list item endings.

### QL-006 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `그 기본 설정은 편리하지만 한계도 있습니다. GitHub Actions는 느려지거나 유지 보수로 다운될 수 있고, 호스팅 머신은 일반적이며, GPU 접근은 대부분의 오픈 소스 프로젝트에서 바로 활성화하기 어렵습니다. Trackio의 경우 이러한 한계가 점점 문제로 다가왔습니다. 기본 단위 테스트와 프런트엔드 확인을 위한 안정적인 CPU CI는 물론 실제 CUDA 하드웨어에서 실행해야 하는 테스트를 위한 GPU CI도 원했습니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-007 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `이 글에서는 GitHub 저장소에 대해 동일한 설정을 단계별로 재현하는 방법을 설명합니다. 에이전트를 사용 중이라면 이 글을 참고하실 수 있는데, 인간용으로 브라우저 기반 지침과 함께 CLI 지침이 함께 제공되기 때문입니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-008 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `이 Space를 먼저 만드는 이유는 GitHub App에 웹훅 URL이 필요하고 그 URL이 Space에서 나오기 때문입니다. 이 Space는 당신의 고유 네임스페이스 아래에 있거나 쓰기 권한이 있는 허깅페이스 org 아래에 있어야 합니다.`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-009 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `빌드가 완료되면 복제된 Space를 엽니다. 현재는 무시해도 되는 "Required Space secrets" 섹션이 보일 것입니다. 다음 단계에서 필요한 GitHub App 웹훅 URL이 랜딩 페이지에 표시되어야 하며, 아래와 같은 형태일 것입니다:`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-010 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `빌드가 완료되면 복제된 Space를 엽니다. 현재는 무시해도 되는 "Required Space secrets" 섹션이 보일 것입니다. 다음 단계에서 필요한 GitHub App 웹훅 URL이 랜딩 페이지에 표시되어야 하며, 아래와 같은 형태일 것입니다:`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-011 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `설정 양식에서 허깅페이스 Jobs에서 CI가 실행되도록 하는 GitHub 리포를 입력합니다:`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-012 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `그런 다음 GitHub App 생성을 위한 버튼을 클릭합니다. GitHub은 App의 이름을 선택하라고 묻습니다. 이름은 GitHub 계정이나 조직에서 사용 가능하면 무엇이든 상관없습니다. 제출하면 최종 화면에 hf CLI를 사용해 dispatcher Space에 App 자격 증명을 업로드하는 정확한 방법이 표시됩니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-013 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `이 시점에서 dispatcher Space가 구성되어 있어야 합니다. GitHub App 설정 흐름은 Space에 App 자격 증명, 웹훅 시크릿 및 허깅페이스 토큰을 업로드하는 명령을 생성합니다.`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-014 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `일반적인 GitHub Action처럼 로그를 확인할 수 있어야 합니다—예를 들어 이 Trackio PR #565에서.`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-015 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `CPU 결과도 고무적이었습니다. 올바른 이미지로 Linux 테스트 작업은 GitHub 호스팅 기준선보다 빨랐습니다. 이는 허깅페이스 Jobs가 특히 맞춤 이미지나 가속기가 필요한 머신 러닝 프로젝트에 실용적인 CI 백엔드가 될 수 있음을 시사합니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-016 accuracy / major

- Message: Translation may add a causal explanation that is not in the source.
- Target: `때문에`
- Suggested fix: Remove invented causal explanation unless the source explicitly states it.
- Reason: The style guide forbids adding technical explanations, reasons, examples, or conclusions.

### QL-017 fluency / minor

- Message: Link text appears untranslated.
- Source: `Trackio`
- Target: `Trackio`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-018 fluency / minor

- Message: Link text appears untranslated.
- Source: `Hugging Face Jobs`
- Target: `Hugging Face Jobs`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-019 fluency / minor

- Message: Link text appears untranslated.
- Source: ``huggingface/jobs-actions``
- Target: ``huggingface/jobs-actions``
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-020 fluency / minor

- Message: Link text appears untranslated.
- Source: ``huggingface/jobs-actions-dispatcher``
- Target: ``huggingface/jobs-actions-dispatcher``
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-021 fluency / minor

- Message: Link text appears untranslated.
- Source: `Hugging Face token`
- Target: `Hugging Face token`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-022 fluency / minor

- Message: Link text appears untranslated.
- Source: `Trackio PR #565`
- Target: `Trackio PR #565`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-023 fluency / minor

- Message: Link text appears untranslated.
- Source: `Docker image`
- Target: `Docker image`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-024 fluency / minor

- Message: Link text appears untranslated.
- Source: `supports mounting volumes`
- Target: `supports mounting volumes`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.
