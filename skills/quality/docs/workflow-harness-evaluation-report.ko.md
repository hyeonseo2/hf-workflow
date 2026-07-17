# 번역 검증 하네스 실행 결과 보고서

작성일: 2026-07-06

## 파이프라인 산출물

`translation_quality_harness.py`를 번역된 글에 실행하면 다음 파일이 생성된다.

| 산출물 | 내용 | 주 사용 대상 |
| --- | --- | --- |
| `quality-report.md` | 사람이 읽는 상세 검토 리포트. 판정 상태, 총점, 영역별 점수, metric 요약, MQM judge 요약, 스타일 가이드 점검 결과, 전체 이슈가 들어간다. | 번역자, 리뷰어, PR 검토자 |
| `quality-report.json` | `schemas/quality_report.schema.json`에 맞춘 구조화 리포트. `metrics`, `mqm_judge`, `style_guide`, `issues`를 분리해 담는다. | CI gate, 대시보드, 후속 자동화 |
| `pr-comment.md` | PR 댓글로 붙일 짧은 요약. 상태, 품질 점수, 스타일 점수, MQM judge 요약, hard failure 수, 주요 스타일 이슈를 담는다. | GitHub PR 댓글 봇 |
| `source-segments.jsonl` | 원문을 세그먼트 단위로 나눈 결과. id, hash, 종류, 위치 정보가 포함된다. | 디버깅, 감사, 회귀 추적 |
| `target-segments.jsonl` | 번역문을 세그먼트 단위로 나눈 결과. | 디버깅, 감사, 회귀 추적 |
| `mqm-judge.jsonl` | 선택 산출물. LLM/fixture MQM judge가 평가한 세그먼트별 점수와 오류 목록이다. | LLM 판정 감사, 디버깅 |
| `metric-cache.json` | 세그먼트 hash 기준 metric/MQM judge 캐시. | 반복 실행, CI 비용 절감 |

최종 판정은 네 가지 중 하나다.

- `auto_pass`: hard failure가 없고, 주요 리뷰 차단 사유도 없으며, 점수가 높다.
- `review_required`: 바로 병합하지 않고 사람이 확인해야 한다. 보통 스타일, 용어, metric 신뢰도 이슈가 여기에 해당한다.
- `reject`: 게시 안전성이나 기술 정확성에 문제가 있거나, 점수가 기준보다 낮다.
- `source_changed`: manifest에 기록된 원문 hash와 현재 원문 hash가 다르다.

## 현재 워크플로우에 맞춰 보정한 내용

현재 자동 번역 workflow의 산출물은 로컬 원문 파일 경로인 `source.file_path`를 포함하지 않는 경우가 많다. 대부분 `source.url`만 들어 있었다. 그래서 하네스를 현재 산출물 구조에 맞게 다음처럼 보정했다.

- `--source`와 `source.file_path`가 없으면 `source.url`에서 원문을 자동으로 가져온다.
- Hugging Face Blog URL이면 `huggingface/blog`의 public raw Markdown을 먼저 찾는다.
- raw Markdown을 찾지 못하면 렌더링된 HTML에서 본문 텍스트를 추출한다.
- 원문 확보 방식은 `metadata.source_format`에 `url_markdown` 또는 `url_html_text`로 남긴다.
- HTML 텍스트만 확보된 경우에는 Markdown 구조 비교가 과하게 실패할 수 있으므로 structural hard gate를 건너뛴다.
- 현재 workflow가 번역문에 자동으로 붙이는 게시용 scaffolding은 비교 전에 제외한다. 제외 대상은 `> Source:`, 자동 TOC, 한국어 번역 안내문, 리뷰 안내 주석, `{#section-1}` 같은 heading anchor다.
- 일반 약어, 도메인, `e.g`, K/M/B/T 단위 현지화, 일반적인 slash 표현, Markdown 링크 URL, inline code 중복, HTML style 속성이 protected token으로 과검출되지 않도록 정규식을 줄였다.
- 본문 숫자, bare URL, model ID, Python/API identifier처럼 유용하지만 과검출 여지가 큰 항목은 deterministic hard failure가 아니라 review gate로 낮췄다.

변경 후 단위 테스트 결과는 다음과 같다.

```text
PYTHONPATH=skills/quality python3 -m pytest -q skills/quality/tests
32 passed
```

## 실제 샘플 실행 결과

현재 번역 PR 산출물 14개에 하네스를 실행했다. 6개는 `reports/pr-*`에 있던 실제 workflow manifest를 사용했고, 나머지 8개는 target front matter에서 임시 manifest를 만들어 같은 경로로 돌렸다. 이 샘플은 비용과 재현성을 위해 LLM MQM judge provider를 기본값인 `off`로 두고 실행했다.

| PR | Manifest | Slug | Status | Score | Hard | Issues | Style | Source |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| #137 | workflow manifest | `paddleocr-transformers` | `review_required` | 63.0 | 0 | 12 | 60.0 | `url_html_text` |
| #138 | workflow manifest | `olmoearth-v1-1` | `review_required` | 66.0 | 0 | 10 | 60.0 | `url_html_text` |
| #141 | workflow manifest | `torch-profiler` | `reject` | 0.0 | 3 | 110 | 60.0 | `url_markdown` |
| #142 | workflow manifest | `openenv-agentic-rl` | `reject` | 39.0 | 2 | 17 | 60.0 | `url_markdown` |
| #143 | workflow manifest | `github-ci-hf-jobs` | `reject` | 49.0 | 0 | 24 | 60.0 | `url_markdown` |
| #144 | workflow manifest | `agentic-resource-discovery-launch` | `reject` | 64.0 | 1 | 14 | 60.0 | `url_markdown` |
| #145 | frontmatter manifest | `peft-beyond-lora` | `reject` | 0.0 | 0 | 71 | 60.0 | `url_markdown` |
| #146 | frontmatter manifest | `is-it-agentic-enough` | `reject` | 0.0 | 0 | 78 | 60.0 | `url_markdown` |
| #153 | frontmatter manifest | `huggingface-hub-release-ci` | `reject` | 36.0 | 1 | 25 | 60.0 | `url_markdown` |
| #154 | frontmatter manifest | `cross-origin-storage` | `reject` | 0.0 | 3 | 93 | 60.0 | `url_markdown` |
| #155 | frontmatter manifest | `ffasr-leaderboard` | `reject` | 47.0 | 0 | 24 | 60.0 | `url_markdown` |
| #156 | frontmatter manifest | `vllm-jobs` | `review_required` | 66.0 | 0 | 16 | 60.0 | `url_markdown` |
| #161 | frontmatter manifest | `eee-community-evals` | `reject` | 58.0 | 0 | 24 | 60.0 | `url_markdown` |
| #163 | frontmatter manifest | `cerebras-gemma4-voice-ai` | `review_required` | 94.0 | 0 | 5 | 83.0 | `url_markdown` |

요약하면 다음과 같다.

- `review_required`: 4건
- `reject`: 10건
- `url_markdown` 원문 사용: 12건
- `url_html_text` 원문 사용: 2건

자주 나온 hard failure는 다음과 같다.

| Hard Failure | Count | 해석 |
| --- | ---: | --- |
| `link target mismatch` | 3 | Markdown 링크 목적지가 원문과 다르다. |
| `inline code mismatch` | 3 | inline code token이 바뀌었거나 사라졌다. |
| `thumbnail` front matter mismatch | 2 | 원문 thumbnail metadata와 target metadata가 다르다. |
| `Markdown table shape mismatch` | 1 | 표의 행 또는 열 구조가 다르다. |
| `code block hash mismatch` | 1 | fenced code block이 바뀌었다. |

스타일 가이드 쪽에서는 다음 규칙이 많이 잡혔다.

| Rule | Count |
| --- | ---: |
| `link_text_translation` | 157 |
| `modal_strength` | 124 |
| `alt_text_caption` | 37 |
| `information_addition` | 20 |
| `first_mention_bilingual` | 12 |
| `translationese` | 10 |
| `list_consistency` | 8 |
| `intro_closing_style` | 1 |

## 판단

하네스는 이제 현재 workflow 산출물에 바로 붙일 수 있다. 로컬 원문 Markdown이 없어도 `source.url`을 보고 원문을 확보한다. `huggingface/blog`에 raw Markdown이 있는 공식 글은 구조 비교까지 수행할 수 있고, raw Markdown이 없는 organization/community 글은 HTML 본문 텍스트로 후퇴한다. 이 경우에는 Markdown 구조 비교를 일부 건너뛰어 불필요한 실패를 줄인다.

이번 샘플 기준으로는 현재 번역 결과를 자동 병합하기 어렵다. code block 변경, inline code 누락, 링크 변경, 오래된 front matter가 실제로 잡혔다. 숫자, bare URL, model ID, API identifier 차이는 계속 리포트에 남기되, 실제 샘플에서 정상적인 현지화와 포맷 차이가 많이 섞였기 때문에 hard failure가 아니라 review gate로 낮췄다.

워크플로우 자체에도 보완할 점이 있다. 현재 manifest는 `source.hash`나 원문 snapshot을 고정하지 않는다. 그래서 upstream 블로그 글이 번역 뒤에 수정되면, 하네스는 차이를 감지할 수는 있지만 그 차이가 번역 오류인지 원문 변경 때문인지 항상 구분하지 못한다. 다음 단계에서는 원문 hash와 원문 snapshot artifact를 함께 저장하는 편이 좋다.

## 남은 작업

- `.github/workflows/daily-translation.yml`에 `translation_quality_harness.py`를 연결한다. 기존 `run_local_review.py` 뒤에 붙이거나, `simple_quality_report.py` 경로를 새 하네스로 교체하면 된다.
- PR별로 전체 하네스 산출물을 artifact로 올린다. 대상은 Markdown 리포트, JSON 리포트, PR 댓글 요약, segment JSONL, metric cache다.
- translation-flow manifest에 `source.hash`와 원문 snapshot 저장을 추가한다.
- `reject`가 나오면 workflow 자체를 실패시킬지, 아니면 PR 자동 병합만 막을지 결정한다.
- OpenAI MQM judge를 실제 운영에서 기본으로 켤지, 고위험 PR/세그먼트에만 제한적으로 켤지 결정하고 threshold를 보정한다.
- 리뷰어 피드백을 보고 스타일 threshold를 조정한다. 특히 `modal_strength`와 `link_text_translation`은 의도적으로 넓게 잡은 review gate라 보정 여지가 있다.
- `pr-comment.md`를 실제 PR 댓글로 게시하는 단계를 추가한다.
