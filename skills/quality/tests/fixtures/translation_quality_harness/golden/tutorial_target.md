---
title: 텍스트 생성 파이프라인 실행하기
---

# 파이프라인 실행하기

`transformers`를 설치하고 [모델 가이드](https://huggingface.co/docs/transformers/main/en/model_doc/auto)를 참고해 `AutoModelForCausalLM`을 불러옵니다.

```python
from transformers import pipeline

generator = pipeline("text-generation", model="acme/model-v1")
print(generator("Hello"))
```

호환되는 GPU가 있을 때만 `--device cuda`를 사용합니다.
