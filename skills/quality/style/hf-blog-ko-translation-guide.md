

# 1. 상위 번역 철학: 원문 voice는 살리고 한국어 문장은 다시 씁니다

기술 블로그는 작성자의 태도와 글의 온도가 중요합니다. 원문이 활기차면 한국어도 약간 활기 있게, 원문이 연구 논문 소개처럼 차분하면 한국어도 차분하게 옮깁니다. 다만 영어식 표현을 그대로 흉내 내면 어색합니다.

| 원문                                                     | 비권장                                      | 권장                                      |
| ------------------------------------------------------ | ---------------------------------------- | --------------------------------------- |
| Let’s dive in!                                         | 뛰어들어 봅시다!                                | 이제 자세히 살펴보겠습니다.                         |
| Let’s dive in!                                         | 들어가 볼까요!                                 | 이제 하나씩 살펴볼게요.                           |
| We’re excited to release our new model.                | 저희는 새 모델을 출시하게 되어 흥분됩니다.                 | 새 모델을 공개하게 되어 기쁩니다.                     |
| In this post, we explore how TGI improves LLM serving. | 이 포스트에서 우리는 TGI가 LLM 서빙을 개선하는 방법을 탐험합니다. | 이번 글에서는 TGI가 LLM 서빙을 어떻게 개선하는지 살펴보겠습니다. |
| Today, we’re taking a closer look at quantization.     | 오늘 우리는 양자화를 더 가까이 살펴봅니다.                 | 이번 글에서는 양자화를 조금 더 자세히 살펴보겠습니다.          |


블로그에서는 `we`, `you`, `let’s`를 기계적으로 옮기지 않는 것이 중요합니다.

|영어 표현|기계적 번역|블로그식 권장|
|---|---|---|
|we’ll show you|우리는 여러분에게 보여줄 것입니다|이 글에서는 설명합니다|
|you can use|당신은 사용할 수 있습니다|사용할 수 있습니다|
|let’s build|만들어 봅시다|직접 만들어 보겠습니다|
|we found that|우리는 발견했습니다|확인한 결과 / 실험 결과|
|as you can see|당신이 볼 수 있듯이|아래 결과에서 볼 수 있듯이|

---

# 2. 문체: 존댓말을 기본으로 하되, 블로그의 온도에 따라 조절합니다

기술 블로그에서는 `합니다체`를 기본으로 두고, 튜토리얼이나 커뮤니티 글에서는 제한적으로 `해요체`를 섞을 수 있습니다. 연구 소개, 모델 발표, 성능 비교 글은 `합니다체`가 안정적입니다.

| 상황      | 권장 톤          | 예시                                    |
| ------- | ------------- | ------------------------------------- |
| 연구 소개   | 차분한 합니다체      | 이 방법은 기존 접근법보다 메모리 사용량을 줄일 수 있습니다.    |
| 제품 발표   | 명확하고 약간 활기 있게 | 이번 릴리스에서는 추론 성능을 개선하는 여러 기능을 추가했습니다.  |
| 튜토리얼    | 친절한 존댓말       | 이제 모델을 로드하고 간단한 추론을 실행해 보겠습니다.        |
| 커뮤니티 후기 | 자연스러운 존댓말     | 실제로 사용해 보니 설정 과정에서 몇 가지 주의할 점이 있었습니다. |
| 릴리즈 노트  | 짧고 사실 중심      | 이번 버전에서는 FlashAttention 지원이 추가되었습니다.  |

## 실전 예시

|원문|비권장|권장|
|---|---|---|
|In this tutorial, you’ll learn how to fine-tune a model.|이 튜토리얼에서 당신은 모델을 파인튜닝하는 법을 배울 것입니다.|이 튜토리얼에서는 모델을 미세 조정하는 방법을 살펴봅니다.|
|Now, let’s run inference.|이제 추론을 실행하자.|이제 추론을 실행해 보겠습니다.|
|If you’re new to Transformers, don’t worry.|Transformers가 처음이라면 걱정하지 마.|Transformers가 처음이어도 괜찮습니다.|
|Pretty neat, right?|꽤 깔끔하죠?|꽤 간단하게 사용할 수 있습니다.|
|You’re all set!|모든 준비가 끝났어요!|이제 사용할 준비가 끝났습니다.|

블로그가 캐주얼하더라도 한국어에서는 과하게 가벼운 말투를 줄이는 편이 좋습니다.

| 원문                                     | 너무 가벼움          | 권장                          |
| -------------------------------------- | --------------- | --------------------------- |
| It’s super easy to get started.        | 시작하는 건 완전 쉽습니다. | 시작하는 방법은 간단합니다.             |
| Just plug it in and you’re good to go. | 그냥 꽂으면 끝입니다.    | 필요한 설정을 추가하면 바로 사용할 수 있습니다. |
| That’s it!                             | 끝!              | 이것으로 설정이 완료됩니다.             |

---

# 3. 문장 구조: 원문 구조를 유지하기보다 한국어 독자의 읽는 순서에 맞춥니다

기술 블로그는 문단 흐름이 중요합니다. 영어의 긴 문장, 관계절, 세미콜론, 콜론 구조를 그대로 옮기면 읽기 어렵습니다.

## 긴 문장 나누기

|원문|비권장|권장|
|---|---|---|
|The model is small, fast, and easy to deploy, making it a good choice for edge applications where latency and memory are critical.|이 모델은 작고 빠르며 배포하기 쉽고, 지연 시간과 메모리가 중요한 엣지 애플리케이션에 좋은 선택이 되게 합니다.|이 모델은 작고 빠르며 배포하기 쉽습니다. 따라서 지연 시간과 메모리 사용량이 중요한 엣지 애플리케이션에 적합합니다.|

## 세미콜론 해체

|원문|비권장|권장|
|---|---|---|
|The model performs well on short inputs; however, longer contexts require more memory.|이 모델은 짧은 입력에서 잘 작동합니다; 그러나 긴 컨텍스트는 더 많은 메모리를 요구합니다.|이 모델은 짧은 입력에서 잘 작동합니다. 다만 긴 컨텍스트를 처리할 때는 더 많은 메모리가 필요합니다.|

## 관계절 분리

|원문|비권장|권장|
|---|---|---|
|We introduce a lightweight model that can run on consumer hardware without sacrificing too much accuracy.|우리는 정확도를 너무 많이 희생하지 않으면서 소비자용 하드웨어에서 실행될 수 있는 경량 모델을 소개합니다.|이번 글에서는 소비자용 하드웨어에서도 실행할 수 있는 경량 모델을 소개합니다. 이 모델은 정확도 손실을 크게 늘리지 않는 것을 목표로 합니다.|

## 콜론 구조 풀기

|원문|비권장|권장|
|---|---|---|
|The idea is simple: reduce memory usage without changing the model architecture.|아이디어는 간단합니다: 모델 아키텍처를 바꾸지 않고 메모리 사용량을 줄입니다.|핵심 아이디어는 간단합니다. 모델 아키텍처를 바꾸지 않고 메모리 사용량을 줄이는 것입니다.|

---

# 4. 의미·조건·확신의 강도는 절대 바꾸지 않습니다

기술 블로그는 문서보다 표현이 부드러워도, `may`, `can`, `should`, `must`, `only`, `up to`, `in some cases` 같은 표현의 의미 강도는 그대로 유지해야 합니다.

|원문 표현|의미|권장 번역|
|---|---|---|
|may|가능성|~일 수 있습니다|
|can|가능|~할 수 있습니다|
|should|권장·기대|~하는 것이 좋습니다 / ~해야 합니다|
|must|필수|반드시 ~해야 합니다|
|only|제한|~만 / 오직 ~|
|up to|최대|최대 ~까지|
|in some cases|일부 경우|일부 경우에는|
|early results suggest|초기 결과상 시사|초기 결과는 ~을 시사합니다|
|not always|항상은 아님|항상 ~인 것은 아닙니다|

## 실전 예시

|원문|비권장|권장|
|---|---|---|
|This approach may improve throughput.|이 접근법은 처리량을 개선합니다.|이 접근법은 처리량을 개선할 수 있습니다.|
|This can reduce memory usage in some cases.|이 방법은 메모리 사용량을 줄입니다.|일부 경우에는 이 방법으로 메모리 사용량을 줄일 수 있습니다.|
|You should use a GPU for larger models.|큰 모델에는 GPU를 사용해야만 합니다.|더 큰 모델을 사용할 때는 GPU를 사용하는 것이 좋습니다.|
|You must set the token before running the script.|스크립트 실행 전에 토큰을 설정하는 것이 좋습니다.|스크립트를 실행하기 전에 반드시 토큰을 설정해야 합니다.|
|The benchmark shows up to 30% speedup.|벤치마크에서 30% 속도 향상을 보였습니다.|벤치마크에서는 최대 30%의 속도 향상을 보였습니다.|
|This does not always lead to better results.|이 방법은 더 나은 결과를 내지 않습니다.|이 방법이 항상 더 나은 결과로 이어지는 것은 아닙니다.|

특히 기술 블로그에서는 성능 개선 문장이 자주 나오므로 `up to`, `average`, `median`, `on our benchmark`, `in our experiments` 같은 조건을 빠뜨리면 안 됩니다.

|원문|위험한 번역|권장|
|---|---|---|
|In our experiments, the model was 2x faster.|이 모델은 2배 빠릅니다.|저희 실험에서는 이 모델이 2배 더 빠르게 동작했습니다.|
|On this benchmark, it outperforms the baseline.|이 모델은 baseline보다 뛰어납니다.|이 벤치마크에서는 baseline보다 좋은 성능을 보였습니다.|
|Early results suggest better alignment.|더 나은 정렬 성능을 보입니다.|초기 결과는 더 나은 정렬 성능을 시사합니다.|

---

# 5. 정보 추가는 원칙적으로 금지하되, 연결 문장은 허용합니다

블로그 번역에서는 독자에게 더 친절하게 설명하고 싶은 유혹이 생깁니다. 그래도 원문에 없는 기술 설명, 평가, 예시, 결론을 임의로 넣으면 안 됩니다.

|원문|비권장|권장|
|---|---|---|
|This post focuses on inference.|이 글에서는 추론을 중심으로 다루며, 학습과 배포 전략도 함께 설명합니다.|이 글에서는 추론을 중심으로 다룹니다.|
|The model supports text generation.|이 모델은 텍스트 생성에 최적화되어 있습니다.|이 모델은 텍스트 생성을 지원합니다.|
|We use LoRA in this example.|이 예제에서는 효율적인 파인튜닝 기법인 LoRA를 사용합니다.|이 예제에서는 LoRA를 사용합니다.|
|The results are promising.|결과는 매우 뛰어납니다.|결과는 긍정적입니다.|
|This is a known limitation.|이는 구조적 한계로 인해 발생합니다.|이는 알려진 한계입니다.|

허용되는 연결 표현은 다음 정도입니다.

|원문 흐름|허용 번역|
|---|---|
|앞 문장의 의미를 다시 받음|즉,|
|대조 관계|다만,|
|조건 상황|이 경우,|
|이미 원문에 예시가 있음|예를 들어,|
|앞에서 실제로 언급함|앞서 설명한 것처럼,|

주의할 점은 `즉`, `다만`, `예를 들어`가 원문에 없는 새 설명을 추가하는 통로가 되지 않게 하는 것입니다.

---

# 6. 용어: Glossary, 기존 번역례, 검색성을 함께 봅니다

기술 블로그에서는 기술 문서보다 독자층이 넓을 수 있습니다. 그래서 용어는 **정확성, 검색성, 이해 가능성**을 함께 봐야 합니다.

## 기본 우선순위

| 우선순위 | 기준                         |
| ---- | -------------------------- |
| 1    | Hugging Face KREW 기존 번역례   |
| 2    | 팀 glossary                 |
| 3    | 기존 승인 PR의 표현               |
| 4    | TTA정보통신용어사전 등 신뢰 가능한 용어 사전 |
| 5    | 한국 ML 커뮤니티에서 널리 쓰이는 표현     |
| 6    | 문서 안에서의 일관성                |

## 실전 예시

|원문|첫 등장 권장|이후 권장|
|---|---|---|
|fine-tuning|미세 조정(fine-tuning)|미세 조정|
|inference|추론|추론|
|checkpoint|체크포인트(checkpoint)|체크포인트|
|quantization|양자화(quantization)|양자화|
|attention mask|어텐션 마스크(attention mask)|어텐션 마스크|
|embedding|임베딩(embedding)|임베딩|
|alignment|정렬(alignment)|정렬|
|serving|서빙(serving)|서빙|
|latency|지연 시간(latency)|지연 시간|
|throughput|처리량(throughput)|처리량|

## 용어 선택 예시

|원문|비권장|권장|이유|
|---|---|---|---|
|fine-tuning|파인튜닝 / 미세조정 혼용|미세 조정(fine-tuning)|문서 내 일관성 확보|
|pretrained model|프리트레인된 모델|사전 훈련된 모델|자연스러운 한국어|
|gold label|골드 레이블|정답 레이블|독자 이해가 쉬움|
|state-of-the-art|예술의 경지|최신 수준 / SOTA|기술 문맥 유지|
|zero-shot|제로 샷|제로샷(zero-shot)|검색성 유지|
|prompt engineering|프롬프트 엔지니어링|프롬프트 엔지니어링|널리 쓰이는 표현|
|hallucination|환각|환각(hallucination)|첫 등장 병기 권장|
|model card|모델 카드|모델 카드|기존 사용례 유지|

`alignment`처럼 문맥에 따라 의미가 달라지는 용어는 특히 주의해야 합니다.

| 원문 맥락                            | 권장 번역                |
| -------------------------------- | -------------------- |
| model alignment                  | 모델 정렬 / 모델 alignment |
| memory alignment                 | 메모리 정렬               |
| text alignment                   | 텍스트 정렬               |
| alignment with human preferences | 사람의 선호에 맞춘 정렬        |
| alignment dataset                | 정렬 데이터셋 / 선호 정렬 데이터셋 |

---

# 7. 제품명, 라이브러리명, 모델명, API명은 번역하지 않습니다

기술 블로그에서도 이 원칙은 그대로 적용됩니다. 블로그 독자는 원문 키워드로 검색하거나 코드를 따라 실행해야 하기 때문입니다.

|유형|원문 유지 예시|
|---|---|
|브랜드|Hugging Face|
|라이브러리|Transformers, Diffusers, Datasets, Tokenizers, PEFT, Accelerate|
|제품|Hub, Space, Inference Endpoints|
|클래스|`AutoTokenizer`, `Trainer`, `AutoModelForCausalLM`|
|함수|`from_pretrained()`, `push_to_hub()`|
|인자|`device_map`, `torch_dtype`, `trust_remote_code`|
|모델 ID|`meta-llama/Llama-3.1-8B`|
|데이터셋 ID|`allenai/c4`, `squad`, `glue`|

## 실전 예시

|원문|비권장|권장|
|---|---|---|
|You can share your demo as a Hugging Face Space.|데모를 허깅페이스 공간으로 공유할 수 있습니다.|데모를 Hugging Face Space로 공유할 수 있습니다.|
|Load the model with AutoModelForCausalLM.|자동인과언어모델로 모델을 로드합니다.|`AutoModelForCausalLM`으로 모델을 로드합니다.|
|Push the model to the Hub.|모델을 허브에 밀어 넣습니다.|모델을 Hub에 업로드합니다.|
|We used PEFT and LoRA for fine-tuning.|우리는 PEFT와 LoRA를 미세 조정에 사용했습니다.|미세 조정에는 PEFT와 LoRA를 사용했습니다.|
|The demo runs on Gradio.|데모는 그라디오에서 실행됩니다.|데모는 Gradio에서 실행됩니다.|

---

# 8. 기술 용어는 단어가 아니라 문맥 단위로 판단합니다

블로그에서는 설명이 문서보다 서술적이어서, 같은 단어도 문맥에 따라 다르게 번역해야 합니다.

|용어|가능한 의미|판단 예시|
|---|---|---|
|head|attention head / 모델 head / 제목|attention head면 “어텐션 헤드”, classifier head면 “분류 헤드”|
|activation|활성화 함수 / 활성화 값|quantization 문맥이면 “활성화 값” 가능성 확인|
|layer|신경망 레이어 / 추상 계층|모델 구조면 “레이어”, 소프트웨어 구조면 “계층”|
|dispatch|요청 분배 / device dispatch|서빙 문맥이면 “분배”, accelerate 문맥이면 “디바이스 배치”|
|compile|일반 컴파일 / `torch.compile`|PyTorch 문맥이면 `torch.compile` 유지|
|prompt|프롬프트 / 지시문 / 입력|LLM 입력이면 “프롬프트”, UX 문맥이면 “안내 문구” 가능|
|token|토큰 / 인증 토큰|NLP면 “토큰”, API auth면 “인증 토큰”|
|serving|모델 서빙 / 제공|ML infra 문맥이면 “서빙” 유지|

## 실전 예시

|원문|비권장|권장|
|---|---|---|
|The classification head is randomly initialized.|분류 머리는 무작위로 초기화됩니다.|분류 헤드는 무작위로 초기화됩니다.|
|Activation quantization reduces memory usage.|활성화 양자화는 메모리 사용량을 줄입니다.|활성화 값 양자화는 메모리 사용량을 줄입니다.|
|The request is dispatched to an available worker.|요청이 사용 가능한 작업자에게 발송됩니다.|요청은 사용 가능한 워커로 분배됩니다.|
|The model can be compiled with `torch.compile`.|모델은 `torch.compile`로 컴파일될 수 있습니다.|`torch.compile`을 사용해 모델을 컴파일할 수 있습니다.|
|Set your token before running the script.|스크립트 실행 전에 토큰을 설정합니다.|스크립트를 실행하기 전에 인증 토큰을 설정합니다.|

---

# 9. 쉬운 한국어를 우선하되, 검색성을 잃지 않습니다

기술 블로그 독자는 배경 지식이 다양합니다. 쉬운 표현이 더 명확하면 쉬운 한국어를 사용합니다. 다만 기술적으로 검색해야 하는 키워드는 영문을 유지하거나 병기합니다.

|원문|비권장|권장|
|---|---|---|
|under the hood|후드 아래에서|내부적으로|
|out of the box|박스 밖에서|별도 설정 없이|
|plug-and-play|플러그 앤 플레이|바로 사용할 수 있는|
|end-to-end|끝에서 끝까지|엔드투엔드(end-to-end)|
|boilerplate code|보일러플레이트 코드|반복 작성해야 하는 기본 코드|
|sanity check|정신 상태 검사|간단한 검증 / 기본 확인|
|edge device|가장자리 장치|엣지 디바이스(edge device)|
|production workload|생산 워크로드|프로덕션 워크로드|

## 실전 예시

|원문|비권장|권장|
|---|---|---|
|Under the hood, the library handles batching automatically.|후드 아래에서 라이브러리는 배칭을 자동으로 처리합니다.|내부적으로는 라이브러리가 배칭을 자동으로 처리합니다.|
|It works out of the box.|박스 밖에서 작동합니다.|별도 설정 없이 바로 작동합니다.|
|This removes a lot of boilerplate code.|이것은 많은 보일러플레이트 코드를 제거합니다.|반복해서 작성해야 하는 기본 코드를 크게 줄여 줍니다.|
|Run a quick sanity check.|빠른 정신 상태 검사를 실행합니다.|간단한 검증을 실행합니다.|
|It is a great fit for production workloads.|프로덕션 워크로드에 훌륭한 적합입니다.|프로덕션 워크로드에 적합합니다.|

---

# 10. 제목: 직역보다 전달력, 검색성, 글의 기대값을 우선합니다

기술 블로그 제목은 독자가 글을 클릭하기 전에 내용을 이해하게 만들어야 합니다. 원문 제목이 길면 한국어에서는 짧게 정리하고, 필요한 경우 부제목으로 풀어 쓰는 방식이 좋습니다.

## 제목 번역 예시

| 원문                                                                             | 비권장                                                        | 권장                                   |
| ------------------------------------------------------------------------------ | ---------------------------------------------------------- | ------------------------------------ |
| How to Fine-tune Large Language Models with Hugging Face Transformers and PEFT | Hugging Face Transformers와 PEFT를 사용하여 대형 언어 모델을 미세 조정하는 방법 | Transformers와 PEFT로 LLM 미세 조정하기      |
| Introducing SmolVLM2: Bringing Video Understanding to Every Device             | SmolVLM2 소개: 모든 장치에 비디오 이해를 가져오기                           | SmolVLM2 공개: 다양한 기기에서 비디오 이해 모델 사용하기 |
| A Gentle Introduction to Quantization                                          | 양자화에 대한 부드러운 소개                                            | 양자화 쉽게 이해하기                          |
| Faster Text Generation with Speculative Decoding                               | 추측 디코딩을 사용한 더 빠른 텍스트 생성                                    | 추측 디코딩으로 텍스트 생성 속도 높이기               |
| What Happens Inside the Pipeline?                                              | 파이프라인 내부에서 무슨 일이 일어나나요?                                    | 파이프라인 내부에서는 어떤 일이 일어날까요?             |
| Building Agents with smolagents                                                | smolagents로 에이전트 구축하기                                      | smolagents로 에이전트 만들기                 |

## 제목 유형별 권장

|글 유형|제목 형식|예시|
|---|---|---|
|튜토리얼|~하기 / ~하는 법|PEFT로 LLM 미세 조정하기|
|개념 설명|~ 이해하기 / ~ 살펴보기|양자화 쉽게 이해하기|
|제품 발표|~ 공개 / ~ 소개|새로운 Inference Endpoint 기능 소개|
|연구 소개|~ 분석 / ~ 살펴보기|BLIP-2 구조와 성능 살펴보기|
|벤치마크|~ 비교 / ~ 평가|텍스트 생성 서빙 성능 비교|
|릴리즈 노트|~ 업데이트|Transformers v4.x 주요 변경 사항|

제목에서 주의할 점은 과장입니다.

|원문|비권장|권장|
|---|---|---|
|Faster inference with quantization|양자화로 추론 속도 혁신하기|양자화로 추론 속도 개선하기|
|A simple guide to RAG|RAG 완전 정복|RAG 기본 가이드|
|Our best open model yet|역대 최고의 오픈 모델|지금까지 공개한 모델 중 가장 강력한 모델|

---

# 11. 섹션 제목과 앵커: 블로그 플랫폼에 따라 적용합니다

기술 블로그가 MDX, Docs, GitHub Markdown처럼 앵커 기반 목차를 쓰면 문서 번역과 동일하게 관리해야 합니다. 일반 블로그 플랫폼에서는 앵커 규칙이 덜 중요하지만, 제목 계층 구조는 여전히 중요합니다.

| 원문                    | 권장                              |
| --------------------- | ------------------------------- |
| `## Why this matters` | `## 중요한 이유[[why-this-matters]]` |
| `## How it works`     | `## 작동 방식[[how-it-works]]`      |
| `## Benchmarks`       | `## 벤치마크[[benchmarks]]`         |
| `## Limitations`      | `## 한계[[limitations]]`          |
| `## What’s next?`     | `## 다음 단계[[whats-next]]`        |

블로그에서 앵커가 필요한 경우, 원문 제목을 규칙으로 추측하기보다 실제 원문 페이지의 URL 앵커를 확인하는 것이 안전합니다. 첨부 transformers 가이드도 `[[...]]` 안의 앵커가 원본 문서 URL과 정확히 일치해야 한다고 설명합니다.

---

# 12. 이모지: 새로 추가하지 않고, 원문 이모지는 의미가 있을 때만 유지합니다

기술 블로그에는 이모지가 들어가는 경우가 있습니다. 하지만 번역자가 임의로 새 이모지를 넣으면 글이 가벼워 보이거나 AI가 쓴 글처럼 보일 수 있습니다.

|상황|처리|
|---|---|
|원문에 없는 이모지|추가하지 않음|
|브랜드 톤에 필요한 원문 이모지|유지 가능|
|문장 의미에 직접 기여|유지 가능|
|단순 장식용 이모지|제거 또는 검토|
|제목에 있는 이모지|검토 후 유지 여부 결정|
|원문보다 이모지 증가|지양|

## 실전 예시

| 원문                                                        | 비권장                                     | 권장                                         |
| --------------------------------------------------------- | --------------------------------------- | ------------------------------------------ |
| Let’s get started 🚀                                      | 이제 시작해봅시다 🚀🔥                          | 이제 시작해 보겠습니다.                              |
| Warning: this API is experimental.                        | 주의: 이 API는 실험적입니다. ⚠️                   | 주의: 이 API는 실험적입니다.                         |
| We’re excited to launch Spaces ZeroGPU 🚀                 | Spaces ZeroGPU를 출시하게 되어 기쁩니다 🎉🚀       | Spaces ZeroGPU를 공개하게 되어 기쁩니다.              |
| This is where the magic happens ✨                         | 여기서 마법이 일어납니다 ✨                         | 핵심 처리는 이 단계에서 이루어집니다.                      |
| The 🤗 Datasets library provides easy access to datasets. | Datasets 라이브러리는 데이터셋에 쉽게 접근할 수 있게 해줍니다. | 🤗 Datasets 라이브러리는 데이터셋에 쉽게 접근할 수 있게 해줍니다. |
| Join the Hugging Face community 🤗                        | Hugging Face 커뮤니티에 참여해 보세요!             | Hugging Face 커뮤니티에 참여해 보세요 🤗              |

원문 이모지가 Hugging Face 브랜드 톤에 직접 기여한다면 유지할 수 있지만, 한국어판에서 과하게 보이면 제거하는 편이 더 자연스럽습니다.

---

# 13. 코드와 인라인 코드는 유지하고, 설명용 주석은 번역합니다

기술 블로그는 코드 예제가 많습니다. 코드 자체는 절대 바꾸면 안 됩니다. 다만 설명용 주석은 독자 이해를 위해 번역할 수 있습니다.

## 코드 블록 예시

원문:

```python
# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Tokenize the input text
inputs = tokenizer("Hello world", return_tensors="pt")
```

권장 번역:

```python
# 토크나이저를 로드합니다
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# 입력 텍스트를 토큰화합니다
inputs = tokenizer("Hello world", return_tensors="pt")
```

## 인라인 코드 예시

|원문|비권장|권장|
|---|---|---|
|Use `AutoTokenizer.from_pretrained()` to load the tokenizer.|토크나이저를 로드하려면 `자동토크나이저.from_pretrained()`를 사용합니다.|토크나이저를 로드하려면 `AutoTokenizer.from_pretrained()`를 사용합니다.|
|Set `device_map="auto"`.|`장치_맵="자동"`으로 설정합니다.|`device_map="auto"`로 설정합니다.|
|Run `huggingface-cli login`.|`허깅페이스-cli 로그인`을 실행합니다.|`huggingface-cli login`을 실행합니다.|

## 블로그에서 자주 나오는 코드 설명

|원문|권장|
|---|---|
|The following snippet loads the model.|다음 코드 조각은 모델을 로드합니다.|
|This script downloads the checkpoint.|이 스크립트는 체크포인트를 다운로드합니다.|
|You can copy and paste this example.|이 예제는 그대로 복사해 실행할 수 있습니다.|
|Replace the model ID with your own.|모델 ID를 본인의 모델 ID로 바꿉니다.|

---

# 14. 링크: 텍스트는 번역하고 target은 유지합니다

블로그에서는 링크 텍스트가 자연스러워야 합니다. 하지만 URL target은 원문과 동일하게 유지해야 합니다.

|원문|권장|
|---|---|
|Read the [model card](https://huggingface.co/...).|[모델 카드](https://huggingface.co/...)를 확인하세요.|
|Check out the [demo](https://huggingface.co/spaces/...).|[데모](https://huggingface.co/spaces/...)를 확인해 보세요.|
|See the [documentation](https://huggingface.co/docs/...).|자세한 내용은 [문서](https://huggingface.co/docs/...)를 참고하세요.|
|The code is available on [GitHub](https://github.com/...).|코드는 [GitHub](https://github.com/...)에서 확인할 수 있습니다.|

비권장 사례:

```markdown
자세한 내용은 [문서](https://huggingface.co/docs/ko/...)를 참고하세요.
```

원문 target이 영어 문서였는데 번역자가 임의로 한국어 경로로 바꾸면 안 됩니다. 링크 변경은 단순 번역 범위를 넘어서는 수정입니다.

---

# 15. 표: 벤치마크와 비교표는 구조를 유지합니다

기술 블로그에는 성능 비교표가 자주 나옵니다. 이 경우 수치, 단위, 조건, 열 이름을 특히 조심해야 합니다.

|원문|비권장|권장|
|---|---|---|
|Throughput|처리량|처리량|
|Latency|대기 시간|지연 시간|
|Memory usage|기억 사용량|메모리 사용량|
|Accuracy|정확성|정확도|
|Speedup|속도 증가|속도 향상|
|Batch size|묶음 크기|배치 크기|

## 벤치마크 표 번역 예시

원문:

|Model|Throughput|Latency|Memory|
|---|--:|--:|--:|
|Model A|120 tok/s|35 ms|8 GB|

권장:

|모델|처리량|지연 시간|메모리|
|---|--:|--:|--:|
|Model A|120 tok/s|35 ms|8 GB|

주의할 점:

|항목|처리|
|---|---|
|`tok/s`|단위이므로 유지|
|`ms`, `GB`|유지|
|모델명|유지|
|숫자|절대 변경 금지|
|열 순서|원문 유지|
|정렬 표시 `---:`|유지|

---

# 16. 리스트: 끝맺음과 정보 단위를 통일합니다

기술 블로그는 기능 소개, 장점 요약, 단계별 설명에 리스트를 많이 씁니다. 같은 리스트 안에서는 문장형과 명사구형을 섞지 않습니다.

## 비권장

```markdown
- 빠른 추론을 지원합니다.
- 낮은 메모리 사용량
- 배포가 쉽습니다.
```

## 권장 1: 문장형

```markdown
- 빠른 추론을 지원합니다.
- 메모리 사용량이 낮습니다.
- 배포가 쉽습니다.
```

## 권장 2: 명사구형

```markdown
- 빠른 추론
- 낮은 메모리 사용량
- 쉬운 배포
```

## 블로그식 기능 소개 예시

|원문|비권장|권장|
|---|---|---|
|Faster generation|더 빠른 생성합니다|더 빠른 생성 속도|
|Lower memory footprint|더 낮은 메모리 발자국|낮은 메모리 사용량|
|Easy deployment|쉬운 배포합니다|쉬운 배포|
|Better support for long context|긴 컨텍스트에 대한 더 나은 지원|긴 컨텍스트 지원 개선|

---

# 17. 번역투를 줄입니다

기술 블로그는 문서보다 읽는 흐름이 중요하기 때문에 번역투를 더 적극적으로 줄여야 합니다.

|지양 표현|권장|
|---|---|
|~에 의해|주어를 바꾸거나 생략|
|~하는 것에 있어|~할 때 / ~에서|
|~를 가지다|있다 / 포함하다 / 제공하다|
|이는 ~입니다|문장 구조 재작성|
|사용되어질 수 있습니다|사용할 수 있습니다|
|~로 하여금|주어를 직접 세움|
|~에 대한|필요하면 문장으로 풀기|

## 실전 예시

|비권장|권장|
|---|---|
|이 모델은 사용자에 의해 쉽게 사용될 수 있습니다.|사용자는 이 모델을 쉽게 사용할 수 있습니다.|
|이는 추론에 대한 새로운 접근법입니다.|이 접근법은 추론 방식을 새롭게 구성합니다.|
|이 기능은 더 나은 성능을 가지게 합니다.|이 기능은 성능 개선에 도움이 됩니다.|
|모델은 여러 장점을 가지고 있습니다.|모델에는 여러 장점이 있습니다.|
|이 설정은 사용되어질 수 있습니다.|이 설정을 사용할 수 있습니다.|
|이는 개발자로 하여금 더 쉽게 배포하게 합니다.|개발자는 더 쉽게 배포할 수 있습니다.|

## 영어식 표현 다듬기

|원문|비권장|권장|
|---|---|---|
|This makes it easy to deploy models.|이것은 모델을 배포하기 쉽게 만듭니다.|이를 통해 모델을 더 쉽게 배포할 수 있습니다.|
|This enables faster iteration.|이것은 더 빠른 반복을 가능하게 합니다.|이를 통해 더 빠르게 반복 실험할 수 있습니다.|
|This gives users more control.|이것은 사용자에게 더 많은 제어를 줍니다.|사용자는 더 세밀하게 제어할 수 있습니다.|
|It helps developers debug issues.|그것은 개발자가 이슈를 디버그하는 것을 돕습니다.|개발자가 문제를 디버깅하는 데 도움이 됩니다.|

---

# 18. 글의 온도: 장르별로 다르게 옮깁니다

기술 블로그는 한 가지 톤으로 통일하면 글이 납작해집니다. 글 유형별로 톤을 다르게 잡아야 합니다.

## 연구 소개

|원문|비권장|권장|
|---|---|---|
|We propose a new method for efficient fine-tuning.|우리는 효율적인 파인튜닝을 위한 새로운 방법을 제안합니다.|이 글에서는 효율적인 미세 조정을 위한 새로운 방법을 소개합니다.|
|The results suggest that the method is competitive.|결과는 이 방법이 경쟁적이라는 것을 제안합니다.|결과는 이 방법이 경쟁력 있는 성능을 낼 수 있음을 시사합니다.|

## 제품 발표

|원문|비권장|권장|
|---|---|---|
|We’re excited to announce a new feature.|새로운 기능을 발표하게 되어 흥분됩니다.|새로운 기능을 공개하게 되어 기쁩니다.|
|This release makes deployment easier.|이 릴리스는 배포를 더 쉽게 만듭니다.|이번 릴리스에서는 배포 과정을 더 간단하게 만들었습니다.|

## 튜토리얼

|원문|비권장|권장|
|---|---|---|
|Let’s start by installing the library.|라이브러리를 설치하는 것으로 시작하자.|먼저 라이브러리를 설치해 보겠습니다.|
|You should see the following output.|당신은 다음 출력을 보아야 합니다.|다음과 같은 출력이 표시됩니다.|

## 커뮤니티 글

|원문|비권장|권장|
|---|---|---|
|I built this over the weekend.|나는 이것을 주말 동안 만들었습니다.|주말 동안 이 프로젝트를 만들어 보았습니다.|
|I learned a few things along the way.|나는 그 과정에서 몇 가지를 배웠습니다.|작업하면서 몇 가지 배운 점이 있었습니다.|

---

# 19. 원문보다 과장하지 않습니다

기술 블로그에서는 홍보성 표현이 나오기 쉽습니다. 하지만 번역자가 원문보다 더 강하게 만들면 신뢰도가 떨어집니다.

|원문|비권장|권장|
|---|---|---|
|promising results|놀라운 결과|긍정적인 결과|
|significant improvement|압도적인 개선|유의미한 개선|
|can improve|개선합니다|개선할 수 있습니다|
|more efficient|훨씬 효율적|더 효율적|
|robust|완벽하게 안정적|견고한|
|lightweight|초경량|경량|
|simple|매우 쉬운|간단한|
|production-ready|즉시 상용화 가능한|프로덕션 환경에서 사용할 수 있는|

## 성능 표현 예시

|원문|비권장|권장|
|---|---|---|
|The model achieves state-of-the-art performance on this benchmark.|이 모델은 모든 작업에서 최고 성능을 달성합니다.|이 모델은 해당 벤치마크에서 SOTA 성능을 달성합니다.|
|It reduces latency by up to 40%.|지연 시간을 40% 줄입니다.|지연 시간을 최대 40%까지 줄입니다.|
|It can handle longer contexts.|더 긴 컨텍스트를 완벽하게 처리합니다.|더 긴 컨텍스트를 처리할 수 있습니다.|
|The method is more stable in our tests.|이 방법은 안정적입니다.|저희 테스트에서는 이 방법이 더 안정적으로 동작했습니다.|

---

# 20. 기술 블로그에 추가하면 좋은 전용 규칙

앞선 규칙에 더해, 기술 블로그 번역에는 아래 요소를 추가하는 것이 좋습니다.

## 20.1 도입부는 “무엇을 다루는 글인지” 빠르게 보여줍니다

|원문|비권장|권장|
|---|---|---|
|In this post, we’ll walk through the new API and show how it simplifies deployment.|이 포스트에서 우리는 새로운 API를 걸어 다니며 그것이 배포를 단순화하는 방법을 보여줄 것입니다.|이번 글에서는 새로운 API를 살펴보고, 이 API가 배포 과정을 어떻게 단순화하는지 설명합니다.|
|Today, we’re sharing what we learned from scaling inference.|오늘 우리는 추론 확장에서 배운 것을 공유합니다.|이번 글에서는 추론을 확장하면서 얻은 경험을 공유합니다.|
|This is the first post in a series on agents.|이것은 에이전트 시리즈의 첫 번째 포스트입니다.|이 글은 에이전트 시리즈의 첫 번째 글입니다.|

## 20.2 마무리 문장은 과한 CTA보다 자연스럽게 정리합니다

|원문|비권장|권장|
|---|---|---|
|Give it a try and let us know what you think!|한번 시도해보고 생각을 알려주세요!|직접 사용해 보시고 의견을 공유해 주세요.|
|We can’t wait to see what you build.|여러분이 무엇을 만들지 기다릴 수 없습니다.|여러분이 어떤 결과물을 만들지 기대하겠습니다.|
|Stay tuned for more updates.|더 많은 업데이트를 위해 채널 고정하세요.|앞으로의 업데이트도 계속 공유드리겠습니다.|

## 20.3 비유와 농담은 의미를 살리되 한국어에서 어색하면 바꿉니다

|원문|비권장|권장|
|---|---|---|
|This is where the magic happens.|여기서 마법이 일어납니다.|핵심 처리는 이 단계에서 이루어집니다.|
|No more wrestling with configuration files.|설정 파일과 더 이상 레슬링하지 않아도 됩니다.|설정 파일 때문에 더 이상 시간을 많이 쓰지 않아도 됩니다.|
|It just works.|그냥 됩니다.|별도 설정 없이 바로 작동합니다.|
|Under the hood, it uses a simple cache.|후드 아래에서 간단한 캐시를 사용합니다.|내부적으로는 간단한 캐시를 사용합니다.|

## 20.4 1인칭 표현은 글의 주체를 보고 선택합니다

|원문|상황|권장|
|---|---|---|
|We trained the model on...|공식 팀 글|저희는 이 모델을 ...로 학습했습니다.|
|We trained the model on...|객관적 기술 설명|이 모델은 ...로 학습되었습니다.|
|I built a small demo.|개인 블로그|작은 데모를 만들어 보았습니다.|
|We found that...|연구·실험 결과|실험 결과, ...을 확인했습니다.|

`we`를 항상 “우리는”으로 옮기면 한국어 블로그에서 어색합니다. 공식 팀의 목소리를 살려야 할 때는 “저희”를 쓰고, 객관적 설명이 더 자연스러울 때는 주어를 생략하거나 수동형으로 정리합니다.

## 20.5 이미지 캡션과 alt text도 번역합니다

기술 블로그에는 그림, 차트, 스크린샷이 자주 들어갑니다. 캡션은 독자가 글을 훑어볼 때 핵심 정보를 얻는 위치이므로 자연스럽게 번역해야 합니다.

|원문|비권장|권장|
|---|---|---|
|Figure 1: Overview of the training pipeline.|그림 1: 훈련 파이프라인의 오버뷰.|그림 1: 학습 파이프라인 개요|
|Benchmark results on A100 GPUs.|A100 GPU들 위의 벤치마크 결과.|A100 GPU에서 측정한 벤치마크 결과|
|The model architecture at a glance.|한눈에 보는 모델 아키텍처.|모델 아키텍처 개요|

이미지 파일 경로는 바꾸지 않습니다.

```markdown
![Overview of the pipeline](./assets/pipeline.png)
```

권장:

```markdown
![파이프라인 개요](./assets/pipeline.png)
```

---

# 21. 기술 블로그용 품질 게이트

## Hard Gate: 실패하면 반드시 수정

|항목|예시|
|---|---|
|코드 변경|`AutoTokenizer`가 `자동토크나이저`로 바뀜|
|인라인 코드 변경|`device_map`이 `장치_맵`으로 바뀜|
|링크 target 변경|원문 URL이 임의로 다른 URL로 바뀜|
|이미지 경로 변경|이미지가 렌더링되지 않음|
|수치 변경|`up to 30%`가 `30%`로 바뀜|
|모델명 변경|`Llama`가 `라마`로 바뀜|
|표 구조 변경|열 개수나 행 개수 변경|
|문단 누락|원문 문단 일부가 번역되지 않음|
|원문에 없는 기술 설명 추가|번역자가 성능 이유를 임의로 설명|

## Review Gate: 사람이 판단

|항목|예시|
|---|---|
|원문보다 과장됨|`can improve`를 “개선합니다”로 번역|
|글의 온도 변화|차분한 연구 소개를 광고 문구처럼 번역|
|해요체 과다|공식 발표 글 전체가 해요체로 번역|
|용어 불일치|fine-tuning을 미세 조정/파인튜닝 혼용|
|검색성 부족|첫 등장 기술 용어의 영문 병기 누락|
|이모지 추가|원문에 없는 이모지 추가|
|제목 과장|“기본 가이드”를 “완전 정복”으로 번역|

## Style Score: 품질 개선 지표

|항목|확인 질문|
|---|---|
|한국어 자연스러움|번역투가 남아 있지 않은가|
|문장 길이|한 문장이 지나치게 길지 않은가|
|문단 흐름|도입-설명-예시-정리가 자연스럽게 이어지는가|
|제목 전달력|글의 내용을 바로 예측할 수 있는가|
|리스트 일관성|문장형과 명사구형이 섞이지 않았는가|
|용어 일관성|같은 개념을 같은 표현으로 번역했는가|
|저자 voice|원문의 태도와 글의 온도가 유지되는가|

---

# 22. 기술 블로그 번역 전용 체크리스트

```text
정확성
[ ] may/can/should/must/up to/in some cases의 의미 강도를 유지했습니다.
[ ] 성능, 품질, 안정성 표현을 원문보다 과장하지 않았습니다.
[ ] 원문에 없는 기술 설명, 장단점, 결론을 추가하지 않았습니다.
[ ] 수치, 단위, 벤치마크 조건을 그대로 유지했습니다.

용어
[ ] 기존 번역례와 glossary를 확인했습니다.
[ ] 검색이 필요한 용어는 첫 등장 시 영문 병기했습니다.
[ ] 제품명, 모델명, API명, 클래스명, 모델 ID는 원문을 유지했습니다.
[ ] 문맥 의존 용어는 문단 단위로 의미를 확인했습니다.

문체와 voice
[ ] 기본 문체는 존댓말로 유지했습니다.
[ ] 글 유형에 맞게 톤을 조정했습니다.
[ ] 저자 voice를 살리되 영어식 표현을 직역하지 않았습니다.
[ ] we/you/let’s를 한국어 문맥에 맞게 처리했습니다.
[ ] 도입부와 마무리가 자연스럽게 읽힙니다.

Markdown과 구조
[ ] 코드 자체를 변경하지 않았습니다.
[ ] 코드 주석은 필요한 경우 한국어로 번역했습니다.
[ ] 인라인 코드를 변경하지 않았습니다.
[ ] 링크 target을 변경하지 않았습니다.
[ ] 이미지 경로를 변경하지 않았습니다.
[ ] 표의 행과 열 구조를 유지했습니다.
[ ] 앵커와 목차가 필요한 문서라면 실제 링크를 확인했습니다.

한국어 품질
[ ] 번역투를 줄였습니다.
[ ] 긴 문장을 필요한 경우 나눴습니다.
[ ] 리스트 끝맺음을 통일했습니다.
[ ] 제목이 짧고 명확하며 검색 가능합니다.
[ ] 일반 본문에 영어 원문이 불필요하게 남아 있지 않습니다.
[ ] 최종 렌더링에서 코드, 표, 이미지, 링크가 깨지지 않습니다.
```

---

# 23. 가이드에 추가하면 좋은 최종 문장

기술 블로그 번역 가이드의 핵심 문장을 하나로 정리하면 아래가 적합합니다.

> 기술 블로그 번역은 원문의 기술적 사실과 저자의 태도를 보존하면서, 한국어 독자가 자연스럽게 읽고 바로 따라 할 수 있는 글로 다시 구성하는 작업입니다. 코드, 링크, 수치, 모델명, API명은 문서 수준으로 엄격하게 보존하고, 문장 구조와 제목, 도입부, 마무리는 한국어 블로그의 읽는 흐름에 맞게 다듬습니다.