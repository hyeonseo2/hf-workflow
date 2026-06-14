"""Pre-publish Lighthouse SEO benchmark.

Produces an industry-comparable 0-100 SEO score *before* the post is published.

Two tiers, auto-selected:

- Tier A (lighthouse): build the Jekyll target repo locally, serve `_site/`
  on localhost, and run Google Lighthouse's SEO category audit against the
  built post page. This is the real benchmark tool, run entirely offline.
- Tier B (heuristic): when the Lighthouse toolchain is unavailable, score the
  post against a Lighthouse-SEO-equivalent rubric computed from the rendered
  HTML / frontmatter. Always works, zero external deps.

`run_benchmark()` tries Tier A and transparently falls back to Tier B,
recording the reason in the result so the report can disclose the mode.

The benchmark score is reported as a separate headline; it does NOT feed the
existing weighted pass/fail score or the exit code.
"""
from __future__ import annotations

import json
import shutil
import socket
import subprocess
import sys
import threading
import time
from contextlib import closing
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))
from heuristic import compute_heuristic_seo  # noqa: E402

# Lighthouse calls a score >= 0.90 "good" (green). We mirror that threshold so
# `passed` means the same thing the Lighthouse UI shows.
GOOD_SCORE = 90


def _which_lighthouse() -> Optional[List[str]]:
    """Resolve a runnable Lighthouse command, or None.

    Prefers a globally installed `lighthouse`; falls back to `npx lighthouse`
    only if a node_modules-resolvable binary exists (we never trigger an
    implicit network install — that would be a surprising side effect)."""
    direct = shutil.which("lighthouse")
    if direct:
        return [direct]
    if shutil.which("npx") and shutil.which("node"):
        probe = subprocess.run(
            ["npx", "--no-install", "lighthouse", "--version"],
            capture_output=True, text=True,
        )
        if probe.returncode == 0:
            return ["npx", "--no-install", "lighthouse"]
    return None


def _jekyll_cmd(target_root: Path) -> Optional[List[str]]:
    """Pick how to build the Jekyll site, or None if no toolchain is present."""
    if (target_root / "Gemfile").exists() and shutil.which("bundle"):
        return ["bundle", "exec", "jekyll", "build"]
    if shutil.which("jekyll"):
        return ["jekyll", "build"]
    return None


def _free_port() -> int:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _slug(file_path: str) -> str:
    """`_posts/2026-05-11-machinecheck.md` -> `machinecheck`."""
    stem = Path(file_path).stem
    parts = stem.split("-", 3)  # strip leading YYYY-MM-DD
    return parts[3] if len(parts) == 4 else stem


def _find_built_path(site_dir: Path, slug: str, title: str) -> Optional[str]:
    """Locate the built post's HTML path under `_site/` without having to
    reimplement Jekyll's permalink rules: match the slug in the path first,
    then fall back to scanning page content for the post title."""
    htmls = list(site_dir.rglob("*.html"))
    for html in htmls:
        if slug and slug in html.relative_to(site_dir).as_posix():
            return "/" + html.relative_to(site_dir).as_posix()
    if title:
        for html in htmls:
            try:
                if title[:40] in html.read_text(encoding="utf-8", errors="ignore"):
                    return "/" + html.relative_to(site_dir).as_posix()
            except OSError:
                continue
    return None


def _serve(directory: Path, port: int) -> ThreadingHTTPServer:
    handler = partial(SimpleHTTPRequestHandler, directory=str(directory))
    httpd = ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


# Lighthouse SEO audits we surface in the report. Names match Lighthouse's
# audit ids so Tier A and Tier B produce the same table.
_AUDIT_LABELS = {
    "document-title": "Document has a <title>",
    "meta-description": "Has a meta description",
    "link-text": "Links have descriptive text",
    "crawlable-anchors": "Links are crawlable",
    "is-crawlable": "Page is indexable (robots)",
    "image-alt": "Images have alt text",
    "hreflang": "Valid hreflang",
    "canonical": "Valid canonical",
    "font-legibility": "Legible font sizes",
    "tap-targets": "Tap targets sized correctly",
}


def _parse_lighthouse(report: Dict[str, Any]) -> Dict[str, Any]:
    """Extract the SEO category score and per-audit status from Lighthouse JSON."""
    seo = report.get("categories", {}).get("seo", {})
    raw = seo.get("score")
    score = round(raw * 100) if isinstance(raw, (int, float)) else 0

    audits = report.get("audits", {})
    rows: List[Dict[str, Any]] = []
    for ref in seo.get("auditRefs", []):
        a = audits.get(ref.get("id"), {})
        mode = a.get("scoreDisplayMode")
        if mode in ("notApplicable", "manual"):
            status = "na"
        elif a.get("score") is None:
            status = "na"
        else:
            status = "pass" if a["score"] >= 0.9 else "fail"
        rows.append({
            "name": ref.get("id"),
            "label": a.get("title") or _AUDIT_LABELS.get(ref.get("id"), ref.get("id")),
            "status": status,
            "message": a.get("explanation") or a.get("title", ""),
        })
    return {"score": score, "audits": rows}


def _run_lighthouse(
    manifest: Dict[str, Any], target_root: Path, frontmatter: Dict[str, Any]
) -> Dict[str, Any]:
    """Tier A. Raises on any missing-toolchain / build / audit failure so the
    caller can fall back to Tier B with the message attached."""
    jekyll = _jekyll_cmd(target_root)
    if not jekyll:
        raise RuntimeError("Jekyll toolchain not found (need bundler+jekyll or jekyll)")
    lh = _which_lighthouse()
    if not lh:
        raise RuntimeError("Lighthouse CLI not found (npm i -g lighthouse)")
    if not shutil.which("google-chrome") and not shutil.which("chromium") \
            and not Path("/Applications/Google Chrome.app").exists():
        raise RuntimeError("Headless Chrome not found")

    site_dir = target_root / "_site"
    build = subprocess.run(
        jekyll, cwd=target_root, capture_output=True, text=True, timeout=300
    )
    if build.returncode != 0:
        raise RuntimeError(f"jekyll build failed: {build.stderr.strip()[:300]}")

    file_path = manifest["translation"]["file_path"]
    slug = _slug(file_path)
    title = str(frontmatter.get("title", ""))
    rel = _find_built_path(site_dir, slug, title)
    if not rel:
        raise RuntimeError(f"Built page for '{slug}' not found under _site/")

    port = _free_port()
    httpd = _serve(site_dir, port)
    try:
        url = f"http://127.0.0.1:{port}{rel}"
        proc = subprocess.run(
            lh + [
                url,
                "--only-categories=seo",
                "--output=json",
                "--output-path=stdout",
                "--quiet",
                '--chrome-flags=--headless=new --no-sandbox',
                "--max-wait-for-load=45000",
            ],
            capture_output=True, text=True, timeout=180,
        )
        if proc.returncode != 0 or not proc.stdout.strip():
            raise RuntimeError(f"lighthouse run failed: {proc.stderr.strip()[:300]}")
        parsed = _parse_lighthouse(json.loads(proc.stdout))
    finally:
        httpd.shutdown()
        shutil.rmtree(site_dir, ignore_errors=True)

    return {
        "mode": "lighthouse",
        "score": parsed["score"],
        "fallback_reason": None,
        "audits": parsed["audits"],
        "passed": parsed["score"] >= GOOD_SCORE,
    }


def _run_lighthouse_url(url: str) -> Dict[str, Any]:
    """Tier A against an already-published URL (no local build). Used by
    `--benchmark-url` for a post-publish re-check."""
    lh = _which_lighthouse()
    if not lh:
        raise RuntimeError("Lighthouse CLI not found (npm i -g lighthouse)")
    proc = subprocess.run(
        lh + [
            url, "--only-categories=seo", "--output=json",
            "--output-path=stdout", "--quiet",
            '--chrome-flags=--headless=new --no-sandbox',
            "--max-wait-for-load=45000",
        ],
        capture_output=True, text=True, timeout=180,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        raise RuntimeError(f"lighthouse run failed: {proc.stderr.strip()[:300]}")
    parsed = _parse_lighthouse(json.loads(proc.stdout))
    return {
        "mode": "lighthouse",
        "score": parsed["score"],
        "fallback_reason": None,
        "audits": parsed["audits"],
        "passed": parsed["score"] >= GOOD_SCORE,
    }


def run_benchmark(
    manifest: Dict[str, Any],
    target_root: Path,
    body: str,
    frontmatter: Dict[str, Any],
    mode: str = "auto",
    benchmark_url: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Return a benchmark result dict, or None when `mode='off'`.

    Result: {mode, score(0-100), fallback_reason, audits[], passed}.
    `mode`: auto | lighthouse | heuristic | off.
    `benchmark_url`: audit this published URL directly instead of building
    the site locally (post-publish re-check).
    """
    if mode == "off":
        return None

    if mode in ("auto", "lighthouse"):
        try:
            if benchmark_url:
                return _run_lighthouse_url(benchmark_url)
            return _run_lighthouse(manifest, target_root, frontmatter)
        except Exception as exc:  # noqa: BLE001 - any failure -> graceful fallback
            if mode == "lighthouse":
                return {
                    "mode": "heuristic",
                    "score": 0,
                    "fallback_reason": f"lighthouse requested but failed: {exc}",
                    "audits": [],
                    "passed": False,
                }
            fallback_reason = f"lighthouse unavailable: {exc}"
    else:
        fallback_reason = "heuristic mode requested"

    result = compute_heuristic_seo(manifest, body, frontmatter)
    result["fallback_reason"] = fallback_reason
    return result
