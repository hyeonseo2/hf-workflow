# HF Blog SEO Skill

Use this skill when optimizing a specific Korean Hugging Face Blog translation
file for SEO.

## Inputs

Prefer a `translation-flow` manifest. If no manifest is provided, ask for:

- source blog URL
- translation file path
- target keyword, if any

## Procedure

1. Read the manifest and the target translation file.
2. Inspect frontmatter fields such as title, description, tags, and slug.
3. Compare the Korean title and description against the source post intent.
4. Improve search clarity without changing the technical meaning.
5. Check heading hierarchy and make headings scannable.
6. Suggest or add relevant internal links only when they are contextually useful.
7. Preserve code blocks, links, frontmatter structure, and technical terms.

## Output

When editing files, summarize:

- title or description changes
- heading changes
- link changes
- any SEO concerns left unresolved

When reviewing only, produce a concise findings list with file references.
