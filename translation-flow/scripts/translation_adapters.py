from __future__ import annotations

import os
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
            from scripts.ecl_translation_pipeline import translate_markdown_with_ecl
        except ModuleNotFoundError:
            try:
                from ecl_translation_pipeline import translate_markdown_with_ecl
            except ModuleNotFoundError as exc:
                raise RuntimeError(
                    "The ECL pipeline requires `markdown-it-py`. "
                    "Install dependencies with `uv sync` or `pip install markdown-it-py`."
                ) from exc

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "The OpenAI adapter requires the `openai` package. "
                "Install dependencies with `uv sync` or `pip install openai`."
            ) from exc

        client = OpenAI()
        core_rules = load_translation_prompt(self.prompt_path)
        target_language = locale_to_language(request.target_locale)
        print(
            f"[translation-openai] model={self.model} target_language={target_language} "
            f"source_chars={len(request.source_markdown)}",
            flush=True,
        )

        def model_call(prompt: str) -> str:
            print(
                f"[translation-openai] request_start prompt_chars={len(prompt)}",
                flush=True,
            )
            response = client.responses.create(
                model=self.model,
                instructions="You are a precise technical translation engine. Follow the user prompt strictly.",
                input=prompt,
            )
            text = response.output_text.strip()
            if not text:
                raise RuntimeError("OpenAI returned an empty translation chunk.")
            print(
                f"[translation-openai] request_done response_chars={len(text)}",
                flush=True,
            )
            return text

        return translate_markdown_with_ecl(
            source_markdown=request.source_markdown,
            core_rules=core_rules,
            target_language=target_language,
            model_call=model_call,
        )


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


def locale_to_language(locale: str) -> str:
    normalized = locale.strip().lower()
    if normalized in {"ko", "ko-kr"}:
        return "Korean"
    if normalized in {"en", "en-us"}:
        return "English"
    return locale


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
    raise ValueError(f"Unknown translator adapter: {name}. Supported: openai, none")