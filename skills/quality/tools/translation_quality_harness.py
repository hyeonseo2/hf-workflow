from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import math
import re
import ssl
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[3]
QUALITY_ROOT = Path(__file__).resolve().parents[1]

FENCE_RE = re.compile(r"^(?P<fence>`{3,}|~{3,})(?P<info>.*)$")
INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
IMAGE_RE = re.compile(r"!\[[^\]]*]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
IMAGE_FULL_RE = re.compile(r"!\[([^\]]*)]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
LINK_RE = re.compile(r"(?<!!)\[[^\]]+]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
LINK_FULL_RE = re.compile(r"(?<!!)\[([^\]]+)]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
URL_RE = re.compile(r"https?://[A-Za-z0-9._~:/?#@!$&'*+,;=%-]+")
MODEL_ID_RE = re.compile(r"\b[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+\b")
PY_IDENTIFIER_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+\b")
ENV_VAR_RE = re.compile(r"\b[A-Z][A-Z0-9]*_[A-Z0-9_]*\b")
CLI_FLAG_RE = re.compile(r"(?<!\w)--[a-zA-Z0-9][a-zA-Z0-9_-]*")
LATEX_INLINE_RE = re.compile(r"\$[^$\n]+\$")
NUMBER_RE = re.compile(r"(?<![A-Za-z0-9_.-])\d+(?:\.\d+)*(?:%|ms|s|[kKmMgGtT]?[bB])?")
TODO_RE = re.compile(r"\b(?:TODO|FIXME|TBD)\b|\{\{|\}\}")
KOREAN_RE = re.compile(r"[가-힣]")
LETTER_RE = re.compile(r"[A-Za-z가-힣]")
ENGLISH_WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z'-]*\b")
EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002700-\U000027BF"
    "\U00002600-\U000026FF"
    "]+"
)

DEFAULT_STYLE_GUIDE_PATH = QUALITY_ROOT / "style" / "hf-blog-ko-translation-guide.md"
DEFAULT_STYLE_POLICY_PATH = QUALITY_ROOT / "configs" / "style_policy.yml"


@dataclass
class Issue:
    id: str
    category: str
    severity: str
    message: str
    segment_id: str = ""
    source_span: str = ""
    target_span: str = ""
    suggested_fix: str = ""
    reason: str = ""
    guide_rule: str = ""
    guide_section: str = ""


@dataclass
class Segment:
    id: str
    kind: str
    text: str
    hash: str
    path: str


@dataclass
class GlossaryEntry:
    source_term: str
    ko_term: str
    policy: str


@dataclass
class MetricConfig:
    qe_metric: str = "heuristic"
    enable_embedding_similarity: bool = True
    enable_chrf: bool = False
    qe_review_threshold: float = 0.55
    embedding_review_threshold: float = 0.08
    metric_cache_path: Path | None = None
    reference_path: Path | None = None
    enable_style_guide: bool = True
    style_guide_path: Path | None = DEFAULT_STYLE_GUIDE_PATH
    style_policy_path: Path | None = DEFAULT_STYLE_POLICY_PATH


@dataclass
class StylePolicy:
    version: int
    guide_path: Path
    policy_path: Path | None
    modal_terms: dict[str, list[str]]
    overstatement_pairs: dict[str, list[str]]
    discouraged_translationese: list[str]
    discouraged_title_terms: list[str]
    first_mention_terms: dict[str, dict[str, str]]
    forbid_added_emoji: bool
    list_consistency_enabled: bool
    require_korean_alt_text: bool


@dataclass
class MarkdownDoc:
    raw: str
    frontmatter: dict[str, str]
    body: str
    parse_errors: list[str]
    code_blocks: list[str]
    inline_code: list[str]
    link_targets: list[str]
    image_targets: list[str]
    urls: list[str]
    model_ids: list[str]
    python_identifiers: list[str]
    env_vars: list[str]
    cli_flags: list[str]
    latex_inline: list[str]
    numbers: list[str]
    table_shapes: list[list[int]]
    todo_markers: list[str]
    segments: list[Segment]
    source_hash: str


@dataclass
class FetchedSource:
    text: str
    source_format: str
    source_path: str


def read_simple_manifest(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    section = ""
    for raw_line in path.read_text(encoding="utf-8").splitlines():
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


def strip_frontmatter(markdown: str) -> tuple[dict[str, str], str]:
    if not markdown.startswith("---\n"):
        return {}, markdown
    end = markdown.find("\n---", 4)
    if end == -1:
        return {}, markdown
    frontmatter_text = markdown[4:end]
    body = markdown[end + 4 :]
    data: dict[str, str] = {}
    current_key = ""
    current_values: list[str] = []
    for line in frontmatter_text.splitlines():
        list_item = re.match(r"^\s*-\s+(.*)$", line)
        if list_item and current_key:
            current_values.append(list_item.group(1).strip().strip('"'))
            data[current_key] = "\n".join(current_values)
            continue
        current_values = []
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            continue
        current_key, value = match.groups()
        data[current_key] = value.strip().strip('"')
    return data, body


def strip_workflow_scaffold(body: str) -> str:
    lines = body.splitlines()
    output: list[str] = []
    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        if stripped.startswith("> Source:"):
            index += 1
            continue
        if stripped == "* TOC":
            index += 1
            while index < len(lines) and lines[index].strip() in {"{:toc}", "<!--toc-->", ""}:
                index += 1
            continue
        if re.match(r"^_이 글은 Hugging Face 블로그의 .*한국어로 번역한 글입니다\._$", stripped):
            index += 1
            continue
        if stripped == "<!--":
            comment_lines = [stripped]
            index += 1
            while index < len(lines):
                comment_lines.append(lines[index].strip())
                if lines[index].strip() == "-->":
                    index += 1
                    break
                index += 1
            comment_text = "\n".join(comment_lines)
            if "Review instructions:" in comment_text:
                continue
            output.extend(comment_lines)
            continue
        if stripped == "---":
            previous_nonblank = next((line.strip() for line in reversed(output) if line.strip()), "")
            remaining_nonblank = next((line.strip() for line in lines[index + 1 :] if line.strip()), "")
            if not previous_nonblank and remaining_nonblank.startswith("#"):
                index += 1
                continue
            if previous_nonblank.startswith("_이 글은 Hugging Face 블로그의") or remaining_nonblank.startswith("<!--"):
                index += 1
                continue
        output.append(lines[index])
        index += 1
    return "\n".join(output)


def strip_heading_anchors(body: str) -> str:
    return re.sub(r"(?m)^(#{1,6}\s+.+?)\s+\{#[A-Za-z0-9_-]+}$", r"\1", body)


def parse_code_blocks(body: str) -> tuple[list[str], str, list[str]]:
    lines = body.splitlines()
    code_blocks: list[str] = []
    body_without_code: list[str] = []
    parse_errors: list[str] = []
    in_fence = False
    current: list[str] = []
    fence_marker = ""

    for line in lines:
        fence = FENCE_RE.match(line.strip())
        if fence and not in_fence:
            in_fence = True
            fence_marker = fence.group("fence")[0]
            current = [line]
            body_without_code.append("")
            continue
        if in_fence:
            current.append(line)
            if fence and fence.group("fence")[0] == fence_marker:
                code_blocks.append("\n".join(current))
                current = []
                in_fence = False
                fence_marker = ""
            body_without_code.append("")
            continue
        body_without_code.append(line)

    if in_fence:
        parse_errors.append("Unclosed fenced code block.")
        code_blocks.append("\n".join(current))

    return code_blocks, "\n".join(body_without_code), parse_errors


def table_shapes(body_without_code: str) -> list[list[int]]:
    shapes: list[list[int]] = []
    current: list[int] = []
    for line in body_without_code.splitlines() + [""]:
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2:
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            current.append(len(cells))
            continue
        if current:
            shapes.append(current)
            current = []
    return shapes


def normalize_segment_text(text: str) -> str:
    text = re.sub(r"!\[([^\]]*)]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)]\([^)]+\)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def segment_hash(text: str) -> str:
    normalized = normalize_segment_text(text)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def is_table_separator(cells: list[str]) -> bool:
    if not cells:
        return False
    return all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def extract_segments(body_without_code: str) -> list[Segment]:
    segments: list[Segment] = []
    paragraph: list[str] = []
    paragraph_start = 0

    def add_segment(kind: str, text: str, line_number: int) -> None:
        normalized = normalize_segment_text(text)
        if not normalized:
            return
        segment_id = f"{kind[0]}_{len(segments) + 1:03d}"
        segments.append(
            Segment(
                id=segment_id,
                kind=kind,
                text=normalized,
                hash=segment_hash(normalized),
                path=f"{kind}:{line_number}",
            )
        )

    def flush_paragraph(line_number: int) -> None:
        nonlocal paragraph
        nonlocal paragraph_start
        if paragraph:
            add_segment("paragraph", " ".join(paragraph), paragraph_start or line_number)
            paragraph = []
            paragraph_start = 0

    for index, line in enumerate(body_without_code.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            flush_paragraph(index)
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_paragraph(index)
            add_segment("heading", heading.group(2), index)
            continue

        list_item = re.match(r"^(?:[-*+]|\d+[.)])\s+(.+)$", stripped)
        if list_item:
            flush_paragraph(index)
            add_segment("list_item", list_item.group(1), index)
            continue

        if stripped.startswith(">"):
            flush_paragraph(index)
            add_segment("blockquote", stripped.lstrip("> ").strip(), index)
            continue

        if stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2:
            flush_paragraph(index)
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if not is_table_separator(cells):
                add_segment("table_row", " | ".join(cells), index)
            continue

        if not paragraph:
            paragraph_start = index
        paragraph.append(stripped)

    flush_paragraph(len(body_without_code.splitlines()) + 1)
    return segments


def normalized_numbers(text: str) -> list[str]:
    values = []
    for match in NUMBER_RE.finditer(text):
        line_start = text.rfind("\n", 0, match.start()) + 1
        prefix = text[line_start : match.start()]
        suffix = text[match.end() : match.end() + 2]
        if not prefix.strip() and suffix.startswith("."):
            continue
        value = re.sub(r"\s+", "", match.group(0))
        values.append(value)
    return values


def strip_markdown_targets(text: str) -> str:
    text = IMAGE_FULL_RE.sub(r"\1", text)
    text = LINK_FULL_RE.sub(r"\1", text)
    return text


def text_for_bare_urls(text: str) -> str:
    text = IMAGE_FULL_RE.sub("", text)
    text = LINK_FULL_RE.sub(r"\1", text)
    return text


def text_for_number_tokens(text: str) -> str:
    text = strip_markdown_targets(text)
    text = INLINE_CODE_RE.sub("", text)
    text = URL_RE.sub("", text)
    text = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(text)


def extract_model_ids(text: str) -> list[str]:
    values: list[str] = []
    skipped_prefixes = ("blog/", "assets/", "images/", "_posts/", "static/", "datasets/")
    skipped_values = {
        "allocating/refilling",
        "and/or",
        "client/server",
        "elementwise/reduction",
        "forward/backward",
        "guides/jobs",
        "shapes/dtypes",
        "train/eval",
    }
    skipped_orgs = {"and", "client", "elementwise", "forward", "guides", "shapes", "tmp", "train"}
    for match in MODEL_ID_RE.finditer(text):
        value = match.group(0)
        before = text[max(0, match.start() - 24) : match.start()]
        if "://" in before:
            continue
        if value.startswith(skipped_prefixes):
            continue
        if value.lower() in skipped_values:
            continue
        org, repo = value.split("/", 1)
        if org.startswith("-") or org.replace(".", "").isdigit():
            continue
        if org.lower().rstrip("_") in skipped_orgs:
            continue
        likely_repo_name = any(char in repo for char in "-_.") or any(char.isdigit() for char in repo) or any(char.isupper() for char in repo)
        if not likely_repo_name:
            continue
        if re.fullmatch(r"[a-zA-Z0-9-]+\.[a-zA-Z]{2,}/[a-zA-Z0-9_.-]+", value):
            continue
        values.append(value)
    return values


def extract_python_identifiers(text: str) -> list[str]:
    values: list[str] = []
    for match in PY_IDENTIFIER_RE.finditer(text):
        value = match.group(0)
        before = text[max(0, match.start() - 24) : match.start()]
        if "://" in before:
            continue
        if value.lower() in {"e.g", "i.e"}:
            continue
        if re.search(r"\.(?:com|co|org|net|io|dev|space|ai)(?:\.|$)", value):
            continue
        values.append(value)
    return values


def fetch_text(url: str, timeout: int = 20) -> str:
    parsed = urllib.parse.urlparse(url)
    request: str | urllib.request.Request
    if parsed.scheme in {"http", "https"}:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "hf-workflow-translation-quality-harness/0.5",
                "Accept": "text/markdown,text/plain,text/html;q=0.8,*/*;q=0.5",
            },
        )
    else:
        request = url
    context = None
    if parsed.scheme == "https":
        try:
            import certifi  # type: ignore[import-not-found]

            context = ssl.create_default_context(cafile=certifi.where())
        except ImportError:
            context = ssl.create_default_context()
    with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def looks_like_markdown(text: str) -> bool:
    sample = text.lstrip()[:1000]
    return sample.startswith("---") or bool(re.search(r"(?m)^title:\s+", sample))


def unique_ordered(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def hf_blog_raw_markdown_candidates(source_url: str, manifest: dict[str, str]) -> list[str]:
    parsed = urllib.parse.urlparse(source_url)
    if parsed.netloc != "huggingface.co" or not parsed.path.startswith("/blog/"):
        return []
    blog_path = parsed.path.removeprefix("/blog/").strip("/")
    slug = manifest.get("source.slug", "")
    bases = unique_ordered(
        [
            blog_path,
            Path(blog_path).name,
            slug,
        ]
    )
    paths: list[str] = []
    for base in bases:
        if base.endswith((".md", ".mdx")):
            paths.append(base)
        else:
            paths.extend([f"{base}.md", f"{base}.mdx", f"{base}/index.md", f"{base}/index.mdx"])
    return [f"https://raw.githubusercontent.com/huggingface/blog/main/{path}" for path in unique_ordered(paths)]


def extract_html_main_text(raw_html: str) -> str:
    def fragment_to_text(fragment: str) -> str:
        fragment = re.sub(r"(?is)<(script|style|svg|noscript)\b.*?</\1>", " ", fragment)
        fragment = re.sub(
            r"(?is)<pre\b[^>]*>(.*?)</pre>",
            lambda m: "\n```\n" + html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() + "\n```\n",
            fragment,
        )
        fragment = re.sub(r"(?i)<br\s*/?>", "\n", fragment)
        fragment = re.sub(r"(?i)</(p|div|section|article|main|li|ul|ol|h[1-6]|blockquote|tr)>", "\n", fragment)
        fragment = re.sub(r"<[^>]+>", " ", fragment)
        fragment = html.unescape(fragment)
        lines = [re.sub(r"[ \t]+", " ", line).strip() for line in fragment.splitlines()]
        return "\n".join(line for line in lines if line)

    candidates = [fragment_to_text(raw_html)]
    for tag in ["main", "article"]:
        for match in re.finditer(rf"<{tag}\b[^>]*>(.*?)</{tag}>", raw_html, flags=re.IGNORECASE | re.DOTALL):
            candidates.append(fragment_to_text(match.group(1)))
    return max(candidates, key=len)


def fetch_source_document(source_url: str, manifest: dict[str, str]) -> FetchedSource | None:
    for candidate in hf_blog_raw_markdown_candidates(source_url, manifest):
        try:
            text = fetch_text(candidate)
        except (OSError, urllib.error.URLError, urllib.error.HTTPError):
            continue
        if looks_like_markdown(text):
            return FetchedSource(text=text, source_format="url_markdown", source_path=candidate)

    try:
        text = fetch_text(source_url)
    except (OSError, urllib.error.URLError, urllib.error.HTTPError):
        return None
    if looks_like_markdown(text):
        return FetchedSource(text=text, source_format="url_markdown", source_path=source_url)
    return FetchedSource(text=extract_html_main_text(text), source_format="url_html_text", source_path=source_url)


def markdown_doc(markdown: str) -> MarkdownDoc:
    frontmatter, body = strip_frontmatter(markdown)
    body = strip_heading_anchors(strip_workflow_scaffold(body))
    code_blocks, body_without_code, parse_errors = parse_code_blocks(body)
    link_targets = LINK_RE.findall(body_without_code)
    image_targets = IMAGE_RE.findall(body_without_code)
    bare_url_text = text_for_bare_urls(body_without_code)
    protected_text = strip_markdown_targets(body_without_code)
    number_text = text_for_number_tokens(body_without_code)
    urls = URL_RE.findall(bare_url_text)
    return MarkdownDoc(
        raw=markdown,
        frontmatter=frontmatter,
        body=body,
        parse_errors=parse_errors,
        code_blocks=code_blocks,
        inline_code=INLINE_CODE_RE.findall(body_without_code),
        link_targets=link_targets,
        image_targets=image_targets,
        urls=urls,
        model_ids=extract_model_ids(protected_text),
        python_identifiers=extract_python_identifiers(protected_text),
        env_vars=ENV_VAR_RE.findall(body_without_code),
        cli_flags=CLI_FLAG_RE.findall(body_without_code),
        latex_inline=LATEX_INLINE_RE.findall(body_without_code),
        numbers=normalized_numbers(number_text),
        table_shapes=table_shapes(body_without_code),
        todo_markers=TODO_RE.findall(body_without_code),
        segments=extract_segments(body_without_code),
        source_hash=hashlib.sha256(markdown.encode("utf-8")).hexdigest(),
    )


def counter_diff(source: Iterable[str], target: Iterable[str]) -> tuple[list[str], list[str]]:
    source_counter = Counter(source)
    target_counter = Counter(target)
    missing = sorted((source_counter - target_counter).elements())
    extra = sorted((target_counter - source_counter).elements())
    return missing, extra


def code_hashes(blocks: list[str]) -> list[str]:
    return [hashlib.sha256(block.encode("utf-8")).hexdigest() for block in blocks]


def issue(
    issues: list[Issue],
    category: str,
    severity: str,
    message: str,
    *,
    segment_id: str = "",
    source_span: str = "",
    target_span: str = "",
    suggested_fix: str = "",
    reason: str = "",
    guide_rule: str = "",
    guide_section: str = "",
) -> None:
    issues.append(
        Issue(
            id=f"QL-{len(issues) + 1:03d}",
            category=category,
            severity=severity,
            message=message,
            segment_id=segment_id,
            source_span=source_span,
            target_span=target_span,
            suggested_fix=suggested_fix,
            reason=reason,
            guide_rule=guide_rule,
            guide_section=guide_section,
        )
    )


def compare_counter(
    issues: list[Issue],
    category: str,
    label: str,
    source_values: Iterable[str],
    target_values: Iterable[str],
    severity: str = "critical",
) -> None:
    missing, extra = counter_diff(source_values, target_values)
    if not missing and not extra:
        return
    message = f"{label} mismatch."
    parts = []
    if missing:
        parts.append(f"missing={missing[:8]}")
    if extra:
        parts.append(f"extra={extra[:8]}")
    gate_label = "Hard gate" if severity == "critical" else "Review gate"
    issue(
        issues,
        category,
        severity,
        message,
        source_span=", ".join(missing[:8]),
        target_span=", ".join(extra[:8]),
        suggested_fix=f"Preserve source {label} exactly.",
        reason=f"{gate_label} exact-match validator failed: " + "; ".join(parts),
    )


def normalize_lookup_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold()).strip()


def term_present(text: str, term: str) -> bool:
    normalized_text = normalize_lookup_text(text)
    normalized_term = normalize_lookup_text(term)
    if not normalized_term:
        return False
    pattern = rf"(?<![0-9a-zA-Z가-힣_/-]){re.escape(normalized_term)}(?![0-9a-zA-Z가-힣_/-])"
    return re.search(pattern, normalized_text) is not None


def load_glossary(paths: list[Path] | None = None) -> list[GlossaryEntry]:
    glossary_paths = paths
    if glossary_paths is None:
        glossary_paths = sorted((QUALITY_ROOT / "glossary").glob("*.tsv"))
    entries: list[GlossaryEntry] = []
    for path in glossary_paths:
        if not path.exists():
            continue
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            for row in reader:
                source_term = (row.get("source_term") or "").strip()
                ko_term = (row.get("ko_term") or "").strip()
                policy = (row.get("policy") or "").strip()
                if source_term and ko_term and policy:
                    entries.append(GlossaryEntry(source_term, ko_term, policy))
    return entries


def load_translation_memory(path: Path | None) -> dict[str, str]:
    if path is None or not path.exists():
        return {}
    memory: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        source = str(row.get("source", "")).strip()
        target = str(row.get("target", "")).strip()
        if source and target:
            memory[normalize_lookup_text(source)] = target
    return memory


def segment_to_json(segment: Segment) -> dict[str, str]:
    return asdict(segment)


def align_segments(source: MarkdownDoc, target: MarkdownDoc) -> list[dict[str, str]]:
    alignments: list[dict[str, str]] = []
    for index, (source_segment, target_segment) in enumerate(zip(source.segments, target.segments), start=1):
        alignments.append(
            {
                "alignment_id": f"a_{index:03d}",
                "source_id": source_segment.id,
                "target_id": target_segment.id,
                "source_hash": source_segment.hash,
                "target_hash": target_segment.hash,
                "source_kind": source_segment.kind,
                "target_kind": target_segment.kind,
                "source_text": source_segment.text,
                "target_text": target_segment.text,
            }
        )
    return alignments


def validate_segment_coverage(issues: list[Issue], source: MarkdownDoc, target: MarkdownDoc) -> None:
    source_count = len(source.segments)
    target_count = len(target.segments)
    if target_count < source_count:
        issue(
            issues,
            "accuracy",
            "major",
            "Source segment coverage is low.",
            source_span=f"source_segments={source_count}",
            target_span=f"target_segments={target_count}",
            suggested_fix="Check for omitted paragraphs, headings, list items, or table cells.",
            reason="Segment count validator found fewer target text segments than source text segments.",
        )
    elif target_count > source_count:
        issue(
            issues,
            "accuracy",
            "major",
            "Target has additional text segments.",
            source_span=f"source_segments={source_count}",
            target_span=f"target_segments={target_count}",
            suggested_fix="Check for duplicated or invented paragraphs.",
            reason="Segment count validator found more target text segments than source text segments.",
        )

    normalized_targets = [
        normalize_lookup_text(segment.text)
        for segment in target.segments
        if len(normalize_lookup_text(segment.text)) >= 20
    ]
    duplicates = sorted(text for text, count in Counter(normalized_targets).items() if count > 1)
    if duplicates:
        issue(
            issues,
            "accuracy",
            "major",
            "Duplicate target segments detected.",
            target_span=" | ".join(duplicates[:5]),
            suggested_fix="Remove repeated translated segments unless the source intentionally repeats them.",
            reason="Duplicate detector found repeated normalized target segments.",
        )

    source_length = sum(len(segment.text) for segment in source.segments)
    target_length = sum(len(segment.text) for segment in target.segments)
    ratio = target_length / max(1, source_length)
    if ratio < 0.35 or ratio > 2.60:
        issue(
            issues,
            "accuracy",
            "major",
            "Target/source segment length ratio is outside the expected range.",
            source_span=f"source_chars={source_length}",
            target_span=f"target_chars={target_length}, ratio={ratio:.2f}",
            suggested_fix="Check for omitted prose, over-expanded translation, or invented content.",
            reason="Length ratio validator uses configured Phase 2 review thresholds.",
        )


def validate_glossary(issues: list[Issue], source: MarkdownDoc, target: MarkdownDoc, glossary: list[GlossaryEntry]) -> None:
    source_text = "\n".join(segment.text for segment in source.segments)
    target_text = "\n".join(segment.text for segment in target.segments)
    for entry in glossary:
        if not term_present(source_text, entry.source_term):
            continue

        source_term_in_target = term_present(target_text, entry.source_term)
        ko_term_in_target = normalize_lookup_text(entry.ko_term) in normalize_lookup_text(target_text)
        policy = entry.policy

        if policy == "required" and not ko_term_in_target:
            issue(
                issues,
                "terminology",
                "major",
                "Required glossary term is not used.",
                source_span=entry.source_term,
                target_span=entry.ko_term,
                suggested_fix=f"Use `{entry.ko_term}` for `{entry.source_term}`.",
                reason="Glossary policy required the Korean term.",
            )
        elif policy == "preferred" and not ko_term_in_target:
            issue(
                issues,
                "terminology",
                "minor",
                "Preferred glossary term is not used.",
                source_span=entry.source_term,
                target_span=entry.ko_term,
                suggested_fix=f"Prefer `{entry.ko_term}` for `{entry.source_term}`.",
                reason="Glossary policy marked this Korean term as preferred.",
            )
        elif policy == "preserve_product_name" and not source_term_in_target:
            issue(
                issues,
                "terminology",
                "major",
                "Product or library name was not preserved.",
                source_span=entry.source_term,
                suggested_fix=f"Preserve `{entry.source_term}` exactly.",
                reason="Glossary policy requires preserving this product/library/model term.",
            )
        elif policy == "preserve_or_first_mention" and not (source_term_in_target or ko_term_in_target):
            issue(
                issues,
                "terminology",
                "minor",
                "First-mention glossary policy was not satisfied.",
                source_span=entry.source_term,
                target_span=entry.ko_term,
                suggested_fix=f"Use `{entry.ko_term}` on first mention or preserve `{entry.source_term}`.",
                reason="Glossary policy allows preservation or first-mention form.",
            )


def translation_memory_match_count(source: MarkdownDoc | None, memory: dict[str, str]) -> int:
    if source is None or not memory:
        return 0
    return sum(1 for segment in source.segments if normalize_lookup_text(segment.text) in memory)


def default_style_policy(style_guide_path: Path | None = None, style_policy_path: Path | None = None) -> StylePolicy:
    return StylePolicy(
        version=read_policy_version(style_policy_path),
        guide_path=style_guide_path or DEFAULT_STYLE_GUIDE_PATH,
        policy_path=style_policy_path,
        modal_terms={
            "may": ["수 있습니다", "일 수 있습니다"],
            "can": ["수 있습니다"],
            "should": ["좋습니다", "해야 합니다"],
            "must": ["반드시", "해야 합니다"],
            "up to": ["최대"],
            "in some cases": ["일부 경우"],
            "not always": ["항상", "것은 아닙니다"],
        },
        overstatement_pairs={
            "can improve": ["개선합니다"],
            "may improve": ["개선합니다"],
            "promising": ["놀라운", "압도적인"],
            "significant": ["압도적인"],
            "production-ready": ["즉시 상용화"],
            "simple guide": ["완전 정복"],
        },
        discouraged_translationese=[
            "에 의해",
            "하는 것에 있어",
            "를 가지",
            "을 가지",
            "사용되어질",
            "로 하여금",
            "후드 아래",
            "박스 밖",
            "뛰어들어",
        ],
        discouraged_title_terms=["완전 정복", "혁신", "역대 최고", "예술의 경지"],
        first_mention_terms={
            "fine-tuning": {"ko": "미세 조정", "required_first": "미세 조정(fine-tuning)"},
            "checkpoint": {"ko": "체크포인트", "required_first": "체크포인트(checkpoint)"},
            "quantization": {"ko": "양자화", "required_first": "양자화(quantization)"},
            "alignment": {"ko": "정렬", "required_first": "정렬(alignment)"},
            "serving": {"ko": "서빙", "required_first": "서빙(serving)"},
            "latency": {"ko": "지연 시간", "required_first": "지연 시간(latency)"},
            "throughput": {"ko": "처리량", "required_first": "처리량(throughput)"},
        },
        forbid_added_emoji=True,
        list_consistency_enabled=True,
        require_korean_alt_text=True,
    )


def read_policy_version(style_policy_path: Path | None) -> int:
    if style_policy_path is None or not style_policy_path.exists():
        return 0
    for line in style_policy_path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^version:\s*(\d+)\s*$", line.strip())
        if match:
            return int(match.group(1))
    return 0


def parse_yaml_scalar(value: str) -> object:
    value = value.strip()
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    return value


def load_style_policy(style_guide_path: Path | None, style_policy_path: Path | None) -> StylePolicy:
    policy_path = style_policy_path or DEFAULT_STYLE_POLICY_PATH
    policy = default_style_policy(style_guide_path or DEFAULT_STYLE_GUIDE_PATH, policy_path)
    if not policy_path.exists():
        return policy

    modal_terms: dict[str, list[str]] = {}
    overstatement_pairs: dict[str, list[str]] = {}
    translationese: list[str] = []
    title_terms: list[str] = []
    first_mention_terms: dict[str, dict[str, str]] = {}
    path_by_level: dict[int, str] = {}
    for raw_line in policy_path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.strip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        level = indent // 2
        stripped = raw_line.strip()
        for existing in list(path_by_level):
            if existing >= level:
                del path_by_level[existing]

        if stripped.startswith("- "):
            value = str(parse_yaml_scalar(stripped[2:]))
            path = [path_by_level[index] for index in sorted(path_by_level)]
            if "modal_strength" in path and "source_terms" in path and path:
                modal_terms.setdefault(path[-1], []).append(value)
            elif "overstatement" in path and "risky_pairs" in path and path:
                overstatement_pairs.setdefault(path[-1], []).append(value)
            elif "translationese" in path and "discouraged" in path:
                translationese.append(value)
            elif "title_quality" in path and "discouraged" in path:
                title_terms.append(value)
            continue

        if ":" not in stripped:
            continue
        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        path_by_level[level] = key
        path = [path_by_level[index] for index in sorted(path_by_level)]
        if not raw_value:
            continue
        value = parse_yaml_scalar(raw_value)
        if path == ["review_rules", "emoji", "forbid_added_emoji"]:
            policy.forbid_added_emoji = bool(value)
        elif path == ["review_rules", "list_consistency", "enabled"]:
            policy.list_consistency_enabled = bool(value)
        elif path == ["review_rules", "alt_text", "require_korean_when_source_english"]:
            policy.require_korean_alt_text = bool(value)
        elif len(path) == 3 and path[0] == "first_mention_terms" and path[2] in {"ko", "required_first"}:
            first_mention_terms.setdefault(path[1], {})[path[2]] = str(value)

    if modal_terms:
        policy.modal_terms = modal_terms
    if overstatement_pairs:
        policy.overstatement_pairs = overstatement_pairs
    if translationese:
        policy.discouraged_translationese = translationese
    if title_terms:
        policy.discouraged_title_terms = title_terms
    if first_mention_terms:
        policy.first_mention_terms = first_mention_terms
    return policy


def contains_any(text: str, phrases: Iterable[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def style_issue(
    issues: list[Issue],
    category: str,
    severity: str,
    message: str,
    guide_rule: str,
    guide_section: str,
    *,
    segment_id: str = "",
    source_span: str = "",
    target_span: str = "",
    suggested_fix: str = "",
    reason: str = "",
) -> None:
    issue(
        issues,
        category,
        severity,
        message,
        segment_id=segment_id,
        source_span=source_span,
        target_span=target_span,
        suggested_fix=suggested_fix,
        reason=reason,
        guide_rule=guide_rule,
        guide_section=guide_section,
    )


def validate_modal_strength(
    issues: list[Issue],
    source: MarkdownDoc,
    target: MarkdownDoc,
    policy: StylePolicy,
) -> None:
    guide_section = "4. 의미·조건·확신의 강도는 절대 바꾸지 않습니다"
    for alignment in align_segments(source, target):
        source_text = normalize_lookup_text(str(alignment["source_text"]))
        target_text = str(alignment["target_text"])
        normalized_target = normalize_lookup_text(target_text)
        for source_term, expected_targets in policy.modal_terms.items():
            if source_term not in source_text:
                continue
            if source_term == "not always":
                valid = all(term in target_text for term in expected_targets)
            else:
                valid = contains_any(target_text, expected_targets) or contains_any(normalized_target, expected_targets)
            if valid:
                continue
            style_issue(
                issues,
                "accuracy",
                "major",
                "Modal or certainty strength may have changed.",
                "modal_strength",
                guide_section,
                segment_id=str(alignment["target_id"]),
                source_span=source_term,
                target_span=target_text,
                suggested_fix=f"Preserve the strength of `{source_term}` using: {', '.join(expected_targets)}.",
                reason="The style guide requires preserving may/can/should/must/up to/in some cases/not always strength.",
            )


def validate_overstatement(
    issues: list[Issue],
    source: MarkdownDoc,
    target: MarkdownDoc,
    policy: StylePolicy,
) -> None:
    guide_section = "19. 원문보다 과장하지 않습니다"
    for alignment in align_segments(source, target):
        source_text = normalize_lookup_text(str(alignment["source_text"]))
        target_text = str(alignment["target_text"])
        for source_phrase, risky_targets in policy.overstatement_pairs.items():
            if source_phrase not in source_text:
                continue
            if source_phrase == "up to" and "최대" in target_text:
                continue
            for risky_target in risky_targets:
                if risky_target not in target_text:
                    continue
                style_issue(
                    issues,
                    "style_locale",
                    "major",
                    "Translation appears stronger or more promotional than the source.",
                    "overstatement",
                    guide_section,
                    segment_id=str(alignment["target_id"]),
                    source_span=source_phrase,
                    target_span=risky_target,
                    suggested_fix="Use a weaker expression that preserves the source claim strength.",
                    reason="The style guide forbids strengthening performance, certainty, or marketing claims.",
                )


def validate_information_addition(issues: list[Issue], source: MarkdownDoc, target: MarkdownDoc) -> None:
    guide_section = "5. 정보 추가는 원칙적으로 금지하되, 연결 문장은 허용합니다"
    source_markers = ["because", "due to", "thanks to", "as a result", "therefore"]
    target_markers = ["때문에", "덕분에", "으로 인해", "따라서", "그러므로"]
    for alignment in align_segments(source, target):
        source_text = normalize_lookup_text(str(alignment["source_text"]))
        target_text = str(alignment["target_text"])
        if any(marker in source_text for marker in source_markers):
            continue
        for marker in target_markers:
            if marker not in target_text:
                continue
            style_issue(
                issues,
                "accuracy",
                "major",
                "Translation may add a causal explanation that is not in the source.",
                "information_addition",
                guide_section,
                segment_id=str(alignment["target_id"]),
                target_span=marker,
                suggested_fix="Remove invented causal explanation unless the source explicitly states it.",
                reason="The style guide forbids adding technical explanations, reasons, examples, or conclusions.",
            )


def validate_translationese(issues: list[Issue], target: MarkdownDoc, policy: StylePolicy) -> None:
    guide_section = "17. 번역투를 줄입니다"
    seen: set[str] = set()
    for phrase in policy.discouraged_translationese:
        if phrase not in target.body or phrase in seen:
            continue
        seen.add(phrase)
        style_issue(
            issues,
            "fluency",
            "minor",
            "Translationese expression found.",
            "translationese",
            guide_section,
            target_span=phrase,
            suggested_fix="Rewrite the sentence in natural Korean.",
            reason="The style guide lists this expression as translationese to avoid.",
        )


def validate_title_style(issues: list[Issue], target: MarkdownDoc, policy: StylePolicy) -> None:
    guide_section = "10. 제목: 직역보다 전달력, 검색성, 글의 기대값을 우선합니다"
    title = target.frontmatter.get("title", "")
    for phrase in policy.discouraged_title_terms:
        if phrase not in title:
            continue
        style_issue(
            issues,
            "style_locale",
            "minor",
            "Title may be exaggerated or clickbait-like.",
            "title_quality",
            guide_section,
            target_span=phrase,
            suggested_fix="Use a concise, searchable title that does not overstate the source.",
            reason="The style guide warns against exaggerated title expressions.",
        )


def validate_intro_closing_style(issues: list[Issue], target: MarkdownDoc) -> None:
    guide_section = "20. 기술 블로그에 추가하면 좋은 전용 규칙"
    risky_phrases = ["이 포스트", "걸어 다니", "기다릴 수 없습니다", "채널 고정", "마법이 일어"]
    candidate_segments = target.segments[:2] + target.segments[-2:]
    for segment in candidate_segments:
        for phrase in risky_phrases:
            if phrase not in segment.text:
                continue
            style_issue(
                issues,
                "style_locale",
                "minor",
                "Intro or closing phrasing sounds mechanically translated.",
                "intro_closing_style",
                guide_section,
                segment_id=segment.id,
                target_span=phrase,
                suggested_fix="Rewrite the intro or closing in natural Korean blog style.",
                reason="The style guide recommends natural Korean openings and closings over mechanical source phrasing.",
            )


def extract_list_item_forms(markdown_body: str) -> list[str]:
    _, body_without_code, _ = parse_code_blocks(markdown_body)
    forms: list[str] = []
    for line in body_without_code.splitlines():
        match = re.match(r"^\s*(?:[-*+]|\d+[.)])\s+(.+)$", line)
        if not match:
            continue
        item = match.group(1).strip()
        if re.search(r"(다|요|니다)[.!?]?$", item):
            forms.append("sentence")
        else:
            forms.append("phrase")
    return forms


def validate_list_consistency(issues: list[Issue], target: MarkdownDoc, policy: StylePolicy) -> None:
    if not policy.list_consistency_enabled:
        return
    forms = extract_list_item_forms(target.body)
    if len(set(forms)) <= 1:
        return
    style_issue(
        issues,
        "style_locale",
        "minor",
        "List mixes sentence-style and phrase-style endings.",
        "list_consistency",
        "16. 리스트: 끝맺음과 정보 단위를 통일합니다",
        target_span=", ".join(forms),
        suggested_fix="Use either sentence-style endings or phrase-style endings consistently within one list.",
        reason="The style guide requires consistent list item endings.",
    )


def validate_emoji_delta(issues: list[Issue], source: MarkdownDoc, target: MarkdownDoc, policy: StylePolicy) -> None:
    if not policy.forbid_added_emoji:
        return
    source_emoji = EMOJI_RE.findall(source.raw)
    target_emoji = EMOJI_RE.findall(target.raw)
    if len(target_emoji) <= len(source_emoji):
        return
    style_issue(
        issues,
        "style_locale",
        "minor",
        "Target adds emoji that are not present in the source.",
        "emoji_delta",
        "12. 이모지: 새로 추가하지 않고, 원문 이모지는 의미가 있을 때만 유지합니다",
        target_span=" ".join(target_emoji),
        suggested_fix="Remove emojis that were not present in the source.",
        reason="The style guide forbids adding new emojis during translation.",
    )


def has_korean(text: str) -> bool:
    return KOREAN_RE.search(text) is not None


def image_pairs_by_path(markdown: str) -> dict[str, str]:
    return {path: alt for alt, path in IMAGE_FULL_RE.findall(markdown)}


def link_pairs_by_target(markdown: str) -> dict[str, str]:
    return {target: label for label, target in LINK_FULL_RE.findall(markdown)}


def validate_alt_text_and_link_text(issues: list[Issue], source: MarkdownDoc, target: MarkdownDoc, policy: StylePolicy) -> None:
    if policy.require_korean_alt_text:
        source_images = image_pairs_by_path(source.body)
        target_images = image_pairs_by_path(target.body)
        for path, source_alt in source_images.items():
            target_alt = target_images.get(path, "")
            if not source_alt or has_korean(source_alt) or has_korean(target_alt):
                continue
            style_issue(
                issues,
                "fluency",
                "minor",
                "Image alt text appears untranslated.",
                "alt_text_caption",
                "20.5 이미지 캡션과 alt text도 번역합니다",
                source_span=source_alt,
                target_span=target_alt,
                suggested_fix="Translate image alt text while preserving the image path.",
                reason="The style guide requires translating image alt text and captions.",
            )

    source_links = link_pairs_by_target(source.body)
    target_links = link_pairs_by_target(target.body)
    for target_url, source_label in source_links.items():
        target_label = target_links.get(target_url, "")
        if not source_label or has_korean(source_label) or has_korean(target_label):
            continue
        style_issue(
            issues,
            "fluency",
            "minor",
            "Link text appears untranslated.",
            "link_text_translation",
            "14. 링크: 텍스트는 번역하고 target은 유지합니다",
            source_span=source_label,
            target_span=target_label,
            suggested_fix="Translate link text while preserving the URL target.",
            reason="The style guide requires translating link text while preserving the link target.",
        )


def validate_first_mention_terms(
    issues: list[Issue],
    source: MarkdownDoc,
    target: MarkdownDoc,
    policy: StylePolicy,
) -> None:
    source_text = "\n".join(segment.text for segment in source.segments)
    target_text = "\n".join(segment.text for segment in target.segments)
    normalized_target = normalize_lookup_text(target_text)
    guide_section = "6. 용어: Glossary, 기존 번역례, 검색성을 함께 봅니다"
    for source_term, rule in policy.first_mention_terms.items():
        if not term_present(source_text, source_term):
            continue
        ko_term = rule.get("ko", "")
        required_first = rule.get("required_first", "")
        if not ko_term or not required_first:
            continue
        if normalize_lookup_text(required_first) in normalized_target:
            continue
        if not (normalize_lookup_text(ko_term) in normalize_lookup_text(target_text) or term_present(target_text, source_term)):
            continue
        style_issue(
            issues,
            "terminology",
            "minor",
            "First mention is missing the recommended bilingual term.",
            "first_mention_bilingual",
            guide_section,
            source_span=source_term,
            target_span=ko_term,
            suggested_fix=f"Use `{required_first}` on first mention, then `{ko_term}` afterward.",
            reason="The style guide recommends preserving searchability by adding English in parentheses on first mention.",
        )


def validate_style_guide(
    issues: list[Issue],
    source: MarkdownDoc | None,
    target: MarkdownDoc,
    policy: StylePolicy | None,
) -> None:
    if policy is None:
        return
    validate_translationese(issues, target, policy)
    validate_title_style(issues, target, policy)
    validate_intro_closing_style(issues, target)
    validate_list_consistency(issues, target, policy)
    if source is None:
        return
    validate_modal_strength(issues, source, target, policy)
    validate_overstatement(issues, source, target, policy)
    validate_information_addition(issues, source, target)
    validate_emoji_delta(issues, source, target, policy)
    validate_alt_text_and_link_text(issues, source, target, policy)
    validate_first_mention_terms(issues, source, target, policy)


def style_penalty(issues: list[Issue]) -> float:
    weights = {
        "modal_strength": 8.0,
        "overstatement": 8.0,
        "translationese": 1.0,
        "title_quality": 3.0,
        "intro_closing_style": 2.0,
        "list_consistency": 2.0,
        "emoji_delta": 2.0,
        "alt_text_caption": 2.0,
        "link_text_translation": 2.0,
        "first_mention_bilingual": 2.0,
        "information_addition": 8.0,
    }
    penalty = 0.0
    for item in issues:
        if not item.guide_rule:
            continue
        penalty += weights.get(item.guide_rule, 2.0)
        if item.severity == "major":
            penalty += 2.0
    return min(40.0, penalty)


def text_tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9가-힣_/-]+", normalize_lookup_text(text))


def protected_terms_for_metric(text: str) -> set[str]:
    terms: set[str] = set()
    for regex in [MODEL_ID_RE, PY_IDENTIFIER_RE, ENV_VAR_RE, CLI_FLAG_RE, URL_RE, LATEX_INLINE_RE]:
        terms.update(match.group(0) for match in regex.finditer(text))
    terms.update(normalized_numbers(text))
    return {normalize_lookup_text(term) for term in terms if term.strip()}


def length_similarity(source_text: str, target_text: str) -> float:
    source_len = max(1, len(source_text))
    target_len = max(1, len(target_text))
    ratio = target_len / source_len
    if 0.45 <= ratio <= 1.80:
        return 1.0
    if ratio < 0.45:
        return max(0.0, ratio / 0.45)
    return max(0.0, 1.80 / ratio)


def protected_overlap_score(source_text: str, target_text: str) -> float:
    source_terms = protected_terms_for_metric(source_text)
    if not source_terms:
        return 1.0
    target_terms = protected_terms_for_metric(target_text)
    return len(source_terms & target_terms) / len(source_terms)


def heuristic_qe_score(source_text: str, target_text: str) -> float:
    if normalize_lookup_text(source_text) == normalize_lookup_text(target_text):
        return 1.0
    length_score = length_similarity(source_text, target_text)
    protected_score = protected_overlap_score(source_text, target_text)
    korean_score = min(1.0, korean_ratio(target_text) / 0.35) if KOREAN_RE.search(target_text) else 0.35
    untranslated_penalty = min(0.35, english_ratio(target_text) * 0.35)
    score = (0.45 * length_score) + (0.30 * protected_score) + (0.25 * korean_score) - untranslated_penalty
    return round(max(0.0, min(1.0, score)), 4)


def char_ngrams(text: str, n: int = 3) -> Counter[str]:
    normalized = re.sub(r"\s+", " ", normalize_lookup_text(text))
    if len(normalized) < n:
        return Counter([normalized]) if normalized else Counter()
    return Counter(normalized[index : index + n] for index in range(len(normalized) - n + 1))


def cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    if not left or not right:
        return 0.0
    common = set(left) & set(right)
    numerator = sum(left[key] * right[key] for key in common)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


def embedding_similarity_score(source_text: str, target_text: str) -> float:
    source_terms = protected_terms_for_metric(source_text)
    target_terms = protected_terms_for_metric(target_text)
    if source_terms:
        protected_score = len(source_terms & target_terms) / len(source_terms)
    else:
        protected_score = 1.0
    lexical_score = cosine_similarity(char_ngrams(source_text), char_ngrams(target_text))
    length_score = length_similarity(source_text, target_text)
    return round(max(0.0, min(1.0, (0.55 * protected_score) + (0.25 * length_score) + (0.20 * lexical_score))), 4)


def chrf_score(reference: str, candidate: str, max_n: int = 6) -> float:
    if not reference and not candidate:
        return 1.0
    if not reference or not candidate:
        return 0.0
    scores: list[float] = []
    for n in range(1, max_n + 1):
        ref_counts = char_ngrams(reference, n)
        cand_counts = char_ngrams(candidate, n)
        overlap = sum((ref_counts & cand_counts).values())
        precision = overlap / max(1, sum(cand_counts.values()))
        recall = overlap / max(1, sum(ref_counts.values()))
        if precision + recall == 0:
            scores.append(0.0)
        else:
            scores.append((2 * precision * recall) / (precision + recall))
    return round(sum(scores) / len(scores), 4)


def load_metric_cache(path: Path | None) -> dict[str, object]:
    if path is None or not path.exists():
        return {}
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return loaded if isinstance(loaded, dict) else {}


def save_metric_cache(path: Path | None, cache: dict[str, object]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def metric_cache_key(metric_name: str, source_hash: str, target_hash: str) -> str:
    return hashlib.sha256(f"{metric_name}:{source_hash}:{target_hash}".encode("utf-8")).hexdigest()


def load_reference_doc(path: Path | None) -> MarkdownDoc | None:
    if path is None or not path.exists():
        return None
    return markdown_doc(path.read_text(encoding="utf-8"))


def run_cometkiwi_wrapper(source_text: str, target_text: str) -> tuple[float | None, str]:
    try:
        import comet  # type: ignore  # noqa: F401
    except Exception:
        return None, "COMETKiwi dependency is not installed; skipped optional metric."
    return None, "COMETKiwi wrapper is available but no model runner is configured."


def evaluate_metrics(
    source: MarkdownDoc | None,
    target: MarkdownDoc,
    config: MetricConfig,
) -> dict[str, object]:
    cache = load_metric_cache(config.metric_cache_path)
    reference_doc = load_reference_doc(config.reference_path)
    alignment = align_segments(source, target) if source else []
    reference_alignment = align_segments(reference_doc, target) if reference_doc else []
    segment_metrics: list[dict[str, object]] = []
    cache_hits = 0
    cache_misses = 0
    warnings: list[str] = []

    for item in alignment:
        source_hash = str(item["source_hash"])
        target_hash = str(item["target_hash"])
        source_text = str(item["source_text"])
        target_text = str(item["target_text"])
        metric_row: dict[str, object] = {
            "alignment_id": item["alignment_id"],
            "source_id": item["source_id"],
            "target_id": item["target_id"],
        }

        if config.qe_metric != "off":
            key = metric_cache_key(f"qe:{config.qe_metric}", source_hash, target_hash)
            if key in cache:
                qe_score = float(cache[key])
                cache_hits += 1
            else:
                cache_misses += 1
                if config.qe_metric == "heuristic":
                    qe_score = heuristic_qe_score(source_text, target_text)
                elif config.qe_metric == "cometkiwi":
                    maybe_score, warning = run_cometkiwi_wrapper(source_text, target_text)
                    if warning and warning not in warnings:
                        warnings.append(warning)
                    qe_score = maybe_score if maybe_score is not None else heuristic_qe_score(source_text, target_text)
                else:
                    qe_score = heuristic_qe_score(source_text, target_text)
                cache[key] = qe_score
            metric_row["qe_score"] = qe_score

        if config.enable_embedding_similarity:
            key = metric_cache_key("embedding_similarity", source_hash, target_hash)
            if key in cache:
                embedding_score = float(cache[key])
                cache_hits += 1
            else:
                cache_misses += 1
                embedding_score = embedding_similarity_score(source_text, target_text)
                cache[key] = embedding_score
            metric_row["embedding_similarity"] = embedding_score

        segment_metrics.append(metric_row)

    if config.enable_chrf and reference_doc:
        for index, item in enumerate(reference_alignment):
            if index >= len(segment_metrics):
                break
            key = metric_cache_key("chrf", str(item["source_hash"]), str(item["target_hash"]))
            if key in cache:
                score = float(cache[key])
                cache_hits += 1
            else:
                cache_misses += 1
                score = chrf_score(str(item["source_text"]), str(item["target_text"]))
                cache[key] = score
            segment_metrics[index]["chrf"] = score

    save_metric_cache(config.metric_cache_path, cache)

    qe_scores = [float(row["qe_score"]) for row in segment_metrics if "qe_score" in row]
    embedding_scores = [float(row["embedding_similarity"]) for row in segment_metrics if "embedding_similarity" in row]
    chrf_scores = [float(row["chrf"]) for row in segment_metrics if "chrf" in row]
    summary = {
        "qe_metric": config.qe_metric,
        "qe_enabled": config.qe_metric != "off",
        "embedding_similarity_enabled": config.enable_embedding_similarity,
        "chrf_enabled": config.enable_chrf and reference_doc is not None,
        "segment_count": len(segment_metrics),
        "cache_hits": cache_hits,
        "cache_misses": cache_misses,
        "warnings": warnings,
    }
    if qe_scores:
        summary["qe_average"] = round(sum(qe_scores) / len(qe_scores), 4)
        summary["qe_min"] = round(min(qe_scores), 4)
    if embedding_scores:
        summary["embedding_similarity_average"] = round(sum(embedding_scores) / len(embedding_scores), 4)
        summary["embedding_similarity_min"] = round(min(embedding_scores), 4)
    if chrf_scores:
        summary["chrf_average"] = round(sum(chrf_scores) / len(chrf_scores), 4)
        summary["chrf_min"] = round(min(chrf_scores), 4)

    return {
        "summary": summary,
        "segments": segment_metrics,
    }


def validate_metric_thresholds(issues: list[Issue], metrics: dict[str, object], config: MetricConfig) -> None:
    for row in metrics.get("segments", []):
        if not isinstance(row, dict):
            continue
        segment_id = str(row.get("target_id") or row.get("source_id") or "")
        if "qe_score" in row and float(row["qe_score"]) < config.qe_review_threshold:
            issue(
                issues,
                "accuracy",
                "major",
                "QE metric score is low.",
                segment_id=segment_id,
                target_span=f"{float(row['qe_score']):.4f}",
                suggested_fix="Review this segment for omission, unrelated translation, or over-compression.",
                reason=f"QE score is below threshold {config.qe_review_threshold:.2f}.",
            )
        if (
            config.enable_embedding_similarity
            and "embedding_similarity" in row
            and float(row["embedding_similarity"]) < config.embedding_review_threshold
        ):
            issue(
                issues,
                "accuracy",
                "minor",
                "Embedding similarity is an outlier.",
                segment_id=segment_id,
                target_span=f"{float(row['embedding_similarity']):.4f}",
                suggested_fix="Review whether the segment still corresponds to the source.",
                reason=f"Embedding similarity is below threshold {config.embedding_review_threshold:.2f}.",
            )


def korean_ratio(text: str) -> float:
    letters = LETTER_RE.findall(text)
    if not letters:
        return 0.0
    korean = KOREAN_RE.findall(text)
    return len(korean) / len(letters)


def english_ratio(text: str) -> float:
    tokens = re.findall(r"[A-Za-z가-힣][A-Za-z가-힣'-]*", text)
    if not tokens:
        return 0.0
    english_words = [token for token in tokens if re.fullmatch(r"[A-Za-z][A-Za-z'-]*", token) and len(token) >= 4]
    return len(english_words) / len(tokens)


def validate_documents(
    target: MarkdownDoc,
    source: MarkdownDoc | None = None,
    *,
    target_path: str = "",
    source_path: str = "",
    source_format: str = "",
    expected_source_hash: str = "",
    glossary: list[GlossaryEntry] | None = None,
    translation_memory: dict[str, str] | None = None,
    metric_config: MetricConfig | None = None,
    style_policy: StylePolicy | None = None,
) -> dict[str, object]:
    issues: list[Issue] = []
    source_changed = False
    glossary_entries = glossary or []
    memory = translation_memory or {}
    metric_settings = metric_config or MetricConfig(qe_metric="off", enable_embedding_similarity=False)
    active_style_policy = style_policy if metric_settings.enable_style_guide else None
    metrics: dict[str, object] = {
        "summary": {
            "qe_metric": metric_settings.qe_metric,
            "qe_enabled": False,
            "embedding_similarity_enabled": False,
            "chrf_enabled": False,
            "segment_count": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "warnings": [],
        },
        "segments": [],
    }
    source_is_structural = source is not None and source_format in {"", "markdown", "url_markdown"}

    for error in target.parse_errors:
        issue(issues, "formatting", "critical", error, reason="Target Markdown parse failed.")

    if "title" not in target.frontmatter:
        issue(
            issues,
            "formatting",
            "critical",
            "Target front matter is missing required key: title.",
            suggested_fix="Add a translated title to front matter.",
        )

    if target.todo_markers:
        issue(
            issues,
            "formatting",
            "critical",
            "TODO/FIXME/TBD or unresolved placeholder marker remains.",
            target_span=", ".join(sorted(set(target.todo_markers))),
            suggested_fix="Remove unresolved markers before publishing.",
        )

    if source is not None:
        if expected_source_hash and source.source_hash != expected_source_hash:
            source_changed = True
            issue(
                issues,
                "accuracy",
                "major",
                "Source hash changed from the expected manifest value.",
                source_span=expected_source_hash,
                target_span=source.source_hash,
                suggested_fix="Review the source article changes before trusting the existing translation.",
                reason="Manifest source.hash does not match the current source snapshot hash.",
            )

        for error in source.parse_errors:
            issue(issues, "formatting", "critical", error, reason="Source Markdown parse failed.")

        if source_is_structural:
            for key in ["authors", "thumbnail", "tags", "blog"]:
                source_value = source.frontmatter.get(key)
                if source_value is None:
                    continue
                target_value = target.frontmatter.get(key)
                if source_value != target_value:
                    severity = "major" if key == "authors" else "critical"
                    issue(
                        issues,
                        "formatting",
                        severity,
                        f"Front matter key `{key}` changed or is missing.",
                        source_span=source_value,
                        target_span=target_value or "",
                        suggested_fix=f"Preserve front matter `{key}` exactly.",
                    )

            compare_counter(issues, "formatting", "code block hash", code_hashes(source.code_blocks), code_hashes(target.code_blocks))
            compare_counter(issues, "technical", "inline code", source.inline_code, target.inline_code)
            compare_counter(issues, "formatting", "link target", source.link_targets, target.link_targets)
            compare_counter(issues, "formatting", "image target", source.image_targets, target.image_targets)
            compare_counter(issues, "formatting", "bare URL", source.urls, target.urls, severity="major")
            compare_counter(issues, "technical", "model or dataset id", source.model_ids, target.model_ids, severity="major")
            compare_counter(issues, "technical", "Python/API identifier", source.python_identifiers, target.python_identifiers, severity="major")
            compare_counter(issues, "technical", "environment variable", source.env_vars, target.env_vars)
            compare_counter(issues, "technical", "CLI flag", source.cli_flags, target.cli_flags)
            compare_counter(issues, "technical", "number/unit token", source.numbers, target.numbers, severity="major")
            compare_counter(issues, "technical", "LaTeX token", source.latex_inline, target.latex_inline)

            if source.table_shapes != target.table_shapes:
                issue(
                    issues,
                    "formatting",
                    "critical",
                    "Markdown table shape mismatch.",
                    source_span=str(source.table_shapes),
                    target_span=str(target.table_shapes),
                    suggested_fix="Preserve source table row and column counts.",
                )

            validate_segment_coverage(issues, source, target)
            metrics = evaluate_metrics(source, target, metric_settings)
            validate_metric_thresholds(issues, metrics, metric_settings)
        else:
            metrics["summary"]["warnings"].append(
                "Source was fetched as HTML text; structural hard gates, segment coverage, and segment metrics were skipped."
            )
        validate_glossary(issues, source, target, glossary_entries)

    validate_style_guide(issues, source, target, active_style_policy)

    kr_ratio = korean_ratio(target.body)
    if kr_ratio < 0.20:
        issue(
            issues,
            "fluency",
            "major",
            "Korean letter ratio is low.",
            target_span=f"{kr_ratio:.2%}",
            suggested_fix="Translate remaining general prose into Korean.",
        )

    en_ratio = english_ratio(target.body)
    if en_ratio > 0.60:
        issue(
            issues,
            "fluency",
            "major",
            "English prose ratio is high.",
            target_span=f"{en_ratio:.2%}",
            suggested_fix="Verify that non-code English prose is intentionally preserved.",
        )

    critical = [item for item in issues if item.severity == "critical"]
    major = [item for item in issues if item.severity == "major"]
    minor = [item for item in issues if item.severity == "minor"]
    style_issues = [item for item in issues if item.guide_rule]
    non_style_major = [item for item in major if not item.guide_rule]
    style_major = [item for item in major if item.guide_rule]
    quality_score = max(
        0.0,
        100.0
        - (len(critical) * 15.0)
        - (len(non_style_major) * 5.0)
        - (len(style_major) * 2.0)
        - (len(minor) * 1.0),
    )
    if critical:
        status = "reject"
    elif source_changed:
        status = "source_changed"
    elif quality_score >= 90 and not major and not style_issues:
        status = "auto_pass"
    elif quality_score >= 75 or (style_issues and quality_score >= 60):
        status = "review_required"
    else:
        status = "reject"

    non_style_accuracy_issues = [item for item in issues if item.category == "accuracy" and not item.guide_rule]
    style_accuracy_major = [item for item in issues if item.category == "accuracy" and item.guide_rule and item.severity == "major"]
    dimension_scores = {
        "adequacy": max(
            0.0,
            min(
                100.0,
                (float(metrics.get("summary", {}).get("qe_average", 1.0)) * 100.0)
                - 20.0 * sum(1 for item in non_style_accuracy_issues if item.severity == "major")
                - 5.0 * len(style_accuracy_major),
            ),
        ),
        "technical_accuracy": max(0.0, 100.0 - 20.0 * sum(1 for item in issues if item.category == "technical")),
        "completeness": max(0.0, 100.0 - 20.0 * len(non_style_accuracy_issues)),
        "terminology": max(0.0, 100.0 - 20.0 * sum(1 for item in issues if item.category == "terminology")),
        "fluency": max(0.0, 100.0 - 15.0 * sum(1 for item in issues if item.category == "fluency")),
        "publishing_integrity": max(0.0, 100.0 - 20.0 * sum(1 for item in issues if item.category == "formatting")),
        "style_locale": max(0.0, 100.0 - style_penalty(issues)),
    }
    style_summary = {
        "enabled": active_style_policy is not None,
        "style_score": dimension_scores["style_locale"],
        "issue_count": len(style_issues),
        "rules": dict(sorted(Counter(item.guide_rule for item in style_issues).items())),
    }

    return {
        "status": status,
        "quality_score": quality_score,
        "hard_failures": [asdict(item) for item in critical],
        "dimension_scores": dimension_scores,
        "issues": [asdict(item) for item in issues],
        "segments": {
            "source": [segment_to_json(segment) for segment in source.segments] if source else [],
            "target": [segment_to_json(segment) for segment in target.segments],
        },
        "segment_alignment": align_segments(source, target) if source else [],
        "metrics": metrics,
        "style_guide": style_summary,
        "metadata": {
            "target_path": target_path,
            "source_path": source_path,
            "source_format": source_format or ("markdown" if source else ""),
            "source_hash": source.source_hash if source else "",
            "expected_source_hash": expected_source_hash,
            "target_hash": target.source_hash,
            "source_available": source is not None,
            "source_changed": source_changed,
            "source_segment_count": len(source.segments) if source else 0,
            "target_segment_count": len(target.segments),
            "aligned_segment_count": min(len(source.segments), len(target.segments)) if source else 0,
            "target_source_length_ratio": (
                sum(len(segment.text) for segment in target.segments)
                / max(1, sum(len(segment.text) for segment in source.segments))
                if source
                else 0
            ),
            "glossary_entry_count": len(glossary_entries),
            "translation_memory_entry_count": len(memory),
            "translation_memory_match_count": translation_memory_match_count(source, memory),
            "qe_metric": metric_settings.qe_metric,
            "metric_cache_path": str(metric_settings.metric_cache_path or ""),
            "reference_path": str(metric_settings.reference_path or ""),
            "style_guide_path": str(active_style_policy.guide_path if active_style_policy else ""),
            "style_policy_path": str(active_style_policy.policy_path if active_style_policy else ""),
            "style_policy_version": active_style_policy.version if active_style_policy else 0,
            "tool": "translation_quality_harness",
            "tool_version": "0.5.0",
        },
    }


def markdown_report(report: dict[str, object]) -> str:
    hard_failures = report["hard_failures"]
    issues = report["issues"]
    dimension_scores = report["dimension_scores"]
    metadata = report["metadata"]
    metric_summary = report.get("metrics", {}).get("summary", {})
    style_summary = report.get("style_guide", {})
    lines = [
        "# Quality Report",
        "",
        f"- Status: {report['status']}",
        f"- Quality Score: {report['quality_score']:.1f}",
        f"- Hard failures: {len(hard_failures)}",
        f"- Issues: {len(issues)}",
        f"- Source available: {metadata.get('source_available')}",
        f"- Source changed: {metadata.get('source_changed')}",
        f"- Source segments: {metadata.get('source_segment_count')}",
        f"- Target segments: {metadata.get('target_segment_count')}",
        "",
        "## Scorecard",
        "",
        "| Dimension | Score |",
        "| --- | ---: |",
    ]
    for name, score in dimension_scores.items():
        lines.append(f"| {name} | {score:.1f} |")

    lines += ["", "## Metrics", ""]
    if metric_summary:
        for key in [
            "qe_metric",
            "qe_average",
            "qe_min",
            "embedding_similarity_average",
            "embedding_similarity_min",
            "chrf_average",
            "chrf_min",
            "cache_hits",
            "cache_misses",
        ]:
            if key in metric_summary:
                lines.append(f"- {key}: {metric_summary[key]}")
        warnings = metric_summary.get("warnings") or []
        for warning in warnings:
            lines.append(f"- warning: {warning}")
    else:
        lines.append("No metric summary available.")

    lines += ["", "## Style Guide", ""]
    lines.append(f"- Enabled: {style_summary.get('enabled', False)}")
    if metadata.get("style_guide_path"):
        lines.append(f"- Guide: `{metadata.get('style_guide_path')}`")
    if metadata.get("style_policy_path"):
        lines.append(f"- Policy: `{metadata.get('style_policy_path')}`")
    if "style_score" in style_summary:
        lines.append(f"- Style score: {style_summary.get('style_score'):.1f}")
    if style_summary.get("rules"):
        lines.append(f"- Rule hits: {style_summary.get('rules')}")

    style_issues = [item for item in issues if item.get("guide_rule")]
    lines += ["", "## Style Guide Findings", ""]
    if not style_issues:
        lines.append("No style guide findings.")
    else:
        lines += [
            "| Rule | Severity | Segment | Current | Suggested |",
            "| --- | --- | --- | --- | --- |",
        ]
        for item in style_issues[:10]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(item.get("guide_rule", "")),
                        str(item.get("severity", "")),
                        str(item.get("segment_id", "")),
                        str(item.get("target_span", "")).replace("|", "\\|"),
                        str(item.get("suggested_fix", "")).replace("|", "\\|"),
                    ]
                )
                + " |"
            )

    lines += ["", "## Issues", ""]
    if not issues:
        lines.append("No issues found.")
    else:
        for item in issues:
            lines += [
                f"### {item['id']} {item['category']} / {item['severity']}",
                "",
                f"- Message: {item['message']}",
            ]
            if item.get("source_span"):
                lines.append(f"- Source: `{item['source_span']}`")
            if item.get("target_span"):
                lines.append(f"- Target: `{item['target_span']}`")
            if item.get("suggested_fix"):
                lines.append(f"- Suggested fix: {item['suggested_fix']}")
            if item.get("reason"):
                lines.append(f"- Reason: {item['reason']}")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def pr_comment_report(report: dict[str, object], max_style_issues: int = 5) -> str:
    issues = report["issues"]
    style_issues = [item for item in issues if item.get("guide_rule")]
    lines = [
        "## Translation Quality Gate",
        "",
        f"- Status: {report['status']}",
        f"- Quality Score: {report['quality_score']:.1f}",
        f"- Style Score: {report.get('style_guide', {}).get('style_score', 0):.1f}",
        f"- Hard failures: {len(report['hard_failures'])}",
        f"- Style guide findings: {len(style_issues)}",
        "",
    ]
    if style_issues:
        lines += ["### Top Style Guide Findings", ""]
        for index, item in enumerate(style_issues[:max_style_issues], start=1):
            segment = item.get("segment_id") or "-"
            lines += [
                f"{index}. `{item.get('guide_rule')}` / `{item.get('severity')}` / segment `{segment}`",
                f"   - Current: {item.get('target_span') or '-'}",
                f"   - Suggested: {item.get('suggested_fix') or '-'}",
            ]
    return "\n".join(lines).rstrip() + "\n"


def write_segments_jsonl(path: Path, segments: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(segment, ensure_ascii=False) for segment in segments]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def resolve_input_path(raw: str, base: Path) -> Path | None:
    if not raw:
        return None
    path = Path(raw)
    if path.is_absolute():
        return path
    return base / path


def build_report(
    manifest_path: Path,
    target_root: Path,
    *,
    source_path: Path | None = None,
    target_path_override: Path | None = None,
    glossary_paths: list[Path] | None = None,
    translation_memory_path: Path | None = None,
    metric_config: MetricConfig | None = None,
    style_guide_path: Path | None = None,
    style_policy_path: Path | None = None,
    fetch_source_url: bool = True,
) -> dict[str, object]:
    manifest = read_simple_manifest(manifest_path)
    target_path = target_path_override
    if target_path is None:
        target_file = manifest.get("translation.file_path", "")
        if not target_file:
            raise ValueError("manifest is missing translation.file_path")
        target_path = resolve_input_path(target_file, target_root)
    if target_path is None or not target_path.exists():
        raise FileNotFoundError(f"target markdown not found: {target_path}")

    if source_path is None:
        manifest_source = manifest.get("source.file_path", "")
        source_path = resolve_input_path(manifest_source, manifest_path.parent)
    source_doc = None
    source_format = ""
    source_path_label = ""
    if source_path is not None and source_path.exists():
        source_doc = markdown_doc(source_path.read_text(encoding="utf-8"))
        source_format = "markdown"
        source_path_label = str(source_path)
    elif fetch_source_url and manifest.get("source.url"):
        fetched_source = fetch_source_document(manifest["source.url"], manifest)
        if fetched_source is not None:
            source_doc = markdown_doc(fetched_source.text)
            source_format = fetched_source.source_format
            source_path_label = fetched_source.source_path

    target_doc = markdown_doc(target_path.read_text(encoding="utf-8"))
    return validate_documents(
        target_doc,
        source_doc,
        target_path=str(target_path),
        source_path=source_path_label or str(source_path or ""),
        source_format=source_format,
        expected_source_hash=manifest.get("source.hash", ""),
        glossary=load_glossary(glossary_paths),
        translation_memory=load_translation_memory(translation_memory_path),
        metric_config=metric_config or MetricConfig(),
        style_policy=load_style_policy(style_guide_path or DEFAULT_STYLE_GUIDE_PATH, style_policy_path or DEFAULT_STYLE_POLICY_PATH),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run deterministic Korean translation hard gates.")
    parser.add_argument("--manifest", required=True, help="Path to translation-flow manifest YAML.")
    parser.add_argument("--target-root", required=True, help="Root directory containing translation.file_path.")
    parser.add_argument("--source", help="Optional source Markdown path. Overrides manifest source.file_path.")
    parser.add_argument("--target", help="Optional target Markdown path. Overrides manifest translation.file_path.")
    parser.add_argument("--output-md", required=True, help="Markdown quality report output path.")
    parser.add_argument("--output-json", required=True, help="JSON quality report output path.")
    parser.add_argument("--output-pr-comment", help="Optional PR comment Markdown summary output path.")
    parser.add_argument("--output-source-segments", help="Optional source segment JSONL output path.")
    parser.add_argument("--output-target-segments", help="Optional target segment JSONL output path.")
    parser.add_argument(
        "--glossary",
        action="append",
        default=[],
        help="Optional glossary TSV path. Can be passed multiple times. Defaults to skills/quality/glossary/*.tsv.",
    )
    parser.add_argument("--translation-memory", help="Optional approved translation memory JSONL path.")
    parser.add_argument(
        "--qe-metric",
        choices=["off", "heuristic", "cometkiwi"],
        default="heuristic",
        help="Reference-free QE metric provider. `cometkiwi` falls back to heuristic when unavailable.",
    )
    parser.add_argument("--disable-embedding-similarity", action="store_true", help="Disable embedding similarity outlier checks.")
    parser.add_argument("--enable-chrf", action="store_true", help="Enable chrF when --reference is provided.")
    parser.add_argument("--reference", help="Optional approved Korean reference Markdown for chrF regression metric.")
    parser.add_argument("--metric-cache", help="Optional JSON cache path for metric results.")
    parser.add_argument("--qe-review-threshold", type=float, default=0.55, help="Review threshold for low QE segment scores.")
    parser.add_argument("--style-guide", help="Optional Korean localization style guide Markdown path.")
    parser.add_argument("--style-policy", help="Optional style policy YAML path.")
    parser.add_argument("--disable-style-guide", action="store_true", help="Disable style-guide validators.")
    parser.add_argument("--no-fetch-source-url", action="store_true", help="Do not fetch source.url when no source Markdown file is available.")
    parser.add_argument("--fail-on-reject", action="store_true", help="Exit non-zero when status is reject.")
    args = parser.parse_args(argv)

    manifest_path = Path(args.manifest).resolve()
    target_root = Path(args.target_root).resolve()
    source_path = Path(args.source).resolve() if args.source else None
    target_path = Path(args.target).resolve() if args.target else None
    glossary_paths = [Path(path).resolve() for path in args.glossary] or None
    translation_memory_path = Path(args.translation_memory).resolve() if args.translation_memory else None
    metric_config = MetricConfig(
        qe_metric=args.qe_metric,
        enable_embedding_similarity=not args.disable_embedding_similarity,
        enable_chrf=args.enable_chrf,
        qe_review_threshold=args.qe_review_threshold,
        metric_cache_path=Path(args.metric_cache).resolve() if args.metric_cache else None,
        reference_path=Path(args.reference).resolve() if args.reference else None,
        enable_style_guide=not args.disable_style_guide,
        style_guide_path=Path(args.style_guide).resolve() if args.style_guide else DEFAULT_STYLE_GUIDE_PATH,
        style_policy_path=Path(args.style_policy).resolve() if args.style_policy else DEFAULT_STYLE_POLICY_PATH,
    )
    report = build_report(
        manifest_path,
        target_root,
        source_path=source_path,
        target_path_override=target_path,
        glossary_paths=glossary_paths,
        translation_memory_path=translation_memory_path,
        metric_config=metric_config,
        style_guide_path=metric_config.style_guide_path,
        style_policy_path=metric_config.style_policy_path,
        fetch_source_url=not args.no_fetch_source_url,
    )

    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    output_md = Path(args.output_md)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(markdown_report(report), encoding="utf-8")

    if args.output_pr_comment:
        output_pr_comment = Path(args.output_pr_comment)
        output_pr_comment.parent.mkdir(parents=True, exist_ok=True)
        output_pr_comment.write_text(pr_comment_report(report), encoding="utf-8")

    segments = report.get("segments", {})
    if args.output_source_segments:
        write_segments_jsonl(Path(args.output_source_segments), segments.get("source", []))
    if args.output_target_segments:
        write_segments_jsonl(Path(args.output_target_segments), segments.get("target", []))

    print(f"Wrote quality JSON report: {output_json}")
    print(f"Wrote quality Markdown report: {output_md}")
    print(f"Status: {report['status']}")
    if args.fail_on_reject and report["status"] == "reject":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
