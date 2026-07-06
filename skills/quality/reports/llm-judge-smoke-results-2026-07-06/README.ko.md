# LLM Judge Smoke Results

이 폴더는 OpenAI 기반 MQM judge가 실제로 켜진 상태에서 생성한 검증 하네스 예시 산출물입니다.

기존 `workflow-harness-sample-results-2026-07-06` 샘플은 비용과 재현성을 위해 `llm_judge.provider=off`로 생성했습니다. 이 폴더는 그와 별도로 `--llm-judge-provider openai`를 켜면 어떤 리포트가 나오는지 보여주기 위한 작은 smoke sample입니다.

## 샘플

| 경로 | 설명 |
| --- | --- |
| `modal-strength/source.md` | 의도적으로 `may`, `up to`, `must`가 들어간 원문 |
| `modal-strength/target.md` | 가능성/최대치/필수 강도를 일부러 바꾼 한국어 번역문 |
| `modal-strength/quality-report.md` | 사람이 읽는 상세 리포트 |
| `modal-strength/quality-report.json` | CI/대시보드용 구조화 리포트 |
| `modal-strength/pr-comment.md` | PR 댓글용 요약 |
| `modal-strength/mqm-judge.jsonl` | 실제 OpenAI MQM judge가 반환한 세그먼트별 판정 |
| `modal-strength/source-segments.jsonl` | 원문 세그먼트 분해 결과 |
| `modal-strength/target-segments.jsonl` | 번역문 세그먼트 분해 결과 |
| `modal-strength/metric-cache.json` | 반복 실행용 metric/MQM 캐시 |

## 실행 요약

- Provider: `openai`
- Model: `gpt-5-nano`
- Status: `review_required`
- Quality score: `81.0`
- Evaluated MQM segments: `3`
- MQM errors: `2`
- MQM severity counts: `{'major': 2}`
- Prompt hash: `10923aaf9e56e0a8e9503592b287e1d477372d1167530621d8206c31498292b6`
- Style guide hash: `937d8cd893578d30e716a3eb513cdf5f10d6fd3ad8f5e77068b57f96e160de12`

LLM judge가 잡은 핵심 오류는 번역 가이드 4번, `의미·조건·확신의 강도는 절대 바꾸지 않습니다` 위반입니다.

- `may improve ... up to 30%`가 `30% 개선합니다`로 단정됨
- `You must set ...`가 `설정하는 것이 좋습니다`로 약화됨

같은 입력에서 deterministic style guide 검사도 `modal_strength`, `overstatement`, `first_mention_bilingual` 이슈를 함께 잡습니다.

## 재실행 예시

```bash
OPENAI_API_KEY=... PYTHONPATH=skills/quality python3 skills/quality/tools/translation_quality_harness.py \
  --manifest skills/quality/reports/llm-judge-smoke-results-2026-07-06/modal-strength/manifest.yaml \
  --target-root skills/quality/reports/llm-judge-smoke-results-2026-07-06/modal-strength \
  --source skills/quality/reports/llm-judge-smoke-results-2026-07-06/modal-strength/source.md \
  --target skills/quality/reports/llm-judge-smoke-results-2026-07-06/modal-strength/target.md \
  --output-json skills/quality/reports/llm-judge-smoke-results-2026-07-06/modal-strength/quality-report.json \
  --output-md skills/quality/reports/llm-judge-smoke-results-2026-07-06/modal-strength/quality-report.md \
  --output-pr-comment skills/quality/reports/llm-judge-smoke-results-2026-07-06/modal-strength/pr-comment.md \
  --output-source-segments skills/quality/reports/llm-judge-smoke-results-2026-07-06/modal-strength/source-segments.jsonl \
  --output-target-segments skills/quality/reports/llm-judge-smoke-results-2026-07-06/modal-strength/target-segments.jsonl \
  --output-mqm-judge-jsonl skills/quality/reports/llm-judge-smoke-results-2026-07-06/modal-strength/mqm-judge.jsonl \
  --metric-cache skills/quality/reports/llm-judge-smoke-results-2026-07-06/modal-strength/metric-cache.json \
  --llm-judge-provider openai \
  --llm-judge-model gpt-5-nano \
  --llm-judge-max-segments 3
```

이 샘플은 운영 번역 PR이 아니라, LLM judge와 스타일 가이드 연결이 실제 리포트에 어떻게 나타나는지 확인하기 위한 의도적 smoke input입니다.
