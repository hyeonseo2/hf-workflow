# HF 번역 워크플로우 변경 보고서 (ECL 파이프라인 기준)

- 작성일: 2026-05-18

---

## 1. 문서 목적

이 문서는 번역 파이프라인의 구조적 변경을 기술적으로 정리한다.

1. 원본 기준선(Pre-ECL) 대비 ECL 도입 시점의 구조 변화
2. GitHub Actions YML 변경과 운영 영향
3. ECL 코어/어댑터/오케스트레이션 코드의 함수 단위 동작
4. 실제 실행 피드백을 반영한 안정화 수정 내역

---

## 2. 단계 구분

| 단계 | 상태 | 근거 |
|---|---|---|
| Phase 0 (Pre-ECL) | 단일 스크립트형 번역 구조, ECL 모듈/adapter 분리 없음 | `hf-workflow-main.zip` 및 초기 노트북 기준선 |
| Phase 1 (ECL 도입) | `ecl_translation_pipeline.py` + `translation_adapters.py` + `create_translation_pr.py` 분리 구조 도입 | 첫 커밋 `28647bf` |
| Phase 2 (안정화) | 단일 요청화, 코드블록 보호, 구조 보존 검증, source fallback/skip 정책 정비 | `3da91d9` 이후 연속 커밋 |


## 3. 시스템 아키텍처

## 3.1 런타임 실행 흐름

```text
[GitHub Actions Trigger]
  ├─ schedule
  └─ workflow_dispatch(date, post_url, dry_run)
        |
        v
[Workflow YML]
  1) checkout
  2) python 환경 구성
  3) output 디렉토리 준비
  4) git author 설정
  5) create_translation_pr.py 실행
        |
        v
[create_translation_pr.py]
  A) 대상 포스트 결정(date 또는 post_url)
  B) 원문 source markdown 확보(raw 우선, 옵션 기반 html fallback)
  C) 번역 adapter 선택(openai)
        |
        v
[translation_adapters.py]
  - OpenAI Responses API 호출 함수 구성
  - ECL 코어 함수로 위임
        |
        v
[ecl_translation_pipeline.py]
  i) fenced code block 보호
  ii) markdown block 파싱
  iii) 단일 요청 프롬프트 생성
  iv) 모델 응답(JSON) 파싱
  v) block/code 복원
        |
        v
[후처리 및 저장]
  - escaped newline 정리
  - TOC/anchor 안정화
  - 구조 보존 검증
  - output 파일 작성
  - commit/push/PR
  - run-summary 기록
```

## 3.2 책임 분리

| 계층 | 파일 | 책임 |
|---|---|---|
| Orchestration | `.github/workflows/daily-translation.yml` | 실행 순서, 권한, 환경변수, 입력 파라미터 |
| Run Controller | `translation-flow/scripts/create_translation_pr.py` | 대상 포스트 식별, 소스 확보, 후처리, git/PR orchestration |
| Model Adapter | `translation-flow/scripts/translation_adapters.py` | 모델 호출 추상화, translator interface 구현 |
| Translation Core | `translation-flow/scripts/ecl_translation_pipeline.py` | 블록 파싱, 보호/복원, 프롬프트 규약, JSON 결과 복원 |

---


## 5. Pre-ECL 기준선과 ECL 도입 차이

## 5.1 Pre-ECL(원본 기준선) 특징

- 모델 호출, 청크 분할, 번역, frontmatter 처리, 파일 입출력이 단일 스크립트에 결합
- 모델 의존성이 직접 하드코딩되어 adapter 경계가 없음
- 워크플로우와 코드 계층 간 분리도가 낮음

주요 함수군(기준선 예):

- `gemini_text(...)` 형태의 모델 직접 호출
- `translate_ecl_chunk(...)`, `translate_ecl(...)`
- `make_chunks(...)` 기반 다중 호출
- `split_frontmatter(...)`, `combine_frontmatter(...)`

## 5.2 ECL 도입 시점(`28647bf`) 핵심 추가

1. 모듈 분리
- `ecl_translation_pipeline.py`: 번역 코어
- `translation_adapters.py`: 모델 adapter
- `create_translation_pr.py`: 실행 오케스트레이션

2. adapter 패턴 도입
- `TranslationRequest`, `TranslationAdapter`, `OpenAITranslationAdapter`

3. 코어 인터페이스 표준화
- `translate_markdown_with_ecl(...)` 중심 호출
- 모델 호출을 `model_call` 콜백으로 분리

4. CI/워크플로우 연결 가능 구조
- CLI 인자 기반 실행 흐름과 commit/push/PR 연결

---

## 6. ECL 도입 이후 안정화 변경

## 6.1 커밋 기반 타임라인

| 커밋 | 변경 파일 | 기술적 변경 |
|---|---|---|
| `28647bf` | `ecl_translation_pipeline.py` | ECL 코어 도입, block 파싱/라벨링, chunk 호출 구조 |
| `3da91d9` | `ecl_translation_pipeline.py`, `translation_adapters.py` | chunk 제거, 단일 요청화, 상세 로그 추가 |
| `514b32b` | `ecl_translation_pipeline.py` | fenced code block 보호/복원 추가 |
| `2154caa` | `create_translation_pr.py` | escaped newline 정규화, frontmatter 보존 강화 |
| `8555b3a` | `create_translation_pr.py` | 수동 TOC/anchor 안정화 강화 |
| `8bc1e48` | `create_translation_pr.py` | 표/이미지/코드블록 개수 기반 구조 보존 검증 |
| `9785787` | `create_translation_pr.py` | RSS 미매칭 시 `post_url` 직접 소스 해석 경로 추가 |
| `23a81a9` | `create_translation_pr.py` | community/non-repo 문서 skip 분기 추가 |
| `f0f4472` | workflow YML | git author 설정으로 commit 실패 방지 |

## 6.2 핵심 구조 전환

도입 초기(다중 요청):

```text
blocks = parse_markdown_blocks(source)
chunks = make_chunks(blocks)
for chunk in chunks:
  prompt = build_prompt(chunk)
  result = model_call(prompt)
  merge(result)
```

현재(단일 요청 + 보호/검증):

```text
protected, code_map = protect_fenced_code_blocks(source)
blocks = parse_markdown_blocks(protected)
prompt = _translation_prompt(...)
result = model_call(prompt)
restored = restore_body(...)
restored = restore_fenced_code_blocks(restored, code_map)
validated = enforce_structure_preservation(source, restored)
```

전환 효과:

- 요청 횟수 감소로 비용/지연/실패 표면 축소
- 문서 전체 문맥 유지로 용어 일관성 향상
- 코드 및 구조 요소 손실 가능성 감소

---

## 7. 번역 코드 함수 상세

## 7.1 `ecl_translation_pipeline.py`

### 7.1.1 `translate_markdown_with_ecl(source_markdown, core_rules, target_language, model_call, ...)`

역할:
- ECL 번역 파이프라인의 메인 엔트리

입력:
- `source_markdown`: 번역 대상 마크다운 본문
- `core_rules`: 번역 규칙 프롬프트 텍스트
- `target_language`: 목표 언어
- `model_call`: 모델 호출 콜백

내부 단계:

1. `protect_fenced_code_blocks`로 코드 영역 placeholder 치환
2. `parse_markdown_blocks`로 블록 단위 파싱
3. `label_blocks`로 번역 단위 식별자 부여
4. `_translation_prompt`로 단일 요청 프롬프트 구성
5. `model_call` 실행
6. `parse_json_array`로 응답 파싱
7. `restore_inline`, `restore_body`, `restore_fenced_code_blocks` 순으로 복원

예외/복원 정책:

- JSON 파싱 실패 시 원문 block fallback
- 비정상 block 항목은 원문 유지 우선

### 7.1.2 `protect_fenced_code_blocks(markdown)` / `restore_fenced_code_blocks(markdown, saved)`

역할:
- fenced code block의 원문 보존

동작:
- 번역 전: 코드블록을 `{{CODE_BLOCK_n}}`로 치환
- 번역 후: placeholder를 원본 코드로 역치환

효과:
- 모델이 코드 내부 문자열/문법을 임의 변환하는 문제 차단

### 7.1.3 `parse_markdown_blocks(body_text)`

역할:
- markdown-it token 기반 블록 분해

특징:
- 제목/문단/목록/표/코드 등 구조별 블록 정규화
- `CODE_BLOCK_n` placeholder는 비번역 대상으로 처리

### 7.1.4 `_translation_prompt(...)`

역할:
- 모델 입력 메시지 생성

강제 규약:

- 출력 형식: JSON array only
- 블록 id 및 순서 유지
- `KEEP_n`, `CODE_BLOCK_n` placeholder 보존

### 7.1.5 `build_context(...)` / `glossary_candidates(...)`

역할:
- 제목/헤딩/용어 후보를 문맥 정보로 제공

목적:
- 용어 일관성 향상
- 과도한 의역 및 설명 증폭 억제

## 7.2 `translation_adapters.py`

### 7.2.1 `OpenAITranslationAdapter.translate(request)`

역할:
- OpenAI API 호출과 ECL 코어 파이프라인 연결

입력 객체:
- `TranslationRequest(title, source_url, source_markdown, target_locale)`

내부 처리:

1. `docs/translation_prompt.md` 로드
2. locale -> language 매핑 (`ko` -> `Korean`)
3. `client.responses.create(...)` 호출 함수 구성
4. `translate_markdown_with_ecl(...)`에 `model_call` 전달

로그:

- 모델명
- source chars
- prompt chars
- response chars

## 7.3 `create_translation_pr.py` (번역 관련 함수군)

### 7.3.1 소스 확보

#### `discover_markdown_urls(post_url, source_html)`
- `post_url`/HTML 힌트로 raw markdown 후보 URL 목록 생성

#### `looks_like_markdown(text)`
- 헤딩/목록/표/코드펜스 패턴 기반 휴리스틱 판정

#### `extract_source_markdown(post_url, source_html, allow_html_fallback=False)`
- 1차: raw markdown fetch 시도
- 2차: `--allow-html-fallback` 옵션일 때만 HTML 추출 허용
- 실패 시: `SourceMarkdownUnavailableError`

### 7.3.2 `post_url` 직접 모드

#### `split_source_frontmatter(markdown)`
- frontmatter 분리 및 핵심 필드 파싱
- 필드: `title`, `date/published/published_at`, `thumbnail`, `authors`

#### `resolve_post_from_source(post_url, allow_html_fallback)`
- RSS 피드를 거치지 않고 source markdown frontmatter로 `FeedPost` 구성
- 필수 필드 부족 시 실패 처리

### 7.3.3 번역 후 안정화

#### `normalize_escaped_newlines(markdown)`
- 과다 escape(`\\n`, `\\r\\n`)를 실제 줄바꿈으로 정규화
- 코드펜스 내부는 비변경

#### `stabilize_manual_toc(markdown)`
- 수동 TOC 섹션 anchor/link 재구성
- `##` 헤딩 anchor 일관성 보정

#### `enforce_structure_preservation(source_markdown, translated_markdown)`
- 표/이미지/코드블록 개수 비교
- 번역 결과에서 구조 요소 감소 시 실패 처리

### 7.3.4 community article 처리

#### `SourceMarkdownUnavailableError`
- raw markdown 미확보 상태를 명시적으로 표현

#### `main(...)`의 `skipped_community` 분기
- community/non-repo 문서는 hard fail 대신 skip 처리
- run-summary에 `skipped_community` 상태 기록

---

## 8. 실행 피드백 기반 수정 매핑

| 관찰된 현상 | 반영 지점 | 수정 내용 |
|---|---|---|
| 모델 호출 횟수 과다 | `3da91d9` | chunk loop 제거, 단일 요청화 |
| 코드블록 변형 | `514b32b` | code placeholder 보호/복원 |
| TOC 링크 불안정 | `514b32b`, `8555b3a` | TOC/anchor 재구성 |
| escaped newline 노이즈 | `2154caa` | newline 정규화 함수 추가 |
| 메타데이터 누락 | `2154caa` | frontmatter passthrough 강화 |
| RSS 미매칭 URL 실패 | `9785787` | source frontmatter 기반 직접 모드 추가 |
| community URL 404 실패 | `23a81a9` | skip 분기 및 summary 기록 |
| Actions commit 실패 | `f0f4472` | workflow git author 설정 추가 |

