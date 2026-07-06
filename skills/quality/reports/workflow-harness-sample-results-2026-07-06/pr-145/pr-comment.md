## Translation Quality Gate

- Status: reject
- Quality Score: 0.0
- Style Score: 60.0
- MQM Judge: off / 0 segments / 0 errors
- Hard failures: 0
- Style guide findings: 57

### Top Style Guide Findings

1. `translationese` / `minor` / segment `-`
   - Current: 에 의해
   - Suggested: Rewrite the sentence in natural Korean.
2. `list_consistency` / `minor` / segment `-`
   - Current: phrase, sentence, sentence, sentence, phrase, sentence
   - Suggested: Use either sentence-style endings or phrase-style endings consistently within one list.
3. `modal_strength` / `major` / segment `h_001`
   - Current: Beyond LoRA: 가장 인기 있는 미세조정 기법을 이길 수 있을까?
   - Suggested: Preserve the strength of `can` using: 수 있습니다.
4. `modal_strength` / `major` / segment `p_004`
   - Current: 오픈 모델을 자신의 데이터로 미세조정하고자 한다면, 아마도 소위 매개변수 효율적 미세조정, 간단히 *PEFT*에 관심이 있을 것입니다. 이 용어는 모델을 미세조정하는 데 필요한 메모리 요구량을 크게 줄여주는 기술들을 설명합니다. 이러한 기법은 수십 가지가 있지만, 거의 모두 "LoRA"라는 것을 선택합니다. 이 블로그 글에서 LoRA가 정말 최선의 선택인지, 정보에 기반한 의사결정을 내리기 위해 어떤 도구들이 있는지, 그리고 LoRA를 넘어 시야를 넓힘으로써 어떻게 이익을 얻을 수 있는지 살펴봅니다.
   - Suggested: Preserve the strength of `can` using: 수 있습니다.
5. `modal_strength` / `major` / segment `p_006`
   - Current: 수많은 오픈 모델이 있지만, 그것들이 자주 당신의 사용 사례에 충분하지는 않습니다. 프롬프트 엔지니어링이 도움이 될 수는 있지만 보통은 충분하지 않습니다. 처음부터 새 모델을 학습시키기보다는 기존 모델을 미세조정하는 것을 고려해야 합니다.
   - Suggested: Preserve the strength of `may` using: 수 있습니다, 일 수 있습니다.
