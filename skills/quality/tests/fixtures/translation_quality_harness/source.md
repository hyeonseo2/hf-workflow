---
title: "Testing Hugging Face Spaces"
authors:
  - hf-team
thumbnail: /blog/assets/testing-spaces/thumbnail.png
---

# Testing Hugging Face Spaces

Hugging Face Spaces can be used to demo models such as meta-llama/Llama-3.1-8B.

The model has 70B parameters and reaches 92.5% accuracy on the benchmark.

Use `AutoTokenizer.from_pretrained()` with the `transformers` library.

![Architecture](/blog/assets/testing-spaces/architecture.png)

See [the model card](https://huggingface.co/meta-llama/Llama-3.1-8B) for details.

| Model | Accuracy |
| --- | ---: |
| Llama | 92.5% |

The loss is $\\alpha + \\beta$.

```python
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")
```
