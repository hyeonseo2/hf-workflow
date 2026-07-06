## Translation Quality Gate

- Status: reject
- Quality Score: 36.0
- Style Score: 60.0
- Hard failures: 1
- Style guide findings: 18

### Top Style Guide Findings

1. `list_consistency` / `minor` / segment `-`
   - Current: sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, sentence, phrase, sentence, phrase, sentence, phrase, phrase, phrase, sentence, sentence
   - Suggested: Use either sentence-style endings or phrase-style endings consistently within one list.
2. `modal_strength` / `major` / segment `p_003`
   - Current: 오랜 기간 동안 우리는 4~6주마다 릴리스를 발표했습니다. 이제는 단일 GitHub Actions 워크플로우에서 매주 릴리스를 발표합니다. 오픈 소스 도구와 오픈-가중치 모델을 사용해 이를 구축했고, 판단이 중요한 한 곳에 사람을 루프에 두었습니다. 이 글의 어떤 내용도 공급업체 계약, 비공개 모델, 또는 자신이 실행할 수 없는 인프라를 요구하지 않습니다. 이는 시작부터의 설계 목표였으며, 다른 유지 관리자가 가져다 사용하고 조정할 수 있는 워크플로우를 원했기 때문입니다.
   - Suggested: Preserve the strength of `can` using: 수 있습니다.
3. `modal_strength` / `major` / segment `l_009`
   - Current: 릴리스 후보가 고정된 상태로 다운스트림 라이브러리의 테스트 브랜치를 열고 테스트합니다.
   - Suggested: Preserve the strength of `can` using: 수 있습니다.
4. `modal_strength` / `major` / segment `p_020`
   - Current: 일부 단계는 순전히 기계적이며 자동화가 가능하다: 버전 증가, 커밋, 태깅, 푸시, 다운스트림 테스트 브랜치 열기, 포스트 릴리스 PR 열기. 이를 누가 생각할 필요가 없다. 항상 올바른 순서대로 일어나도록 해야 하며, 이것이 CI 워크플로우가 잘하는 일이다.
   - Suggested: Preserve the strength of `can` using: 수 있습니다.
5. `modal_strength` / `major` / segment `l_074`
   - Current: **Breakages가 더 일찍 드러난다.** RC 후보 기간 동안 다운스트림 테스트 브랜치가 통합 이슈를 빠르게 포착합니다.
   - Suggested: Preserve the strength of `can` using: 수 있습니다.
