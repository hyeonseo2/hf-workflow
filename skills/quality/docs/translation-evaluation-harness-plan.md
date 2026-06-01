# Hugging Face Blog Korean Translation Evaluation Harness Plan

## 목적

이 문서는 `translation-evaluation-harness-prd.md`를 구현 가능한 실행 계획으로 변환한 것이다. 목표는 단순히 번역문에 점수를 매기는 것이 아니라, Hugging Face 공식 블로그 한국어 로컬라이징 결과가 **게시 가능한 상태인지 판정하고, 수정해야 할 오류를 재현 가능하게 찾아내는 품질 게이트**를 만드는 것이다.

핵심 원칙은 다음과 같다.

- 품질 점수와 게시 가능 여부를 분리한다.
- 코드, 모델명, 링크, 수식, 숫자, front matter 손상은 점수와 무관하게 차단한다.
- 자연스러운 한국어보다 기술적 안전성을 우선한다.
- 자동 평가는 최종 판단자가 아니라 리뷰 우선순위 지정 장치로 사용한다.
- 하네스 결과는 Markdown 리포트와 JSON artifact로 모두 남긴다.

## 성공 기준

하네스가 성공했다고 볼 수 있는 조건은 다음이다.

- Markdown, 코드, 링크, 이미지, 표, LaTeX, front matter 손상으로 인한 게시 실패를 PR 단계에서 차단한다.
- 모델명, dataset id, API명, benchmark 수치, 라이선스/제한사항 오역을 `critical` 또는 hard failure로 잡는다.
- 승인된 좋은 번역 golden set의 false reject 비율을 10% 이하로 유지한다.
- 의도적으로 오류를 심은 challenge set의 critical 오류 탐지율을 90% 이상으로 유지한다.
- PR 리포트가 사람이 바로 수정할 수 있는 segment, span, severity, suggested fix를 포함한다.
- 같은 입력과 같은 설정에서는 같은 gate 결과와 유사한 점수 분포가 재현된다.

## 범위

### 포함

- `translation-flow` manifest 기반 입력 처리
- 원문 Markdown 또는 HTML snapshot과 번역 Markdown 비교
- Markdown AST 기반 구조 검증
- 보호 토큰 추출, 마스킹, exact-match 검증
- 숫자, 단위, 날짜, benchmark 수치 비교
- glossary 및 제품/라이브러리/모델명 정책 검증
- COMETKiwi 또는 유사 reference-free QE 점수
- LLM 기반 MQM span annotation
- hard gate, score, reviewer routing 산출
- Markdown/JSON 리포트 생성
- golden set, challenge set, 회귀 테스트

### 제외

- 새 번역 생성
- 번역문 자동 수정 반영
- SEO 제목/메타 설명 최적화
- 원문 자체의 기술적 사실 검증
- 출판 저장소 전체 빌드 검증

## 품질 모델

PRD의 6개 품질 축을 하네스의 1차 scorecard로 사용한다.

| 품질 축 | 내부 이름 | 주요 검사 | 게이트 성격 |
| --- | --- | --- | --- |
| 의미 충실도 | `adequacy` | 주장, 조건, 한계, 인과관계 보존 | critical 가능 |
| 기술 정확성 | `technical_accuracy` | 코드, API, 모델명, 수식, benchmark 수치 | hard gate 중심 |
| 완전성 | `completeness` | segment 누락, 중복, 임의 추가 | hard gate + score |
| 한국어 가독성 | `fluency` | 문법, 조사, 어순, 직역투 | score + review |
| 용어 일관성 | `terminology` | glossary, 이전 승인 번역, 제품명 정책 | score + review, 일부 hard gate |
| 게시 안전성 | `publishing_integrity` | Markdown, front matter, 링크, 이미지, 표, LaTeX | hard gate 중심 |

기존 plan의 `fidelity`, `format`, `localization` 개념은 위 scorecard로 흡수한다. 특히 `publishing_integrity`는 일반적인 번역 품질 점수와 별도이며, 손상되면 즉시 reject할 수 있다.

## 입력과 출력

### 입력

기본 입력은 현재 워크플로우의 manifest다.

```yaml
source:
  url: https://huggingface.co/blog/...
  title: ...
translation:
  file_path: _posts/...
  pr_url: ...
handoff:
  quality:
    checks:
      - fidelity
      - terminology
      - formatting
```

하네스 단계에서 추가로 해석하거나 생성할 입력은 다음이다.

```text
source_md: 원문 Markdown 또는 원문 HTML을 정규화한 Markdown
target_md: 한국어 번역 Markdown
glossary.tsv: 필수/권장/보존 용어집
protected_patterns.yml: 모델명, 코드, URL, 수식 등 보존 패턴
style_guide_ko.md: 한국어 기술 블로그 문체 가이드
translation_memory.jsonl: 승인된 기존 번역 segment
eval_config.yml: 점수 가중치, threshold, whitelist
source_snapshot.md: 실행 시점 원문 snapshot
```

### 출력

사람이 읽는 리포트:

```text
reports/pr-XXX/quality-report.md
```

자동화용 artifact:

```text
reports/pr-XXX/quality-report.json
reports/pr-XXX/source-snapshot.md
reports/pr-XXX/source-segments.jsonl
reports/pr-XXX/target-segments.jsonl
```

권장 JSON shape:

```json
{
  "status": "review_required",
  "quality_score": 86.5,
  "hard_failures": [],
  "dimension_scores": {
    "adequacy": 88,
    "technical_accuracy": 92,
    "completeness": 95,
    "terminology": 78,
    "fluency": 84,
    "publishing_integrity": 100
  },
  "mqm_errors": [
    {
      "segment_id": "p_014",
      "category": "terminology",
      "severity": "major",
      "source_span": "inference endpoint",
      "target_span": "추론 끝점",
      "suggested_fix": "Inference Endpoint 또는 추론 엔드포인트",
      "reason": "Hugging Face 제품/기술 용어로 오해 가능성이 큼"
    }
  ]
}
```

## 처리 파이프라인

1. Manifest 해석
   - `source.url`, `source.title`, `translation.file_path`, `translation.pr_url`을 읽는다.
   - 대상 번역 파일과 원문 snapshot 경로를 결정한다.

2. 원문 snapshot 생성
   - URL에서 원문을 fetch한다.
   - 가능하면 Hugging Face Blog 원본 Markdown을 우선 사용한다.
   - HTML만 있으면 Markdown/AST로 정규화한다.
   - source segment별 hash를 저장해 이후 원문 변경을 감지한다.

3. Markdown AST 파싱
   - source와 target을 모두 AST로 파싱한다.
   - heading, paragraph, list item, table cell, code fence, inline code, link, image, HTML block, LaTeX를 구분한다.
   - parse 실패는 hard failure다.

4. Segment 추출 및 정렬
   - 번역 대상 text node만 segment로 추출한다.
   - 각 segment에 `segment_id`, AST path, source hash, source text, target text를 부여한다.
   - heading/list/table cell도 segment로 다루되 code block은 기본적으로 번역 대상에서 제외한다.

5. 보호 토큰 마스킹
   - 코드, inline code, URL, image path, model id, dataset id, 파일 경로, API identifier, 숫자, 단위, LaTeX, HTML tag를 placeholder로 치환한다.
   - 번역 후 placeholder가 정확히 복원되었는지 검사한다.

6. Hard gate 실행
   - 게시 안전성과 기술 정확성 손상을 먼저 판정한다.
   - hard failure가 있으면 score 계산은 계속하되 최종 status는 `reject`다.

7. 자동 metric 평가
   - glossary compliance, language ID, length ratio, duplicate segment, embedding similarity를 계산한다.
   - COMETKiwi 또는 유사 QE metric으로 reference-free 품질 점수를 계산한다.
   - chrF/SacreBLEU는 승인 reference가 있는 회귀 테스트에서만 참고 지표로 사용한다.

8. LLM MQM judge
   - segment 단위로 span-level 오류를 JSON으로 생성한다.
   - 문서 단위 judge는 용어 일관성, 핵심 주장, 한계/라이선스/주의사항 보존을 확인한다.
   - critical 또는 고위험 segment에는 second judge를 선택적으로 적용한다.

9. 점수 집계 및 라우팅
   - hard failure, MQM penalty, QE score, dimension score를 합산한다.
   - `auto_pass`, `review_required`, `reject`, `source_changed` 중 하나를 산출한다.

10. 리포트 생성
   - Markdown 리포트는 한국어로 작성한다.
   - JSON key와 category 이름은 영어로 유지한다.
   - PR comment에는 상위 이슈와 suggested fix만 간결하게 노출한다.

## Hard Gate 설계

Hard gate는 점수화하지 않고 막아야 하는 오류다.

| 게이트 | 검증 방식 | 실패 예시 | 결과 |
| --- | --- | --- | --- |
| Markdown parse | source/target AST parse 가능 여부 | code fence 닫힘 누락 | reject |
| front matter | 필수 key 존재, 비번역 key 보존 | `authors` 변경 | reject |
| code block | fenced code block hash 비교 | Python 코드 일부 번역 | reject |
| inline code | inline code token exact match | `AutoModelForCausalLM` 변경 | reject |
| URL/image path | exact match 또는 whitelist | `/blog/assets/...` 손상 | reject |
| 숫자/단위 | 숫자, %, 날짜, benchmark 수치 비교 | 13B -> 30B | reject 또는 review |
| model/dataset ID | `org/name` 패턴 보존 | `meta-llama/Llama-3` 오타 | reject |
| LaTeX | 수식 token 보존 | `\\alpha` 변경 | reject |
| 표 구조 | 열 수, 행 수, cell 개수 비교 | 표 열 깨짐 | reject |
| segment coverage | source segment hash coverage | 문단 누락 | reject |
| 원문 잔존 | 영어 일반 문장 잔존율 | 문단 전체 미번역 | review 또는 reject |

MVP 정책:

- code block은 전부 보존한다.
- code block 내부 주석 번역은 허용하지 않는다.
- inline code, URL, image path, model id, dataset id는 exact match를 기본으로 한다.
- 숫자/단위는 exact match를 기본으로 하되, 한국어 표기 차이 whitelist를 둔다.
- `title`을 제외한 front matter key는 보존 중심으로 처리한다.

## 보호 토큰 정책

초기 `protected_patterns.yml`은 다음 범주를 포함한다.

```yaml
protected_patterns:
  model_id: "\\b[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+\\b"
  python_identifier: "\\b[A-Za-z_][A-Za-z0-9_]*(\\.[A-Za-z_][A-Za-z0-9_]*)+\\b"
  url: "https?://[^\\s)]+"
  markdown_image: "!\\[[^\\]]*\\]\\([^\\)]+\\)"
  markdown_link: "\\[[^\\]]+\\]\\([^\\)]+\\)"
  inline_code: "`[^`]+`"
  percentage: "\\b\\d+(\\.\\d+)?%"
  env_var: "\\b[A-Z][A-Z0-9_]{2,}\\b"
  cli_flag: "(?<!\\w)--[a-zA-Z0-9][a-zA-Z0-9_-]*"
  latex_inline: "\\$[^$]+\\$"
```

마스킹 예:

```text
Source: Use `AutoModelForCausalLM` with meta-llama/Llama-3.1-8B.
Masked: Use <PROTECTED_001> with <PROTECTED_002>.
```

검증:

- source protected token 집합과 target protected token 집합을 비교한다.
- placeholder 복원 실패는 hard failure다.
- token 순서가 의미에 영향을 주는 경우 순서도 비교한다.

## 용어집 정책

용어집은 참고 문서가 아니라 validator 입력이다.

```tsv
source_term    ko_term              policy
model card     모델 카드             required
inference      추론                  required
fine-tuning    파인튜닝              preferred
Hub            Hugging Face Hub      preserve_or_first_mention
Space          Space                 preserve_product_name
dataset        데이터셋              required
benchmark      벤치마크              required
```

정책 의미:

- `required`: 해당 번역을 반드시 사용한다.
- `preferred`: 권장 번역으로 감점 또는 review 사유가 될 수 있다.
- `preserve_product_name`: 제품명으로 보고 원문을 유지한다.
- `preserve_or_first_mention`: 첫 언급은 병기하고 이후 원문 유지 또는 합의된 표현 사용을 허용한다.

초기 추천:

- Hugging Face 제품명, 라이브러리명, 모델명, dataset id는 원문을 보존한다.
- `dataset`, `benchmark`, `model card`, `fine-tuning`, `inference` 같은 일반 기술 용어는 glossary로 관리한다.
- 동일 글 안에서 같은 source term의 번역이 흔들리면 `terminology` major 또는 minor로 기록한다.

## MQM 기반 채점

하네스의 품질 오류는 MQM 스타일로 분류한다.

| Category | 세부 오류 | 예시 |
| --- | --- | --- |
| `accuracy` | 오역, 누락, 추가, 반대 의미, 과잉 일반화 | `can be used`를 `반드시 사용해야 함`으로 번역 |
| `terminology` | 용어 오역, 제품명 오역, 일관성 위반 | `Space`를 `공간`으로 번역 |
| `technical` | 코드/API/model/dataset/수식/숫자 오류 | `pipeline()`을 `파이프라인()`으로 변경 |
| `fluency` | 문법, 조사, 어순, 띄어쓰기 | 직역투로 의미가 흐려짐 |
| `style_locale` | 톤, 독자 수준, 한국어 기술 문체 | 과도한 구어체 또는 마케팅식 표현 |
| `formatting` | Markdown, 표, 링크, 이미지, HTML 손상 | table pipe 누락 |

Severity와 penalty:

```text
neutral  = 0
minor    = 1
major    = 5
critical = 25 + automatic reject
```

Category weight:

```text
accuracy      x 2.0
technical     x 2.0
terminology   x 1.5
formatting    x 1.5
fluency        x 1.0
style_locale   x 1.0
```

점수식:

```text
APT = Σ(severity_weight * category_weight)

NormalizedPenalty = APT / max(1, source_word_count) * 1000

QualityScore =
  100
  - min(60, NormalizedPenalty * calibration_factor)
  - hard_validator_penalty
```

초기에는 `calibration_factor`를 고정하지 않고 golden set과 challenge set으로 보정한다. BLEU, chrF, SacreBLEU류 lexical metric은 한국어 토큰화와 자연스러운 의역에 민감하므로 주력 gate가 아니라 reference가 있는 회귀 테스트의 참고 지표로 둔다.

## LLM MQM Judge 설계

LLM judge는 점수 생성기가 아니라 span-level 오류 주석기다.

### Segment judge 입력

```text
System:
You are a Korean localization QA reviewer for Hugging Face technical blog posts.
Evaluate only translation quality and publishing risk.
Do not rewrite unless an error exists.

Inputs:
- Source segment
- Korean translation
- Glossary entries relevant to this segment
- Protected tokens
- Style guide summary
- Neighboring context, if available

Output:
Strict JSON only.
```

### Segment judge 출력

```json
{
  "segment_id": "p_021",
  "adequacy_score": 0.88,
  "fluency_score": 0.82,
  "technical_score": 1.0,
  "errors": [
    {
      "category": "accuracy",
      "severity": "major",
      "source_span": "can be used to",
      "target_span": "반드시 사용해야 합니다",
      "explanation": "가능성을 의무로 바꾸어 의미가 강해졌습니다.",
      "suggested_fix": "사용할 수 있습니다"
    }
  ]
}
```

### 안정화 장치

- 번역 생성 모델과 평가 모델을 분리한다.
- temperature는 낮게 고정한다.
- JSON schema validation을 적용한다.
- `source_span`, `target_span`, `explanation`, `suggested_fix`가 없으면 오류로 채택하지 않는다.
- 고위험 segment는 second judge를 적용한다.
- judge prompt는 "좋다/나쁘다"가 아니라 "게시 리스크가 있는 오류인가"를 판단하게 한다.
- LLM judge 결과는 cache key로 `source_hash`, `target_hash`, `prompt_version`, `model`을 사용한다.

## 자동 평가 지표

### MVP 지표

| 지표 | 용도 | 사용 방식 |
| --- | --- | --- |
| Markdown structural diff | 게시 안전성 | hard gate |
| protected token match | 기술 정확성 | hard gate |
| glossary compliance | 용어 일관성 | score + review |
| language ID | 미번역/혼입 탐지 | review |
| length ratio | 누락/과잉 번역 탐지 | review |
| COMETKiwi | reference-free 품질 추정 | score + triage |
| LLM MQM judge | 오류 span, 설명, 수정안 | score + PR comment |
| chrF/SacreBLEU | reference가 있을 때 회귀 참고 | 참고용 |

### Reference가 없는 신규 글

대부분의 신규 HF Blog 글은 승인된 한국어 reference가 없으므로 다음 조합을 기본으로 한다.

```text
Rule-based gates
+ COMETKiwi / QE metric
+ LLM MQM judge
+ glossary/style validator
+ human review sampling
```

### Reference가 있는 회귀 테스트

golden set에는 reference-based metric을 추가할 수 있다. 단독 합격 기준으로 쓰지 않고, prompt/model 변경 후 점수 분포가 급격히 흔들리는지 확인하는 용도로 제한한다.

## 라우팅 기준

초기 기준은 PRD의 상태 모델을 따른다. 실제 threshold는 gold set으로 보정한다.

| 상태 | 조건 | GitHub check |
| --- | --- | --- |
| `auto_pass` | hard failure 없음, critical 없음, major 없음, score >= 90 | pass |
| `review_required` | hard failure 없음, score 75-89, major 1개 이하, glossary 위반 일부 | pass 또는 neutral |
| `reject` | hard failure 있음, critical 있음, score < 75, 기술 오류 major 다수 | fail |
| `source_changed` | source hash 변경으로 기존 번역 stale 가능성 있음 | fail 또는 review |

초기 운영 추천:

- 안정화 전에는 `auto_pass`도 사람이 표본 리뷰한다.
- `review_required`는 PR check를 실패시키지 않되 PR comment에 수정 후보를 노출한다.
- `reject`는 PR check를 실패시킨다.
- draft PR은 생성하되 merge 가능 상태로 두지 않는다.

## 리포트 설계

Markdown 리포트는 PR에서 사람이 읽는 문서다.

```markdown
# Quality Report

- Status: Review Required
- Quality Score: 86.5
- Hard failures: 0
- Critical MQM errors: 0
- Major MQM errors: 1
- Minor MQM errors: 7

## Scorecard

| Dimension | Score | Notes |
| --- | ---: | --- |
| Adequacy | 88 | 핵심 의미는 보존됨 |
| Technical Accuracy | 92 | 보호 토큰 위반 없음 |
| Terminology | 78 | glossary 위반 4건 |
| Publishing Integrity | 100 | Markdown 구조 정상 |

## Top Issues

### QL-001 Terminology / Major

- Segment: `p_021`
- Source: `inference endpoint`
- Current: `추론 끝점`
- Suggested: `추론 엔드포인트` 또는 `Inference Endpoint`
- Reason: Hugging Face 제품/기술 용어로 오해 가능성이 큼
```

PR comment는 상위 이슈만 축약한다.

```text
Status: Review Required
Quality Score: 86.5

Hard failures: 0
Major MQM errors: 1
Minor MQM errors: 7
Glossary violations: 4
Protected token violations: 0

Top issues:
1. p_021 Terminology / Major
   Source: inference endpoint
   Current: 추론 끝점
   Suggested: 추론 엔드포인트 또는 Inference Endpoint
```

## 저장소 배치 계획

PRD는 독립 `translation-qa/` 구조를 제안하지만, 현재 저장소 책임 분리에 맞춰 `skills/quality` 아래에 둔다. `translation-flow`는 계속 manifest 생성과 PR 오케스트레이션만 담당한다.

권장 구조:

```text
skills/quality/
  configs/
    eval_config.yml
    protected_patterns.yml
    gates.yml
  glossary/
    ko.tsv
    product_terms.tsv
    ml_terms.tsv
  style/
    style_guide_ko.md
    examples_good_bad.md
  schemas/
    quality_report.schema.json
    mqm_judge.schema.json
  tools/
    translation_quality_harness.py
  qa_harness/
    markdown_parser.py
    segmenter.py
    aligner.py
    validators/
      markdown_structure.py
      protected_tokens.py
      glossary.py
      numbers.py
      links.py
      latex.py
      language_id.py
    metrics/
      cometkiwi.py
      chrf.py
      embedding_similarity.py
    judges/
      mqm_prompt.md
      llm_judge.py
    reporting/
      markdown_report.py
      pr_comment.py
  tests/
    challenge_set.yml
    fixtures/
      source.md
      target_good.md
      target_bad.md
```

`skills/quality/tools/simple_quality_report.py`는 유지한다. 새 하네스는 별도 CLI로 추가해 기존 로컬 리뷰 흐름을 깨지 않는다.

## GitHub Actions 통합 계획

초기에는 현재 `scripts/run_local_review.py`에서 새 하네스를 호출하게 하고, 이후 별도 quality gate workflow로 분리한다.

권장 command shape:

```bash
python -m skills.quality.tools.translation_quality_harness \
  --manifest reports/pr-130/manifest.yaml \
  --target-root hugging-face-krew.github.io \
  --output-md reports/pr-130/quality-report.md \
  --output-json reports/pr-130/quality-report.json \
  --fail-on-reject
```

Workflow 단계:

```yaml
name: translation-quality-gate

on:
  pull_request:
    paths:
      - "posts/**/*.md"
      - "ko/**/*.md"
      - "glossary/**/*.tsv"
      - "configs/**/*.yml"

jobs:
  qa:
    runs-on: ubuntu-latest
    steps:
      - checkout
      - setup-python
      - install-dependencies
      - run: python -m translation_qa lint-markdown
      - run: python -m translation_qa evaluate --source "$SOURCE" --target "$TARGET"
      - run: python -m translation_qa render-report
      - run: python -m translation_qa comment-pr
```

현재 repo에서는 위 module naming을 그대로 쓰기보다 `skills/quality/tools/translation_quality_harness.py`로 시작하고, 안정화 후 패키지화 여부를 결정한다.

## 테스트 계획

### Golden Set

사람이 승인한 좋은 번역을 저장한다.

초기 목표:

- 5-10개 글로 시작
- 3개월 내 30개 글
- 모델 릴리스, 튜토리얼, 연구/벤치마크, 제품 발표 글을 모두 포함

검증 목적:

- 좋은 번역이 과도하게 reject되지 않는지 확인
- threshold와 calibration factor 보정
- prompt/model 변경 시 점수 분포 회귀 확인

### Challenge Set

의도적으로 오류를 심은 target을 저장한다.

초기 오류 유형:

- 제품명 오역: `Hugging Face Space` -> `허깅페이스 공간`
- 코드 변형: `AutoTokenizer.from_pretrained()` -> `자동토크나이저.from_pretrained()`
- 수치 오류: `70B parameters` -> `7B 파라미터`
- 의미 강도 변화: `can be used` -> `반드시 사용해야 함`
- 한계 누락: `may not work on all GPUs` -> `모든 GPU에서 작동함`
- 라이선스 위험: `non-commercial license` -> `상업적으로 사용 가능`
- benchmark 방향성 반전: `lower is better` -> `높을수록 좋음`
- code fence 누락
- URL/image path 변경
- source segment 삭제

검증 목적:

- hard gate가 구조/보호 토큰 오류를 차단하는지 확인
- LLM MQM judge가 의미 오류를 span-level로 잡는지 확인
- critical 오류가 항상 `reject`로 이어지는지 확인

### Unit/Integration Test

필수 테스트:

- manifest 파싱
- Markdown AST 파싱 실패 처리
- front matter key 보존
- segment extraction과 source hash 생성
- code block hash 비교
- inline code exact match
- URL/image path 비교
- 숫자/단위 비교
- protected pattern extraction
- glossary policy 적용
- MQM penalty 계산
- routing 결정
- JSON schema validation
- Markdown report rendering

## 구현 로드맵

### Phase 0: 정책과 fixture 정리

목표: 구현 전에 gate와 score의 입력 계약을 고정한다.

작업:

- `configs/eval_config.yml` 작성
- `configs/protected_patterns.yml` 작성
- `configs/gates.yml` 작성
- `glossary/ko.tsv`, `product_terms.tsv`, `ml_terms.tsv` 초안 작성
- `schemas/quality_report.schema.json` 작성
- challenge fixture 5개 이상 작성

완료 기준:

- 하네스 없이도 어떤 오류가 `reject`, `review_required`, `auto_pass`인지 문서와 config로 설명 가능

### Phase 1: Deterministic Hard Gate MVP

목표: API key 없이 CI에서 재현 가능한 hard gate를 만든다.

작업:

- 새 CLI `tools/translation_quality_harness.py` 추가
- source/target Markdown AST parser 도입
- front matter validator 구현
- code fence/code block hash validator 구현
- inline code, URL, image path validator 구현
- protected token validator 구현
- 숫자/단위 validator 구현
- table/LaTeX validator 구현
- JSON/Markdown 리포트 출력
- `--fail-on-reject` exit code 구현

완료 기준:

- 기존 manifest로 local replay 가능
- challenge set의 구조/보호 토큰 오류가 reject됨
- `simple_quality_report.py`와 공존함

### Phase 2: Segment와 Glossary

목표: 번역 품질 평가의 최소 단위인 segment 계약을 안정화한다.

작업:

- AST text node segment 추출
- source segment hash 생성
- source/target segment alignment
- segment coverage validator 구현
- glossary validator 구현
- language ID, length ratio, duplicate detector 구현
- translation memory lookup 인터페이스 추가

완료 기준:

- 문단 누락, 중복, 임의 추가를 감지
- 용어집 위반을 category/severity와 함께 리포트
- source hash 변경 시 `source_changed` 상태를 산출

### Phase 3: 자동 Metric

목표: hard gate로 잡히지 않는 품질 위험을 score와 triage 신호로 만든다.

작업:

- COMETKiwi 또는 pluggable QE metric wrapper 구현
- embedding similarity 이상치 탐지 추가
- reference가 있는 fixture에 chrF/SacreBLEU 참고 지표 추가
- metric 결과 cache 구현
- dimension score 집계 구현

완료 기준:

- QE metric을 끄고 켤 수 있음
- API/model dependency가 없어도 deterministic gate는 계속 동작
- 낮은 QE segment가 `review_required` 후보로 표시됨

### Phase 4: LLM MQM Judge

목표: 의미 오역, 누락, 추가, 용어 오역을 span-level로 설명 가능한 이슈로 만든다.

작업:

- `judges/mqm_prompt.md` 작성
- `schemas/mqm_judge.schema.json` 작성
- segment judge 구현
- document judge 구현
- JSON schema validation과 retry 정책 구현
- judge cache 구현
- high-risk segment second judge 옵션 구현
- PR comment용 suggested fix 추출

완료 기준:

- challenge set의 의미 오류를 major/critical로 탐지
- 오류마다 `source_span`, `target_span`, `explanation`, `suggested_fix`가 있음
- critical MQM error가 항상 `reject`를 유발

### Phase 5: Calibration과 운영 통합

목표: 실제 PR gate로 운영 가능한 threshold와 리포트 흐름을 만든다.

작업:

- golden set 10개 이상 수집
- challenge set 10개 이상 확장
- `calibration_factor`와 pass/review/reject threshold 보정
- `scripts/run_local_review.py`에 새 하네스 연결
- GitHub Actions check summary 또는 PR comment 생성
- reports에 source snapshot과 JSON artifact 저장
- reviewer feedback label 수집 방식 정의

완료 기준:

- golden set false reject <= 10%
- challenge set critical detection >= 90%
- `reject`는 GitHub check 실패
- `review_required`는 PR comment로 사람 리뷰 지점을 노출

### Phase 6: 개선 루프

목표: 하네스 결과가 다음 번역 품질 개선으로 되돌아가게 한다.

작업:

- 반복 glossary 위반 집계
- false positive/false negative 라벨링
- translation prompt에 보호 규칙 자동 주입
- translation memory 기반 용어/문체 추천
- 고위험 segment 자동 second review
- 후보 번역 N개 생성 후 QE/LLM reranking 검토
- error taxonomy별 dashboard 준비

완료 기준:

- 반복 오류가 다음 번역에서 감소
- 리뷰 시간이 감소했는지 측정 가능
- threshold와 glossary 변경 이력이 추적됨

## 의사결정 필요 사항

### 1. 평가 목적

추천안: 점수 산출 중심이 아니라 게시 가능성 판정 중심으로 확정한다.

이유: 기술 블로그는 치명 오류 하나가 전체 글의 신뢰를 훼손한다. 좋은 문장 점수보다 위험한 번역을 놓치지 않는 것이 우선이다.

### 2. 코드 블록 정책

추천안: MVP에서는 code block 전체를 보존한다.

주석까지 번역하려고 하면 실행 가능성과 diff 안정성이 나빠진다. 문서용 코드 주석 번역은 안정화 이후 별도 whitelist 모드로 연다.

### 3. 제품명과 일반 용어 정책

추천안: 제품명, 라이브러리명, 모델명, dataset id는 원문 유지. 일반 ML 용어는 glossary로 관리한다.

결정 필요:

- `Hub`, `Spaces`, `Inference Endpoints`의 첫 언급 병기 규칙
- `fine-tuning`, `checkpoint`, `inference`, `dataset` 표준 번역
- 용어집 위반을 `minor`, `major`, hard failure 중 어디까지 올릴지

### 4. LLM judge 도입 시점

추천안: 구현 로드맵에는 Phase 4로 두되, PRD MVP 기준에 맞춰 Beta 이전에는 반드시 붙인다.

규칙 기반 gate만으로는 의미 강도 변화, 제한사항 누락, benchmark 방향성 반전을 충분히 잡기 어렵다. 단, API dependency 때문에 deterministic gate와 분리해 선택 실행 가능하게 만든다.

### 5. COMETKiwi 사용 방식

추천안: gate 단독 기준이 아니라 review triage와 dimension score 입력으로 사용한다.

COMETKiwi는 reference-free 평가에 유용하지만, 낮은 점수만으로 reject하지 않는다. hard failure 또는 MQM critical과 결합해 판단한다.

### 6. PR 실패 정책

추천안: `reject`만 GitHub check 실패로 처리하고, `review_required`는 check pass 또는 neutral + PR comment로 시작한다.

하네스 안정화 전부터 review_required를 실패로 처리하면 false positive로 번역 흐름이 막힐 수 있다.

### 7. 원문 보관과 stale 처리

추천안: 실행 시점의 source snapshot과 segment hash를 reports에 저장하고, hash 변경 시 `source_changed`를 산출한다.

원문이 조용히 업데이트되면 기존 번역이 낡을 수 있으므로, source hash는 재현성과 stale 감지에 모두 필요하다.

### 8. 자동 수정 여부

추천안: 하네스는 자동 수정하지 않고 suggested fix만 제안한다.

QA 도구가 원문 의미를 임의로 바꾸면 책임 경계가 흐려진다. 수정은 번역 단계나 사람 리뷰 단계에서 반영한다.

### 9. 평가 데이터 위치

추천안: 하네스 로직, glossary, style guide, golden/challenge fixture는 `skills/quality` 아래에 둔다.

현재 저장소의 책임 분리상 `translation-flow`는 manifest 생성과 PR 작업에 집중하고, 품질 평가 정책은 quality skill이 소유하는 것이 맞다.

### 10. 리포트 언어

추천안: Markdown 리포트와 PR comment는 한국어, JSON schema key와 category enum은 영어.

리뷰어 경험과 자동화 안정성을 동시에 만족한다.

## 다음 구현 순서

1. `configs/`, `glossary/`, `schemas/`, `tests/fixtures/` 뼈대를 만든다.
2. `translation_quality_harness.py` CLI skeleton을 만든다.
3. Markdown parse, front matter, code/link/image/protected token hard gate부터 구현한다.
4. JSON report schema와 Markdown report renderer를 붙인다.
5. challenge set으로 hard gate 회귀 테스트를 만든다.
6. segment extraction, glossary validator, coverage validator를 추가한다.
7. COMETKiwi와 LLM MQM judge는 deterministic gate가 안정화된 뒤 pluggable dependency로 연결한다.
8. `scripts/run_local_review.py`와 GitHub Actions에 `reject` gate만 먼저 연결한다.

## PRD 대비 반영 사항

- 단일 `overall_score` 중심 계획을 PRD의 `quality_score` + hard failure + MQM penalty + routing 모델로 변경했다.
- 품질 축을 `fidelity/format/localization` 중심에서 `adequacy/technical_accuracy/completeness/fluency/terminology/publishing_integrity`로 재정렬했다.
- hard gate를 별도 최우선 단계로 강화했다.
- MQM category, severity, penalty, category weight를 구현 계획에 포함했다.
- COMETKiwi는 reference-free QE metric으로 추가하되 단독 gate가 아닌 triage 입력으로 정의했다.
- LLM judge는 점수기가 아니라 span-level 오류 주석기로 정의했다.
- source snapshot과 segment hash 기반 `source_changed` 상태를 추가했다.
- golden set과 challenge set을 threshold calibration의 필수 입력으로 명시했다.
- PRD의 독립 `translation-qa/` 구조를 현재 저장소 책임 분리에 맞춰 `skills/quality` 하위 구조로 조정했다.
