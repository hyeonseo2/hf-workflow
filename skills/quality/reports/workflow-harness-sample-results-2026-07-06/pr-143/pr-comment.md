## Translation Quality Gate

- Status: reject
- Quality Score: 49.0
- Style Score: 60.0
- MQM Judge: off / 0 segments / 0 errors
- Hard failures: 0
- Style guide findings: 20

### Top Style Guide Findings

1. `list_consistency` / `minor` / segment `-`
   - Current: phrase, phrase, phrase, phrase, sentence, sentence, sentence, sentence, sentence
   - Suggested: Use either sentence-style endings or phrase-style endings consistently within one list.
2. `modal_strength` / `major` / segment `p_003`
   - Current: 그 기본 설정은 편리하지만 한계도 있습니다. GitHub Actions는 느려지거나 유지 보수로 다운될 수 있고, 호스팅 머신은 일반적이며, GPU 접근은 대부분의 오픈 소스 프로젝트에서 바로 활성화하기 어렵습니다. Trackio의 경우 이러한 한계가 점점 문제로 다가왔습니다. 기본 단위 테스트와 프런트엔드 확인을 위한 안정적인 CPU CI는 물론 실제 CUDA 하드웨어에서 실행해야 하는 테스트를 위한 GPU CI도 원했습니다.
   - Suggested: Preserve the strength of `can` using: 수 있습니다.
3. `modal_strength` / `major` / segment `p_006`
   - Current: 이 글에서는 GitHub 저장소에 대해 동일한 설정을 단계별로 재현하는 방법을 설명합니다. 에이전트를 사용 중이라면 이 글을 참고하실 수 있는데, 인간용으로 브라우저 기반 지침과 함께 CLI 지침이 함께 제공되기 때문입니다.
   - Suggested: Preserve the strength of `can` using: 수 있습니다.
4. `modal_strength` / `major` / segment `p_029`
   - Current: 이 Space를 먼저 만드는 이유는 GitHub App에 웹훅 URL이 필요하고 그 URL이 Space에서 나오기 때문입니다. 이 Space는 당신의 고유 네임스페이스 아래에 있거나 쓰기 권한이 있는 허깅페이스 org 아래에 있어야 합니다.
   - Suggested: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
5. `modal_strength` / `major` / segment `p_035`
   - Current: 빌드가 완료되면 복제된 Space를 엽니다. 현재는 무시해도 되는 "Required Space secrets" 섹션이 보일 것입니다. 다음 단계에서 필요한 GitHub App 웹훅 URL이 랜딩 페이지에 표시되어야 하며, 아래와 같은 형태일 것입니다:
   - Suggested: Preserve the strength of `can` using: 수 있습니다.
