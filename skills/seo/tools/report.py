"""Render an SEO eval result (from ``seo_eval.evaluate``) as markdown.

Kept separate from the orchestrator so the machine-readable result dict stays
the single source of truth and the human report is a pure view over it.
"""
from __future__ import annotations

from typing import Any


def _check_line(c: dict[str, Any]) -> str:
    sev = c.get("severity", "")
    if sev == "info":
        return f"ℹ️ {c['name']}: {c['message']}"
    icon = "✅" if c["passed"] else ("❌" if sev == "required" else "⚠️")
    return f"{icon} {c['name']}: {c['message']}"


def _rubric_summary(rub: dict[str, Any]) -> str:
    if not rub.get("available"):
        return f"skeleton — not run ({rub.get('reason', '')})"
    passed = rub.get("passed")
    return (f"{'✅ pass' if passed else '❌ fail'} "
            f"(mean {rub.get('mean')}, min {rub.get('min')})")


def render_markdown(result: dict[str, Any], *, post_display: str = "") -> str:
    gate = result["gate"]
    det = result["deterministic"]
    inp = result["input"]

    lines: list[str] = []
    status = "✅ PASS" if gate["passed"] else "❌ FAIL"
    lines += [
        "# SEO Eval Report",
        "",
        f"**Gate: {status}** — {gate['reason']}",
        "",
        f"- File: `{post_display or inp['file_path']}`",
        f"- Source: {inp.get('source_url') or '—'}",
        f"- Primary keyword: {inp.get('primary_keyword') or '(none — D5 skipped)'}",
        f"- Mode: {inp['mode']}",
        "",
        "## Gate",
        "",
        f"- Deterministic REQUIRED (D1–D7): "
        f"{'✅ pass' if det['required']['passed'] else '❌ fail'}",
        f"- Rubric (R1–R6): {_rubric_summary(result['rubric'])}",
        "",
        "## Required checks (gated)",
        "",
    ]
    lines += [_check_line(c) for c in det["required"]["checks"]] or ["_(none)_"]

    lines += ["", "## Advisory checks (not gated)", ""]
    lines += [_check_line(c) for c in det["advisory"]["checks"]] or ["_(none)_"]

    fm = result.get("frontmatter_advisory")
    if fm:
        lines += [
            "",
            "## Frontmatter (advisory — written by metadata step, not gated)",
            "",
        ]
        lines += [_check_line(c) for c in fm["checks"]]

    if not gate["passed"]:
        fails = [c for c in det["required"]["checks"] if not c["passed"]]
        if fails:
            lines += ["", "## Feedback — fix these to pass", ""]
            lines += [f"{i}. **{c['name']}** — {c['message']}"
                      for i, c in enumerate(fails, 1)]

    bm = result.get("benchmark")
    if bm:
        lines += [
            "",
            "## Benchmark (Lighthouse SEO — informational, not gated)",
            "",
            f"**{bm.get('score', 0)}/100** (mode: {bm.get('mode', '?')}"
            + (f" — {bm['fallback_reason']}" if bm.get("fallback_reason") else "")
            + ")",
        ]
        for a in bm.get("audits", []):
            icon = {"pass": "✅", "fail": "❌", "na": "➖"}.get(a.get("status"), "·")
            lines.append(f"{icon} {a.get('label', a.get('name'))}: {a.get('message', '')}")

    return "\n".join(lines) + "\n"
