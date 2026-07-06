## Translation Quality Gate

- Status: review_required
- Quality Score: 94.0
- Style Score: 83.0
- MQM Judge: off / 0 segments / 0 errors
- Hard failures: 0
- Style guide findings: 5

### Top Style Guide Findings

1. `translationese` / `minor` / segment `-`
   - Current: 에 의해
   - Suggested: Rewrite the sentence in natural Korean.
2. `modal_strength` / `major` / segment `p_014`
   - Current: 그 안정성은 특히 롱테일에서 중요합니다. 많은 시스템이 합리적인 중앙값 응답 시간을 제공할 수 있지만, 간헐적으로 발생하는 느린 응답은 대화를 여전히 불안정하게 만듭니다.
   - Suggested: Preserve the strength of `can` using: 수 있습니다.
3. `link_text_translation` / `minor` / segment `-`
   - Current: Hugging Face Space
   - Suggested: Translate link text while preserving the URL target.
4. `link_text_translation` / `minor` / segment `-`
   - Current: huggingface/speech-to-speech
   - Suggested: Translate link text while preserving the URL target.
5. `first_mention_bilingual` / `minor` / segment `-`
   - Current: 지연 시간
   - Suggested: Use `지연 시간(latency)` on first mention, then `지연 시간` afterward.
