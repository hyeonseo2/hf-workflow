# 번역 검증 하네스 샘플 산출물

생성일: 2026-07-06

이 폴더는 Hugging Face Blog 한국어 번역 검증 하네스를 실제 번역 PR 산출물에 실행한 결과를 모아둔 공유용 묶음이다.

이 디렉터리에는 검증 결과 요약만 버전 관리한다. PR별 JSON, Markdown,
segment JSONL, metric cache는 저장소 크기와 코드 리뷰 노이즈를 줄이기 위해
커밋하지 않고 CI artifact로 보관한다.

## 폴더 구조

원본 CI artifact의 각 PR 폴더에는 가능한 경우 다음 파일이 들어 있다.

| 파일 | 내용 |
| --- | --- |
| `quality-report.md` | 사람이 읽는 상세 검토 리포트. status, 총점, 영역별 점수, metric 요약, 스타일 가이드 이슈, 전체 이슈 목록을 포함한다. |
| `quality-report.json` | CI나 대시보드에서 읽을 수 있는 구조화 리포트. |
| `pr-comment.md` | GitHub PR 댓글로 붙일 수 있는 짧은 요약. |
| `source-segments.jsonl` | 원문 세그먼트 분해 결과. |
| `target-segments.jsonl` | 번역문 세그먼트 분해 결과. |
| `mqm-judge.jsonl` | LLM/fixture MQM judge를 켰을 때 생성되는 세그먼트별 판정 결과. |
| `metric-cache.json` | 반복 실행용 metric 캐시. |

이 폴더의 14개 PR 샘플은 비용과 재현성을 위해 LLM judge를 끈 상태(`provider=off`)로 생성됐다. 실제 OpenAI MQM judge가 켜진 산출물 예시는 `skills/quality/reports/llm-judge-smoke-results-2026-07-06/`에 따로 추가했다.

`pr-137`, `pr-138`은 원문을 raw Markdown으로 찾지 못해 HTML 텍스트 fallback으로 실행됐다. 이 경우 structural segment metric을 건너뛰기 때문에 `metric-cache.json`이 생성되지 않았다.

## 포함된 샘플

| PR | Slug | Status | Score | Hard Failures | Source |
| --- | --- | --- | ---: | ---: | --- |
| `pr-137` | `paddleocr-transformers` | `review_required` | 63.0 | 0 | `url_html_text` |
| `pr-138` | `olmoearth-v1-1` | `review_required` | 66.0 | 0 | `url_html_text` |
| `pr-141` | `torch-profiler` | `reject` | 0.0 | 3 | `url_markdown` |
| `pr-142` | `openenv-agentic-rl` | `reject` | 39.0 | 2 | `url_markdown` |
| `pr-143` | `github-ci-hf-jobs` | `reject` | 49.0 | 0 | `url_markdown` |
| `pr-144` | `agentic-resource-discovery-launch` | `reject` | 64.0 | 1 | `url_markdown` |
| `pr-145` | `peft-beyond-lora` | `reject` | 0.0 | 0 | `url_markdown` |
| `pr-146` | `is-it-agentic-enough` | `reject` | 0.0 | 0 | `url_markdown` |
| `pr-153` | `huggingface-hub-release-ci` | `reject` | 36.0 | 1 | `url_markdown` |
| `pr-154` | `cross-origin-storage` | `reject` | 0.0 | 3 | `url_markdown` |
| `pr-155` | `ffasr-leaderboard` | `reject` | 47.0 | 0 | `url_markdown` |
| `pr-156` | `vllm-jobs` | `review_required` | 66.0 | 0 | `url_markdown` |
| `pr-161` | `eee-community-evals` | `reject` | 58.0 | 0 | `url_markdown` |
| `pr-163` | `cerebras-gemma4-voice-ai` | `review_required` | 94.0 | 0 | `url_markdown` |

## 보는 순서

1. 먼저 각 PR 폴더의 `quality-report.md`를 본다.
2. 자동화 연동이나 대시보드 확인이 필요하면 `quality-report.json`을 본다.
3. 실제 PR 댓글에 어떤 내용이 올라갈지 보려면 `pr-comment.md`를 본다.
4. 특정 문단 정렬이나 누락 여부를 확인하려면 `source-segments.jsonl`, `target-segments.jsonl`을 비교한다.

전체 실행 결과 해석은 `skills/quality/docs/workflow-harness-evaluation-report.ko.md`에 정리되어 있다.
