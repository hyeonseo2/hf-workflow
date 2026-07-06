## Translation Quality Gate

- Status: review_required
- Quality Score: 81.0
- Style Score: 60.0
- MQM Judge: openai / 3 segments / 2 errors
- Hard failures: 0
- Style guide findings: 5

### Top Style Guide Findings

1. `modal_strength` / `major` / segment `p_002`
   - Current: 이 접근법은 처리량을 30% 개선합니다. 스크립트를 실행하기 전에 HF_TOKEN 환경 변수를 설정하는 것이 좋습니다.
   - Suggested: Preserve the strength of `may` using: 수 있습니다, 일 수 있습니다.
2. `modal_strength` / `major` / segment `p_002`
   - Current: 이 접근법은 처리량을 30% 개선합니다. 스크립트를 실행하기 전에 HF_TOKEN 환경 변수를 설정하는 것이 좋습니다.
   - Suggested: Preserve the strength of `must` using: 반드시, 해야 합니다.
3. `modal_strength` / `major` / segment `p_002`
   - Current: 이 접근법은 처리량을 30% 개선합니다. 스크립트를 실행하기 전에 HF_TOKEN 환경 변수를 설정하는 것이 좋습니다.
   - Suggested: Preserve the strength of `up to` using: 최대.
4. `overstatement` / `major` / segment `p_002`
   - Current: 개선합니다
   - Suggested: Use a weaker expression that preserves the source claim strength.
5. `first_mention_bilingual` / `minor` / segment `-`
   - Current: 처리량
   - Suggested: Use `처리량(throughput)` on first mention, then `처리량` afterward.
