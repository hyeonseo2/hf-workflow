from __future__ import annotations

from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo

from scripts.create_translation_pr import (
    FeedPost,
    build_translation_markdown,
    html_to_markdown,
    parse_feed,
    select_posts,
    slug_from_url,
)
from scripts.translation_adapters import (
    PlaceholderTranslationAdapter,
    TranslationRequest,
    default_prompt_path,
    load_translation_prompt,
)


def test_parse_rss_feed_items() -> None:
    xml = """<?xml version="1.0"?>
    <rss>
      <channel>
        <item>
          <title>Test Post</title>
          <link>https://huggingface.co/blog/test-post</link>
          <pubDate>Mon, 11 May 2026 00:00:00 GMT</pubDate>
          <description>Summary</description>
        </item>
      </channel>
    </rss>
    """

    posts = parse_feed(xml)

    assert len(posts) == 1
    assert posts[0].title == "Test Post"
    assert posts[0].slug == "test-post"
    assert posts[0].published_date == date(2026, 5, 11)
    assert posts[0].published_at.tzinfo is not None


def test_parse_atom_feed_entries() -> None:
    xml = """<?xml version="1.0"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
      <entry>
        <title>Atom Post</title>
        <link href="https://huggingface.co/blog/atom-post" />
        <published>2026-05-11T12:00:00Z</published>
      </entry>
    </feed>
    """

    posts = parse_feed(xml)

    assert len(posts) == 1
    assert posts[0].url == "https://huggingface.co/blog/atom-post"
    assert posts[0].published_date == date(2026, 5, 11)


def test_select_posts_by_date() -> None:
    posts = [
        FeedPost("A", "https://huggingface.co/blog/a", datetime(2026, 5, 10, tzinfo=timezone.utc), "a"),
        FeedPost("B", "https://huggingface.co/blog/b", datetime(2026, 5, 11, tzinfo=timezone.utc), "b"),
    ]

    selected = select_posts(posts, date(2026, 5, 11), None, ZoneInfo("UTC"))

    assert [post.slug for post in selected] == ["b"]


def test_select_posts_by_local_timezone_date() -> None:
    posts = [
        FeedPost(
            "A",
            "https://huggingface.co/blog/a",
            datetime(2026, 5, 10, 18, 44, 11, tzinfo=timezone.utc),
            "a",
        ),
    ]

    selected = select_posts(posts, date(2026, 5, 11), None, ZoneInfo("Asia/Seoul"))

    assert [post.slug for post in selected] == ["a"]


def test_slug_from_url() -> None:
    assert slug_from_url("https://huggingface.co/blog/Transformers-to-MLX?x=1") == "transformers-to-mlx"


def test_build_translation_markdown_preserves_source_metadata() -> None:
    post = FeedPost(
        title="Hello MLX",
        url="https://huggingface.co/blog/hello-mlx",
        published_at=datetime(2026, 5, 11, tzinfo=timezone.utc),
        slug="hello-mlx",
    )

    markdown = build_translation_markdown(
        post,
        "# 안녕하세요\n\n본문입니다.",
        "none",
        "https://huggingface.co/blog/hello-mlx",
    )

    assert "layout: post" in markdown
    assert 'source_url: "https://huggingface.co/blog/hello-mlx"' in markdown
    assert "translation_status: \"draft\"" in markdown
    assert 'translator: "none"' in markdown
    assert "# 안녕하세요" in markdown


def test_html_to_markdown_extracts_article_shape() -> None:
    source = """
    <html><body><article><h1>Hello</h1><p>Use <code>mlx_lm</code>.</p>
    <pre><code>print("hi")</code></pre></article></body></html>
    """

    markdown = html_to_markdown(source)

    assert "# Hello" in markdown
    assert "Use `mlx_lm`." in markdown
    assert 'print("hi")' in markdown


def test_html_to_markdown_removes_blog_page_chrome() -> None:
    source = """
    <div class="blog-content">
      <div class="mb-4"><a href="/blog">Back to Articles</a></div>
      <h1>Title</h1>
      <div class="not-prose"><nav><li>Table of contents</li></nav></div>
      <p>Actual body with <a href="/models">models</a>.</p>
    </div>
    """

    markdown = html_to_markdown(source)

    assert "Back to Articles" not in markdown
    assert "Table of contents" not in markdown
    assert "# Title" in markdown
    assert "Actual body with [models](/models)." in markdown


def test_placeholder_adapter_keeps_source_markdown() -> None:
    adapter = PlaceholderTranslationAdapter()

    translated = adapter.translate(
        TranslationRequest(
            title="Hello",
            source_url="https://huggingface.co/blog/hello",
            source_markdown="# Hello",
        )
    )

    assert "TODO: Add Korean translation." in translated
    assert "# Hello" in translated


def test_default_translation_prompt_is_stored_in_docs() -> None:
    prompt = load_translation_prompt(default_prompt_path())

    assert "Hugging Face technical blog posts" in prompt
    assert "Output Korean Markdown only" in prompt
    assert "Chunking Rules" in prompt
