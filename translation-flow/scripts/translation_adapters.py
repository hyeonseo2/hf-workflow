from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Protocol


@dataclass(frozen=True)
class TranslationRequest:
    title: str
    source_url: str
    source_markdown: str
    target_locale: str = "ko"


class TranslationAdapter(Protocol):
    name: str

    def translate(self, request: TranslationRequest) -> str:
        """Return translated markdown body only."""


class PlaceholderTranslationAdapter:
    name = "none"

    def translate(self, request: TranslationRequest) -> str:
        return (
            "TODO: Add Korean translation.\n\n"
            "## Source text\n\n"
            "```markdown\n"
            f"{request.source_markdown.strip()}\n"
            "```\n"
        )


class OpenAITranslationAdapter:
    name = "openai"

    def __init__(self, model: Optional[str] = None, prompt_path: Optional[Path] = None) -> None:
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5-nano")
        self.prompt_path = prompt_path or default_prompt_path()

    def translate(self, request: TranslationRequest) -> str:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "The OpenAI adapter requires the `openai` package. "
                "Install dependencies with `uv sync` or `pip install openai`."
            ) from exc

        client = OpenAI()
        response = client.responses.create(
            model=self.model,
            instructions=load_translation_prompt(self.prompt_path),
            input=build_openai_input(request),
        )
        text = response.output_text.strip()
        if not text:
            raise RuntimeError("OpenAI returned an empty translation.")
        return strip_markdown_fence(text)


class GeminiTranslationAdapter:
    name = "gemini"

    def translate(self, request: TranslationRequest) -> str:
        raise NotImplementedError("Gemini adapter is not implemented yet.")


class LocalTranslationAdapter:
    name = "local"

    def translate(self, request: TranslationRequest) -> str:
        raise NotImplementedError("Local translation adapter is not implemented yet.")


FALLBACK_TRANSLATION_PROMPT = """You are translating Hugging Face technical blog posts into Korean.

Output Korean Markdown only. Preserve source meaning, Markdown structure, links,
images, tables, and code blocks. Do not translate code, identifiers, model
names, API names, package names, commands, or URLs. Write natural Korean for
technical readers. Do not add commentary or a preface.
"""


def default_prompt_path() -> Path:
    return Path(__file__).resolve().parents[1] / "docs" / "translation_prompt.md"


def load_translation_prompt(prompt_path: Path) -> str:
    if prompt_path.exists():
        return prompt_path.read_text().strip()
    return FALLBACK_TRANSLATION_PROMPT.strip()


def build_openai_input(request: TranslationRequest) -> str:
    return f"""Translate this Hugging Face Blog post into Korean.

Title: {request.title}
Source URL: {request.source_url}
Target locale: {request.target_locale}

Markdown source:

```markdown
{request.source_markdown.strip()}
```
"""


def strip_markdown_fence(text: str) -> str:
    match = re.fullmatch(r"\s*```(?:markdown|md)?\s*(.*?)\s*```\s*", text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()


def get_translation_adapter(
    name: str,
    model: Optional[str] = None,
    prompt_path: Optional[Path] = None,
) -> TranslationAdapter:
    normalized = name.strip().lower()
    if normalized == "openai":
        return OpenAITranslationAdapter(model=model, prompt_path=prompt_path)
    if normalized in {"none", "placeholder"}:
        return PlaceholderTranslationAdapter()
    if normalized == "gemini":
        return GeminiTranslationAdapter()
    if normalized == "local":
        return LocalTranslationAdapter()
    raise ValueError(f"Unknown translator adapter: {name}")
