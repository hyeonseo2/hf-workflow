from __future__ import annotations

import argparse
import re
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


def parse_frontmatter(markdown: str) -> dict[str, str]:
    if not markdown.startswith("---"):
        return {}
    end = markdown.find("\n---", 3)
    if end == -1:
        return {}
    frontmatter: dict[str, str] = {}
    for line in markdown[3:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip().strip('"')
    return frontmatter


def headings(markdown: str) -> list[str]:
    return [line.strip() for line in markdown.splitlines() if re.match(r"^#{1,4}\s+", line)]


def status(ok: bool) -> str:
    return "PASS" if ok else "WARN"


def build_report(manifest_path: Path, target_root: Path) -> str:
    manifest = read_simple_manifest(manifest_path)
    file_path = manifest.get("translation.file_path", "")
    source_title = manifest.get("source.title", "")
    source_url = manifest.get("source.url", "")
    translation_path = target_root / file_path
    markdown = translation_path.read_text()
    fm = parse_frontmatter(markdown)
    h = headings(markdown)

    checks = [
        ("frontmatter title exists", bool(fm.get("title"))),
        ("frontmatter slug exists", bool(fm.get("slug"))),
        ("source_url exists", fm.get("source_url") == source_url),
        ("categories exists", bool(fm.get("categories"))),
        ("has H1", any(line.startswith("# ") for line in h)),
        ("has at least three section headings", len([line for line in h if line.startswith("## ")]) >= 3),
        ("has source attribution sentence", "Hugging Face 블로그" in markdown),
    ]

    lines = [
        "# SEO Report",
        "",
        f"- Manifest: `{manifest_path}`",
        f"- Translation file: `{translation_path}`",
        f"- Source: {source_url}",
        f"- Source title: {source_title}",
        "",
        "## Checks",
        "",
    ]
    for name, ok in checks:
        lines.append(f"- {status(ok)}: {name}")

    lines += [
        "",
        "## Frontmatter",
        "",
        f"- title: {fm.get('title', '')}",
        f"- slug: {fm.get('slug', '')}",
        f"- categories: {fm.get('categories', '')}",
        "",
        "## Heading Snapshot",
        "",
    ]
    lines.extend(f"- `{heading}`" for heading in h[:10])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a simple SEO report for a translated post.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--target-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_report(Path(args.manifest), Path(args.target_root)))
    print(f"Wrote SEO report: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
