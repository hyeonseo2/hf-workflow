---
title: "Hugging Face Spaces 테스트"
authors:
  - hf-team
thumbnail: /blog/assets/testing-spaces/thumbnail.png
---

# Hugging Face Spaces 테스트

Hugging Face Spaces는 meta-llama/Llama-3.1-8B 같은 모델을 데모하는 데 사용할 수 있습니다.

`transformers` 라이브러리와 함께 `자동토크나이저.from_pretrained()`를 사용합니다.

```python
from transformers import AutoTokenizer
tokenizer = 자동토크나이저.from_pretrained("meta-llama/Llama-3.1-8B")
```
