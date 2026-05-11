from __future__ import annotations

import argparse
import re
import urllib.request
from pathlib import Path


def read_simple_manifest(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    section = ""
    for raw_line in path.read_text().splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("- "):
            continue
        if not raw_line.startswith(" ") and raw_line.endswith(":"):
            section = raw_line[:-1].strip()
            continue
        match = re.match(r"^\s{2}([A-Za-z0-9_]+):\s*(.*)$", raw_line)
        if not match:
            continue
        key, value = match.groups()
        data[f"{section}.{key}"] = value.strip().strip('"')
    return data


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "quality-skills/0.1"})
    with urllib.request.urlopen(request, timeout=30) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def strip_frontmatter(markdown: str) -> str:
    if markdown.startswith("---"):
        end = markdown.find("\n---", 3)
        if end != -1:
            return markdown[end + 4 :]
    return markdown


def count_code_fences(markdown: str) -> int:
    return len(re.findall(r"^```", markdown, flags=re.MULTILINE))


def korean_ratio(text: str) -> float:
    letters = re.findall(r"[A-Za-z가-힣]", text)
    if not letters:
        return 0.0
    korean = [ch for ch in letters if "가" <= ch <= "힣"]
    return len(korean) / len(letters)


def status(ok: bool) -> str:
    return "PASS" if ok else "WARN"


def build_report(manifest_path: Path, target_root: Path, fetch_source: bool = False) -> str:
    manifest = read_simple_manifest(manifest_path)
    file_path = manifest.get("translation.file_path", "")
    source_url = manifest.get("source.url", "")
    translation_path = target_root / file_path
    markdown = translation_path.read_text()
    body = strip_frontmatter(markdown)
    source_text = fetch_text(source_url) if fetch_source and source_url else ""

    code_fences = count_code_fences(body)
    ratio = korean_ratio(body)
    todo_count = body.count("TODO")
    checks = [
        ("translation body is not empty", len(body.strip()) > 500),
        ("no TODO marker remains", todo_count == 0),
        ("code fences are balanced", code_fences % 2 == 0),
        ("contains Korean prose", ratio >= 0.25),
        ("source attribution exists", source_url in markdown),
    ]

    lines = [
        "# Quality Report",
        "",
        f"- Manifest: `{manifest_path}`",
        f"- Translation file: `{translation_path}`",
        f"- Source: {source_url}",
        "",
        "## Checks",
        "",
    ]
    for name, ok in checks:
        lines.append(f"- {status(ok)}: {name}")

    lines += [
        "",
        "## Metrics",
        "",
        f"- body characters: {len(body)}",
        f"- Korean letter ratio: {ratio:.2%}",
        f"- code fence markers: {code_fences}",
        f"- TODO markers: {todo_count}",
        f"- fetched source characters: {len(source_text)}",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a simple quality report for a translated post.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--target-root", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--fetch-source", action="store_true")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_report(Path(args.manifest), Path(args.target_root), fetch_source=args.fetch_source))
    print(f"Wrote quality report: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
