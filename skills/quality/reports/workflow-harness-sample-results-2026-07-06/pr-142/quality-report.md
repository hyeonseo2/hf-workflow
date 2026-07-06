# Quality Report

- Status: reject
- Quality Score: 39.0
- Hard failures: 2
- Issues: 17
- Source available: True
- Source changed: False
- Source segments: 30
- Target segments: 30

## Scorecard

| Dimension | Score |
| --- | ---: |
| adequacy | 74.3 |
| technical_accuracy | 80.0 |
| completeness | 100.0 |
| terminology | 60.0 |
| fluency | 0.0 |
| publishing_integrity | 40.0 |
| style_locale | 60.0 |

## Metrics

- qe_metric: heuristic
- qe_average: 0.9427
- qe_min: 0.5859
- embedding_similarity_average: 0.8025
- embedding_similarity_min: 0.2747
- cache_hits: 60
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
- Rule hits: {'alt_text_caption': 2, 'link_text_translation': 4, 'modal_strength': 4, 'translationese': 1}

## Style Guide Findings

| Rule | Severity | Segment | Current | Suggested |
| --- | --- | --- | --- | --- |
| translationese | minor |  | 에 의해 | Rewrite the sentence in natural Korean. |
| modal_strength | major | p_003 | OpenEnv는 터미널, 브라우저 또는 에이전트가 상호작용할 수 있는 그 밖의 실행 환경처럼 에이전트형 실행 환경을 만드는 도구입니다. 그리고 오늘, OpenEnv가 더 개방적으로 바뀌어 에이전트를 학습하는 미래를 오픈 소스로 만들게 되었음을 발표하게 되어 기쁩니다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_010 | 프런티어 연구소들은 모델과 하네스가 대체로 손발이 맞게 함께 작동하도록 학습합니다. 모델은 하네스를 사용하도록 학습되며 그 특성에 맞게 최적화됩니다. 모델은 이 하네스들 너머로 다소 일반화될 수 있지만, 학습의 효율성을 능가하는 것은 아무것도 없습니다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_016 | 최근 릴리스에서 OpenEnv는 **RL 환경 간 상호 운용성 계층**이 되었습니다. 그것의 역할은 환경이 게시되고 배포되며 에이전트에 의해 소비되는 방식을 표준화하는 것입니다. 보상 정의나 학습 루프가 어떻게 작동하는지를 지시하지는 않습니다. 보상 정의, 채점 기준, 트레이너별 로직은 이에 특화된 라이브러리에 속합니다. OpenEnv는 모두가 연결할 수 있는 공통 소켓입니다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_019 | 익숙한 프로토콜과 표준 패키징. 환경은 HTTP와 WebSocket 같은 표준 프로토콜로 서비스되며 Docker로 패키징됩니다. MCP는 1급 시민으로서, OpenEnv 환경은 MCP 서버와 즉시 호환되며 동일한 환경이 시뮬레이션(훈련/평가)과 생산 모드에서 일관되게 동작합니다. | Preserve the strength of `can` using: 수 있습니다. |
| alt_text_caption | minor |  | Thumbnail for the blog post | Translate image alt text while preserving the image path. |
| alt_text_caption | minor |  | the open source reinforcement learning ecosystem | Translate image alt text while preserving the image path. |
| link_text_translation | minor |  | github.com/huggingface/OpenEnv | Translate link text while preserving the URL target. |
| link_text_translation | minor |  |  | Translate link text while preserving the URL target. |
| link_text_translation | minor |  |  | Translate link text while preserving the URL target. |

## Issues

### QL-001 formatting / major

- Message: Front matter key `authors` changed or is missing.
- Source: `user: burtenshaw
user: spisakjo
user: lysandre
user: darktex
user: willcb
user: qjoy
user: pawalt
user: cwing-nv
user: danielhanchen
user: andrewzhou
user: thegovind
user: shimmyshimmer
user: Hamid-Nazeri
user: Sanyam
user: zkwentz
user: emre0
user: lewtun
user: sergiopaniego
user: banghua
user: unseenmars`
- Target: `user: burtenshaw
user: spisakjo
user: lysandre
user: darktex
user: willcb
user: charlesfrye
user: cwing-nv
user: danielhanchen
user: andrewzhou
user: shimmyshimmer
user: Hamid-Nazeri
user: Sanyam
user: zkwentz
user: emre0
user: lewtun
user: sergiopaniego`
- Suggested fix: Preserve front matter `authors` exactly.

### QL-002 formatting / critical

- Message: Front matter key `thumbnail` changed or is missing.
- Source: `/blog/assets/openenv/thumbnail3.png`
- Target: `/blog/assets/openenv/thumbnail_expansion.png`
- Suggested fix: Preserve front matter `thumbnail` exactly.

### QL-003 formatting / critical

- Message: link target mismatch.
- Source: `https://github.com/huggingface/OpenEnv/pull/794, https://github.com/huggingface/OpenEnv/pull/795`
- Target: `https://github.com/huggingface/OpenEnv/pull/727, https://github.com/huggingface/OpenEnv/pull/731`
- Suggested fix: Preserve source link target exactly.
- Reason: Hard gate exact-match validator failed: missing=['https://github.com/huggingface/OpenEnv/pull/794', 'https://github.com/huggingface/OpenEnv/pull/795']; extra=['https://github.com/huggingface/OpenEnv/pull/727', 'https://github.com/huggingface/OpenEnv/pull/731']

### QL-004 technical / major

- Message: number/unit token mismatch.
- Target: `1`
- Suggested fix: Preserve source number/unit token exactly.
- Reason: Review gate exact-match validator failed: extra=['1']

### QL-005 terminology / minor

- Message: First-mention glossary policy was not satisfied.
- Source: `Hub`
- Target: `Hugging Face Hub`
- Suggested fix: Use `Hugging Face Hub` on first mention or preserve `Hub`.
- Reason: Glossary policy allows preservation or first-mention form.

### QL-006 terminology / major

- Message: Product or library name was not preserved.
- Source: `Datasets`
- Suggested fix: Preserve `Datasets` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-007 fluency / minor

- Message: Translationese expression found.
- Target: `에 의해`
- Suggested fix: Rewrite the sentence in natural Korean.
- Reason: The style guide lists this expression as translationese to avoid.

### QL-008 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `OpenEnv는 터미널, 브라우저 또는 에이전트가 상호작용할 수 있는 그 밖의 실행 환경처럼 에이전트형 실행 환경을 만드는 도구입니다. 그리고 오늘, OpenEnv가 더 개방적으로 바뀌어 에이전트를 학습하는 미래를 오픈 소스로 만들게 되었음을 발표하게 되어 기쁩니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-009 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `프런티어 연구소들은 모델과 하네스가 대체로 손발이 맞게 함께 작동하도록 학습합니다. 모델은 하네스를 사용하도록 학습되며 그 특성에 맞게 최적화됩니다. 모델은 이 하네스들 너머로 다소 일반화될 수 있지만, 학습의 효율성을 능가하는 것은 아무것도 없습니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-010 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `최근 릴리스에서 OpenEnv는 **RL 환경 간 상호 운용성 계층**이 되었습니다. 그것의 역할은 환경이 게시되고 배포되며 에이전트에 의해 소비되는 방식을 표준화하는 것입니다. 보상 정의나 학습 루프가 어떻게 작동하는지를 지시하지는 않습니다. 보상 정의, 채점 기준, 트레이너별 로직은 이에 특화된 라이브러리에 속합니다. OpenEnv는 모두가 연결할 수 있는 공통 소켓입니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-011 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `익숙한 프로토콜과 표준 패키징. 환경은 HTTP와 WebSocket 같은 표준 프로토콜로 서비스되며 Docker로 패키징됩니다. MCP는 1급 시민으로서, OpenEnv 환경은 MCP 서버와 즉시 호환되며 동일한 환경이 시뮬레이션(훈련/평가)과 생산 모드에서 일관되게 동작합니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-012 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `Thumbnail for the blog post`
- Target: `Thumbnail for the blog post`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-013 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `the open source reinforcement learning ecosystem`
- Target: `the open source reinforcement learning ecosystem`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-014 fluency / minor

- Message: Link text appears untranslated.
- Source: `github.com/huggingface/OpenEnv`
- Target: `github.com/huggingface/OpenEnv`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-015 fluency / minor

- Message: Link text appears untranslated.
- Source: `RFC 006`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-016 fluency / minor

- Message: Link text appears untranslated.
- Source: `RFC 007`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-017 fluency / minor

- Message: Link text appears untranslated.
- Source: `RFC 008`
- Target: `RFC 008`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.
