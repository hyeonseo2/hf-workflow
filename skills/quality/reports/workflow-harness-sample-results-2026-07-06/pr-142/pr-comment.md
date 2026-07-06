## Translation Quality Gate

- Status: reject
- Quality Score: 39.0
- Style Score: 60.0
- Hard failures: 2
- Style guide findings: 11

### Top Style Guide Findings

1. `translationese` / `minor` / segment `-`
   - Current: 에 의해
   - Suggested: Rewrite the sentence in natural Korean.
2. `modal_strength` / `major` / segment `p_003`
   - Current: OpenEnv는 터미널, 브라우저 또는 에이전트가 상호작용할 수 있는 그 밖의 실행 환경처럼 에이전트형 실행 환경을 만드는 도구입니다. 그리고 오늘, OpenEnv가 더 개방적으로 바뀌어 에이전트를 학습하는 미래를 오픈 소스로 만들게 되었음을 발표하게 되어 기쁩니다.
   - Suggested: Preserve the strength of `can` using: 수 있습니다.
3. `modal_strength` / `major` / segment `p_010`
   - Current: 프런티어 연구소들은 모델과 하네스가 대체로 손발이 맞게 함께 작동하도록 학습합니다. 모델은 하네스를 사용하도록 학습되며 그 특성에 맞게 최적화됩니다. 모델은 이 하네스들 너머로 다소 일반화될 수 있지만, 학습의 효율성을 능가하는 것은 아무것도 없습니다.
   - Suggested: Preserve the strength of `can` using: 수 있습니다.
4. `modal_strength` / `major` / segment `p_016`
   - Current: 최근 릴리스에서 OpenEnv는 **RL 환경 간 상호 운용성 계층**이 되었습니다. 그것의 역할은 환경이 게시되고 배포되며 에이전트에 의해 소비되는 방식을 표준화하는 것입니다. 보상 정의나 학습 루프가 어떻게 작동하는지를 지시하지는 않습니다. 보상 정의, 채점 기준, 트레이너별 로직은 이에 특화된 라이브러리에 속합니다. OpenEnv는 모두가 연결할 수 있는 공통 소켓입니다.
   - Suggested: Preserve the strength of `can` using: 수 있습니다.
5. `modal_strength` / `major` / segment `p_019`
   - Current: 익숙한 프로토콜과 표준 패키징. 환경은 HTTP와 WebSocket 같은 표준 프로토콜로 서비스되며 Docker로 패키징됩니다. MCP는 1급 시민으로서, OpenEnv 환경은 MCP 서버와 즉시 호환되며 동일한 환경이 시뮬레이션(훈련/평가)과 생산 모드에서 일관되게 동작합니다.
   - Suggested: Preserve the strength of `can` using: 수 있습니다.
