# HF KREW Translation Monitor

This is a dependency-free static dashboard. The source ZIP archive, generated
`data/reports.json`, and `Hugging-Face-KREW/hugging-face-krew.github.io` target
repository are read-only inputs. The dashboard never creates or changes GitHub
or repository data.

## Regenerate Report Data

From the repository root, regenerate the committed snapshot with:

```bash
python3 dashboard/scripts/build_data.py /path/to/hf-workflow-main.zip dashboard/data/reports.json
```

The source archive must contain the repository's `reports/pr-*/` directories.
Replace the source archive path when preparing a new read-only snapshot.
Review the resulting JSON before committing it; the browser application only
reads the committed `dashboard/data/reports.json` file.

## Run Locally

```bash
cd dashboard
npm test
npm run dev
```

Open http://127.0.0.1:4173/.

The dashboard reads the report snapshot first, then checks public GitHub Pull
Request state immediately and every five minutes while the page is visible. A
manual refresh, returning to a visible tab, and reconnecting online use the
same in-flight request.

GitHub requests are unauthenticated public API GET requests, so they are
subject to GitHub's public rate limit. After a successful response the browser
stores a normalized local cache. If a later request is unavailable or limited,
the dashboard retains the cached and report data and shows a stale status.

## Translation Progress Panel

The progress panel compares merged translations against official posts on
https://huggingface.co/blog. The browser reads two additional public sources:

- `https://raw.githubusercontent.com/huggingface/blog/main/_blog.yml` for the
  official post list (posts tagged `community` or `enterprise` are excluded,
  and org/user community articles are not in this file at all).
- The target repository's earliest pull request whose title starts with
  `Translate Hugging Face blog post:`. This is treated as the HuggingFace Blog
  Agent adoption date, and only posts published on or after that date count
  toward the progress denominator.

Both results are cached in `localStorage` for one hour. If either fetch fails,
the panel keeps the last cached progress and the rest of the dashboard is
unaffected.

## Static Hosting

1. Regenerate and review `dashboard/data/reports.json` locally.
2. Upload the contents of `dashboard/` to any static web host.
3. Serve `index.html` at the site root with the `data/`, `js/`, `assets/`, and
   `styles.css` paths unchanged.

No backend, token, build step, or write-capable GitHub credential is required.
