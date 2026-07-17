# Hugging Face 한국어 번역 모범 사례

이 문서는 Hugging Face 한국어 번역 과정에서 실제로 발생한 PR, 이슈, 리뷰
코멘트를 근거로 재사용 가능한 모범 사례만 정리한다. 일반 번역 컨벤션, 용어집,
스타일 가이드가 아니며, 출처 링크가 없는 항목은 포함하지 않는다.

## 컨텍스트 압축에서의 역할

이 문서는 ECL guide context compression의 "모범사례 corpus"로 사용한다. 압축
단계에서는 이 문서 전체를 번역 프롬프트에 넣지 않고, 현재 원문에서 감지된
Markdown/MDX 구조, code/CLI/API, link/image, benchmark/metric, review workflow
특성에 맞는 사례 section만 선택한다.

압축 결과는 다음을 목표로 한다.

- 현재 글에서 특히 조심해야 할 실제 Hugging Face 한국어 번역 사례를 짧게 남긴다.
- 일반 규칙은 `hf_translation_conventions.md`가 담당하고, 이 문서는 실제 PR과
  리뷰에서 나온 반복 가능한 판단 근거를 제공한다.
- 출처 링크는 이 문서 안에서는 유지하지만, compressed guide에는 필요한 경우에만
  짧게 반영한다.
- 구체적인 source-to-target glossary mapping은 만들지 않는다. 용어 매핑은 별도
  Glossary section이 담당한다.

## 압축 선택 기준

source profile에 다음 특성이 보이면 관련 사례군을 우선 선택한다.

- Markdown, MDX, TOC, anchor, `_toctree.yml`, `[[open-in-colab]]`,
  `[[autodoc]]`가 보이면 "문서 구조와 렌더링 문법" 사례를 우선한다.
- fenced code block, inline code, CLI command, API class, environment variable,
  model ID가 보이면 "코드와 실행 예제 보존" 사례를 우선한다.
- link, URL, image, HTML tag, Colab, notebook이 보이면 "링크와 미디어 보존"
  사례를 우선한다.
- tutorial, quicktour, install, run, step-by-step 문맥이면 "문장 구조와 절차 표현"
  사례를 우선한다.
- large translation, review, PR, maintainer, build, preview 문맥이면 "작업 범위와
  리뷰 흐름", "협업 기록과 대량 번역 운영", "품질 관리와 유지보수" 사례를
  우선한다.
- benchmark, metric, score, result, safety, ethics, deprecated 문맥이면 원문 의미
  강도와 최신 원문 동기화를 다루는 사례를 우선한다.

## 모범 사례

이 섹션의 사례는 `huggingface/smolagents`, `huggingface/transformers`,
`huggingface/lerobot` 등 Hugging Face 저장소의 실제 한국어 번역 PR, 추적 이슈,
리뷰 코멘트에서 가져온다. 일반적인 Hugging Face 문서 번역에도 적용할 수 있지만,
출처는 각 사례의 "출처" 링크를 우선한다.

구조는 `### 유형`, `#### 사례`, `**출처**`를 따른다. 모든 사례는
`**출처**` 아래에 최소 하나 이상의 직접 링크를 가져야 한다. `**출처**`는
압축 chunk가 출처 링크만으로 분리되지 않도록 heading으로 쓰지 않는다.

사례 채택 기준:

- 실제 Hugging Face 한국어 번역 PR, 추적 이슈, 리뷰 코멘트에서 나온다.
- 빌드, 리뷰 흐름, 문서 구조, 코드 보존, 반복 가능한 품질 판단에 영향을 준다.
- 단순 취향 표현이나 사소한 glossary 교정은 독립 사례로 두지 않는다.

### 작업 범위와 리뷰 흐름

작업 범위, 추적 이슈, 리뷰 순서를 안정화한 사례다.

#### 번역 작업은 추적 이슈와 연결

한국어 번역 PR은 어떤 번역 이슈의 일부인지 명시한다. smolagents 한국어 번역은
`[i18n-ko] Translating smolagents docs to Korean` 이슈를, Transformers 한국어
번역은 `Translating docs to Korean` 이슈를 기준점으로 삼고 개별 PR 본문에서
`Part of` 링크로 해당 이슈를 연결했다.

**권장**

```md
Part of https://github.com/huggingface/smolagents/issues/1607
Part of https://github.com/huggingface/transformers/issues/20179
```

**판단 기준**

- 개별 번역 PR이 전체 번역 계획과 연결되어야 리뷰어가 범위를 파악할 수 있다.
- 같은 문서 묶음의 용어와 리뷰 기준을 추적 이슈에서 공유할 수 있다.

**출처**

- smolagents 한국어 번역 추적 이슈: https://github.com/huggingface/smolagents/issues/1607
- `rag.md` 번역 PR 본문: https://github.com/huggingface/smolagents/pull/1646
- `agents.md` 번역 PR 본문: https://github.com/huggingface/smolagents/pull/1720
- Transformers 한국어 번역 추적 이슈: https://github.com/huggingface/transformers/issues/20179
- Transformers `tasks/translation.mdx` 번역 PR 본문: https://github.com/huggingface/transformers/pull/22805
- Transformers `llm_tutorial_optimization.md` 번역 PR 본문: https://github.com/huggingface/transformers/pull/32372

#### PR 제목과 본문 템플릿을 일관되게 사용

smolagents와 Transformers 한국어 번역 PR들은 제목을 `[i18n-KO] Translated
<file>.md to Korean` 또는 `🌐 [i18n-KO] Translated <file>.md to Korean` 형식으로
작성하고, 리뷰 전 체크리스트에 번역 누락/중복, 맞춤법, 용어집, Inline TOC,
live preview 확인을 포함했다.

**권장 PR 제목**

```md
[i18n-KO] Translated `tools.md` to Korean
```

**권장 체크리스트**

```md
- [x] Check for missing / redundant translations (번역 누락/중복 검사)
- [x] Grammar Check (맞춤법 검사)
- [x] Review or Add new terms to glossary (용어 확인 및 추가)
- [x] Check Inline TOC (e.g. `[[lowercased-header]]`)
- [x] Check live-preview for gotchas (live-preview로 정상작동 확인)
```

**출처**

- `tools.md` 번역 PR 본문: https://github.com/huggingface/smolagents/pull/1835
- `using_different_models.md` 번역 PR 본문: https://github.com/huggingface/smolagents/pull/1772
- Transformers `quicktour.md` 수정 PR 본문: https://github.com/huggingface/transformers/pull/24664
- Transformers `big_bird.md` 번역 PR 본문: https://github.com/huggingface/transformers/pull/40445

#### KREW 리뷰 후 Hugging Face maintainer 최종 리뷰 요청

실제 smolagents와 Transformers 번역 PR에서는 먼저 PseudoLab/KREW 팀원에게
한국어 리뷰를 요청하고, 한국어 리뷰 반영 후 Hugging Face maintainer에게 최종
리뷰를 요청했다.

**권장 흐름**

1. 번역자가 셀프 체크리스트를 완료한다.
2. KREW 또는 한국어 리뷰어에게 용어/문체 리뷰를 요청한다.
3. 리뷰 반영 후 `@albertvillanova`, `@stevhliu` 등 해당 프로젝트 maintainer에게
   최종 리뷰를 요청한다.
4. 문서 preview 봇 코멘트를 확인한다.

**출처**

- KREW 가이드와 멘토 피드백 반영 언급: https://github.com/huggingface/smolagents/pull/1646#issuecomment-3377230736
- KREW 승인 후 maintainer 리뷰 요청: https://github.com/huggingface/smolagents/pull/1646#issuecomment-3400220226
- maintainer 승인: https://github.com/huggingface/smolagents/pull/1646#pullrequestreview-3334079420
- doc-builder preview 봇 코멘트: https://github.com/huggingface/smolagents/pull/1720#issuecomment-3400305719
- Transformers `quicktour.md`의 PseudoLab 리뷰 후 maintainer 리뷰 요청: https://github.com/huggingface/transformers/pull/24664#issuecomment-1645196288
- Transformers `big_bird.md`의 KREW 리뷰와 maintainer 승인: https://github.com/huggingface/transformers/pull/40445#pullrequestreview-3171834109
- Transformers `big_bird.md` maintainer 승인: https://github.com/huggingface/transformers/pull/40445#pullrequestreview-3324548403
- Agents Course maintainer가 한국어 리뷰어 확인을 요청한 사례: https://github.com/huggingface/agents-course/pull/606#pullrequestreview-3623482407

### 문서 구조와 렌더링 문법

문서 트리, 앵커, MDX 컴포넌트, 렌더링 구조처럼 번역 품질보다 문서 동작에 먼저
영향을 주는 사례다.

#### `_toctree.yml`에서는 `local`은 유지하고 `title`만 번역

사이드바 항목을 활성화할 때 `local` 경로는 파일 참조이므로 번역하지 않는다.
화면에 표시되는 `title`만 한국어로 옮긴다.

**권장**

```yaml
- local: reference/agents
  title: 에이전트 관련 객체
```

**지양**

```yaml
- local: reference/에이전트
  title: 에이전트 관련 객체
```

**출처**

- `agents.md` 번역 PR의 `_toctree.yml` 변경: https://github.com/huggingface/smolagents/pull/1720
- `title: 에이전트 관련 객체` 리뷰 제안: https://github.com/huggingface/smolagents/pull/1720#discussion_r2415565531
- `tools.md` 번역 PR의 `_toctree.yml` 변경: https://github.com/huggingface/smolagents/pull/1835
- Transformers `tasks/translation.mdx`의 `_toctree.yml` 변경: https://github.com/huggingface/transformers/pull/22805
- Transformers `big_bird.md`의 `local: model_doc/big_bird` 변경: https://github.com/huggingface/transformers/pull/40445

#### 새 언어를 처음 추가할 때는 빌드 언어 목록, TOC, placeholder를 함께 검토

새 한국어 문서 묶음을 처음 만들 때는 번역 파일만 추가해서 끝나지 않는다.
Transformers 초기 한국어 인덱스 PR에서는 PR preview에 한국어가 나타나려면
문서를 `_toctree.yml`에 연결해야 했고, `ko`를 문서 빌드 워크플로의 언어 목록에
추가했다. Agents Course 첫 한국어 추가 PR에서도 `_toctree.yml` 구조, workflow의
`languages` 목록, 누락 파일 때문에 여러 차례 build 오류가 확인되었다. 반대로 아직
번역하지 않은 템플릿 파일을 많이 복사해 두는 것은 리뷰를 흐리므로 삭제 대상이
되었다. 빈 섹션이 빌드 오류를 내면 `in_translation` 같은 placeholder로 명시한다.

**점검**

- 새 언어 코드가 문서 preview/build 대상에 포함되는가?
- `_toctree.yml`에 실제 번역 파일과 placeholder가 의도한 범위만 들어갔는가?
- 아직 번역하지 않은 원문 템플릿 파일을 대량 복사해 두지 않았는가?
- 빈 섹션 때문에 doc-builder 오류가 나지 않는가?

**출처**

- Transformers 첫 한국어 인덱스 PR: https://github.com/huggingface/transformers/pull/20180
- maintainer가 `_toctree.yml` 연결과 템플릿 파일 삭제를 안내한 댓글: https://github.com/huggingface/transformers/pull/20180#issuecomment-1312450687
- 번역자가 워크플로 언어 코드, `_toctree.yml`, `in_translation.mdx`를 반영한 댓글: https://github.com/huggingface/transformers/pull/20180#issuecomment-1312471458
- smolagents 첫 한국어 인덱스 PR의 ko 디렉터리와 toctree 추가 요약: https://github.com/huggingface/smolagents/pull/1581#pullrequestreview-3035200804
- LeRobot 한국어 구조와 `in_translation.md` 추가 PR: https://github.com/huggingface/lerobot/pull/3126
- Agents Course 첫 한국어 폴더와 `_toctree.yml` 추가 PR: https://github.com/huggingface/agents-course/pull/157
- Agents Course에서 `_toctree.yml` 문제로 build 예외가 난다는 리뷰: https://github.com/huggingface/agents-course/pull/157#pullrequestreview-2780836877
- Agents Course에서 원문 `_toctree.yml`과 비교해 `local`/`title` 구조를 맞추라는 리뷰: https://github.com/huggingface/agents-course/pull/157#discussion_r2063072251
- Agents Course에서 workflow의 `languages`에 `ko`를 추가하라는 리뷰: https://github.com/huggingface/agents-course/pull/157#pullrequestreview-2870113931
- Agents Course에서 `_toctree.yml`의 누락 파일 참조를 제거하라는 리뷰: https://github.com/huggingface/agents-course/pull/157#pullrequestreview-2880596864
- Audio Course 한국어 번역 PR에서 workflow `languages: en bn ko`와 한국어 `_toctree.yml`을 함께 추가한 사례: https://github.com/huggingface/audio-transformers-course/pull/68

#### 원문 제목과 사이드바 제목이 다르면 문서 역할을 기준으로 조정

영어 원문 제목과 `_toctree.yml` 표시 제목이 다를 수 있다. 이 경우 단순 직역보다
해당 페이지가 실제로 다루는 내용을 기준으로 정하되, 리뷰어와 합의한다.

**사례**

- 원문 문서 제목: `Agents`
- 사이드바 문맥: Agent 관련 API 객체 페이지
- 최종 권장: `에이전트 관련 객체`

**출처**

- 제목 수정 제안과 번역자의 설명: https://github.com/huggingface/smolagents/pull/1720#discussion_r2416103703
- 리뷰어의 후속 확인: https://github.com/huggingface/smolagents/pull/1720#discussion_r2422501662

#### Inline TOC 앵커는 번역하지 않음

Hugging Face 문서에서는 제목 뒤에 `[[...]]` 형태의 명시적 앵커가 붙는다. 제목은
번역하되 앵커 문자열은 원문 기준으로 유지한다.

**권장**

```md
# Agentic RAG[[agentic-rag]]
## RAG(검색 증강 생성) 소개[[introduction-to-retrieval-augmented-generation-rag]]
```

**지양**

```md
# Agentic RAG[[에이전틱-rag]]
```

**출처**

- `rag.md` 번역 PR의 제목/앵커: https://github.com/huggingface/smolagents/pull/1646
- PR 본문 체크리스트의 Inline TOC 확인 항목: https://github.com/huggingface/smolagents/pull/1646
- Transformers 앵커 링크 수정 PR: https://github.com/huggingface/transformers/pull/22796
- Transformers `quicktour.md`의 앵커 수정과 maintainer 승인: https://github.com/huggingface/transformers/pull/24664#pullrequestreview-1540761743

#### 목록 안 문장은 원문과 같은 불릿/들여쓰기 구조를 유지

목록 항목에 이어지는 문장을 번역할 때 들여쓰기를 잃으면 원문에서는 같은 불릿에
속하던 문장이 별도 문단으로 렌더링될 수 있다. LeRobot
`bring_your_own_policies.mdx` 한국어 번역 PR에서는 `DiTFlow Example` 문장이
원문의 같은 목록 항목에서 빠져 별도 문단으로 렌더링된다는 리뷰가 있었다. 이 PR은
아직 병합 전이므로 번역 승인 사례가 아니라, Markdown 구조 보존 원칙의 근거로만
사용한다.

**점검**

- 원문 목록 항목에 이어지는 문장이 같은 불릿 안에 남아 있는가?
- 줄바꿈을 바꾸더라도 들여쓰기와 list nesting이 유지되는가?
- 번역 후 preview에서 목록과 문단 경계가 원문과 같은가?

**출처**

- LeRobot `bring_your_own_policies.mdx` 한국어 번역 PR: https://github.com/huggingface/lerobot/pull/3383
- 목록 항목 밖으로 빠져 렌더링 구조가 바뀐다는 리뷰: https://github.com/huggingface/lerobot/pull/3383#discussion_r3082424888

#### `[[open-in-colab]]` 지시문은 그대로 유지

문서 렌더링 지시문은 번역하지 않는다. smolagents 예제 번역 PR들은 한국어 문서
상단에서도 `[[open-in-colab]]`을 그대로 유지했다.

**권장**

```md
[[open-in-colab]]
```

**출처**

- `rag.md` 번역 PR: https://github.com/huggingface/smolagents/pull/1646
- `inspect_runs.md` 번역 PR: https://github.com/huggingface/smolagents/pull/1747
- `using_different_models.md` 번역 PR: https://github.com/huggingface/smolagents/pull/1772
- Transformers `tasks/translation.mdx` 번역 PR: https://github.com/huggingface/transformers/pull/22805
- Transformers `llm_tutorial_optimization.md` 번역 PR: https://github.com/huggingface/transformers/pull/32372

#### `[[autodoc]]`와 API 경로는 번역하지 않음

`[[autodoc]]`는 `doc-builder`가 해석하는 지시문이다. 대상 객체명과 모듈 경로도
Python API 참조이므로 번역하지 않는다. 제목은 한국어로 쓸 수 있지만 앵커의 API
경로와 `[[autodoc]]` 대상은 유지한다.

**권장**

```md
## 로컬 Python 실행기[[smolagents.LocalPythonExecutor]]

[[autodoc]] smolagents.local_python_executor.LocalPythonExecutor
```

**출처**

- `agents.md` 번역 PR의 `[[autodoc]]` 유지: https://github.com/huggingface/smolagents/pull/1720
- `tools.md` 번역 PR의 `[[autodoc]]` 유지: https://github.com/huggingface/smolagents/pull/1835
- Transformers `main_classes/quantization.md`의 `[[autodoc]]` 유지: https://github.com/huggingface/transformers/pull/33959
- Transformers `model_doc/big_bird.md`의 `[[autodoc]]` 유지: https://github.com/huggingface/transformers/pull/40445

#### API 클래스명은 원문 유지

`CodeAgent`, `ToolCallingAgent`, `InferenceClientModel`, `LiteLLMModel` 같은 클래스명은
번역하지 않는다. 설명 문장만 한국어로 옮긴다.

**권장**

```md
[`CodeAgent`]는 Python 코드로 도구 호출을 작성합니다.
[`ToolCallingAgent`]는 JSON 형식으로 도구 호출을 작성합니다.
```

**출처**

- `agents.md` 번역 PR의 `CodeAgent`, `ToolCallingAgent` 유지: https://github.com/huggingface/smolagents/pull/1720
- `using_different_models.md` 번역 PR의 모델 클래스명 유지: https://github.com/huggingface/smolagents/pull/1772
- Transformers `trainer.md`의 `Trainer`, `Seq2SeqTrainer`, `TrainingArguments` 유지: https://github.com/huggingface/transformers/pull/32260
- Transformers `big_bird.md`의 `BigBirdConfig`, `BigBirdTokenizerFast` 유지: https://github.com/huggingface/transformers/pull/40445

#### MDX/HTML 컴포넌트는 유지하고 내부 문장만 번역

`<Tip warning={true}>` 같은 컴포넌트명과 속성은 번역하지 않는다. 컴포넌트 내부의
경고 문장만 한국어로 옮긴다.

**권장**

```mdx
<Tip warning={true}>

Smolagents는 실험적인 API로 언제든지 변경될 수 있습니다.

</Tip>
```

**출처**

- `agents.md` 번역 PR의 `<Tip warning={true}>` 유지: https://github.com/huggingface/smolagents/pull/1720
- `tools.md` 번역 PR의 `<Tip warning={true}>` 유지: https://github.com/huggingface/smolagents/pull/1835
- Transformers `tasks/translation.mdx`의 `<Tip>`, `<frameworkcontent>`, `<pt>`, `<tf>` 유지: https://github.com/huggingface/transformers/pull/22805
- Transformers `big_bird.md`의 `<hfoptions>`, `<hfoption>` 유지: https://github.com/huggingface/transformers/pull/40445

#### 실험적 API 경고는 약화하지 않음

`experimental API` 경고는 독자가 호환성 위험을 이해해야 하므로 반드시 유지한다.
표현은 자연스럽게 다듬되, "언제든지 변경될 수 있다"와 "결과도 달라질 수 있다"는
의미를 약화하지 않는다.

**권장**

> Smolagents는 실험적인 API로 언제든지 변경될 수 있습니다. API나 사용되는 모델이 변경될 수 있기 때문에 에이전트가 반환하는 결과도 달라질 수 있습니다.

**출처**

- `agents.md` 번역 PR의 경고문: https://github.com/huggingface/smolagents/pull/1720
- `tools.md` 번역 PR의 경고문: https://github.com/huggingface/smolagents/pull/1835

### 문장 구조와 절차 표현

단어 하나의 표기보다, 번역문이 원문 의미와 독자 행동을 더 명확히 보존하도록 만든
리뷰 사례다.

#### 영어 콜론을 한국어 문장에 기계적으로 옮기지 않음

영어 문서에서 목록이나 코드 블록 앞에 콜론(`:`)을 쓰더라도 한국어에서는 문장을
마침표로 끝내는 편이 자연스러운 경우가 많다.

**지양**

> 플랫폼에서의 실제 모습은 다음과 같습니다:

**권장**

> 플랫폼에서의 실제 모습은 다음과 같습니다.

**출처**

- `inspect_runs.md`의 콜론 제거 제안: https://github.com/huggingface/smolagents/pull/1747#discussion_r2417237401
- `web_browser.md`의 콜론 제거 제안: https://github.com/huggingface/smolagents/pull/1748#discussion_r2417310172
- `rag.md`의 콜론 제거 제안: https://github.com/huggingface/smolagents/pull/1646#discussion_r2410793629
- Transformers `llm_tutorial_optimization.md` 리뷰의 콜론을 마침표로 대체했다는 요약: https://github.com/huggingface/transformers/pull/32372#pullrequestreview-2218369929

#### 직역보다 자연스러운 한국어 문장 구조를 우선

원문 의미가 유지된다면 영어식 명사구 구조를 한국어 서술 구조로 바꾼다.

**지양**

> 검색된 사실에 응답의 근거를 둠으로써 환각 현상을 줄입니다.

**권장**

> 답변의 근거를 검색 결과에 두어 환각 현상을 줄입니다.

**출처**

- `rag.md` 자연스러운 문장 제안: https://github.com/huggingface/smolagents/pull/1646#discussion_r2257520022

#### "-을 가능하게 합니다"를 남용하지 않음

영어의 "enable/make possible" 구조를 그대로 옮기면 번역투가 된다. 한국어에서는
주어를 바꿔 자연스러운 상태 서술로 바꾸는 편이 낫다.

**지양**

> 지식 베이스와의 더 자연스러운 상호작용을 가능하게 합니다.

**권장**

> 지식 베이스와의 상호작용이 더 자연스러워집니다.

**출처**

- `rag.md` 리뷰 제안: https://github.com/huggingface/smolagents/pull/1646#discussion_r2257525584

#### 절차 문장은 독자가 수행할 행동을 명확하게 씀

튜토리얼에서 "Run the following" 같은 문장은 "다음을 실행하세요" 또는 "다음
명령어를 실행합니다"로 옮긴다. 한국어 문장 끝에 불필요한 콜론을 붙이지 않는다.

**권장**

> 먼저 필요한 의존성을 설치하기 위해 다음을 실행하세요.

**출처**

- `web_browser.md` 리뷰 제안: https://github.com/huggingface/smolagents/pull/1748#discussion_r2417310900

### 코드와 실행 예제 보존

실행되는 코드, 명령어, 식별자는 보존하되 주석과 설명 문장은 문맥에 따라 번역할 수
있다는 사례다.

#### 코드 주석은 번역할 수 있지만 실행 코드는 보존

예제 코드 안의 주석은 독자 이해를 위해 한국어로 옮길 수 있다. 하지만 변수명,
환경 변수명, URL, 문자열 리터럴 중 실행 의미가 있는 값은 바꾸지 않는다.

**권장**

```python
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com" # 유럽 지역
# os.environ["LANGFUSE_HOST"] = "https://us.cloud.langfuse.com" # 미국 지역
# Hugging Face 토큰을 입력합니다.
os.environ["HF_TOKEN"] = "hf_..."
```

**출처**

- `inspect_runs.md`의 `EU region` 주석 번역 제안: https://github.com/huggingface/smolagents/pull/1747#discussion_r2417279263
- `US region` 주석 번역 제안: https://github.com/huggingface/smolagents/pull/1747#discussion_r2417279943
- `Hugging Face token` 주석 번역 제안: https://github.com/huggingface/smolagents/pull/1747#discussion_r2417284489

#### 코드 예제의 docstring과 인자 설명은 번역 가능

사용자 정의 도구 예제에서 docstring, `Args`, 인자 설명은 문서 독자가 읽는 설명
역할을 하므로 번역할 수 있다. 단, 함수명과 인자명 자체는 그대로 둔다.

**권장**

```python
def go_back() -> None:
    """이전 페이지로 돌아갑니다."""
```

```python
"""
인자:
    text: 검색할 텍스트
    nth_result: 이동할 n번째 검색 결과 (기본값: 1)
"""
```

**출처**

- `web_browser.md`의 `Args` 번역 제안: https://github.com/huggingface/smolagents/pull/1748#discussion_r2417312126
- `text` 인자 설명 번역 제안: https://github.com/huggingface/smolagents/pull/1748#discussion_r2417318745
- `go_back` docstring 번역 제안: https://github.com/huggingface/smolagents/pull/1748#discussion_r2417321692

#### 코드 블록 속 오류 메시지와 사용자 입력은 신중하게 유지

예제 안에서 사용자에게 보여 주는 영어 출력, 오류 메시지, 검색 질의는 모델 동작과
연결될 수 있다. smolagents 번역 사례에서도 `Match n°... not found`, `Found ...
matches`, 영어 `agent.run()` 질의 등은 유지되었다.

**판단 기준**

- 코드의 실행 결과나 테스트 기대값이면 원문 유지
- 독자 설명용 주석이면 번역 가능
- 모델 입력 예시이면 모델/태스크의 언어 의존성을 확인한 뒤 결정

**출처**

- `web_browser.md` 번역 PR의 코드 블록: https://github.com/huggingface/smolagents/pull/1748
- `async_agent.md` 번역 PR의 `curl` 예시와 JSON 응답: https://github.com/huggingface/smolagents/pull/1749
- Transformers `tasks/translation.mdx`의 모델 입력/출력 예시: https://github.com/huggingface/transformers/pull/22805
- Transformers `big_bird.md`의 `[MASK]` 입력 예시와 CLI 예시: https://github.com/huggingface/transformers/pull/40445

#### 모델 ID, 환경 변수, API 키 플레이스홀더는 번역하지 않음

`model_id`, `HF_TOKEN`, `GEMINI_API_KEY`, `<YOUR-GEMINI-API-KEY>`,
`REMOVE_PARAMETER` 등은 코드 실행과 직접 연결되므로 번역하지 않는다.

**권장**

```python
model = OpenAIServerModel(
    model_id="gemini-2.0-flash",
    api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=GEMINI_API_KEY,
)
```

**출처**

- `using_different_models.md` 번역 PR의 모델/API 예시: https://github.com/huggingface/smolagents/pull/1772
- `inspect_runs.md` 번역 PR의 환경 변수 예시: https://github.com/huggingface/smolagents/pull/1747
- Transformers `tasks/translation.mdx`의 `t5-small`, `my_awesome_opus_books_model` 예시: https://github.com/huggingface/transformers/pull/22805
- Transformers `big_bird.md`의 `google/bigbird-roberta-base` 예시: https://github.com/huggingface/transformers/pull/40445

### 링크와 미디어 보존

링크 목적지, 이미지, HTML 태그는 문서 렌더링과 참조 무결성에 직접 영향을 주는
사례다.

#### 외부 링크와 상대 링크는 유지하고 링크 텍스트만 번역

링크 대상은 바꾸지 않는다. 링크 텍스트는 한국어로 옮길 수 있다.

**권장**

```md
[소개 가이드](../index)
[Starlette 문서](https://www.starlette.io/)
```

**출처**

- `agents.md` 번역 PR의 `[소개 가이드](../index)` 사용: https://github.com/huggingface/smolagents/pull/1720
- `async_agent.md` 번역 PR의 외부 링크 유지: https://github.com/huggingface/smolagents/pull/1749

#### 언어별 리소스 링크는 한국어 경로로 연결되는지 확인

코스 문서처럼 Colab, Studio Lab, 노트북 링크가 별도 리소스를 가리키는 경우에는
표시 문장만 번역해서는 부족하다. 링크 대상이 영어 리소스(`course/en/...`)로 남아
있으면 한국어 독자가 현지화된 노트북을 열 수 없다. Hugging Face Course 한국어 PR
`#1101`은 아직 open 상태이므로 병합 승인 사례는 아니지만, 한국어 문서의 notebook
링크를 `course/en/...`에서 `course/ko/...`로 바꾸고 중복 TOC를 정리한 실제 점검
사례로 볼 수 있다.

**점검**

- Colab, Studio Lab, notebook 링크가 한국어 리소스가 있는 경우 `ko` 경로를 가리키는가?
- 링크 target을 바꿨다면 preview에서 실제로 열리는가?
- `_toctree.yml` 중복 항목과 리소스 링크 수정이 같은 사용자 경험 문제인지 분리해 설명했는가?

**출처**

- Hugging Face Course 한국어 구조와 notebook 링크 수정 PR: https://github.com/huggingface/course/pull/1101
- PR 본문에서 영어 notebook 링크가 한국어 notebook 링크로 바뀌어야 한다고 설명한 사례: https://github.com/huggingface/course/pull/1101
- PR diff에서 `course/en/chapter*` 링크를 `course/ko/chapter*`로 바꾼 사례: https://github.com/huggingface/course/pull/1101/files

#### 이미지와 HTML 태그는 구조를 유지

문서 안의 `<div>`, `<img>` 태그와 이미지 URL은 렌더링에 영향을 주므로 구조를
유지한다. 이미지 주변 설명만 번역한다.

**권장**

```html
<div class="flex justify-center">
    <img src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/smolagents/inspect_run_phoenix.gif"/>
</div>
```

**출처**

- `inspect_runs.md` 번역 PR의 이미지 HTML 유지: https://github.com/huggingface/smolagents/pull/1747

### 협업 기록과 대량 번역 운영

여러 번역자가 동시에 움직일 때 범위, 상태, 리뷰 반영 여부를 공개적으로 남긴
사례다.

#### 리뷰 코멘트는 반영 여부를 댓글로 남김

여러 리뷰어가 번역 표현을 제안한 경우, 반영 완료 여부를 PR 코멘트로 남기면
리뷰 흐름이 명확해진다.

**권장**

> 리뷰 반영해서 수정해두었습니다. 여유 있을 때 확인해 주세요.

**출처**

- `rag.md` 리뷰 반영 댓글: https://github.com/huggingface/smolagents/pull/1646#issuecomment-3386216144
- `inspect_runs.md` 리뷰 반영 댓글: https://github.com/huggingface/smolagents/pull/1747#issuecomment-3402195894
- `web_browser.md` 리뷰 반영 댓글: https://github.com/huggingface/smolagents/pull/1748#issuecomment-3371819078

#### Transformers에서는 `(번역중)`이 항상 "누가 작업 중"이라는 뜻은 아님

Transformers 한국어 추적 이슈에서는 `_toctree.yml`의 `in_translation` 또는
`(번역중)` 표시가 실제로 누군가가 현재 작업 중이라는 뜻이 아니라, 아직 번역이
필요한 항목을 나타낼 수 있다고 설명했다. 따라서 새 번역을 시작할 때는 표시만
보고 포기하지 말고 추적 이슈, 스프레드시트, 최근 PR을 함께 확인한다.

**판단 기준**

- `_toctree.yml`에서 `local: in_translation`인 항목을 찾는다.
- 같은 파일을 번역하는 열린 PR이 있는지 확인한다.
- 추적 이슈나 팀 문서에서 작업 배정 상태를 확인한다.

**출처**

- maintainer가 `_toctree.yml`의 `in_translation` 항목을 보라고 안내한 댓글: https://github.com/huggingface/transformers/issues/20179#issuecomment-3109418241
- `(번역중)`이 현재 누군가 작업 중이라는 뜻은 아닐 수 있다는 maintainer 답변: https://github.com/huggingface/transformers/issues/20179#issuecomment-3109550710
- KREW 멤버가 번역 상태표와 기여 가이드를 안내한 댓글: https://github.com/huggingface/transformers/issues/20179#issuecomment-3112715480

#### 대량 번역은 진행률과 남은 파일 수를 공개적으로 공유

Transformers 한국어 번역은 추적 이슈에서 진행률과 남은 파일 수를 공유했다. 대량
번역에서는 어떤 파일이 완료되었고 무엇이 남았는지 공개적으로 공유해야 중복 PR과
리뷰 병목을 줄일 수 있다.

**권장**

```md
- 73% done
- 6 PRs pending review
- 15 files left to translate
```

**출처**

- Transformers 한국어 번역 진행률 공유 댓글: https://github.com/huggingface/transformers/issues/20179#issuecomment-1687183517
- `in_translation` 항목 확인 안내: https://github.com/huggingface/transformers/issues/20179#issuecomment-3109418241
- 번역 상태표와 팀 기여 가이드 안내: https://github.com/huggingface/transformers/issues/20179#issuecomment-3112715480

#### PR 템플릿은 번역자와 리뷰어의 역할을 분리

Transformers 한국어 번역 PR 본문에는 `Before reviewing`, `Who can review?
(Initial)`, `Who can review? (Final)` 같은 구역이 반복된다. 이는 한국어 리뷰와
maintainer 리뷰를 구분하고, 어떤 체크가 끝난 뒤 누구를 호출해야 하는지 명확하게
한다.

**권장**

```md
## Before reviewing
- [x] Check for missing / redundant translations (번역 누락/중복 검사)
- [x] Grammar Check (맞춤법 검사)
- [x] Review or Add new terms to glossary (용어 확인 및 추가)

## Who can review? (Initial)
May you please review this PR?

## Who can review? (Final)
@stevhliu May you please review this PR?
```

**출처**

- Transformers PR 템플릿 gist 안내 댓글: https://github.com/huggingface/transformers/issues/20179#issuecomment-1493219351
- `quicktour.md` PR의 PseudoLab/maintainer 리뷰 구분: https://github.com/huggingface/transformers/pull/24664
- `llm_tutorial_optimization.md` PR의 팀별 리뷰어 구분: https://github.com/huggingface/transformers/pull/32372
- `big_bird.md` PR의 KREW 리뷰와 final reviewer 구분: https://github.com/huggingface/transformers/pull/40445

#### 커밋 단계를 나누면 원문 복사, 초벌 번역, 수동 교정, 리뷰 반영이 보임

Transformers 한국어 추적 이슈에서는 번역 PR을 `docs: ko: <file-name>`,
`feat: [nmt|manual] draft`, `fix: manual edits`, `fix: resolve suggestions`처럼
나눠 진행하는 방식을 제안했다. 큰 문서는 diff를 단계별로 읽을 수 있어야 리뷰가
쉬워진다.

**권장 커밋 흐름**

```text
docs: ko: <file-name>
feat: [nmt|manual] draft
fix: manual edits
fix: resolve suggestions
```

**출처**

- 4단계 커밋 흐름 제안 댓글: https://github.com/huggingface/transformers/issues/20179#issuecomment-1528191933
- maintainer가 squash 후 주 커밋 메시지는 PR 제목이라고 답한 댓글: https://github.com/huggingface/transformers/issues/20179#issuecomment-1529697161
- `model_sharing.mdx` merge에서 배운 점을 바탕으로 제안했다는 맥락: https://github.com/huggingface/transformers/issues/20179#issuecomment-1528191933

#### LLM 초벌 번역은 가능하지만 사람의 교정 책임을 명시

Transformers 한국어 추적 이슈에는 ChatGPT로 초벌 번역을 빠르게 만드는 방법이
공유되었지만, 최종 품질은 입력 정확도와 proofreading에 달려 있다고 명시했다.
따라서 LLM 초벌 번역을 쓰더라도 PR에는 번역 누락, 용어, 문체, 코드 보존을 사람이
검토했다는 흔적이 남아야 한다.

**판단 기준**

- LLM이 코드 블록, 표, 앵커, 제품명을 바꾸지 않았는가?
- 번역자가 용어집과 맞춤법을 직접 확인했는가?
- 리뷰어가 자연스러운 한국어와 기술 의미를 다시 확인했는가?

**출처**

- ChatGPT를 초벌 번역에 사용하는 방법과 proofreading 필요성 안내: https://github.com/huggingface/transformers/issues/20179#issuecomment-1518928278
- `llm_tutorial_optimization.md` PR의 리뷰 전 체크리스트: https://github.com/huggingface/transformers/pull/32372
- `llm_tutorial_optimization.md`의 자연스러운 문장과 용어 통일 리뷰: https://github.com/huggingface/transformers/pull/32372#pullrequestreview-2218369929

### 품질 관리와 유지보수

번역 PR 안팎에서 원문 문제, 중복 문단, 공통 파일 충돌, docs build까지 확인한
사례다.

#### 번역 중 발견한 원문 문서 문제는 함께 고칠 수 있음

Transformers `quicktour.md` PR은 한국어 번역만 고친 것이 아니라 영어 원문의
불명확한 설명도 함께 수정했다. 예를 들어 document question answering 설명,
TensorFlow 입력 전달 설명, `Trainer`에 전달하는 항목 설명처럼 원문 자체가 어색한
부분을 정리했다. 이런 경우 PR 본문에 한국어와 영어 문서를 함께 수정했다고 밝히고,
maintainer가 원문 변경까지 확인할 수 있게 한다.

**판단 기준**

- 원문이 단순히 번역하기 어려운 것이 아니라 실제로 부정확하거나 불명확한가?
- 번역문만 조용히 고치면 원문과 한국어 문서가 의미상 달라지는가?
- 원문 변경이 작고 문서 개선 범위 안에 들어가는가?

**출처**

- `quicktour.md` PR 본문에서 한국어와 영어 문서 문제를 함께 수정했다고 밝힌 사례: https://github.com/huggingface/transformers/pull/24664
- 영어 `quicktour.md`의 document question answering 설명 수정 diff: https://github.com/huggingface/transformers/pull/24664
- maintainer가 영어 `quicktour` 변경도 괜찮다고 승인한 리뷰: https://github.com/huggingface/transformers/pull/24664#pullrequestreview-1540761743

#### 윤리와 안전 문서는 최신 원문과 동기화하고 위험 표현을 약화하지 않음

Diffusers `ethical_guidelines.md` 한국어 업데이트 PR은 최신 영어 원문에 맞춰
윤리 지침을 동기화하고, 위험, 책임, 안전 장치 설명을 더 명확하게 정리했다.
윤리, 안전, 라이선스, 제한 사항 같은 문서는 자연스러운 한국어보다 먼저 원문이
전달하는 위험 범위와 책임 강도가 보존되는지 확인해야 한다.

**점검**

- 최신 영어 원문과 문단 구성, 항목, 링크가 맞는가?
- 위험, 제한, 책임, 안전 장치의 강도가 약해지지 않았는가?
- "오래된 번역을 다듬는" PR이라도 최신 원문과 동기화했다고 PR 본문에 밝히는가?

**출처**

- Diffusers `ethical_guidelines.md` 한국어 업데이트 PR: https://github.com/huggingface/diffusers/pull/12435
- 최신 영어 버전과 동기화하고 clarity/consistency를 확인했다는 PR 본문: https://github.com/huggingface/diffusers/pull/12435
- maintainer 승인: https://github.com/huggingface/diffusers/pull/12435#pullrequestreview-3307433802
- doc-builder preview 코멘트: https://github.com/huggingface/diffusers/pull/12435#issuecomment-3374230924

#### deprecated 기능 안내는 번역 문서에서도 즉시 정리

영어 원문에서 더 이상 권장하지 않는 기능이 삭제되거나 대체되었는데 번역 문서가
예전 설치 방법을 계속 안내하면 사용자가 잘못된 환경 변수와 패키지를 따라 하게 된다.
Hugging Face Hub PR #3804에서는 한국어 문서에 남아 있던 `hf_transfer` 설치 안내와
`HF_HUB_ENABLE_HF_TRANSFER=1` 설정을 제거하고, `HF_XET_HIGH_PERFORMANCE`로
대체되는 deprecation 경고를 반영했다.

**점검**

- 원문에서 deprecated된 기능이 한국어 문서에 남아 있지 않은가?
- 환경 변수, CLI 출력, 안내 문구가 같은 방향으로 갱신되었는가?
- 한국어 reviewer가 wording을 확인했고 maintainer 승인 흐름이 남아 있는가?

**출처**

- Korean and German translated docs의 `hf_transfer` deprecation 반영 PR: https://github.com/huggingface/huggingface_hub/pull/3804
- `docs/source/ko/guides/upload.md`에서 `hf_transfer` 권장 안내를 deprecation 문구로 바꾼 diff: https://github.com/huggingface/huggingface_hub/pull/3804/files
- `docs/source/ko/package_reference/environment_variables.md`에서 `HF_HUB_ENABLE_HF_TRANSFER` 설명을 warning으로 바꾼 diff: https://github.com/huggingface/huggingface_hub/pull/3804/files
- maintainer가 CLI 출력에서는 항목을 남기지 말고 삭제하자고 제안한 리뷰: https://github.com/huggingface/huggingface_hub/pull/3804#discussion_r2812578449
- 한국어 reviewer가 문구를 확인한 댓글: https://github.com/huggingface/huggingface_hub/pull/3804#issuecomment-3908729002
- maintainer 최종 승인: https://github.com/huggingface/huggingface_hub/pull/3804#pullrequestreview-3832137703

#### 긴 기술 문서는 리뷰 요약에 변경 축을 남김

Transformers `llm_tutorial_optimization.md`처럼 긴 문서는 리뷰 코멘트가 많아지기
쉽다. 리뷰어가 어떤 축으로 검토했는지 PR 리뷰 요약에 남기면 번역자가 반영 범위를
파악하기 쉽고, maintainer도 한국어 리뷰가 단순 오탈자 검사를 넘어 기술 의미와
문장 품질을 봤다는 것을 확인할 수 있다.

**권장 리뷰 요약**

```md
- 반복되는 핵심 용어를 통일했습니다.
- 한국어 문장에 어색하게 남은 콜론을 마침표로 바꿨습니다.
- 긴 문장을 자연스러운 한국어 문장으로 다듬었습니다.
```

**출처**

- `llm_tutorial_optimization.md`의 용어 통일, 콜론 처리, 문장 수정 리뷰 요약: https://github.com/huggingface/transformers/pull/32372#pullrequestreview-2218369929
- 번역자가 여러 리뷰 제안을 반영하며 답변한 댓글들: https://github.com/huggingface/transformers/pull/32372#discussion_r1706491129
- maintainer 최종 승인: https://github.com/huggingface/transformers/pull/32372#pullrequestreview-2228379010

#### 원문과 번역문이 중복으로 남아 있으면 삭제 요청 대상

Transformers `main_classes/quantization.md` 리뷰에서는 이미 번역해 둔 문장 아래에
원문이 그대로 남아 있어 삭제 제안이 올라왔다. 초벌 번역 후에는 원문 문단이
남아 있지 않은지 반드시 확인한다.

**점검**

- 같은 의미의 영어 문단과 한국어 문단이 연속으로 남아 있지 않은가?
- 자동 번역 중 원문이 일부만 남지 않았는가?
- API명, 모델명처럼 유지해야 하는 영어와 삭제해야 하는 원문 문장을 구분했는가?

**출처**

- `quantization.md`의 원문 중복 문단 삭제 제안: https://github.com/huggingface/transformers/pull/33959#discussion_r1788631752
- `HfQuantizer` 관련 원문 중복 문장 삭제 제안: https://github.com/huggingface/transformers/pull/33959#discussion_r1788631765
- 변경 요청 후 maintainer 승인: https://github.com/huggingface/transformers/pull/33959#pullrequestreview-2355561199

#### 깨진 문자나 이상한 기호를 제거할 때는 의미 보존 여부를 확인

Transformers `bitsandbytes.md` 한국어 PR에서는 문장 안에 알 수 없는 깨진 문자가
섞여 maintainer가 이를 제거하면서 의미가 그대로인지 확인해 달라고 요청했다. 이런
문자는 단순 오탈자처럼 보여도 자동 번역, 인코딩, 복사 과정에서 생긴 손상일 수
있으므로, 삭제 후 원문 의미가 보존되는지 확인해야 한다.

**점검**

- `�`, 갑작스러운 `?`, 깨진 제어 문자처럼 원문에 없는 문자가 섞여 있지 않은가?
- 삭제하거나 고친 뒤 원문 기술 의미가 유지되는가?
- maintainer가 문자를 제거한 제안을 했다면 번역자가 의미 보존 여부를 확인했는가?

**출처**

- `bitsandbytes.md`에서 깨진 문자를 제거하며 의미 보존 확인을 요청한 리뷰: https://github.com/huggingface/transformers/pull/32408#discussion_r1706022011
- 같은 PR의 두 번째 깨진 문자 제거 리뷰: https://github.com/huggingface/transformers/pull/32408#discussion_r1706022382
- maintainer가 의미 변화 여부 확인을 요청한 리뷰 요약: https://github.com/huggingface/transformers/pull/32408#pullrequestreview-2222094237
- 번역자가 제안 반영을 확인한 댓글: https://github.com/huggingface/transformers/pull/32408#issuecomment-2275659548
- maintainer 최종 승인: https://github.com/huggingface/transformers/pull/32408#pullrequestreview-2228384985

#### 구조 변경 PR은 번역 정확도보다 원문 구조와의 동기화가 핵심

Transformers `_toctree.yml` 구조 개편 PR에서는 maintainer가 최신 원문 구조와
맞는지 확인을 요청했고, 영어 문서 구조 담당자가 구조가 맞는지 확인했다. 이런 PR은
문장 번역보다 `local`, 섹션 순서, `isExpanded`, 삭제된 항목이 원문 구조와
동기화되어 있는지가 핵심이다.

**점검**

- 영어 `_toctree.yml`의 최신 구조와 섹션 순서가 맞는가?
- 번역된 제목이 전체 문서 묶음에 영향을 주는지 확인했는가?
- 모든 제목을 한 PR에서 끝낼 수 없으면 후속 번역 계획을 남겼는가?

**출처**

- Transformers `_toctree.yml` 구조 개편 PR: https://github.com/huggingface/transformers/pull/23112
- maintainer가 최신 변경과 맞는지 확인 요청한 리뷰: https://github.com/huggingface/transformers/pull/23112#pullrequestreview-1410941234
- 구조는 맞지만 일부 제목은 후속 번역하겠다는 답변: https://github.com/huggingface/transformers/pull/23112#issuecomment-1533268610

#### 중복 TOC 문제는 진행 중인 PR 전체에 퍼질 수 있으므로 전용 PR로 정리

Transformers 번역 스프린트 중 `_toctree.yml`의 `Quantization Methods` 섹션이
중복된 문제가 여러 열린 PR에 퍼질 수 있다는 논의가 있었다. 대량 번역 중 공통 파일
문제가 발견되면, 모든 현재 PR에 개별 수정 요구를 하기보다 병합 흐름을 고려해 전용
정리 PR을 제안할 수 있다.

**권장 판단**

- 공통 파일 문제가 여러 PR에 이미 퍼졌는가?
- 개별 PR마다 수정하면 충돌이 늘어나는가?
- 현재 PR들이 병합된 뒤 한 번에 고치는 편이 안정적인가?

**출처**

- `_toctree.yml` 중복 섹션 문제와 해결 방식 문의: https://github.com/huggingface/transformers/issues/20179#issuecomment-2398880236
- 현재 PR들이 병합된 뒤 전용 PR로 제거하는 것이 쉽겠다는 maintainer 답변: https://github.com/huggingface/transformers/issues/20179#issuecomment-2401094002
- `quantization.md`가 `_toctree.yml`의 quantization 항목을 갱신한 실제 PR: https://github.com/huggingface/transformers/pull/33959

#### maintainer 리뷰는 번역 승인뿐 아니라 style, conflict, docs build를 포함

Transformers `trainer.md` PR에서는 maintainer가 번역에 감사하면서도 `make style`과
conflict 해결을 요청했다. `big_bird.md` PR에서는 `build-doc` 코멘트와
`Building docs for all languages...` 액션이 이어졌다. 번역 품질이 좋아도 저장소의
스타일, 충돌, 문서 빌드가 완료되어야 병합될 수 있다.

**완료 기준**

- 한국어 리뷰가 끝났다.
- maintainer가 요청한 `make style` 또는 conflict를 해결했다.
- doc-builder preview 또는 docs build 상태를 확인했다.

**출처**

- `trainer.md` maintainer의 `make style`과 conflict 해결 요청: https://github.com/huggingface/transformers/pull/32260#pullrequestreview-2226249977
- 번역자가 conflict 해결 후 재리뷰를 요청한 댓글: https://github.com/huggingface/transformers/pull/32260#issuecomment-2275045569
- `big_bird.md`의 `build-doc` 요청: https://github.com/huggingface/transformers/pull/40445#issuecomment-3391029005
- `big_bird.md`의 docs build 액션 댓글: https://github.com/huggingface/transformers/pull/40445#issuecomment-3391032540