# HF Blog Translation Quality Skill

Use this skill when reviewing a specific Korean Hugging Face Blog translation
file for quality.

## Inputs

Prefer a `translation-flow` manifest. If no manifest is provided, ask for:

- source blog URL or source text
- translation file path
- any project terminology rules

## Procedure

1. Read the manifest and the target translation file.
2. Fetch or inspect the source post when available.
3. Check fidelity: the Korean text should preserve the source meaning.
4. Check fluency: Korean should read naturally for technical readers.
5. Check terminology: product names, model names, API names, and library names
   should be consistent.
6. Check formatting: frontmatter, headings, links, images, tables, and code
   blocks should be preserved.
7. Flag untranslated English only when it is prose that should have been
   translated. Do not flag code, identifiers, model names, or product names.

## Output

Use a compact scorecard:

- fidelity
- fluency
- terminology
- formatting
- links

When editing files, summarize the fixes and any remaining risks.
