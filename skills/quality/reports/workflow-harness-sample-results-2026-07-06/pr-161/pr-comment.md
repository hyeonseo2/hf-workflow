## Translation Quality Gate

- Status: reject
- Quality Score: 58.0
- Style Score: 60.0
- MQM Judge: off / 0 segments / 0 errors
- Hard failures: 0
- Style guide findings: 19

### Top Style Guide Findings

1. `translationese` / `minor` / segment `-`
   - Current: 를 가지
   - Suggested: Rewrite the sentence in natural Korean.
2. `modal_strength` / `major` / segment `p_016`
   - Current: 이것은 평가를 보고하거나 읽는 모든 사람에게 새로운 기능이며, 기존 EEE 기여자들만의 것이 아닙니다. 자사 모델을 보고하는 평가자와 타인의 모델을 보고하는 제3자 평가자 모두 커뮤니티 Evals와 EEE에 제출할 수 있으며, 허브를 둘러보는 누구나 전체 기록으로 연결되는 결과를 얻습니다. 조직의 공식 허깅페이스 계정을 통해 데이터를 제출하면, EvalEval에 verified 확인 표시가 표시되어 독자들에게 숫자가 출처에서 직접 왔음을 알리는 신호가 됩니다. 이 글의 나머지 부분은 허깅페이스 커뮤니티 Evals가 무엇인지와 변환기가 하는 일에 대해 설명합니다.
   - Suggested: Preserve the strength of `can` using: 수 있습니다.
3. `modal_strength` / `major` / segment `p_035`
   - Current: **아무 것도 당신의 서명 없이는 푸시되지 않습니다.** 도구는 로컬 YAML 프리뷰와 검토 파일을 작성하여 확인할 수 있게 하고, 준비된 것과 주의가 필요한 것을 보여주는 보고서를 출력합니다. 커밋 메시지를 입력하고 OPEN PRS를 입력한 후에만 PR을 엽니다. 컬렉션에 대해 캐시된 결과를 재실행하면 --force를 넘겨주지 않는 한 재사용됩니다.
   - Suggested: Preserve the strength of `can` using: 수 있습니다.
4. `alt_text_caption` / `minor` / segment `-`
   - Current: Verified Evaluators on Eval Cards
   - Suggested: Translate image alt text while preserving the image path.
5. `alt_text_caption` / `minor` / segment `-`
   - Current: EvalEval as source on SmolLM2 Model Page
   - Suggested: Translate image alt text while preserving the image path.
