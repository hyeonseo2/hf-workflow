# Quality Report

- Status: review_required
- Quality Score: 66.0
- Hard failures: 0
- Issues: 16
- Source available: True
- Source changed: False
- Source segments: 48
- Target segments: 48

## Scorecard

| Dimension | Score |
| --- | ---: |
| adequacy | 64.3 |
| technical_accuracy | 80.0 |
| completeness | 100.0 |
| terminology | 60.0 |
| fluency | 10.0 |
| publishing_integrity | 100.0 |
| style_locale | 60.0 |

## Metrics

- qe_metric: heuristic
- qe_average: 0.943
- qe_min: 0.5949
- embedding_similarity_average: 0.8123
- embedding_similarity_min: 0.3051
- cache_hits: 0
- cache_misses: 96

## Style Guide

- Enabled: True
- Guide: `/Users/harheem/hf-workflow/skills/quality/style/hf-blog-ko-translation-guide.md`
- Policy: `/Users/harheem/hf-workflow/skills/quality/configs/style_policy.yml`
- Style score: 60.0
- Rule hits: {'information_addition': 1, 'intro_closing_style': 1, 'link_text_translation': 6, 'modal_strength': 5}

## Style Guide Findings

| Rule | Severity | Segment | Current | Suggested |
| --- | --- | --- | --- | --- |
| intro_closing_style | minor | p_048 | 이 포스트 | Rewrite the intro or closing in natural Korean blog style. |
| modal_strength | major | p_016 | 일반적인 OpenAI 스타일의 JSON을 반환하며, choices[0].message.content에 "Hello! How can I assist you today? 😊"이 들어 있습니다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_018 | 시작하기 전 빠른 상태 점검: curl https://<job_id>--8000.hf.jobs/v1/models -H "Authorization: Bearer $(hf auth token)"에 모델이 나열되어 있어야 합니다. | Preserve the strength of `should` using: 좋습니다, 해야 합니다. |
| modal_strength | major | b_020 | **🔐 엔드포인트는 게이트되어 공개되지 않습니다.** 모든 요청은 작업의 네임스페이스에 대한 읽기 권한이 있는 허깅페이스 토큰이 필요합니다. 일반 브라우저 방문은 거부됩니다. 사실상 작업 프록시는 API 게이트 역할을 하며, 접근은 귀하(및 귀하의 조직)에게 한정됩니다. 개인 사용에는 괜찮지만 URL을 다룰 때는 공개로 여길 것을 기대하지 말고 토큰을 신뢰할 수 없는 곳에 붙여넣지 마십시오. 더 세밀하거나 공개 접근이 필요하면 대신 적절한 게이트웨이를 앞에 두십시오. 아래의 HF Jobs or Inference Endpoints?를 참조하십시오. | Preserve the strength of `must` using: 반드시, 해야 합니다. |
| modal_strength | major | p_023 | 설정한 --timeout은 안전망이며(자동 중지 기능이 있습니다). 그러나 명시적으로 취소하는 것이 더 저렴합니다. a10g-large은 시간당 $1.50에 실행되며 전체 가격표는 hf jobs hardware에서 확인하고 모델에 맞는 가장 작은 플래버를 선택하세요. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_046 | 좀 더 프로덕션에 가까운 것을 원하신다면 **Inference Endpoints**를 선택하세요. 이들은 장기 실행되는 서비스에 필요한 운영상의 편의 기능을 제공합니다: 더 세밀한 접근 제어(엔드포인트가 공개, 보호, 또는 비공개일 수 있음)와 제로 스케일링으로 비활성 상태에서도 과금되지 않습니다. 지속 가능한 엔드포인트를 구축하려면 이것이 필요한 도구입니다. | Preserve the strength of `can` using: 수 있습니다. |
| information_addition | major | p_038 | 따라서 | Remove invented causal explanation unless the source explicitly states it. |
| link_text_translation | minor |  | Inference Endpoints | Translate link text while preserving the URL target. |
| link_text_translation | minor |  | HF Jobs or Inference Endpoints? | Translate link text while preserving the URL target. |
| link_text_translation | minor |  | Serve Models on Jobs guide | Translate link text while preserving the URL target. |

## Issues

### QL-001 technical / major

- Message: Python/API identifier mismatch.
- Source: `llama.cpp`
- Suggested fix: Preserve source Python/API identifier exactly.
- Reason: Review gate exact-match validator failed: missing=['llama.cpp']

### QL-002 terminology / major

- Message: Product or library name was not preserved.
- Source: `Hugging Face`
- Suggested fix: Preserve `Hugging Face` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-003 terminology / major

- Message: Product or library name was not preserved.
- Source: `Gradio`
- Suggested fix: Preserve `Gradio` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-004 style_locale / minor

- Message: Intro or closing phrasing sounds mechanically translated.
- Target: `이 포스트`
- Suggested fix: Rewrite the intro or closing in natural Korean blog style.
- Reason: The style guide recommends natural Korean openings and closings over mechanical source phrasing.

### QL-005 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `일반적인 OpenAI 스타일의 JSON을 반환하며, choices[0].message.content에 "Hello! How can I assist you today? 😊"이 들어 있습니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-006 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `should`
- Target: `시작하기 전 빠른 상태 점검: curl https://<job_id>--8000.hf.jobs/v1/models -H "Authorization: Bearer $(hf auth token)"에 모델이 나열되어 있어야 합니다.`
- Suggested fix: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-007 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `must`
- Target: `**🔐 엔드포인트는 게이트되어 공개되지 않습니다.** 모든 요청은 작업의 네임스페이스에 대한 읽기 권한이 있는 허깅페이스 토큰이 필요합니다. 일반 브라우저 방문은 거부됩니다. 사실상 작업 프록시는 API 게이트 역할을 하며, 접근은 귀하(및 귀하의 조직)에게 한정됩니다. 개인 사용에는 괜찮지만 URL을 다룰 때는 공개로 여길 것을 기대하지 말고 토큰을 신뢰할 수 없는 곳에 붙여넣지 마십시오. 더 세밀하거나 공개 접근이 필요하면 대신 적절한 게이트웨이를 앞에 두십시오. 아래의 HF Jobs or Inference Endpoints?를 참조하십시오.`
- Suggested fix: Preserve the strength of `must` using: 반드시, 해야 합니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-008 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `설정한 --timeout은 안전망이며(자동 중지 기능이 있습니다). 그러나 명시적으로 취소하는 것이 더 저렴합니다. a10g-large은 시간당 $1.50에 실행되며 전체 가격표는 hf jobs hardware에서 확인하고 모델에 맞는 가장 작은 플래버를 선택하세요.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-009 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `좀 더 프로덕션에 가까운 것을 원하신다면 **Inference Endpoints**를 선택하세요. 이들은 장기 실행되는 서비스에 필요한 운영상의 편의 기능을 제공합니다: 더 세밀한 접근 제어(엔드포인트가 공개, 보호, 또는 비공개일 수 있음)와 제로 스케일링으로 비활성 상태에서도 과금되지 않습니다. 지속 가능한 엔드포인트를 구축하려면 이것이 필요한 도구입니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-010 accuracy / major

- Message: Translation may add a causal explanation that is not in the source.
- Target: `따라서`
- Suggested fix: Remove invented causal explanation unless the source explicitly states it.
- Reason: The style guide forbids adding technical explanations, reasons, examples, or conclusions.

### QL-011 fluency / minor

- Message: Link text appears untranslated.
- Source: `Inference Endpoints`
- Target: `Inference Endpoints`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-012 fluency / minor

- Message: Link text appears untranslated.
- Source: `HF Jobs or Inference Endpoints?`
- Target: `HF Jobs or Inference Endpoints?`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-013 fluency / minor

- Message: Link text appears untranslated.
- Source: `Serve Models on Jobs guide`
- Target: `Serve Models on Jobs guide`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-014 fluency / minor

- Message: Link text appears untranslated.
- Source: `Gradio`
- Target: `Gradio`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-015 fluency / minor

- Message: Link text appears untranslated.
- Source: `huggingface.co/settings/keys`
- Target: `huggingface.co/settings/keys`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-016 fluency / minor

- Message: Link text appears untranslated.
- Source: `Pi`
- Target: `Pi`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.
