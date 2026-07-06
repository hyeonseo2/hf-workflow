# Quality Report

- Status: reject
- Quality Score: 64.0
- Hard failures: 1
- Issues: 14
- Source available: True
- Source changed: False
- Source segments: 38
- Target segments: 38

## Scorecard

| Dimension | Score |
| --- | ---: |
| adequacy | 71.2 |
| technical_accuracy | 100.0 |
| completeness | 100.0 |
| terminology | 60.0 |
| fluency | 10.0 |
| publishing_integrity | 80.0 |
| style_locale | 60.0 |

## Metrics

- qe_metric: heuristic
- qe_average: 0.9123
- qe_min: 0.6023
- embedding_similarity_average: 0.8277
- embedding_similarity_min: 0.5479
- cache_hits: 0
- cache_misses: 76

## Style Guide

- Enabled: True
- Guide: `/Users/harheem/hf-workflow/skills/quality/style/hf-blog-ko-translation-guide.md`
- Policy: `/Users/harheem/hf-workflow/skills/quality/configs/style_policy.yml`
- Style score: 60.0
- Rule hits: {'link_text_translation': 5, 'list_consistency': 1, 'modal_strength': 4, 'translationese': 1}

## Style Guide Findings

| Rule | Severity | Segment | Current | Suggested |
| --- | --- | --- | --- | --- |
| translationese | minor |  | 에 의해 | Rewrite the sentence in natural Korean. |
| list_consistency | minor |  | phrase, sentence, sentence, phrase, phrase, phrase, phrase, phrase, phrase, phrase | Use either sentence-style endings or phrase-style endings consistently within one list. |
| modal_strength | major | p_004 | 이번 글에서는 사양과 허깅페이스가 이를 어떻게 구현했는지, 그리고 ARD에서 시작해 구축하는 방법에 대해 살펴보겠습니다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_019 | 스킬 타입은 추가 변환을 수반합니다. 많은 Spaces가 에이전트가 그들과 상호 작용하는 방법을 설명하는 agents.md 파일을 제공합니다. Discover가 그 파일을 읽고 스킬 소비자가 기대하는 프런트매터: name, description, 그리고 Space ID, Hub URL, 앱 URL, 그리고 원래 agents.md URL를 포함하는 소스 메타데이터로 래핑합니다. 그 결과는 일반 스킬 흐름을 통해 설치하거나 로드할 수 있는 스킬이 됩니다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_019 | 스킬 타입은 추가 변환을 수반합니다. 많은 Spaces가 에이전트가 그들과 상호 작용하는 방법을 설명하는 agents.md 파일을 제공합니다. Discover가 그 파일을 읽고 스킬 소비자가 기대하는 프런트매터: name, description, 그리고 Space ID, Hub URL, 앱 URL, 그리고 원래 agents.md URL를 포함하는 소스 메타데이터로 래핑합니다. 그 결과는 일반 스킬 흐름을 통해 설치하거나 로드할 수 있는 스킬이 됩니다. | Preserve the strength of `should` using: 좋습니다, 해야 합니다. |
| modal_strength | major | p_024 | REST API 또는 MCP 서버를 사용하여 카탈로그를 직접 검색할 수도 있습니다. | Preserve the strength of `can` using: 수 있습니다. |
| link_text_translation | minor |  | https://github.com/huggingface/hf-discover | Translate link text while preserving the URL target. |
| link_text_translation | minor |  | https://github.com/huggingface/huggingface\_hub | Translate link text while preserving the URL target. |
| link_text_translation | minor |  | https://agenticresourcediscovery.org/ | Translate link text while preserving the URL target. |
| link_text_translation | minor |  | https://huggingface.co/docs/hub/agents-skills | Translate link text while preserving the URL target. |

## Issues

### QL-001 formatting / critical

- Message: Front matter key `thumbnail` changed or is missing.
- Source: `/blog/assets/agentic-resource-discovery-launch/thumbnail_.png`
- Target: `/blog/assets/agentic-resource-discovery-launch/thumbnail.png`
- Suggested fix: Preserve front matter `thumbnail` exactly.

### QL-002 terminology / minor

- Message: Preferred glossary term is not used.
- Source: `serving`
- Target: `서빙`
- Suggested fix: Prefer `서빙` for `serving`.
- Reason: Glossary policy marked this Korean term as preferred.

### QL-003 terminology / major

- Message: Product or library name was not preserved.
- Source: `Hugging Face Hub`
- Suggested fix: Preserve `Hugging Face Hub` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-004 fluency / minor

- Message: Translationese expression found.
- Target: `에 의해`
- Suggested fix: Rewrite the sentence in natural Korean.
- Reason: The style guide lists this expression as translationese to avoid.

### QL-005 style_locale / minor

- Message: List mixes sentence-style and phrase-style endings.
- Target: `phrase, sentence, sentence, phrase, phrase, phrase, phrase, phrase, phrase, phrase`
- Suggested fix: Use either sentence-style endings or phrase-style endings consistently within one list.
- Reason: The style guide requires consistent list item endings.

### QL-006 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `이번 글에서는 사양과 허깅페이스가 이를 어떻게 구현했는지, 그리고 ARD에서 시작해 구축하는 방법에 대해 살펴보겠습니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-007 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `스킬 타입은 추가 변환을 수반합니다. 많은 Spaces가 에이전트가 그들과 상호 작용하는 방법을 설명하는 agents.md 파일을 제공합니다. Discover가 그 파일을 읽고 스킬 소비자가 기대하는 프런트매터: name, description, 그리고 Space ID, Hub URL, 앱 URL, 그리고 원래 agents.md URL를 포함하는 소스 메타데이터로 래핑합니다. 그 결과는 일반 스킬 흐름을 통해 설치하거나 로드할 수 있는 스킬이 됩니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-008 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `스킬 타입은 추가 변환을 수반합니다. 많은 Spaces가 에이전트가 그들과 상호 작용하는 방법을 설명하는 agents.md 파일을 제공합니다. Discover가 그 파일을 읽고 스킬 소비자가 기대하는 프런트매터: name, description, 그리고 Space ID, Hub URL, 앱 URL, 그리고 원래 agents.md URL를 포함하는 소스 메타데이터로 래핑합니다. 그 결과는 일반 스킬 흐름을 통해 설치하거나 로드할 수 있는 스킬이 됩니다.`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-009 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `REST API 또는 MCP 서버를 사용하여 카탈로그를 직접 검색할 수도 있습니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-010 fluency / minor

- Message: Link text appears untranslated.
- Source: `https://github.com/huggingface/hf-discover`
- Target: `https://github.com/huggingface/hf-discover`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-011 fluency / minor

- Message: Link text appears untranslated.
- Source: `https://github.com/huggingface/huggingface\_hub`
- Target: `https://github.com/huggingface/huggingface\_hub`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-012 fluency / minor

- Message: Link text appears untranslated.
- Source: `https://agenticresourcediscovery.org/`
- Target: `https://agenticresourcediscovery.org/`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-013 fluency / minor

- Message: Link text appears untranslated.
- Source: `https://huggingface.co/docs/hub/agents-skills`
- Target: `https://huggingface.co/docs/hub/agents-skills`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-014 fluency / minor

- Message: Link text appears untranslated.
- Source: `https://huggingface.co/spaces`
- Target: `https://huggingface.co/spaces`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.
