## Translation Quality Gate

- Status: review_required
- Quality Score: 66.0
- Style Score: 60.0
- MQM Judge: off / 0 segments / 0 errors
- Hard failures: 0
- Style guide findings: 13

### Top Style Guide Findings

1. `intro_closing_style` / `minor` / segment `p_048`
   - Current: 이 포스트
   - Suggested: Rewrite the intro or closing in natural Korean blog style.
2. `modal_strength` / `major` / segment `p_016`
   - Current: 일반적인 OpenAI 스타일의 JSON을 반환하며, choices[0].message.content에 "Hello! How can I assist you today? 😊"이 들어 있습니다.
   - Suggested: Preserve the strength of `can` using: 수 있습니다.
3. `modal_strength` / `major` / segment `p_018`
   - Current: 시작하기 전 빠른 상태 점검: curl https://<job_id>--8000.hf.jobs/v1/models -H "Authorization: Bearer $(hf auth token)"에 모델이 나열되어 있어야 합니다.
   - Suggested: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
4. `modal_strength` / `major` / segment `b_020`
   - Current: **🔐 엔드포인트는 게이트되어 공개되지 않습니다.** 모든 요청은 작업의 네임스페이스에 대한 읽기 권한이 있는 허깅페이스 토큰이 필요합니다. 일반 브라우저 방문은 거부됩니다. 사실상 작업 프록시는 API 게이트 역할을 하며, 접근은 귀하(및 귀하의 조직)에게 한정됩니다. 개인 사용에는 괜찮지만 URL을 다룰 때는 공개로 여길 것을 기대하지 말고 토큰을 신뢰할 수 없는 곳에 붙여넣지 마십시오. 더 세밀하거나 공개 접근이 필요하면 대신 적절한 게이트웨이를 앞에 두십시오. 아래의 HF Jobs or Inference Endpoints?를 참조하십시오.
   - Suggested: Preserve the strength of `must` using: 반드시, 해야 합니다.
5. `modal_strength` / `major` / segment `p_023`
   - Current: 설정한 --timeout은 안전망이며(자동 중지 기능이 있습니다). 그러나 명시적으로 취소하는 것이 더 저렴합니다. a10g-large은 시간당 $1.50에 실행되며 전체 가격표는 hf jobs hardware에서 확인하고 모델에 맞는 가장 작은 플래버를 선택하세요.
   - Suggested: Preserve the strength of `can` using: 수 있습니다.
