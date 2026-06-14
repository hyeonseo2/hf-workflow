"""Rubric (LLM) evaluation — Module 1b.

STAGE-1 SKELETON. The rubric judges six qualitative SEO/GEO criteria that the
deterministic checks cannot. Stage 1 ships the interface only: ``evaluate()``
returns an *unavailable* result, so the orchestrator's AND gate runs on the
deterministic result alone, with a clearly marked seam where the LLM judge
plugs in next (model follows SKILL.md, or a scripted OpenAI call for CI).

Rubric items (design `seo-eval-decisions.md` §6), scored 1–5:
  R1  첫 문단 답변성(GEO): 맥락 없이 핵심 질문에 직답/정의
  R2  heading 검색의도 정합성
  R3  alt 의미 정확성
  R4  citation 권위·적합성
  R5  인용가능성(자기완결 문장)
  R6  키워드 검색-무결성 — 검색어인 영문 고유명사/기술용어 보존, primary keyword가
      실제 검색 가능한 용어로 표현. (번역 fluency/자연스러움은 범위 밖)

Gate (design §6): rubric PASS = 평균 ≥ 4 AND 최저 ≥ 3.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

RUBRIC_ITEMS: dict[str, str] = {
    "R1": "첫 문단 답변성(GEO): 맥락 없이 핵심 질문에 직답/정의",
    "R2": "heading 검색의도 정합성",
    "R3": "alt 의미 정확성",
    "R4": "citation 권위·적합성",
    "R5": "인용가능성(자기완결 문장)",
    "R6": "키워드 검색-무결성 (검색어 용어 보존)",
}

PASS_MEAN = 4.0
PASS_MIN = 3


@dataclass
class RubricResult:
    """Outcome of the rubric pass.

    ``available=False`` means the rubric did not run; ``passed`` is then ``None``
    and the orchestrator falls back to the deterministic gate alone.
    """

    available: bool = False
    scores: dict[str, int] = field(default_factory=dict)  # {"R1": 1..5, ...}
    notes: dict[str, str] = field(default_factory=dict)
    reason: str = "rubric not run (stage-1 skeleton)"

    @property
    def mean(self) -> Optional[float]:
        if not self.scores:
            return None
        return round(sum(self.scores.values()) / len(self.scores), 2)

    @property
    def min(self) -> Optional[int]:
        return min(self.scores.values()) if self.scores else None

    @property
    def passed(self) -> Optional[bool]:
        if not self.available or not self.scores:
            return None
        return self.mean >= PASS_MEAN and self.min >= PASS_MIN

    def to_dict(self) -> dict[str, Any]:
        return {
            "available": self.available,
            "scores": self.scores,
            "mean": self.mean,
            "min": self.min,
            "passed": self.passed,
            "reason": self.reason,
        }


def evaluate(
    body: str,
    frontmatter: dict[str, Any],
    manifest: dict[str, Any],
    *,
    source_url: str = "",
    primary_keyword: str = "",
) -> RubricResult:
    """SKELETON: return an unavailable result.

    Stage 2 implements the LLM judge here and returns populated ``scores``.
    The signature is fixed so the orchestrator needs no change when it lands.
    """
    return RubricResult(available=False, reason="rubric not run (stage-1 skeleton)")
