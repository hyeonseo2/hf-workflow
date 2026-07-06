# Quality Report

- Status: reject
- Quality Score: 58.0
- Hard failures: 0
- Issues: 24
- Source available: True
- Source changed: False
- Source segments: 41
- Target segments: 41

## Scorecard

| Dimension | Score |
| --- | ---: |
| adequacy | 85.4 |
| technical_accuracy | 60.0 |
| completeness | 100.0 |
| terminology | 60.0 |
| fluency | 0.0 |
| publishing_integrity | 80.0 |
| style_locale | 60.0 |

## Metrics

- qe_metric: heuristic
- qe_average: 0.9539
- qe_min: 0.6163
- embedding_similarity_average: 0.8202
- embedding_similarity_min: 0.2807
- cache_hits: 0
- cache_misses: 82

## Style Guide

- Enabled: True
- Guide: `/Users/harheem/hf-workflow/skills/quality/style/hf-blog-ko-translation-guide.md`
- Policy: `/Users/harheem/hf-workflow/skills/quality/configs/style_policy.yml`
- Style score: 60.0
- Rule hits: {'alt_text_caption': 3, 'link_text_translation': 13, 'modal_strength': 2, 'translationese': 1}

## Style Guide Findings

| Rule | Severity | Segment | Current | Suggested |
| --- | --- | --- | --- | --- |
| translationese | minor |  | 를 가지 | Rewrite the sentence in natural Korean. |
| modal_strength | major | p_016 | 이것은 평가를 보고하거나 읽는 모든 사람에게 새로운 기능이며, 기존 EEE 기여자들만의 것이 아닙니다. 자사 모델을 보고하는 평가자와 타인의 모델을 보고하는 제3자 평가자 모두 커뮤니티 Evals와 EEE에 제출할 수 있으며, 허브를 둘러보는 누구나 전체 기록으로 연결되는 결과를 얻습니다. 조직의 공식 허깅페이스 계정을 통해 데이터를 제출하면, EvalEval에 verified 확인 표시가 표시되어 독자들에게 숫자가 출처에서 직접 왔음을 알리는 신호가 됩니다. 이 글의 나머지 부분은 허깅페이스 커뮤니티 Evals가 무엇인지와 변환기가 하는 일에 대해 설명합니다. | Preserve the strength of `can` using: 수 있습니다. |
| modal_strength | major | p_035 | **아무 것도 당신의 서명 없이는 푸시되지 않습니다.** 도구는 로컬 YAML 프리뷰와 검토 파일을 작성하여 확인할 수 있게 하고, 준비된 것과 주의가 필요한 것을 보여주는 보고서를 출력합니다. 커밋 메시지를 입력하고 OPEN PRS를 입력한 후에만 PR을 엽니다. 컬렉션에 대해 캐시된 결과를 재실행하면 --force를 넘겨주지 않는 한 재사용됩니다. | Preserve the strength of `can` using: 수 있습니다. |
| alt_text_caption | minor |  | Verified Evaluators on Eval Cards | Translate image alt text while preserving the image path. |
| alt_text_caption | minor |  | EvalEval as source on SmolLM2 Model Page | Translate image alt text while preserving the image path. |
| alt_text_caption | minor |  | TUI of the Converter | Translate image alt text while preserving the image path. |
| link_text_translation | minor |  | here | Translate link text while preserving the URL target. |
| link_text_translation | minor |  | EvalEval Coalition | Translate link text while preserving the URL target. |
| link_text_translation | minor |  | Community Evals | Translate link text while preserving the URL target. |
| link_text_translation | minor |  | MMLU | Translate link text while preserving the URL target. |

## Issues

### QL-001 formatting / major

- Message: Front matter key `authors` changed or is missing.
- Source: `user: irenesolaiman
user: julien-c`
- Target: `user: deepmage121`
- Suggested fix: Preserve front matter `authors` exactly.

### QL-002 technical / major

- Message: model or dataset id mismatch.
- Source: `_ever/hf-community-evals`
- Target: `_ever/hf-community-`
- Suggested fix: Preserve source model or dataset id exactly.
- Reason: Review gate exact-match validator failed: missing=['_ever/hf-community-evals']; extra=['_ever/hf-community-']

### QL-003 technical / major

- Message: number/unit token mismatch.
- Target: `1, 2, 2, 3, 3`
- Suggested fix: Preserve source number/unit token exactly.
- Reason: Review gate exact-match validator failed: extra=['1', '2', '2', '3', '3']

### QL-004 terminology / major

- Message: Product or library name was not preserved.
- Source: `Hugging Face`
- Suggested fix: Preserve `Hugging Face` exactly.
- Reason: Glossary policy requires preserving this product/library/model term.

### QL-005 terminology / minor

- Message: First-mention glossary policy was not satisfied.
- Source: `Hub`
- Target: `Hugging Face Hub`
- Suggested fix: Use `Hugging Face Hub` on first mention or preserve `Hub`.
- Reason: Glossary policy allows preservation or first-mention form.

### QL-006 fluency / minor

- Message: Translationese expression found.
- Target: `를 가지`
- Suggested fix: Rewrite the sentence in natural Korean.
- Reason: The style guide lists this expression as translationese to avoid.

### QL-007 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `이것은 평가를 보고하거나 읽는 모든 사람에게 새로운 기능이며, 기존 EEE 기여자들만의 것이 아닙니다. 자사 모델을 보고하는 평가자와 타인의 모델을 보고하는 제3자 평가자 모두 커뮤니티 Evals와 EEE에 제출할 수 있으며, 허브를 둘러보는 누구나 전체 기록으로 연결되는 결과를 얻습니다. 조직의 공식 허깅페이스 계정을 통해 데이터를 제출하면, EvalEval에 verified 확인 표시가 표시되어 독자들에게 숫자가 출처에서 직접 왔음을 알리는 신호가 됩니다. 이 글의 나머지 부분은 허깅페이스 커뮤니티 Evals가 무엇인지와 변환기가 하는 일에 대해 설명합니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-008 accuracy / major

- Message: Modal or certainty strength may have changed.
- Source: `can`
- Target: `**아무 것도 당신의 서명 없이는 푸시되지 않습니다.** 도구는 로컬 YAML 프리뷰와 검토 파일을 작성하여 확인할 수 있게 하고, 준비된 것과 주의가 필요한 것을 보여주는 보고서를 출력합니다. 커밋 메시지를 입력하고 OPEN PRS를 입력한 후에만 PR을 엽니다. 컬렉션에 대해 캐시된 결과를 재실행하면 --force를 넘겨주지 않는 한 재사용됩니다.`
- Suggested fix: Preserve the strength of `can` using: 수 있습니다.
- Reason: The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.

### QL-009 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `Verified Evaluators on Eval Cards`
- Target: `Verified Evaluators on Eval Cards`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-010 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `EvalEval as source on SmolLM2 Model Page`
- Target: `EvalEval as source on SmolLM2 Model Page`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-011 fluency / minor

- Message: Image alt text appears untranslated.
- Source: `TUI of the Converter`
- Target: `TUI of the Converter`
- Suggested fix: Translate image alt text while preserving the image path.
- Reason: The style guide requires translating image alt text and captions.

### QL-012 fluency / minor

- Message: Link text appears untranslated.
- Source: `here`
- Target: `here`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-013 fluency / minor

- Message: Link text appears untranslated.
- Source: `EvalEval Coalition`
- Target: `EvalEval Coalition`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-014 fluency / minor

- Message: Link text appears untranslated.
- Source: `Community Evals`
- Target: `Community Evals`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-015 fluency / minor

- Message: Link text appears untranslated.
- Source: `MMLU`
- Target: `MMLU`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-016 fluency / minor

- Message: Link text appears untranslated.
- Source: `evaluation settings that we found are commonly unreported`
- Target: `evaluation settings that we found are commonly unreported`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-017 fluency / minor

- Message: Link text appears untranslated.
- Source: `GitHub repository`
- Target: `GitHub repository`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-018 fluency / minor

- Message: Link text appears untranslated.
- Source: `the EEE datastore`
- Target: `the EEE datastore`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-019 fluency / minor

- Message: Link text appears untranslated.
- Source: `verified`
- Target: `verified`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-020 fluency / minor

- Message: Link text appears untranslated.
- Source: `official benchmarks`
- Target: `official benchmarks`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-021 fluency / minor

- Message: Link text appears untranslated.
- Source: `Humanity's Last Exam`
- Target: `Humanity's Last Exam`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-022 fluency / minor

- Message: Link text appears untranslated.
- Source: `Eval Cards`
- Target: `Eval Cards`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-023 fluency / minor

- Message: Link text appears untranslated.
- Source: `community eval converter tool`
- Target: `community eval converter tool`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.

### QL-024 fluency / minor

- Message: Link text appears untranslated.
- Source: `evalevalai.com/every\_eval\_ever/hf-community-evals`
- Target: `evalevalai.com/every\_eval\_ever/hf-community-evals`
- Suggested fix: Translate link text while preserving the URL target.
- Reason: The style guide requires translating link text while preserving the link target.
