# Hugging Face 공식 블로그 한국어 로컬라이징 검증/채점 하네스 기획안

## 1. 기획 방향

이 하네스의 목표는 “좋아 보이는 번역”을 하나의 점수로만 평가하는 것이 아니라, **게시해도 되는 번역인지 판정하고, 수정해야 할 오류를 재현 가능하게 찾아내는 것**입니다. Hugging Face 공식 블로그는 Markdown 기반이며, 글 작성 가이드에서도 front matter, thumbnail, authors, `_blog.yml`, PR 기반 게시 흐름, LaTeX, figure caption, highlight box, Gradio Space embed 같은 구조적 요소를 다룹니다. 따라서 이 프로젝트의 하네스는 일반 번역 품질 평가보다 **기술 문서·Markdown·코드·모델명·수식 보존 검증**을 더 강하게 가져가야 합니다. ([GitHub][1])

추천 구조는 다음입니다.

**1차: 하드 게이트**
Markdown, 코드, 링크, 수식, 숫자, 모델명, API명, front matter, 이미지 경로 등 “깨지면 안 되는 것”을 규칙 기반으로 검증합니다. 실패 시 점수와 무관하게 reject합니다.

**2차: 번역 품질 점수화**
MQM 기반 오류 분류, COMETKiwi 같은 reference-free MT 품질 추정, LLM-as-judge 평가를 결합합니다. MQM은 번역 오류를 유형·심각도별로 구조화하고 품질 지표로 변환하는 프레임워크이므로 이 프로젝트의 채점 스키마로 적합합니다. ([themqm.org][2])

**3차: 휴먼 리뷰 라우팅**
자동 통과, 리뷰 필요, 반려를 나눕니다. 특히 WMT25에서도 자동 번역 평가에서 reference-based 지표가 segment-level에서 여전히 강하고, 오류 span 탐지는 정밀도와 재현율 균형이 어렵다고 보고되었습니다. 즉, 자동 평가만으로 최종 품질을 단정하지 말고, 자동 평가를 “리뷰 우선순위 지정 장치”로 써야 합니다. ([ACL 앤솔로지][3])

---

## 2. “좋은 번역”의 측정 가능 정의

이 프로젝트에서 좋은 번역은 아래 6개 조건을 모두 만족해야 합니다.

| 품질 축    |                                              측정 기준 | 대표 오류                                 |
| ------- | -------------------------------------------------: | ------------------------------------- |
| 의미 충실도  |                           원문 주장, 조건, 한계, 인과관계가 보존됨 | “supports”를 “권장한다”로 과잉 번역, 한계 조건 누락   |
| 기술 정확성  |       모델명, 라이브러리명, API명, 코드, 수식, benchmark 수치가 정확함 | `transformers`를 일반명사 “변환기”로 번역, 숫자 변경 |
| 완전성     |                       원문 segment가 누락·중복·임의 추가되지 않음 | 문단 생략, 설명 추가, 요약 번역                   |
| 한국어 가독성 |                              한국어 독자가 자연스럽게 읽을 수 있음 | 직역투, 조사 오류, 어색한 어순                    |
| 용어 일관성  |                             glossary와 이전 승인 번역을 따름 | “inference”를 추론/인퍼런스/실행으로 혼용          |
| 게시 안전성  | Markdown 렌더링, 링크, 이미지, 표, LaTeX, front matter가 유지됨 | code fence 깨짐, 표 열 수 변경, 링크 손상        |

핵심은 **품질 점수와 게시 가능 여부를 분리**하는 것입니다. 예를 들어 문장 대부분이 자연스러워도 모델 ID 하나가 바뀌면 기술 블로그로서는 치명 오류입니다. 반대로 사소한 띄어쓰기 오류는 점수 감점 대상이지만 자동 reject 사유는 아닙니다.

---

## 3. 하네스 전체 아키텍처

권장 입력은 다음입니다.

```text
source_md: 원문 Markdown
target_md: 한국어 번역 Markdown
glossary.tsv: 용어집
protected_patterns.yml: 번역 금지/보존 패턴
style_guide_ko.md: 한국어 스타일 가이드
translation_memory.jsonl: 승인된 기존 번역 segment
eval_config.yml: 점수 가중치, threshold, whitelist
```

권장 출력은 다음입니다.

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

권장 파이프라인은 다음 순서입니다.

1. **Markdown AST 파싱**
   Markdown을 텍스트로만 비교하지 말고 AST로 파싱합니다. heading, paragraph, list, table cell, code fence, inline code, link, image, HTML block, LaTeX를 구분합니다.

2. **Segment 추출 및 정렬**
   번역 대상 text node만 segment로 추출하고, 각 segment에 `segment_id`, AST path, source hash를 부여합니다.

3. **보호 토큰 마스킹**
   코드, 모델 ID, dataset ID, URL, 파일 경로, API identifier, 숫자, 수식, HTML tag 등을 placeholder로 보호합니다.

4. **하드 게이트 검증**
   Markdown 구조, code fence, front matter, 링크, 이미지 경로, 수식, 숫자, 보존 토큰, segment 누락 여부를 검증합니다.

5. **자동 품질 평가**
   COMETKiwi 또는 유사 reference-free metric, glossary 위반 검사, embedding similarity, language ID, 길이 ratio, 중복 검사 등을 수행합니다. COMETKiwi는 source sentence와 translation을 입력받아 0~1 품질 점수를 반환하는 reference-free MT 평가 모델입니다. ([Hugging Face][4])

6. **LLM 기반 MQM judge**
   segment 단위와 문서 단위로 오류 span, 오류 유형, severity, 수정 제안을 JSON으로 생성합니다.

7. **점수 집계 및 라우팅**
   hard fail, quality score, MQM penalty, 자동 metric score, reviewer 필요 여부를 산출합니다.

8. **PR 리포트 생성**
   GitHub Actions에서 Markdown 리포트와 JSON artifact를 생성하고, PR comment로 수정해야 할 segment를 보여줍니다.

---

## 4. 하드 게이트 설계

하드 게이트는 “점수화하지 말고 막아야 하는 오류”입니다.

| 게이트            | 검증 방식                                    | 실패 예시                     | 결과               |
| -------------- | ---------------------------------------- | ------------------------- | ---------------- |
| Markdown parse | 원문·번역문 모두 AST parse 가능해야 함               | code fence 닫힘 누락          | reject           |
| front matter   | 필수 key 존재, 비번역 key 보존                    | `authors` 변경              | reject           |
| 코드 보존          | fenced code block hash 비교                | Python 코드 일부 번역           | reject           |
| inline code 보존 | inline code token exact match            | `AutoModelForCausalLM` 변경 | reject           |
| URL/이미지 경로     | URL, image path exact match 또는 whitelist | `/blog/assets/...` 손상     | reject           |
| 숫자/단위          | 숫자, %, 날짜, benchmark 수치 비교               | 13B → 30B                 | reject 또는 review |
| 모델/dataset ID  | `org/name` 패턴 보존                         | `meta-llama/Llama-3` 오타   | reject           |
| LaTeX          | 수식 token 보존                              | `\alpha` 변경               | reject           |
| 표 구조           | 열 수, 행 수, cell 개수 비교                     | 표 열 깨짐                    | reject           |
| 번역 누락          | source segment coverage                  | 문단 누락                     | reject           |
| 원문 잔존          | 영어 문장 잔존율 검사                             | 문단 전체 미번역                 | review/reject    |

권장 정책은 **코드 블록은 MVP에서 절대 번역하지 않는 것**입니다. 코드 주석까지 번역하려고 하면 실행 가능성과 diff 안정성이 나빠집니다. 추후 “문서용 코드 주석 번역 허용”을 별도 모드로 열 수 있습니다.

---

## 5. MQM 기반 채점 스키마

MQM식으로 오류를 다음처럼 분류합니다.

| 대분류          | 세부 오류                         | 예시                                   |
| ------------ | ----------------------------- | ------------------------------------ |
| Accuracy     | 오역, 누락, 추가, 반대 의미, 과잉 일반화     | “model can”을 “model will always”로 번역 |
| Terminology  | 용어 오역, 제품명 오역, 일관성 위반         | “Space”를 “공간”으로 번역                   |
| Technical    | 코드/API/model/dataset/수식/숫자 오류 | `pipeline()`을 `파이프라인()`으로 변경         |
| Fluency      | 문법, 조사, 어순, 띄어쓰기              | 직역투로 의미가 흐려짐                         |
| Style/Locale | 톤, 독자 수준, 한국어 기술 문체           | 과도한 구어체 또는 마케팅식 표현                   |
| Formatting   | Markdown, 표, 링크, 이미지, HTML 손상 | table pipe 누락                        |

severity는 MQM 관례를 따르되 프로젝트에 맞게 조정합니다. MQM scorecard는 neutral, minor, major, critical 같은 severity를 쓰며, 예시 multiplier로 0–1–5–25를 제시합니다. critical error는 많은 시스템에서 자동 fail로 처리됩니다. ([themqm.org][5])

추천 penalty는 다음입니다.

```text
Neutral  = 0
Minor    = 1
Major    = 5
Critical = 25 + automatic fail
```

기술 블로그 특성을 반영해 category weight를 추가합니다.

```text
Accuracy       × 2.0
Technical      × 2.0
Terminology    × 1.5
Formatting     × 1.5
Fluency         × 1.0
Style/Locale    × 1.0
```

권장 점수식은 다음입니다.

```text
APT = Σ(severity_weight × category_weight)

NormalizedPenalty = APT / max(1, source_word_count) × 1000

QualityScore = 100 - min(60, NormalizedPenalty × calibration_factor) - hard_validator_penalty
```

단, `calibration_factor`와 pass threshold는 초기에 고정하지 말고, 승인된 번역 gold set으로 보정해야 합니다. 한국어는 교착어라 surface-level lexical metric이 tokenization에 민감합니다. SacreBLEU 자체는 BLEU, chrF, chrF++, TER와 significance testing을 지원하지만, 한국어에서는 lexical-level 지표가 custom pre-tokenization 없이 신뢰도가 흔들릴 수 있다는 연구가 있습니다. 따라서 BLEU류 점수는 주력 지표가 아니라 regression trend나 참고 지표로만 두는 편이 안전합니다. ([GitHub][6])

---

## 6. 자동 평가 지표 구성

### 추천 MVP 지표

| 지표                       | 용도                                 | 권장 사용              |
| ------------------------ | ---------------------------------- | ------------------ |
| Markdown structural diff | 게시 안정성                             | hard gate          |
| protected token match    | 기술 정확성                             | hard gate          |
| glossary compliance      | 용어 일관성                             | score + review     |
| language ID              | 미번역/혼입 탐지                          | review             |
| length ratio             | 누락/과잉 번역 탐지                        | review             |
| COMETKiwi                | reference-free 품질 추정               | score + triage     |
| LLM MQM judge            | 오류 span, 설명, 수정안 생성                | score + PR comment |
| chrF/SacreBLEU           | gold reference가 있을 때 regression 참고 | 참고용                |

### reference translation이 있는 경우

승인된 한국어 reference가 있는 segment에는 COMET reference-based metric, chrF, BERTScore/BLEURT류를 추가할 수 있습니다. 다만 실제 블로그 번역은 “정답 하나”가 아니라 좋은 번역 후보가 여러 개일 수 있으므로, reference-based metric을 단독 합격 기준으로 쓰면 자연스러운 의역을 과도하게 벌점 처리할 수 있습니다.

### reference translation이 없는 경우

대부분의 신규 블로그는 reference가 없을 가능성이 높습니다. 이 경우 추천 조합은 다음입니다.

```text
Rule-based gates
+ COMETKiwi / QE metric
+ LLM MQM judge
+ glossary/style validator
+ human review sampling
```

---

## 7. LLM-as-judge 설계

LLM judge는 “점수만 주는 모델”이 아니라 **span-level 오류 주석기**로 설계해야 합니다.

### Segment judge 입력

```text
System:
You are a Korean localization QA reviewer for Hugging Face technical blog posts.
Evaluate only the translation quality. Do not rewrite unless an error exists.

Inputs:
- Source segment
- Korean translation
- Glossary
- Protected tokens
- Style guide
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

### 문서 단위 judge

Segment judge만 쓰면 전체 문맥 오류를 놓칩니다. 문서 단위 judge는 다음을 봅니다.

* 용어 일관성
* 문단 간 지시어/대명사 일관성
* 제목과 본문 톤 일관성
* 반복되는 오역 패턴
* source article의 핵심 주장 보존 여부
* 결론/주의사항/한계/라이선스 관련 문장의 보존 여부

### judge 안정화 장치

* 번역 생성 모델과 평가 모델을 분리합니다.
* temperature는 낮게 고정합니다.
* JSON schema validation을 적용합니다.
* 동일 segment에 대해 judge 2개를 쓰거나, 고위험 segment만 second judge를 적용합니다.
* LLM judge가 오류를 주장하면 반드시 `source_span`, `target_span`, `explanation`, `suggested_fix`를 요구합니다.
* “좋다/나쁘다”가 아니라 “게시 리스크가 있는 오류인가?”를 판단하게 합니다.

---

## 8. 나쁜 번역을 예방하는 장치

하네스는 사후 평가뿐 아니라 **오류가 나오기 어렵게 만드는 장치**를 포함해야 합니다.

### 8.1 보호 토큰 placeholder화

번역 전에 아래 항목을 placeholder로 바꿉니다.

```yaml
protected_patterns:
  model_id: "\\b[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+\\b"
  python_identifier: "\\b[A-Za-z_][A-Za-z0-9_]*(\\.[A-Za-z_][A-Za-z0-9_]*)+\\b"
  url: "https?://[^\\s)]+"
  markdown_image: "!\\[[^\\]]*\\]\\([^\\)]+\\)"
  markdown_link: "\\[[^\\]]+\\]\\([^\\)]+\\)"
  inline_code: "`[^`]+`"
  percentage: "\\b\\d+(\\.\\d+)?%"
```

예를 들어 `AutoModelForCausalLM`은 `<PROTECTED_042>`로 마스킹하고, 번역 후 원래 값으로 복원합니다. 이렇게 하면 번역 모델이 코드나 모델명을 “친절하게” 바꾸는 사고를 줄일 수 있습니다.

### 8.2 용어집 강제

용어집은 단순 참고 문서가 아니라 validator 입력이어야 합니다.

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

주의할 점은 “무조건 한글화”가 좋은 현지화는 아니라는 것입니다. Hugging Face 제품명, 라이브러리명, 모델명은 영어 원문을 유지하는 편이 검색 가능성과 기술 정확성에 유리합니다.

### 8.3 번역 메모리

기존 승인 번역에서 segment-level translation memory를 만듭니다.

```json
{
  "source": "This guide will show you how to fine-tune...",
  "target": "이 가이드에서는 ... 파인튜닝하는 방법을 설명합니다.",
  "article": "transformers-finetune.md",
  "approved_at": "2026-...",
  "reviewer": "..."
}
```

새 번역 시 유사 segment를 검색해 용어와 문체를 맞춥니다.

### 8.4 challenge set

하네스가 잘못된 번역을 실제로 잡는지 확인하려면 의도적으로 오류를 심은 challenge set이 필요합니다.

예시 항목:

| 테스트 유형        | 원문                                | 잘못된 번역 예                    |
| ------------- | --------------------------------- | --------------------------- |
| 제품명 오역        | Hugging Face Space                | 허깅페이스 공간                    |
| 코드 변형         | `AutoTokenizer.from_pretrained()` | `자동토크나이저.from_pretrained()` |
| 수치 오류         | 70B parameters                    | 7B 파라미터                     |
| 의미 강도 변화      | can be used                       | 반드시 사용해야 함                  |
| 한계 누락         | may not work on all GPUs          | 모든 GPU에서 작동함                |
| 라이선스 위험       | non-commercial license            | 상업적으로 사용 가능                 |
| benchmark 방향성 | lower is better                   | 높을수록 좋음                     |

---

## 9. 통과/리뷰/반려 기준

초기 추천 기준은 다음입니다. 실제 threshold는 gold set으로 보정해야 합니다.

| 상태              | 조건                                                        |
| --------------- | --------------------------------------------------------- |
| Auto Pass       | hard failure 없음, critical 없음, major 없음, score ≥ 90        |
| Review Required | hard failure 없음, score 75–89, major 1개 이하, glossary 위반 일부 |
| Reject          | hard failure 있음, critical 있음, score < 75, 기술 오류 major 다수  |
| Source Changed  | 원문 hash 변경, 기존 번역 stale 가능성 있음                            |

하드 failure 예시는 다음입니다.

```text
- Markdown parse 실패
- code fence 불일치
- URL, 이미지 경로, 모델 ID 손상
- source segment 누락
- 숫자/단위/benchmark 값 변경
- critical MQM error 존재
- front matter 필수 key 누락
```

리뷰 필요 예시는 다음입니다.

```text
- COMETKiwi 하위 10% segment
- 길이 ratio 이상치
- glossary preferred term 미준수
- LLM judge major error 1개
- 원문 영어 문장 일부 잔존
- 동일 용어 번역 불일치
```

---

## 10. GitHub Actions 통합안

PR이 올라오면 다음 workflow를 실행합니다.

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
      - run: python -m translation_qa evaluate --source $SOURCE --target $TARGET
      - run: python -m translation_qa render-report
      - run: python -m translation_qa comment-pr
```

PR comment는 이렇게 구성합니다.

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

2. p_034 Accuracy / Minor
   Source: can be used
   Current: 반드시 사용해야 합니다
   Suggested: 사용할 수 있습니다
```

---

## 11. 저장소 구조 추천

```text
translation-qa/
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
      mqm_schema.json
      llm_judge.py
    reporting/
      pr_comment.py
      html_report.py
  tests/
    challenge_set.yml
    fixtures/
      source.md
      target_good.md
      target_bad.md
  reports/
```

---

## 12. 운영 로드맵

### MVP

* Markdown AST parser
* protected token validator
* 숫자/URL/코드/LaTeX/표 구조 validator
* glossary validator
* COMETKiwi scoring
* LLM MQM judge
* PR report

### Beta

* 승인 번역 gold set 구축
* challenge set 구축
* threshold calibration
* reviewer feedback 수집
* translation memory 적용
* 문서 단위 judge 추가

### Production

* reviewer별 disagreement 분석
* error taxonomy별 dashboard
* source article 변경 감지
* 반복 오류 자동 학습
* 고위험 segment 자동 second review
* 후보 번역 N개 생성 후 QE/LLM reranking

---

## 13. 의사결정 필요 항목과 추천안

| 의사결정 항목        | 선택지                           | 추천안                                  | 이유                                                                                           |
| -------------- | ----------------------------- | ------------------------------------ | -------------------------------------------------------------------------------------------- |
| 평가 목적          | 점수 산출 중심 / 게시 가능성 판정 중심       | 게시 가능성 판정 중심                         | 기술 블로그는 치명 오류 1개가 전체 신뢰를 훼손합니다.                                                              |
| 범위             | 공식 블로그만 / 커뮤니티 블로그 포함         | 공식 블로그 우선                            | 공식 repo 구조와 품질 기준을 먼저 안정화하는 편이 좋습니다. 중국어 번역 repo도 공식 블로그 fork 기반 협업 형태가 존재합니다. ([GitHub][7]) |
| 번역 톤           | 구어체 / 문어체 / 혼합                | 문어체 기반의 자연스러운 기술 블로그체                | “합니다” 중심, 설명 문장은 간결하게. 과한 마케팅 톤은 피하는 편이 좋습니다.                                                |
| 제목 번역          | 원문 유지 / 한국어화 / 병기             | 한국어화 + 필요 시 영문 병기                    | 독자 접근성은 높이고 검색 가능한 핵심 용어는 유지합니다.                                                             |
| 제품명 처리         | 전부 번역 / 전부 원문 / 선별            | 제품·라이브러리·모델명은 원문 유지                  | Hub, Space, Transformers, Diffusers 같은 명칭은 제품/프로젝트명으로 유지하는 편이 안전합니다.                         |
| 코드 블록          | 주석까지 번역 / 전부 보존               | MVP에서는 전부 보존                         | 실행 가능성과 diff 안정성이 우선입니다.                                                                     |
| front matter   | title만 번역 / 전체 보존 / 전부 번역     | `title`은 번역, `thumbnail/authors`는 보존 | 게시 메타데이터 손상을 막아야 합니다.                                                                        |
| 자동 수정          | 자동 반영 / 제안만 / 금지              | 제안만                                  | 번역 QA가 원문 의미를 임의로 바꾸는 위험을 줄입니다.                                                              |
| LLM judge 사용   | 사용 안 함 / 내부 모델 / 외부 API       | 내부 규칙 + COMETKiwi + LLM judge 조합     | 자동 metric만으로는 오류 설명과 수정 지시가 부족합니다.                                                           |
| reference 번역   | 만들지 않음 / 일부 구축 / 전체 구축        | 일부 gold set 구축                       | threshold 보정과 regression test에 필요합니다.                                                        |
| pass threshold | 고정 90점 / 문서별 조정 / calibration | calibration 후 문서 유형별 threshold       | 블로그 난이도와 길이에 따라 점수 분포가 다릅니다.                                                                 |
| 리뷰 정책          | 전수 휴먼 리뷰 / 자동 통과 허용 / 표본 리뷰   | 초기 전수 리뷰, 안정화 후 자동 통과 허용             | 하네스 신뢰도가 검증되기 전까지는 과신하면 안 됩니다.                                                               |
| source 변경 대응   | 수동 확인 / hash 기반 감지            | source segment hash 기반 stale flag    | 원문 업데이트 후 기존 번역이 조용히 낡는 문제를 막습니다.                                                            |
| 공개/비공개 데이터     | 외부 API 허용 / 로컬만               | 공개 블로그는 API 가능, 비공개 초안은 로컬만          | 초안·엠바고 글이 있다면 데이터 유출 리스크를 분리해야 합니다.                                                          |

---

## 14. 최종 추천안

이 프로젝트는 **“번역 점수기”가 아니라 “로컬라이징 품질 게이트”**로 설계하는 것이 맞습니다.

추천 MVP는 다음 조합입니다.

```text
Markdown AST 구조 검증
+ protected token exact-match 검증
+ 숫자/링크/이미지/수식/표 validator
+ glossary validator
+ COMETKiwi reference-free score
+ LLM 기반 MQM span annotation
+ PR comment report
+ gold/challenge set 기반 calibration
```

가장 경계해야 할 설계는 **단일 자동 점수로 번역 품질을 판정하는 방식**입니다. 한국어 기술 번역에서는 자연스러운 문장보다 더 우선되는 항목이 있습니다. 모델명, 코드, 수치, 라이선스, 한계 조건, benchmark 방향성 같은 항목은 한 번 틀리면 독자에게 잘못된 기술 판단을 유도할 수 있습니다. 따라서 하네스의 1순위는 “좋은 번역을 보상하는 것”보다 **위험한 번역을 놓치지 않는 것**이어야 합니다.

[1]: https://github.com/huggingface/blog/blob/main/README.md "blog/README.md at main · huggingface/blog · GitHub"
[2]: https://themqm.org/ "MQM (Multidimensional Quality Metrics) – The place to go to learn about MQM"
[3]: https://aclanthology.org/2025.wmt-1.24/ "Findings of the WMT25 Shared Task on Automated Translation Evaluation Systems: Linguistic Diversity is Challenging and References Still Help - ACL Anthology"
[4]: https://huggingface.co/Unbabel/wmt22-cometkiwi-da "Unbabel/wmt22-cometkiwi-da · Hugging Face"
[5]: https://themqm.org/error-types-2/the-mqm-scoring-models/ "The MQM Scoring Models – MQM (Multidimensional Quality Metrics)"
[6]: https://github.com/mjpost/sacrebleu "GitHub - mjpost/sacrebleu: Reference BLEU implementation that auto-downloads test sets and reports a version string to facilitate cross-lab comparisons · GitHub"
[7]: https://github.com/huggingface-cn/hf-blog-translation "GitHub - huggingface-cn/hf-blog-translation: Chinese Localization repo for HF blog posts / Hugging Face 中文博客翻译协作。 · GitHub"
