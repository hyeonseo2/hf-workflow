"""Compile archived translation workflow reports into a static JSON snapshot."""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile


MANIFEST_PATH = re.compile(r"(?:^|/)reports/pr-(\d+)/manifest\.yaml$")
CHECK_LINE = re.compile(r"-\s+(PASS|WARN|FAIL):\s*(.+)$")
KEY_VALUE_LINE = re.compile(r"-\s+([^:]+):\s*(.*)$")
HEADING_LINE = re.compile(r"-\s+`(.+)`$")


def _parse_scalar(value: str):
    value = value.strip()
    if value == "[]":
        return []
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return json.loads(value)
    return value


def _yaml_lines(text: str):
    lines = []
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        lines.append((len(raw_line) - len(raw_line.lstrip(" ")), stripped))
    return lines


def _parse_yaml_block(lines, index: int, indent: int):
    if index >= len(lines) or lines[index][0] < indent:
        return {}, index
    if lines[index][1].startswith("- "):
        values = []
        while index < len(lines) and lines[index][0] == indent:
            item = lines[index][1]
            if not item.startswith("- "):
                break
            values.append(_parse_scalar(item[2:]))
            index += 1
        return values, index

    mapping = {}
    while index < len(lines) and lines[index][0] == indent:
        content = lines[index][1]
        if content.startswith("- ") or ":" not in content:
            break
        key, value = content.split(":", 1)
        index += 1
        if value.strip():
            mapping[key.strip()] = _parse_scalar(value)
        elif index < len(lines) and lines[index][0] > indent:
            mapping[key.strip()], index = _parse_yaml_block(lines, index, lines[index][0])
        else:
            mapping[key.strip()] = {}
    return mapping, index


def parse_manifest(text: str) -> dict:
    """Parse the constrained manifest YAML used by the workflow archive."""
    lines = _yaml_lines(text)
    if not lines:
        return {}
    manifest, _ = _parse_yaml_block(lines, 0, lines[0][0])
    return manifest


def parse_report(text: str) -> dict:
    """Normalize checks and detail sections from a quality or SEO report."""
    result = {"checks": [], "metrics": {}, "frontmatter": {}, "headings": []}
    section = None
    for line in text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if section == "Checks":
            match = CHECK_LINE.fullmatch(line.strip())
            if match:
                status = {"PASS": "pass", "WARN": "warning", "FAIL": "fail"}[match.group(1)]
                result["checks"].append({"status": status, "text": match.group(2)})
        elif section in {"Metrics", "Frontmatter"}:
            match = KEY_VALUE_LINE.fullmatch(line.strip())
            if match:
                key = "metrics" if section == "Metrics" else "frontmatter"
                result[key][match.group(1)] = match.group(2)
        elif section == "Heading Snapshot":
            match = HEADING_LINE.fullmatch(line.strip())
            if match:
                result["headings"].append(match.group(1))

    statuses = {check["status"] for check in result["checks"]}
    if "fail" in statuses:
        result["status"] = "fail"
    elif "warning" in statuses:
        result["status"] = "warning"
    elif "pass" in statuses:
        result["status"] = "pass"
    else:
        result["status"] = "warning"
    return result


def _report_result(zip_file: ZipFile, path: str, enabled: bool, detail_keys):
    file_name = Path(path).name
    if path not in zip_file.namelist():
        result = {
            "enabled": enabled,
            "available": False,
            "status": "missing",
            "checks": [],
            "fileName": file_name,
            "content": "",
        }
        for key in detail_keys:
            result[key] = {} if key in {"metrics", "frontmatter"} else []
        return result

    content = zip_file.read(path).decode("utf-8")
    parsed = parse_report(content)
    result = {
        "enabled": enabled,
        "available": True,
        "status": parsed["status"],
        "checks": parsed["checks"],
        "fileName": file_name,
        "content": content,
    }
    for key in detail_keys:
        result[key] = parsed[key]
    return result


def compile_archive(archive_path: Path) -> dict:
    """Compile every archived manifest and its optional generated reports."""
    archive_path = Path(archive_path)
    reports = []
    repositories = set()
    seen_pr_numbers = set()

    with ZipFile(archive_path) as zip_file:
        for name in zip_file.namelist():
            match = MANIFEST_PATH.search(name)
            if not match:
                continue
            pr_number = int(match.group(1))
            if pr_number in seen_pr_numbers:
                raise ValueError(f"duplicate manifest for PR {pr_number}")
            seen_pr_numbers.add(pr_number)

            manifest = parse_manifest(zip_file.read(name).decode("utf-8"))
            translation = manifest.get("translation", {})
            repository = translation.get("target_repo") if isinstance(translation, dict) else None
            if not isinstance(repository, str) or not repository.strip():
                raise ValueError(
                    f"manifest for PR {pr_number} must contain a non-empty "
                    "translation.target_repo"
                )
            repositories.add(repository)
            report_root = name.rsplit("/", 1)[0]
            handoff = manifest.get("handoff", {})
            quality_settings = handoff.get("quality", {})
            seo_settings = handoff.get("seo", {})
            reports.append(
                {
                    "prNumber": pr_number,
                    "run": manifest.get("run", {}),
                    "source": manifest.get("source", {}),
                    "translation": translation,
                    "requestAvailable": f"{report_root}/request.md" in zip_file.namelist(),
                    "quality": _report_result(
                        zip_file,
                        f"{report_root}/quality-report.md",
                        bool(quality_settings.get("enabled", False)),
                        ("metrics",),
                    ),
                    "seo": _report_result(
                        zip_file,
                        f"{report_root}/seo-report.md",
                        bool(seo_settings.get("enabled", False)),
                        ("frontmatter", "headings"),
                    ),
                }
            )

    if len(repositories) != 1:
        raise ValueError("all manifests must use the same target repository")

    reports.sort(key=lambda report: report["prNumber"], reverse=True)
    timestamps = [report["run"].get("created_at") for report in reports]
    report_snapshot_at = max(
        (timestamp for timestamp in timestamps if timestamp),
        key=datetime.fromisoformat,
    )
    return {
        "schemaVersion": 1,
        "sourceArchive": archive_path.name,
        "reportSnapshotAt": report_snapshot_at,
        "repository": repositories.pop(),
        "reports": reports,
    }


def write_snapshot(archive_path: Path, output_path: Path) -> None:
    """Write the compiled archive snapshot as deterministic JSON."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(
            compile_archive(archive_path), ensure_ascii=False, indent=2, sort_keys=True
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: build_data.py ARCHIVE_PATH OUTPUT_PATH")
    write_snapshot(Path(sys.argv[1]), Path(sys.argv[2]))
