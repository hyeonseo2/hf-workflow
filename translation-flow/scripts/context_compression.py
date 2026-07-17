from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


DEFAULT_MAX_GUIDE_CHARS = 1200
DEFAULT_SOURCE_EXCERPT_CHARS = 2500
DEFAULT_MAX_SELECTED_GUIDE_CHARS = 6000
DEFAULT_MAX_SELECTED_GUIDE_CHUNKS = 8
FENCE_RE = re.compile(r"```[\s\S]*?```")
HEADING_LINE_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
FENCE_BOUNDARY_RE = re.compile(r"^\s*(`{3,}|~{3,})")
FRONTMATTER_TITLE_RE = re.compile(r"(?m)^title:\s*[\"']?(.+?)[\"']?\s*$")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", re.MULTILINE)
LINK_RE = re.compile(r"!?\[[^\]]*\]\([^)]+\)|https?://\S+")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
GLOSSARY_ARROW_RE = re.compile(r"\s[-=]>\s")
GLOSSARY_COLON_RE = re.compile(r"^[-*]\s+([^:]{1,80}):\s*(.{1,80})$")
ALLOWED_COLON_LABELS = {
    "style",
    "hard rules",
    "soft preferences",
    "article-specific notes",
    "notes",
    "risk areas",
    "terminology policy",
}
FEATURE_TERMS = {
    "has_code": ("code", "cli", "command", "identifier", "api", "package", "environment", "file path", "코드", "명령어", "식별자"),
    "has_table": ("table", "markdown", "format", "structure", "표", "구조"),
    "has_links": ("link", "url", "reference", "링크"),
    "has_images": ("image", "thumbnail", "이미지"),
    "has_benchmark_terms": ("benchmark", "leaderboard", "metric", "score", "number", "comparison", "벤치마크", "지표", "수치", "비교"),
    "has_cli_terms": ("cli", "command", "flag", "install", "package", "명령어", "플래그"),
    "has_model_or_dataset_terms": ("model", "dataset", "library", "repository", "organization", "모델", "데이터셋", "라이브러리", "저장소"),
}


@dataclass(frozen=True)
class SourceProfile:
    title: str
    headings: tuple[str, ...]
    excerpt: str
    features: tuple[str, ...]

    def to_markdown(self) -> str:
        heading_text = "\n".join(f"- {heading}" for heading in self.headings) or "- none"
        feature_text = "\n".join(f"- {feature}" for feature in self.features) or "- none"
        return "\n".join(
            [
                f"Title: {self.title or 'unknown'}",
                "",
                "Headings:",
                heading_text,
                "",
                "Detected features:",
                feature_text,
                "",
                "Source excerpt:",
                self.excerpt.strip() or "(empty)",
            ]
        )


@dataclass(frozen=True)
class GuideChunk:
    path: Path
    heading: str
    text: str

    def to_markdown(self) -> str:
        heading = self.heading or self.path.name
        return f"## {self.path.name} / {heading}\n{self.text.strip()}"


@dataclass(frozen=True)
class MarkdownHeading:
    start: int
    end: int
    title: str


def iter_markdown_headings(text: str) -> list[MarkdownHeading]:
    headings: list[MarkdownHeading] = []
    in_fence = False
    fence_marker_char = ""
    fence_marker_len = 0
    offset = 0
    for line in text.splitlines(keepends=True):
        fence_match = FENCE_BOUNDARY_RE.match(line)
        if fence_match:
            marker = fence_match.group(1)
            marker_char = marker[0]
            marker_len = len(marker)
            if not in_fence:
                in_fence = True
                fence_marker_char = marker_char
                fence_marker_len = marker_len
            elif marker_char == fence_marker_char and marker_len >= fence_marker_len:
                in_fence = False
                fence_marker_char = ""
                fence_marker_len = 0
            offset += len(line)
            continue

        if not in_fence:
            heading_match = HEADING_LINE_RE.match(line.rstrip("\r\n"))
            if heading_match:
                headings.append(
                    MarkdownHeading(
                        start=offset,
                        end=offset + len(line),
                        title=heading_match.group(2).strip(),
                    )
                )
        offset += len(line)
    return headings


def default_guide_paths() -> list[Path]:
    docs_dir = Path(__file__).resolve().parents[1] / "docs"
    return [
        docs_dir / "hf_translation_conventions.md",
        docs_dir / "hf_ko_translation_best_practice.md",
    ]


def parse_guide_paths(raw: str | None, base_dir: Path | None = None) -> list[Path]:
    if not raw or not raw.strip():
        return default_guide_paths()
    root = base_dir or Path.cwd()
    paths: list[Path] = []
    for item in raw.split(","):
        value = item.strip()
        if not value:
            continue
        path = Path(value).expanduser()
        paths.append(path if path.is_absolute() else root / path)
    return paths


def build_source_profile(source_markdown: str, source_excerpt_chars: int = DEFAULT_SOURCE_EXCERPT_CHARS) -> SourceProfile:
    headings = tuple(heading.title for heading in iter_markdown_headings(source_markdown))
    title_match = FRONTMATTER_TITLE_RE.search(source_markdown)
    title = title_match.group(1).strip() if title_match else ""
    if not title and headings:
        title = headings[0]

    excerpt = source_markdown.strip()
    if len(excerpt) > source_excerpt_chars:
        excerpt = excerpt[:source_excerpt_chars].rstrip() + "\n..."

    features = detect_features(source_markdown)
    return SourceProfile(title=title, headings=headings[:12], excerpt=excerpt, features=tuple(features))


def detect_features(source_markdown: str) -> list[str]:
    lowered = source_markdown.lower()
    features: list[str] = []
    if FENCE_RE.search(source_markdown) or INLINE_CODE_RE.search(source_markdown):
        features.append("has_code")
    if TABLE_SEPARATOR_RE.search(source_markdown):
        features.append("has_table")
    if LINK_RE.search(source_markdown):
        features.append("has_links")
    if IMAGE_RE.search(source_markdown):
        features.append("has_images")
    if any(term in lowered for term in ("benchmark", "leaderboard", "mteb", "accuracy", "score", "metric", "retrieval")):
        features.append("has_benchmark_terms")
    if re.search(r"\b(pip|uv|npm|python|conda|git)\s+", lowered) or re.search(r"\s--[a-z0-9-]+", lowered):
        features.append("has_cli_terms")
    if any(term in lowered for term in ("model", "dataset", "tokenizer", "transformers", "hugging face")):
        features.append("has_model_or_dataset_terms")
    return features


def load_guide_docs(guide_paths: list[Path]) -> list[tuple[Path, str]]:
    docs: list[tuple[Path, str]] = []
    for path in guide_paths:
        try:
            content = path.read_text(encoding="utf-8").strip()
        except OSError:
            continue
        if content:
            docs.append((path, content))
    return docs


def split_guide_doc(path: Path, content: str) -> list[GuideChunk]:
    matches = iter_markdown_headings(content)
    if not matches:
        return [GuideChunk(path=path, heading=path.name, text=content.strip())]

    chunks: list[GuideChunk] = []
    preface = content[: matches[0].start].strip()
    if preface:
        chunks.append(GuideChunk(path=path, heading=path.name, text=preface))

    for index, match in enumerate(matches):
        start = match.start
        end = matches[index + 1].start if index + 1 < len(matches) else len(content)
        heading = match.title
        text = content[start:end].strip()
        if text:
            chunks.append(GuideChunk(path=path, heading=heading, text=text))
    return chunks


def tokenize_for_retrieval(text: str) -> set[str]:
    tokens = re.findall(r"[0-9A-Za-z가-힣][0-9A-Za-z가-힣_./+-]*", text.lower())
    return {token for token in tokens if len(token) >= 2}


def profile_query_terms(source_profile: SourceProfile) -> set[str]:
    terms = tokenize_for_retrieval(
        "\n".join([source_profile.title, *source_profile.headings, source_profile.excerpt])
    )
    for feature in source_profile.features:
        terms.update(FEATURE_TERMS.get(feature, ()))
    return {term.lower() for term in terms}


def score_guide_chunk(chunk: GuideChunk, source_profile: SourceProfile) -> int:
    chunk_terms = tokenize_for_retrieval(f"{chunk.heading}\n{chunk.text}")
    query_terms = profile_query_terms(source_profile)
    score = len(chunk_terms & query_terms)
    lowered = f"{chunk.heading}\n{chunk.text}".lower()

    for feature in source_profile.features:
        if any(term.lower() in lowered for term in FEATURE_TERMS.get(feature, ())):
            score += 4

    if any(term in lowered for term in ("필수", "must", "보존", "preserve", "자연스러운", "natural")):
        score += 2
    return score


def select_guide_chunks(
    guide_docs: list[tuple[Path, str]],
    source_profile: SourceProfile,
    max_chunks: int = DEFAULT_MAX_SELECTED_GUIDE_CHUNKS,
    max_chars: int = DEFAULT_MAX_SELECTED_GUIDE_CHARS,
) -> list[GuideChunk]:
    chunks = [
        chunk
        for path, content in guide_docs
        for chunk in split_guide_doc(path, content)
    ]
    ranked = sorted(
        ((score_guide_chunk(chunk, source_profile), index, chunk) for index, chunk in enumerate(chunks)),
        key=lambda item: (-item[0], item[1]),
    )

    selected: list[GuideChunk] = []
    used_chars = 0
    for score, _, chunk in ranked:
        if len(selected) >= max_chunks:
            break
        if score <= 0 and selected:
            continue
        rendered = chunk.to_markdown()
        next_chars = used_chars + len(rendered) + (2 if selected else 0)
        if selected and next_chars > max_chars:
            continue
        selected.append(chunk)
        used_chars = next_chars

    return selected


def build_compression_prompt(
    source_profile: SourceProfile,
    guide_chunks: list[GuideChunk],
    max_chars: int = DEFAULT_MAX_GUIDE_CHARS,
) -> str:
    guide_text = "\n\n".join(
        chunk.to_markdown()
        for chunk in guide_chunks
    )
    return f"""
Compress the selected guide context into article-specific Korean translation guidance.

[Source Profile]
{source_profile.to_markdown()}

[Selected Guide Context]
{guide_text}

[Task]
- Return concise Markdown bullets only.
- Keep the result under {max_chars} characters.
- Focus on style, preservation policy, risk areas, and article-specific cautions.
- Do not translate the source article.
- Do not summarize source facts.
- Do not output source->target glossary mappings.
- Do not repeat concrete glossary entries.
- Do not invent terminology translations.
- Terminology mappings are handled separately by the Glossary section.
""".strip()


def sanitize_compressed_guide(raw_text: str, max_chars: int = DEFAULT_MAX_GUIDE_CHARS) -> str:
    text = strip_wrapping_fence(raw_text).strip()
    if not text:
        return ""

    kept: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.lower().startswith(("compressed translation guide", "translation guide")):
            continue
        if is_glossary_like_line(line):
            continue
        kept.append(line)

    return trim_lines_to_chars(kept, max_chars)


def strip_wrapping_fence(text: str) -> str:
    stripped = text.strip()
    if not stripped.startswith("```") or not stripped.endswith("```"):
        return stripped
    lines = stripped.splitlines()
    if len(lines) <= 2:
        return ""
    return "\n".join(lines[1:-1]).strip()


def is_glossary_like_line(line: str) -> bool:
    lowered = line.lower()
    if "glossary" in lowered:
        return True
    if GLOSSARY_ARROW_RE.search(line):
        return True
    match = GLOSSARY_COLON_RE.match(line)
    if not match:
        return False
    left = match.group(1).strip().strip("`*_").lower()
    right = match.group(2).strip()
    if left in ALLOWED_COLON_LABELS:
        return False
    return len(left.split()) <= 4 and len(right.split()) <= 6


def trim_lines_to_chars(lines: list[str], max_chars: int) -> str:
    if max_chars <= 0:
        return ""
    selected: list[str] = []
    used = 0
    for line in lines:
        next_used = used + len(line) + (1 if selected else 0)
        if next_used > max_chars:
            if not selected:
                return line[:max_chars].rstrip()
            break
        selected.append(line)
        used = next_used
    return "\n".join(selected).strip()


def build_compressed_guide(
    source_markdown: str,
    guide_paths: list[Path],
    model_call: Callable[[str], str],
    max_chars: int = DEFAULT_MAX_GUIDE_CHARS,
    source_excerpt_chars: int = DEFAULT_SOURCE_EXCERPT_CHARS,
) -> str:
    guide_docs = load_guide_docs(guide_paths)
    if not guide_docs:
        return ""

    source_profile = build_source_profile(source_markdown, source_excerpt_chars=source_excerpt_chars)
    selected_chunks = select_guide_chunks(guide_docs, source_profile)
    if not selected_chunks:
        return ""

    prompt = build_compression_prompt(source_profile, selected_chunks, max_chars=max_chars)
    try:
        raw_text = model_call(prompt)
    except Exception as exc:
        print(f"[context-compression] compression failed; continuing without guide: {exc}", flush=True)
        return ""
    compressed = sanitize_compressed_guide(raw_text, max_chars=max_chars)
    print(
        f"[context-compression] guide_docs={len(guide_docs)} selected_chunks={len(selected_chunks)} "
        f"raw_chars={len(raw_text)} compressed_chars={len(compressed)}",
        flush=True,
    )
    return compressed