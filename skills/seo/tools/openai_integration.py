"""OpenAI-backed SEO judge and metadata generator seams.

The SEO skill keeps deterministic checkers separate from semantic decisions.
This module is the production provider for those semantic decisions. Tests can
still inject local stubs through the existing judge/generator callables.
"""
from __future__ import annotations

import json
import os
import re
from typing import Any, Callable


DEFAULT_MODEL = "gpt-5-nano"
OPENAI_WARNING_PREFIX = "openai_unavailable:"


def _json_from_text(text: str) -> dict[str, Any]:
    text = text.strip()
    if not text:
        raise ValueError("OpenAI returned an empty response")
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not match:
            raise
        data = json.loads(match.group(0))
    if not isinstance(data, dict):
        raise ValueError("OpenAI response must be a JSON object")
    return data


def _client(client: Any | None = None) -> Any:
    if client is not None:
        return client
    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def _call_json(
    *,
    instructions: str,
    payload: dict[str, Any],
    model: str,
    client: Any | None = None,
) -> dict[str, Any]:
    response = _client(client).responses.create(
        model=model,
        instructions=instructions,
        input=json.dumps(payload, ensure_ascii=False),
    )
    return _json_from_text(response.output_text)


def make_openai_judge(
    *,
    model: str | None = None,
    client: Any | None = None,
) -> Callable[[str, dict[str, Any]], dict[str, Any]]:
    """Return a rubric judge that maps OpenAI failures to failing checks."""
    selected_model = model or os.getenv("OPENAI_MODEL") or DEFAULT_MODEL

    def judge(name: str, payload: dict[str, Any]) -> dict[str, Any]:
        try:
            if name == "semantic_metadata":
                return _call_json(
                    model=selected_model,
                    client=client,
                    instructions=(
                        "You are a Korean technical SEO policy judge. "
                        "Compare only the provided title, description, H1, headings, "
                        "and opening text. Return JSON with status "
                        "PASS, NEEDS_CHANGES, or FAIL; issues as a string array; "
                        "evidence as a string array; and reason as a short string."
                    ),
                    payload={"judge": name, "evidence": payload},
                )
            if name == "alt_semantics":
                return _call_json(
                    model=selected_model,
                    client=client,
                    instructions=(
                        "You are a Korean technical SEO image-alt judge. "
                        "Evaluate only non-empty alt text usefulness from the provided "
                        "image evidence. Ignore empty alt coverage. Return JSON with "
                        "status PASS, NEEDS_CHANGES, or FAIL; problem_images as an "
                        "array of objects with src, alt, reason; and reason as a short string."
                    ),
                    payload={"judge": name, "evidence": payload},
                )
            return {"status": "FAIL", "issues": [f"unknown judge: {name}"],
                    "evidence": [], "reason": f"unknown judge: {name}"}
        except Exception as exc:  # noqa: BLE001 - CI should surface provider failures as gate failures.
            if name == "alt_semantics":
                return {
                    "status": "FAIL",
                    "problem_images": [],
                    "reason": f"{OPENAI_WARNING_PREFIX} {exc}",
                }
            return {
                "status": "FAIL",
                "issues": [f"{OPENAI_WARNING_PREFIX} {exc}"],
                "evidence": [],
                "reason": f"{OPENAI_WARNING_PREFIX} {exc}",
            }

    return judge


def make_openai_metadata_generator(
    *,
    model: str | None = None,
    client: Any | None = None,
    allow_deterministic_fallback: bool = False,
) -> Callable[[dict[str, Any]], dict[str, Any]]:
    """Return a metadata generator.

    OpenAI is the primary path. If it is unavailable, the generator either emits
    an explicit warning with an empty candidate or a conservative deterministic
    fallback when explicitly allowed for local testing.
    """
    selected_model = model or os.getenv("OPENAI_MODEL") or DEFAULT_MODEL

    def fallback_candidate(evidence: dict[str, Any]) -> dict[str, Any]:
        frontmatter = evidence.get("frontmatter", {}) or {}
        content = evidence.get("content", {}) or {}
        title = str(frontmatter.get("title") or content.get("first_heading") or "").strip()
        description = str(frontmatter.get("description") or content.get("first_paragraph") or "").strip()
        return {
            "candidate": {
                "title": title,
                "description": description[:170],
                "categories": frontmatter.get("categories") or [],
                "image": frontmatter.get("image") or "",
            }
        }

    def generator(evidence: dict[str, Any]) -> dict[str, Any]:
        try:
            data = _call_json(
                model=selected_model,
                client=client,
                instructions=(
                    "You are a Korean technical SEO metadata writer. "
                    "Generate metadata only from the provided evidence. Do not invent "
                    "facts. Return JSON with candidate.title, candidate.description, "
                    "candidate.categories, candidate.image, and warnings. Do not create "
                    "canonical or hreflang values."
                ),
                payload={"task": "metadata_candidate", "evidence": evidence},
            )
            candidate = data.get("candidate", data)
            if not isinstance(candidate, dict):
                candidate = {}
            warnings = data.get("warnings", [])
            if not isinstance(warnings, list):
                warnings = [str(warnings)]
            return {"candidate": candidate, "warnings": [str(w) for w in warnings]}
        except Exception as exc:  # noqa: BLE001
            warning = f"{OPENAI_WARNING_PREFIX} {exc}"
            if allow_deterministic_fallback:
                payload = fallback_candidate(evidence)
                payload["warnings"] = [warning, "deterministic_metadata_fallback_used"]
                return payload
            return {"candidate": {}, "warnings": [warning]}

    return generator


def has_openai_failure(warnings: list[str]) -> bool:
    return any(str(w).startswith(OPENAI_WARNING_PREFIX) for w in warnings)
