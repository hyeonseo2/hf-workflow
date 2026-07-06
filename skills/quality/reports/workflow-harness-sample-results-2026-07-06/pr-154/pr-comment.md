## Translation Quality Gate

- Status: reject
- Quality Score: 0.0
- Style Score: 60.0
- Hard failures: 3
- Style guide findings: 76

### Top Style Guide Findings

1. `translationese` / `minor` / segment `-`
   - Current: 에 의해
   - Suggested: Rewrite the sentence in natural Korean.
2. `translationese` / `minor` / segment `-`
   - Current: 를 가지
   - Suggested: Rewrite the sentence in natural Korean.
3. `list_consistency` / `minor` / segment `-`
   - Current: sentence, phrase, sentence, sentence, sentence
   - Suggested: Use either sentence-style endings or phrase-style endings consistently within one list.
4. `modal_strength` / `major` / segment `p_010`
   - Current: 그러나 Xenova/whisper-tiny.en은(는) 인기 있는 모델이며(앞에서 언급했듯이 Transformer.js의 기본 ASR 모델이기도 합니다), 이를 사용하는 앱이 여러 개일 수 있음을 쉽게 상상할 수 있습니다. 이 상황을 시뮬레이션하기 위해, 이전의 동일한 예제 앱을 different origin에서 제공하는 것으로 가정합니다. 이 다른 원본(origin) 애플리케이션을 방문하면, 거의 즉시 사용할 수 있도록 하는 대신 브라우저는 모든 모델 리소스를 다시 다운로드하고 캐시해야 하므로 바이트 단위로 동일하더라도 중복 다운로드 및 저장이 발생합니다. 이 toy 예제에서도 이는 누적되어 177 MB의 중복 다운로드 및 저장으로 이어진다는 점을 Chrome DevTools의 Storage 섹션에서 확인할 수 있습니다 Application panel. 이를 상상해 보실 수 있습니다.
   - Suggested: Preserve the strength of `up to` using: 최대.
5. `modal_strength` / `major` / segment `p_023`
   - Current: 다양한 앱이 서로 다른 오리진에서 실행되더라도 결국 동일한 CDN URL에서 리소스를 제공한다면 캐싱 문제는 없을 것이라고 생각할 수 있습니다. 하지만 오랜 기간 브라우저에서의 캐싱 방식은 그렇지 않습니다. 기사 Gaining security and privacy by partitioning the cache가 모든 세부 정보를 다룹니다. 본질적으로, 캐시가 오리진별로 분리되어 있어 타이밍 공격을 방지합니다: 웹사이트가 HTTP 요청에 응답하는 데 걸리는 시간은 브라우저가 과거에 같은 리소스에 접근했다는 것을 암시할 수 있어 보안 및 개인정보 유출 취약점을 만들 수 있습니다.
   - Suggested: Preserve the strength of `should` using: 좋습니다, 해야 합니다.
