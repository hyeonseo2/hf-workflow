---
title: "Hugging Face Spaces 테스트"
authors:
  - hf-team
thumbnail: /blog/assets/testing-spaces/thumbnail.png
---

# Hugging Face Spaces 테스트

Hugging Face Spaces는 meta-llama/Llama-3.1-8B 같은 모델을 데모하는 데 사용할 수 있습니다.

이 모델은 70B 파라미터를 가지며 벤치마크에서 92.5% 정확도에 도달합니다.

`transformers` 라이브러리와 함께 `AutoTokenizer.from_pretrained()`를 사용합니다.

![Architecture](/blog/assets/testing-spaces/architecture.png)

자세한 내용은 [모델 카드](https://huggingface.co/meta-llama/Llama-3.1-8B)를 참고하세요.

| Model | Accuracy |
| --- | ---: |
| Llama | 92.5% |

```python
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")
```
