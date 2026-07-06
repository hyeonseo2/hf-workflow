# Quality Report

- Status: reject
- Quality Score: 36.0
- Hard failures: 1
- Issues: 25
- Source available: True
- Source changed: False
- Source segments: 93
- Target segments: 93

## Scorecard

| Dimension | Score |
| --- | ---: |
| adequacy | 70.4 |
| technical_accuracy | 40.0 |
| completeness | 100.0 |
| terminology | 0.0 |
| fluency | 0.0 |
| publishing_integrity | 100.0 |
| style_locale | 60.0 |

## Metrics

- qe_metric: heuristic
- qe_average: 0.9544
- qe_min: 0.6462
- embedding_similarity_average: 0.7967
- embedding_similarity_min: 0.2567
- cache_hits: 186
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
- Rule hits: {'first_mention_bilingual': 1, 'information_addition': 1, 'link_text_translation': 11, 'list_consistency': 1, 'modal_strength': 4}

## Style Guide Findings

| Rule | Severity | Segment | Current | Suggested |
| --- | --- | --- | --- | --- |
| list_consistency | minor |  | sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, phrase, sentence, phrase, sentence, phrase, phrase, phrase, sentence, sentence | Use either sentence-style endings or phrase-style endings consistently within one list. |
| modal_strength | major | p_003 | 오랜 기간 동안 우리는 4~6주마다 릴리스를 발표했습니다. 이제는 단일 GitHub Actions 워크플로우에서 매주 릴리스를 발표합니다. 오픈 소스 도구와 오픈-가중치 모델을 사용해 이를 구축했고, 판단이 중요한 한 곳에 사람을 루프에 두었습니다. 이 글의 어떤 내용도 공급업체 계약, 비공개 모델, 또는 자신이 실행할 수 없는 인프라를 요구하지 않습니다. 이는 시작부터의 설계 목표였으며, 다른 유지 관리자가 가져다 사용하고 조정할 수 있는 워크플로우를 원했기 때문입니다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | l_009 | 릴리스 후보가 고정된 상태로 다운스트림 라이브러리의 테스트 브랜치를 열고 테스트합니다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_020 | 일부 단계는 순전히 기계적이며 자동화가 가능하다: 버전 증가, 커밋, 태깅, 푸시, 다운스트림 테스트 브랜치 열기, 포스트 릴리스 PR 열기. 이를 누가 생각할 필요가 없다. 항상 올바른 순서대로 일어나도록 해야 하며, 이것이 CI 워크플로우가 잘하는 일이다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | l_074 | **Breakages가 더 일찍 드러난다.** RC 후보 기간 동안 다운스트림 테스트 브랜치가 통합 이슈를 빠르게 포착합니다. | Preserve the strength of `can` using: 수 있습니다. |
| information_addition | major | p_092 | 때문에 | Remove invented causal explanation unless the source explicitly states it. |
| link_text_translation | minor |  | OpenCode | Translate link text while preserving the URL target. |
| link_text_translation | minor |  | GLM-5.2 | Translate link text while preserving the URL target. |
| link_text_translation | minor |  | HF Inference Providers | Translate link text while preserving the URL target. |
| link_text_translation | minor |  | Trusted Publishing | Translate link text while preserving the URL target. |

## Issues

### QL-001 technical / critical

- Message: inline code mismatch.
- Source: `curl | bash`
- Suggested fix: Preserve source inline code exactly.
- Reason: Hard gate exact-match validator failed: missing=['curl | bash']

### QL-002 technical / major

- Message: Python/API identifier mismatch.
- Source: `vX.Y.Z, vX.Y.Z`
- Target: `vX.Y`
- Suggested fix: Preserve source Python/API identifier exactly.
- Reason: Review gate exact-match validator failed: missing=['vX.Y.Z', 'vX.Y.Z']; extra=['vX.Y']

### QL-003 technical / major

- Message: number/unit token mismatch.
- Target: `0, 15, 2, 30, 40`
- Suggested fix: Preserve source number/unit token exactly.
- Reason: Review gate exact-match validator failed: extra=['0', '15', '2', '30', '40']

### QL-004 terminology / major

- Message: Required glossary term is not used.
- Source: `inference`
- Target: `추론`
- Suggested fix: Use `추론` for `inference`.
- Reason: Glossary policy required the Korean term.

### QL-005 terminology / major

- Message: Required glossary term is not used.
- Source: `dataset`
- Target: `데이터셋`
- Suggested fix: Use `데이터셋` for `dataset`.
- Reason: Glossary policy required the Korean term.

### QL-006 terminology / major

- Message: Product or library name was not preserved.
- Source: `Hugging Face`
- Suggested fix: Preserve `Hugging Face` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-007 terminology / minor

- Message: First-mention glossary policy was not satisfied.
- Source: `Hub`
- Target: `Hugging Face Hub`
- Suggested fix: Use `Hugging Face Hub` on first mention or preserve `Hub`.
- Reason: Glossary policy allows preservation or first-mention form.

### QL-008 style_locale / minor

- Message: List mixes sentence-style and phrase-style endings.
- Target: `sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, phrase, sentence, phrase, sentence, phrase, phrase, phrase, sentence, sentence`
- Suggested fix: Use either sentence-style endings or phrase-style endings consistently within one list.
- Reason: The style guide requires consistent list item endings.

### QL-009 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `오랜 기간 동안 우리는 4~6주마다 릴리스를 발표했습니다. 이제는 단일 GitHub Actions 워크플로우에서 매주 릴리스를 발표합니다. 오픈 소스 도구와 오픈-가중치 모델을 사용해 이를 구축했고, 판단이 중요한 한 곳에 사람을 루프에 두었습니다. 이 글의 어떤 내용도 공급업체 계약, 비공개 모델, 또는 자신이 실행할 수 없는 인프라를 요구하지 않습니다. 이는 시작부터의 설계 목표였으며, 다른 유지 관리자가 가져다 사용하고 조정할 수 있는 워크플로우를 원했기 때문입니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-010 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `릴리스 후보가 고정된 상태로 다운스트림 라이브러리의 테스트 브랜치를 열고 테스트합니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-011 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `일부 단계는 순전히 기계적이며 자동화가 가능하다: 버전 증가, 커밋, 태깅, 푸시, 다운스트림 테스트 브랜치 열기, 포스트 릴리스 PR 열기. 이를 누가 생각할 필요가 없다. 항상 올바른 순서대로 일어나도록 해야 하며, 이것이 CI 워크플로우가 잘하는 일이다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-012 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `**Breakages가 더 일찍 드러난다.** RC 후보 기간 동안 다운스트림 테스트 브랜치가 통합 이슈를 빠르게 포착합니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-013 accuracy / major

- Message: Translation may add a causal explanation that is not in the source.
- Target: `때문에`
- Suggested fix: Remove invented causal explanation unless the source explicitly states it.
- Reason: The style guide forbids adding technical explanations, reasons, examples, or conclusions.

### QL-014 fluency / minor

- Message: Link text appears untranslated.
- Source: `OpenCode`
- Target: `OpenCode`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-015 fluency / minor

- Message: Link text appears untranslated.
- Source: `GLM-5.2`
- Target: `GLM-5.2`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-016 fluency / minor

- Message: Link text appears untranslated.
- Source: `HF Inference Providers`
- Target: `HF Inference Providers`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-017 fluency / minor

- Message: Link text appears untranslated.
- Source: `Trusted Publishing`
- Target: `Trusted Publishing`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-018 fluency / minor

- Message: Link text appears untranslated.
- Source: `fork it`
- Target: `fork it`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-019 fluency / minor

- Message: Link text appears untranslated.
- Source: `here's a recent one`
- Target: `here's a recent one`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-020 fluency / minor

- Message: Link text appears untranslated.
- Source: `skills`
- Target: `skills`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-021 fluency / minor

- Message: Link text appears untranslated.
- Source: `Skills`
- Target: `Skills`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-022 fluency / minor

- Message: Link text appears untranslated.
- Source: `PEP 740`
- Target: `PEP 740`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-023 fluency / minor

- Message: Link text appears untranslated.
- Source: `scripts`
- Target: `scripts`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-024 fluency / minor

- Message: Link text appears untranslated.
- Source: `skill Markdown`
- Target: `skill Markdown`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-025 terminology / minor

- Message: First mention is missing the recommended bilingual term.
- Source: `checkpoint`
- Target: `체크포인트`
- Suggested fix: Use `체크포인트(checkpoint)` on first mention, then `체크포인트` afterward.
- Reason: The style guide recommends preserving searchability by adding English in parentheses on first mention.
