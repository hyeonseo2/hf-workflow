# Style Guide Evaluation Implementation Plan

## 목적

`style/hf-blog-ko-translation-guide.md`를 번역 품질 하네스의 평가 기준으로 연결한다. 현재 하네스는 Phase 0-3 기준으로 Markdown 구조, 보호 토큰, glossary, segment coverage, heuristic QE metric을 평가한다. 이 계획은 새 가이드의 규칙을 hard gate, review gate, style score, LLM judge rubric으로 나누어 구현하는 방법을 정의한다.

목표는 "가이드를 사람이 읽는 문서"로만 두지 않고, PR 리포트와 JSON 리포트에서 다음을 자동으로 드러내는 것이다.

- 반드시 수정해야 하는 게시 위험
- 사람이 판단해야 하는 문체/의미 위험
- 한국어 블로그 품질을 높이는 style score
- 어떤 가이드 조항을 근거로 이슈가 발생했는지

## 가이드 자산 위치

원문 가이드는 다음 위치에 둔다.

```text
skills/quality/style/hf-blog-ko-translation-guide.md
```

하네스 기본 설정에는 다음 입력을 추가한다.

```yaml
style:
  guide_path: skills/quality/style/hf-blog-ko-translation-guide.md
  policy_path: skills/quality/configs/style_policy.yml
  enabled: true
```

원문 Markdown은 사람이 읽는 canonical guide로 유지하고, 자동 평가에는 별도 `style_policy.yml`을 사용한다. 긴 가이드를 매 실행마다 ad hoc으로 파싱하면 규칙 변경 추적과 테스트가 어려워지기 때문이다.

## 평가 축 매핑

가이드의 내용을 현재 scorecard에 다음처럼 연결한다.

| 가이드 영역 | 하네스 category | 평가 방식 | 기본 라우팅 |
| --- | --- | --- | --- |
| 코드, 인라인 코드, 링크 target, 이미지 경로, 표 보존 | `technical`, `formatting` | hard gate | `reject` |
| 수치, 모델명, API명, bare URL 보존 | `technical`, `formatting` | review gate + score 감점 | `review_required`, 저점이면 `reject` |
| 문단 누락, 원문에 없는 기술 설명 추가 | `accuracy` | segment coverage + LLM judge | `reject` 또는 `review_required` |
| may/can/should/must/up to/in some cases 의미 강도 | `accuracy` | modal/hedging validator + LLM judge | `review_required`, critical 가능 |
| 과장, 성능 표현 강화 | `accuracy`, `style_locale` | claim strength validator + LLM judge | `review_required` |
| glossary, 첫 등장 영문 병기, 문맥 의존 용어 | `terminology` | glossary validator + context rule | `review_required` |
| 제품명, 라이브러리명, 모델명, API명 보존 | `technical`, `terminology` | protected token + glossary policy | `reject` |
| 한국어 문체, 번역투, 긴 문장, 리스트 일관성 | `fluency`, `style_locale` | deterministic style lint + LLM judge | style score 감점 |
| 제목 전달력, 도입부, 마무리, 글의 온도 | `style_locale` | LLM document judge | `review_required` |
| 이모지 추가/증가 | `style_locale`, `formatting` | emoji validator | `review_required` |
| 이미지 alt text와 caption 번역 | `formatting`, `fluency` | image alt/caption validator | `review_required` |

## 정책 파일 설계

새 파일:

```text
skills/quality/configs/style_policy.yml
```

권장 구조:

```yaml
version: 1

style_guide:
  guide_path: skills/quality/style/hf-blog-ko-translation-guide.md

hard_gate_rules:
  preserve_inline_code: true
  preserve_link_targets: true
  preserve_image_paths: true
  preserve_numbers: true
  preserve_model_ids: true
  preserve_table_shape: true

review_rules:
  modal_strength:
    source_terms:
      may: ["~일 수 있습니다", "~할 수 있습니다"]
      can: ["~할 수 있습니다"]
      should: ["~하는 것이 좋습니다", "~해야 합니다"]
      must: ["반드시", "~해야 합니다"]
      up to: ["최대"]
      in some cases: ["일부 경우"]
  overstatement:
    risky_pairs:
      "can improve": ["개선합니다"]
      "promising": ["놀라운", "압도적인"]
      "significant": ["압도적인"]
      "production-ready": ["즉시 상용화"]
  translationese:
    discouraged:
      - "~에 의해"
      - "~하는 것에 있어"
      - "~를 가지"
      - "사용되어질"
      - "~로 하여금"
  emoji:
    forbid_added_emoji: true
  list_consistency:
    enabled: true

style_score:
  max_penalty:
    modal_strength: 20
    overstatement: 20
    translationese: 10
    title_quality: 10
    list_consistency: 5
    emoji: 5
```

## 구현 단계

### Step 1: Style Guide Loader

목표: 하네스가 가이드와 정책 파일을 명시적으로 인식하게 한다.

작업:

- `--style-guide` CLI 옵션 추가
- `--style-policy` CLI 옵션 추가
- 기본값은 `skills/quality/style/hf-blog-ko-translation-guide.md`와 `configs/style_policy.yml`
- JSON report metadata에 `style_guide_path`, `style_policy_version` 기록
- Markdown report에 "Style Guide" 섹션 추가

완료 기준:

- style guide 경로가 리포트에 남는다.
- policy 파일이 없어도 기존 Phase 0-3 검사는 계속 동작한다.

### Step 2: Deterministic Style Validators

목표: LLM 없이도 잡을 수 있는 가이드 위반을 자동 탐지한다.

추가 validator:

- `modal_strength`: source의 `may/can/should/must/up to/in some cases/not always`와 target의 강도 표현 비교
- `overstatement`: 원문보다 강한 홍보/성능 표현 탐지
- `translationese`: "~에 의해", "사용되어질 수", "후드 아래에서" 같은 번역투 탐지
- `emoji_delta`: 원문에 없던 이모지 추가 탐지
- `list_consistency`: 같은 list 안에서 문장형/명사구형 혼합 탐지
- `title_style`: 제목 과장 표현과 과도한 직역 후보 탐지
- `intro_closing_style`: 도입부/마무리의 직역투 표현 탐지
- `alt_text_caption`: 이미지 alt text가 번역되었는지, path는 보존되었는지 확인

라우팅:

- modal strength가 의미를 반대로 바꾸면 `accuracy/major`
- `must`를 "좋습니다"로 약화하거나 `may`를 단정으로 강화하면 `accuracy/major`
- 원문에 없는 이모지는 `style_locale/minor` 또는 반복 시 `major`
- 번역투는 `fluency/minor`

완료 기준:

- deterministic validator만으로 가이드의 hard gate와 일부 review gate를 리포트할 수 있다.
- 새 negative fixture에서 각 validator가 최소 1건 이상 탐지된다.

### Step 3: Style Score Aggregation

목표: 가이드 기반 문체 평가를 기존 `dimension_scores`에 반영한다.

변경:

- `style_locale` score를 report에 명시적으로 추가하거나 기존 `fluency`와 분리한다.
- 현재 JSON schema의 `dimension_scores`에 `style_locale` 추가를 검토한다.
- `quality_score` 계산에서 hard gate는 계속 우선하고, style issue는 감점 중심으로 처리한다.

권장 점수:

```text
style_score = 100 - min(40, style_penalty)

style_penalty =
  modal_strength_major * 8 +
  overstatement_major * 8 +
  translationese_minor * 1 +
  list_consistency_minor * 2 +
  emoji_minor * 2 +
  title_style_minor * 3
```

완료 기준:

- style issue가 있어도 critical/hard failure가 없으면 기본적으로 `review_required` 또는 style score 감점으로 남는다.
- technical hard gate와 style score가 섞여서 잘못 `auto_pass`되지 않는다.

### Step 4: Glossary 강화

목표: 가이드의 용어 우선순위와 첫 등장 병기 규칙을 현재 glossary validator에 반영한다.

작업:

- `glossary/*.tsv`에 `first_mention`, `preserve`, `context` column 추가 검토
- `fine-tuning`, `checkpoint`, `quantization`, `alignment`, `serving`, `latency`, `throughput` 등 가이드 용어 반영
- 첫 등장 규칙 구현: `미세 조정(fine-tuning)` 이후 `미세 조정`
- 문맥 의존 용어는 deterministic rule로 한계가 있으므로 LLM judge에 전달

완료 기준:

- 검색성 필요한 용어의 첫 등장 영문 병기 누락을 `terminology/minor` 또는 `major`로 표시한다.
- 제품명/모델명/API명은 glossary 및 protected-token review gate로 계속 보존하되, 과검출 가능성이 큰 항목은 hard failure로 바로 올리지 않는다.

### Step 5: LLM MQM Judge Rubric 반영

목표: deterministic rule로 잡기 어려운 가이드 규칙을 LLM judge rubric으로 평가한다.

`judges/mqm_prompt.md`에 포함할 rubric:

- 원문 voice와 글의 온도가 유지되었는가
- `we/you/let's`를 한국어 문맥에 맞게 처리했는가
- 의미 강도와 조건 표현이 보존되었는가
- 원문보다 과장하거나 기술 설명을 추가하지 않았는가
- 제목, 도입부, 마무리가 한국어 블로그로 자연스러운가
- 문맥 의존 용어를 올바르게 판단했는가
- 번역투와 영어식 표현이 과하지 않은가

LLM judge 출력:

```json
{
  "segment_id": "p_014",
  "guide_rule": "modal_strength",
  "category": "accuracy",
  "severity": "major",
  "source_span": "may improve",
  "target_span": "개선합니다",
  "explanation": "가능성을 단정으로 바꾸어 의미 강도가 강해졌습니다.",
  "suggested_fix": "개선할 수 있습니다"
}
```

완료 기준:

- guide rule id가 JSON issue에 남는다.
- PR comment에서 "어떤 가이드 기준을 어겼는지"를 사람이 이해할 수 있다.

### Step 6: Fixtures와 Challenge Set 확장

가이드 기반 negative fixture를 추가한다.

필수 fixture:

- `may`를 단정으로 번역
- `must`를 권장으로 약화
- `up to 30%`에서 "최대" 누락
- `can improve`를 "개선합니다"로 번역
- 원문에 없는 성능 이유 추가
- `Hugging Face Space`를 "허깅페이스 공간"으로 번역
- `under the hood`를 "후드 아래에서"로 번역
- 원문에 없는 이모지 추가
- 리스트 문장형/명사구형 혼합
- 링크 target은 유지하되 링크 텍스트 미번역
- 이미지 path는 유지하되 alt text 미번역

완료 기준:

- 각 fixture는 기대 category/severity를 갖는다.
- `python3 -m pytest -q`에서 style guide validator 회귀 테스트가 통과한다.

### Step 7: Report UX

목표: 리뷰어가 가이드 위반을 빠르게 이해하고 고칠 수 있게 한다.

Markdown report에 추가:

```markdown
## Style Guide Findings

| Rule | Severity | Segment | Current | Suggested |
| --- | --- | --- | --- | --- |
| modal_strength | major | p_014 | 개선합니다 | 개선할 수 있습니다 |
```

JSON issue에 추가할 필드:

```json
{
  "guide_rule": "modal_strength",
  "guide_section": "4. 의미·조건·확신의 강도는 절대 바꾸지 않습니다"
}
```

완료 기준:

- PR comment는 top style issues를 3-5개만 보여준다.
- 전체 근거는 Markdown/JSON artifact에서 확인 가능하다.

## 현재 하네스와의 통합 지점

현재 구현된 `translation_quality_harness.py` 기준으로 다음 함수/영역을 확장한다.

- `MetricConfig`: style policy path 추가
- `Issue`: `guide_rule`, `guide_section` 필드 추가
- `validate_documents`: style validator 호출 추가
- `markdown_report`: style guide summary 추가
- `quality_report.schema.json`: style fields 추가
- `tests/fixtures/translation_quality_harness`: guide-based negative fixture 추가
- `tests/challenge_set.yml`: style guide challenge case 추가

## 우선순위

1. `style_policy.yml`과 guide loader 추가
2. deterministic validator 중 modal strength, overstatement, emoji delta부터 구현
3. glossary first-mention rule 추가
4. style score와 report/schema 확장
5. LLM MQM judge에 guide rubric 주입
6. PR comment와 calibration으로 운영 연결

가장 먼저 구현할 가치는 `modal_strength`와 `overstatement`다. 이 둘은 문체 문제가 아니라 의미와 신뢰도 문제이며, Hugging Face 기술 블로그에서 성능/제한사항을 잘못 전달할 가능성이 크다.

## 남은 의사결정

- `style_locale`을 별도 dimension score로 추가할지, 기존 `fluency`에 포함할지
- 첫 등장 영문 병기 누락을 `minor`로 둘지, 핵심 용어는 `major`로 올릴지
- 코드 주석 번역을 허용할지, 현재 Phase 1처럼 code block exact-match를 유지할지
- LLM judge가 style issue suggested fix를 자동 생성하게 할지, 제안만 하고 수정은 사람이 하게 할지
- 원문 voice 평가를 전수로 할지, low-QE/high-risk segment에만 할지
