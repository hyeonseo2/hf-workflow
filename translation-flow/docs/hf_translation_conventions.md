# Hugging Face 번역 컨벤션

이 문서는 Hugging Face 기술 블로그를 한국어로 번역할 때 ECL 번역
파이프라인과 guide context compression이 참고할 수 있는 필수 컨벤션을 정의한다.

압축 단계에서는 이 문서를 통째로 번역 프롬프트에 넣지 않는다. 원문 title,
heading, excerpt, detected features를 기준으로 관련 section만 선택한 뒤 짧은
article-specific guide capsule로 압축한다. 따라서 각 section은 독립적으로 읽혀도
의미가 유지되도록 작성한다.

## 번역 목표

- 원문의 기술적 사실, 저자의 태도, 확신의 강도, 제한 조건을 보존한다.
- 한국어 독자가 자연스럽게 읽고 그대로 따라 할 수 있는 기술 블로그 문체로
  옮긴다.
- 코드, 인라인 코드, 링크 target, 이미지 경로, 수치, 단위, 표 구조, 모델명,
  API명, 제품명은 엄격하게 보존한다.
- 영어 문장 구조를 기계적으로 따라가지 말고 한국어 독자의 읽는 순서에 맞게
  문장을 다시 구성한다.

## Style / voice 문체

- 단어 단위 직역보다 자연스러운 한국어 기술 블로그 문체를 우선한다.
- `we`, `you`, `let's`를 기계적으로 옮기지 않는다. 필요하면 주어를 생략하거나
  객관적 서술로 바꾼다.
- 공식 팀의 목소리가 필요한 경우에는 "저희"를 사용할 수 있지만, 과도하게 반복하지
  않는다.
- 원문이 중립적인 경우 홍보성 표현이나 과장된 감탄을 추가하지 않는다.
- "탐험합니다", "뛰어들어 봅시다", "당신은 사용할 수 있습니다"처럼 영어식
  표현을 그대로 옮긴 번역투를 피한다.
- 기술 설명은 차분하고 명확하게 쓴다. 과장된 마케팅 문구보다 정확한 설명을
  우선한다.

## Meaning strength / modal 표현 보존

- `may`는 가능성으로 옮기고 단정하지 않는다.
- `can`은 가능 또는 기능 지원으로 옮긴다.
- `should`는 권장, 기대, 필요의 강도를 문맥에 맞게 유지한다.
- `must`는 필수 조건으로 옮긴다.
- `only`, `up to`, `in some cases`, `not always` 같은 제한 표현을 빠뜨리지 않는다.
- `early results suggest`, `results are promising`처럼 조심스러운 표현을 확정적
  성능 주장으로 바꾸지 않는다.
- benchmark, evaluation, result 문장에서는 수치뿐 아니라 확신의 강도도 보존한다.

## 정보 추가 금지

- 원문에 없는 기술 설명, 평가, 예시, 원인, 결론을 추가하지 않는다.
- 모델 성능, 제품 완성도, 연구 결과를 원문보다 강하게 말하지 않는다.
- `즉`, `다만`, `이 경우`, `예를 들어`, `앞서 설명한 것처럼` 같은 연결 표현은
  원문의 흐름을 자연스럽게 이어야 할 때만 사용한다.
- 연결 표현을 새 설명이나 해석을 추가하는 통로로 사용하지 않는다.
- source article의 범위를 넓히지 않는다. inference 글을 training, deployment,
  optimization 전체를 다루는 글처럼 번역하지 않는다.

## Terminology policy 용어 처리

- 용어는 정확성, 검색성, 이해 가능성, 문서 내부 일관성을 함께 고려한다.
- Hugging Face 제품명, 모델명, 데이터셋명, 벤치마크명, 라이브러리명, 조직명,
  저장소명은 원문 표기를 유지한다.
- glossary section에서 이미 선택된 한국어 용어가 있으면 글 전체에서 일관되게
  사용한다.
- 한국어 독자에게 영어 표기가 더 익숙한 기술 용어는 원문 병기나 원문 유지가
  더 자연스러운지 문맥으로 판단한다.
- `alignment`, `head`, `activation`, `layer`, `dispatch`, `prompt`, `token`,
  `serving`처럼 문맥 의존적인 용어는 단어 단위가 아니라 문단 단위로 판단한다.
- compressed guide는 구체적인 source-to-target 용어 매핑을 새로 만들지 않는다.
  용어 매핑은 별도 Glossary section이 담당한다.

## Model / dataset / product 이름 보존

- `Hugging Face`, `Transformers`, `Diffusers`, `Datasets`, `Tokenizers`, `PEFT`,
  `Accelerate`, `Hub`, `Spaces`, `Inference Endpoints`, `Gradio` 같은 브랜드,
  라이브러리, 제품명은 원문 표기를 유지한다.
- 모델 ID, 데이터셋 ID, repository ID, organization ID는 번역하지 않는다.
- `meta-llama/Llama-3.1-8B`, `allenai/c4`, `squad`, `glue`처럼 slash, hyphen,
  version number가 포함된 ID는 문자 단위로 보존한다.
- 모델명과 데이터셋명이 일반 명사처럼 보이더라도 문맥상 고유명사이면 번역하지
  않는다.

## Code / CLI / API 보존

- fenced code block의 실행 토큰은 변경하지 않는다.
- 설명용 code comment는 문맥상 안전할 때 한국어로 번역할 수 있지만, identifier,
  string literal, option, path, value는 바꾸지 않는다.
- 인라인 코드의 내용은 정확히 보존한다.
- CLI 명령어, package name, import path, class name, function name, method name,
  argument name, environment variable, config key는 번역하지 않는다.
- `AutoTokenizer`, `Trainer`, `AutoModelForCausalLM`, `from_pretrained()`,
  `push_to_hub()`, `device_map`, `torch_dtype`, `trust_remote_code` 같은 API 요소는
  원문 그대로 둔다.
- `huggingface-cli login`, `pip install`, `uv run`, `python train.py`,
  `--model-id` 같은 command와 flag는 번역하지 않는다.

## Markdown / MDX 구조 보존

- 제목, heading level, 목록, 표, 이미지, 링크, 각주, blockquote, fenced code
  block, MDX component 구조를 보존한다.
- Markdown syntax를 한국어 문장에 맞게 정리할 수는 있지만, 구조적 의미가 바뀌면
  안 된다.
- 원문의 문단 또는 section을 누락하지 않는다.
- MDX component name, prop name, import statement, JSX-like syntax는 번역하지
  않는다.
- frontmatter에서 title처럼 번역 대상인 필드만 번역하고, slug, date, tags, author,
  thumbnail, path 같은 메타데이터는 임의로 바꾸지 않는다.

## Link / image / anchor 보존

- 링크 텍스트는 번역할 수 있지만 link target은 바꾸지 않는다.
- 영어 문서 링크를 임의로 `/ko/` 경로로 바꾸지 않는다.
- 이미지 alt text와 caption은 번역할 수 있지만 이미지 파일 경로는 바꾸지 않는다.
- 명시 anchor가 있으면 원문과 동일하게 유지한다.
- heading 뒤의 `[[anchor-id]]`, `{#anchor-id}` 같은 anchor syntax를 삭제하거나
  번역하지 않는다.
- 원문에 없는 emoji를 추가하지 않는다. 원문 emoji도 의미나 브랜드 톤에 직접
  기여하지 않으면 늘리지 않는다.

## Table / benchmark / metric / number 보존

- 표의 열 수, 행 수, 열 순서, alignment marker를 유지한다.
- table cell의 설명 텍스트는 번역하되 모델명, 데이터셋명, metric name, score,
  unit, version number는 정확히 보존한다.
- benchmark name, leaderboard name, metric name, rank, score, percentage, unit,
  latency, throughput, memory 수치를 바꾸지 않는다.
- 비교 방향을 보존한다. higher is better, lower is better, faster, slower,
  reduction, increase, decrease의 의미가 바뀌면 안 된다.
- `up to 30%`는 최대값 표현으로 유지하고 평균값이나 보장값처럼 번역하지 않는다.
- 실험 결과 문장은 원문의 조건, 범위, 제한을 함께 보존한다.

## Title / heading 제목 처리

- 제목은 짧고 명확하며 검색 가능하게 번역한다.
- 원문보다 과장하지 않는다.
- `simple guide`, `best`, `faster`, `state-of-the-art` 같은 표현은 문맥의 강도에
  맞게 옮긴다.
- heading은 직역보다 전달력과 정보 구조를 우선하되, anchor가 있으면 anchor는
  그대로 유지한다.
- 제목에 제품명, 모델명, benchmark명이 있으면 원문 표기를 보존한다.

## Korean quality 한국어 품질

- 번역투를 줄이고 자연스러운 한국어 기술 문장으로 쓴다.
- `~에 의해`, `~하는 것에 있어`, `~를 가지다`, `이는 ~입니다`,
  `사용되어질 수 있습니다`, `~로 하여금` 같은 표현은 문맥에 맞게 고친다.
- `under the hood`는 문맥상 "내부적으로"처럼 자연스럽게 옮긴다.
- `out of the box`는 문맥상 "별도 설정 없이"처럼 옮긴다.
- list 안에서는 문장형과 명사구형을 섞지 않는다.
- 같은 개념은 글 전체에서 같은 표현으로 유지한다.

## 운영 참고

- 이 문서는 guide context compression의 입력 문서다.
- 압축 결과는 현재 글에 필요한 번역 주의사항만 짧게 남긴다.
- 압축 결과는 원문을 번역하거나 원문 사실을 요약하지 않는다.
- 압축 결과는 구체적인 glossary mapping을 만들지 않는다.