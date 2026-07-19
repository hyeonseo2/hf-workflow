"""Compile archived translation workflow reports into a static JSON snapshot.

Reports normally come from the archived `reports/pr-N/` files. When a report
file is missing there, the snapshot can be backfilled from the HF Agent review
comment (`<!-- hf-agent-report -->`) posted on the translation PR itself.
"""

import argparse
import json
import os
import re
import urllib.request
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile


MANIFEST_PATH = re.compile(r"(?:^|/)reports/pr-(\d+)/manifest\.yaml$")
CHECK_LINE = re.compile(r"-\s+(PASS|WARN|FAIL):\s*(.+)$")
KEY_VALUE_LINE = re.compile(r"-\s+([^:]+):\s*(.*)$")
HEADING_LINE = re.compile(r"-\s+`(.+)`$")

AGENT_COMMENT_MARKER = "<!-- hf-agent-report -->"
AGENT_GATE_ROW = re.compile(r"\|\s*(Quality|SEO)\s*\|\s*([^|]+?)\s*\|")
AGENT_SECTION = re.compile(
    r"<summary>(Quality|SEO) report[^<]*</summary>\s*(.*?)\s*</details>", re.DOTALL
)
AGENT_EMOJI_LINE = re.compile(r"(✅|⛔|❌|🟠|⚠️)\s*(.+)")
AGENT_EMOJI_STATUS = {"✅": "pass", "⛔": "fail", "❌": "fail", "🟠": "warning", "⚠️": "warning"}
AGENT_SOURCE_LINE = re.compile(r"-\s+Source:\s+(https?://\S+)")
AGENT_FILE_LINE = re.compile(r"-\s+(?:Translation file|File):\s+`?([^`\s]+)`?")
POST_DATE = re.compile(r"(\d{4}-\d{2}-\d{2})-")
TRANSLATE_BRANCH_PREFIX = "translate/"
COMMENT_FILE_NAME = "PR 리뷰 코멘트 (hf-agent-report)"
REPORT_DETAIL_KEYS = {"quality": ("metrics",), "seo": ("frontmatter", "headings")}

GITHUB_API = "https://api.github.com"


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

    result["status"] = _derive_status(result["checks"])
    return result


def _derive_status(checks) -> str:
    statuses = {check["status"] for check in checks}
    for status in ("fail", "warning", "pass"):
        if status in statuses:
            return status
    return "warning"


def _emoji_report(text: str):
    """Parse the emoji-line report format used by the SEO eval markdown."""
    checks = []
    frontmatter = {}
    section = None
    for line in text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip().lower()
            continue
        match = AGENT_EMOJI_LINE.fullmatch(line.strip())
        if not match or section is None:
            continue
        status = AGENT_EMOJI_STATUS.get(match.group(1))
        if status is None:
            continue
        if section.startswith("frontmatter"):
            key, _, value = match.group(2).partition(":")
            frontmatter[key.strip()] = value.strip()
        elif "checks" in section:
            checks.append({"status": status, "text": match.group(2)})
    return checks, frontmatter


def parse_agent_comment(body) -> dict:
    """Extract per-skill reports from an `hf-agent-report` PR review comment."""
    if not isinstance(body, str) or AGENT_COMMENT_MARKER not in body:
        return {}
    summary_head = body.split("<details>", 1)[0]
    gates = {
        skill.lower(): "pass" if "Pass" in outcome else "fail"
        for skill, outcome in AGENT_GATE_ROW.findall(summary_head)
    }
    sections = {
        skill.lower(): content.strip() + "\n"
        for skill, content in AGENT_SECTION.findall(body)
    }

    comment = {}
    for skill in REPORT_DETAIL_KEYS:
        if skill not in gates and skill not in sections:
            continue
        content = sections.get(skill, "")
        parsed = parse_report(content)
        checks = parsed["checks"]
        frontmatter = parsed["frontmatter"]
        if not checks:
            checks, emoji_frontmatter = _emoji_report(content)
            frontmatter = frontmatter or emoji_frontmatter
        comment[skill] = {
            "status": gates.get(skill) or _derive_status(checks),
            "checks": checks,
            "content": content,
            "metrics": parsed["metrics"],
            "frontmatter": frontmatter,
            "headings": parsed["headings"],
        }
    return comment


def _missing_report(enabled: bool, file_name: str, detail_keys):
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


def _comment_report(skill_data: dict, enabled: bool, detail_keys):
    result = {
        "enabled": enabled,
        "available": True,
        "status": skill_data["status"],
        "checks": skill_data["checks"],
        "fileName": COMMENT_FILE_NAME,
        "content": skill_data["content"],
        "origin": "pr-comment",
    }
    for key in detail_keys:
        result[key] = skill_data[key]
    return result


def _report_result(zip_file: ZipFile, path: str, enabled: bool, detail_keys):
    file_name = Path(path).name
    if path not in zip_file.namelist():
        return _missing_report(enabled, file_name, detail_keys)

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
    return {
        "schemaVersion": 1,
        "sourceArchive": archive_path.name,
        "reportSnapshotAt": _snapshot_timestamp(reports),
        "repository": repositories.pop(),
        "reports": reports,
    }


def _snapshot_timestamp(reports) -> str:
    timestamps = [report["run"].get("created_at") for report in reports]
    return max(
        (timestamp for timestamp in timestamps if timestamp),
        key=datetime.fromisoformat,
    )


def _normalize_timestamp(value: str) -> str:
    return f"{value[:-1]}+00:00" if value.endswith("Z") else value


def apply_agent_comments(snapshot: dict, comments: dict) -> None:
    """Backfill reports that are missing from the archive with PR comment data."""
    for entry in snapshot["reports"]:
        comment = comments.get(entry["prNumber"])
        if not comment:
            continue
        for skill, detail_keys in REPORT_DETAIL_KEYS.items():
            skill_data = comment.get(skill)
            if entry[skill]["available"] or not skill_data:
                continue
            entry[skill] = _comment_report(skill_data, entry[skill]["enabled"], detail_keys)


def append_comment_entries(snapshot: dict, pulls, comments: dict) -> None:
    """Add rows for open translation PRs that only exist as review comments."""
    known = {entry["prNumber"] for entry in snapshot["reports"]}
    appended = False
    for pull in pulls:
        number = pull["number"]
        comment = comments.get(number)
        if number in known or not comment:
            continue
        content = "\n".join(
            comment[skill]["content"] for skill in REPORT_DETAIL_KEYS if skill in comment
        )
        source_match = AGENT_SOURCE_LINE.search(content)
        file_match = AGENT_FILE_LINE.search(content)
        file_path = file_match.group(1) if file_match else ""
        if "_posts/" in file_path:
            file_path = file_path[file_path.index("_posts/"):]
        branch = pull.get("branch", "")
        source_url = source_match.group(1) if source_match else ""
        slug = (
            branch[len(TRANSLATE_BRANCH_PREFIX):]
            if branch.startswith(TRANSLATE_BRANCH_PREFIX)
            else source_url.rstrip("/").rsplit("/", 1)[-1]
        )
        date_match = POST_DATE.search(file_path)
        reports = {
            skill: _comment_report(comment[skill], True, detail_keys)
            if skill in comment
            else _missing_report(True, COMMENT_FILE_NAME, detail_keys)
            for skill, detail_keys in REPORT_DETAIL_KEYS.items()
        }
        snapshot["reports"].append(
            {
                "prNumber": number,
                "run": {"id": f"pr-{number}-comment", "created_at": comment.get("createdAt", "")},
                "source": {
                    "url": source_url,
                    "slug": slug,
                    "title": pull.get("title") or slug,
                    "published_date": date_match.group(1) if date_match else "",
                },
                "translation": {
                    "target_repo": snapshot["repository"],
                    "branch": branch,
                    "file_path": file_path,
                    "pr_url": pull.get("htmlUrl", ""),
                    "locale": "ko",
                },
                "requestAvailable": False,
                "quality": reports["quality"],
                "seo": reports["seo"],
            }
        )
        appended = True
    if appended:
        snapshot["reports"].sort(key=lambda report: report["prNumber"], reverse=True)
        snapshot["reportSnapshotAt"] = _snapshot_timestamp(snapshot["reports"])


def _github_json(path: str, token: str = ""):
    request = urllib.request.Request(
        f"{GITHUB_API}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "hf-workflow-dashboard-snapshot",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def fetch_open_translation_pulls(repository: str, token: str = ""):
    pulls = _github_json(f"/repos/{repository}/pulls?state=open&per_page=100", token)
    return [
        {
            "number": pull["number"],
            "title": pull.get("title") or "",
            "branch": branch,
            "htmlUrl": pull.get("html_url") or "",
        }
        for pull in pulls
        if (branch := (pull.get("head") or {}).get("ref") or "").startswith(
            TRANSLATE_BRANCH_PREFIX
        )
    ]


def fetch_agent_comments(repository: str, pr_numbers, token: str = ""):
    comments = {}
    for number in pr_numbers:
        listing = _github_json(
            f"/repos/{repository}/issues/{number}/comments?per_page=100", token
        )
        for payload in reversed(listing):
            parsed = parse_agent_comment(payload.get("body"))
            if parsed:
                parsed["createdAt"] = _normalize_timestamp(payload.get("created_at") or "")
                comments[number] = parsed
                break
    return comments


def merge_github_reports(snapshot: dict, token: str = "") -> None:
    """Fetch and merge PR review comments for reports the archive lacks."""
    repository = snapshot["repository"]
    known = {entry["prNumber"] for entry in snapshot["reports"]}
    incomplete = [
        entry["prNumber"]
        for entry in snapshot["reports"]
        if not (entry["quality"]["available"] and entry["seo"]["available"])
    ]
    pulls = fetch_open_translation_pulls(repository, token)
    candidates = sorted(set(incomplete) | ({pull["number"] for pull in pulls} - known))
    comments = fetch_agent_comments(repository, candidates, token)
    apply_agent_comments(snapshot, comments)
    append_comment_entries(snapshot, pulls, comments)


def write_snapshot(
    archive_path: Path, output_path: Path, *, fetch_github: bool = False, token: str = ""
) -> None:
    """Write the compiled archive snapshot as deterministic JSON."""
    snapshot = compile_archive(archive_path)
    if fetch_github:
        merge_github_reports(snapshot, token)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive_path", type=Path)
    parser.add_argument("output_path", type=Path)
    parser.add_argument(
        "--archive-only",
        action="store_true",
        help="skip the GitHub PR comment backfill and use archived files alone",
    )
    args = parser.parse_args()
    write_snapshot(
        args.archive_path,
        args.output_path,
        fetch_github=not args.archive_only,
        token=os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN") or "",
    )
