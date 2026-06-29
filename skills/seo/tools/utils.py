"""Utility functions for SEO skill"""
import re
from pathlib import Path
from typing import Dict, Any

import yaml


def parse_frontmatter(content: str) -> tuple[Dict[str, Any], str]:
    """
    Parse Jekyll frontmatter from markdown content.

    Uses a real YAML parser so multi-line block lists, quoted strings, and
    nested structures round-trip correctly (the previous hand-rolled parser
    broke on block-style `categories:` lists).

    Returns:
        (frontmatter_dict, body_content)
    """
    pattern = r'^---\s*\n(.*?)\n---\s*\n?(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return {}, content

    yaml_content, body = match.group(1), match.group(2)
    try:
        frontmatter = yaml.safe_load(yaml_content) or {}
    except yaml.YAMLError:
        frontmatter = {}
    if not isinstance(frontmatter, dict):
        frontmatter = {}

    return frontmatter, body


def count_chars(text: str) -> int:
    """Unicode codepoint count (the right SERP-truncation proxy for Korean;
    byte length would unfairly penalize CJK at 3 bytes/char)."""
    return len(text.strip())


def is_mostly_korean(text: str) -> bool:
    """True if Hangul outweighs ASCII letters — used to pick language-aware
    length thresholds."""
    hangul = len(re.findall(r'[가-힣]', text))
    ascii_letters = len(re.findall(r'[A-Za-z]', text))
    return hangul >= ascii_letters


def count_words(text: str) -> int:
    """Count words in text"""
    return len(text.split())


def extract_headings(content: str) -> list[tuple[int, str]]:
    """
    Extract headings from markdown content.

    Returns:
        List of (level, text) tuples
    """
    headings = []
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            text = line.lstrip('#').strip()
            if text:
                headings.append((level, text))
    return headings


def extract_images(content: str) -> list[Dict[str, str]]:
    """
    Extract images from markdown content.

    Returns:
        List of dicts with 'src' and 'alt' keys
    """
    images = []

    # Markdown images: ![alt](src)
    pattern = r'!\[(.*?)\]\((.*?)\)'
    for match in re.finditer(pattern, content):
        images.append({
            'alt': match.group(1),
            'src': match.group(2)
        })

    # HTML images: <img ...>. Scan the whole tag and read src/alt independently
    # so an alt-LESS <img> (e.g. `<figure><img src=…>`) is captured with alt=''
    # and still counted against alt-coverage, instead of being silently skipped.
    for match in re.finditer(r'<img\b[^>]*>', content, re.IGNORECASE):
        tag = match.group(0)
        src_m = re.search(r'src=["\']([^"\']*)["\']', tag, re.IGNORECASE)
        if not src_m:
            continue
        alt_m = re.search(r'alt=["\']([^"\']*)["\']', tag, re.IGNORECASE)
        images.append({
            'src': src_m.group(1),
            'alt': alt_m.group(1) if alt_m else '',
        })

    return images


def extract_links(content: str) -> list[str]:
    """Extract markdown links from content, excluding image embeds.

    A leading ``!`` (i.e. ``![alt](src)``) marks an image, not a link. Matching
    it here would double-count images as citations (D4) and internal links (D9),
    so the negative lookbehind drops image syntax.
    """
    links = []
    pattern = r'(?<!\!)\[([^\]]+)\]\(([^\)]+)\)'
    for match in re.finditer(pattern, content):
        links.append(match.group(2))
    return links


def check_citations(content: str) -> int:
    """
    Count potential citations in content.
    Looks for:
    - [Source](url)
    - "quote" — Source
    - According to X
    - X% (statistics)
    """
    count = 0

    # Links as citations
    links = extract_links(content)
    count += len([l for l in links if 'http' in l])

    # "According to" patterns
    according_pattern = r'(according to|based on|reported by|study by|research by)'
    count += len(re.findall(according_pattern, content, re.IGNORECASE))

    # Statistics with percentage
    stats_pattern = r'\d+%|\d+\.\d+%'
    count += len(re.findall(stats_pattern, content))

    return count


def _is_boilerplate_line(line: str) -> bool:
    """True for template scaffolding that precedes the real lede on Jekyll/KREW
    posts — HTML comments (incl. ``<!--toc-->``), the ``{:toc}`` / ``* TOC``
    table-of-contents markers, and Liquid tags. Treated as not-prose so the
    opening-summary measurement reflects the introduction, not the TOC."""
    s = line.strip()
    if not s:
        return True
    if s.startswith('<!--') and s.endswith('-->'):
        return True
    if (s.startswith('{%') and s.endswith('%}')) or (s.startswith('{{') and s.endswith('}}')):
        return True
    if '{:toc}' in s:
        return True
    if re.match(r'^[*+\-]\s*TOC\b', s, re.IGNORECASE):
        return True
    return False


def _is_attribution(paragraph: str) -> bool:
    """True for the italic source-attribution line KREW posts place before the
    lede (e.g. ``_이 글은 … 을 번역한 글입니다._``) — not the real opening."""
    s = paragraph.strip()
    italic = (s.startswith('_') and s.endswith('_')) or (s.startswith('*') and s.endswith('*'))
    return italic and ('번역' in s)


def get_opening_paragraphs(content: str, num_paragraphs: int = 3) -> str:
    """Get the first N real paragraphs from markdown content.

    Skips template boilerplate (HTML comments / ``<!--toc-->`` / ``{:toc}`` /
    ``* TOC`` / Liquid tags) and the italic source-attribution line so the
    opening reflects the actual introduction rather than the table of contents
    (PR #8 review: previously a false-positive source for the opening check).
    """
    # Remove frontmatter if exists
    _, body = parse_frontmatter(content)

    paragraphs = []
    for block in body.split('\n\n'):
        # Drop boilerplate lines inside the block (e.g. `<!--toc-->` glued to text).
        kept = [ln for ln in block.split('\n') if not _is_boilerplate_line(ln)]
        para = '\n'.join(kept).strip()
        if not para or para.startswith('#') or _is_attribution(para):
            continue
        paragraphs.append(para)

    return '\n\n'.join(paragraphs[:num_paragraphs])
