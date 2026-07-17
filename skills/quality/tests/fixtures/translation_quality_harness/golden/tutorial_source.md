---
title: Run a text generation pipeline
---

# Run the pipeline

Install `transformers` and load `AutoModelForCausalLM` from the [model guide](https://huggingface.co/docs/transformers/main/en/model_doc/auto).

```python
from transformers import pipeline

generator = pipeline("text-generation", model="acme/model-v1")
print(generator("Hello"))
```

Use `--device cuda` only when a compatible GPU is available.
