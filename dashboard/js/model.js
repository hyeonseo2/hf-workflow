const PULL_STATES = new Set(['open', 'merged', 'closed', 'unknown']);
const REPORT_STATUSES = new Set(['pass', 'warning', 'fail']);
const BLOG_TRANSLATION_PREFIX = 'Translate Hugging Face blog post:';

function reportNeedsAttention(report) {
  return report?.status === 'warning' || report?.status === 'fail';
}

function reportIsIncomplete(report) {
  return report?.enabled !== false && (
    report?.available !== true || !REPORT_STATUSES.has(report?.status)
  );
}

function reviewStateFor(report) {
  const results = [report.quality, report.seo];
  if (results.some(reportNeedsAttention)) {
    return 'attention';
  }
  return results.some(reportIsIncomplete) ? 'pending' : 'complete';
}

function unknownPull(prNumber) {
  return { number: prNumber, state: 'unknown' };
}

function pullFor(pulls, prNumber) {
  const pull = pulls instanceof Map ? pulls.get(prNumber) : undefined;
  if (!pull || !PULL_STATES.has(pull.state)) {
    return unknownPull(prNumber);
  }
  return { ...pull, number: prNumber };
}

function titleFromPull(pull) {
  const title = typeof pull?.title === 'string' ? pull.title.trim() : '';
  return title.startsWith(BLOG_TRANSLATION_PREFIX)
    ? title.slice(BLOG_TRANSLATION_PREFIX.length).trim()
    : title;
}

function isTranslationPull(pull) {
  return typeof pull?.title === 'string' && pull.title.startsWith(BLOG_TRANSLATION_PREFIX);
}

function shouldIncludeReport(report, pulls) {
  if (!(pulls instanceof Map)) {
    return true;
  }
  const pull = pulls.get(report?.prNumber);
  return typeof pull?.title !== 'string' || isTranslationPull(pull);
}

function slugFromSourceUrl(value, fallback) {
  try {
    const url = new URL(String(value));
    const slug = url.pathname.split('/').filter(Boolean).pop();
    return slug || fallback;
  } catch {
    return fallback;
  }
}

function missingReport(fileName) {
  return {
    enabled: true,
    available: false,
    status: 'missing',
    checks: [],
    fileName,
    content: '',
  };
}

function reportFromOpenPull(pull) {
  const fallbackSlug = `pr-${pull.number}`;
  const slug = slugFromSourceUrl(pull.sourceUrl, fallbackSlug);
  const title = titleFromPull(pull) || `PR #${pull.number}`;
  return {
    prNumber: pull.number,
    title,
    slug,
    source: {
      title,
      slug,
      url: pull.sourceUrl ?? pull.htmlUrl ?? '',
      published_date: typeof pull.createdAt === 'string' ? pull.createdAt.slice(0, 10) : '',
    },
    translation: {
      target_repo: '',
      branch: '',
      file_path: '',
      pr_url: pull.htmlUrl ?? '',
      locale: 'ko',
    },
    quality: missingReport('quality-report.md'),
    seo: missingReport('seo-report.md'),
    requestAvailable: false,
    githubOnly: true,
  };
}

export function joinReports(reports, pulls = new Map()) {
  if (!Array.isArray(reports)) {
    return [];
  }
  const reportNumbers = new Set();
  const trackedReports = reports.filter((report) => shouldIncludeReport(report, pulls));
  const items = trackedReports.map((report) => {
    const prNumber = report?.prNumber;
    reportNumbers.add(prNumber);
    const source = report?.source ?? {};
    return {
      ...report,
      prNumber,
      title: source.title ?? '',
      slug: source.slug ?? '',
      pr: pullFor(pulls, prNumber),
      reviewState: reviewStateFor(report ?? {}),
    };
  });
  if (pulls instanceof Map) {
    for (const pull of pulls.values()) {
      if (pull?.state === 'open'
        && Number.isInteger(pull.number)
        && !reportNumbers.has(pull.number)
        && isTranslationPull(pull)) {
        const report = reportFromOpenPull(pull);
        items.push({
          ...report,
          pr: pullFor(pulls, pull.number),
          reviewState: reviewStateFor(report),
        });
      }
    }
  }
  return items;
}

export function filterReports(items, { query = '', prState = 'all', reviewState = 'all' } = {}) {
  const normalizedQuery = String(query).trim().toLocaleLowerCase();
  return items.filter((item) => {
    const searchable = [item.prNumber, item.title, item.slug, item.source?.url]
      .filter((value) => value !== null && value !== undefined)
      .join(' ')
      .toLocaleLowerCase();
    const reviewMatches = reviewState === 'all'
      || (reviewState === 'needs-review'
        ? item.reviewState === 'attention' || item.reviewState === 'pending'
        : item.reviewState === reviewState);
    return (!normalizedQuery || searchable.includes(normalizedQuery))
      && (prState === 'all' || item.pr?.state === prState)
      && reviewMatches;
  });
}

export function computeProgress(posts = [], items = []) {
  const states = new Map();
  for (const item of items) {
    if (item?.slug) {
      states.set(item.slug, item.pr?.state);
    }
  }
  const mergedSlugs = [];
  const openSlugs = [];
  for (const post of posts) {
    const state = states.get(post?.slug);
    if (state === 'merged') {
      mergedSlugs.push(post.slug);
    } else if (state === 'open') {
      openSlugs.push(post.slug);
    }
  }
  const total = posts.length;
  const merged = mergedSlugs.length;
  const open = openSlugs.length;
  const datedPosts = posts.filter((post) => typeof post?.date === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(post.date));
  const postsByDate = new Map();
  for (const post of datedPosts) {
    const state = states.get(post.slug);
    const entry = postsByDate.get(post.date) ?? {
      date: post.date,
      total: 0,
      merged: 0,
      open: 0,
      remaining: 0,
      slugs: [],
    };
    entry.total += 1;
    entry.slugs.push(post.slug);
    if (state === 'merged') {
      entry.merged += 1;
    } else if (state === 'open') {
      entry.open += 1;
    } else {
      entry.remaining += 1;
    }
    postsByDate.set(post.date, entry);
  }
  const sortedDates = [...postsByDate.keys()].sort();
  const days = [];
  if (sortedDates.length > 0) {
    const cursor = new Date(`${sortedDates[0]}T00:00:00Z`);
    const last = new Date(`${sortedDates[sortedDates.length - 1]}T00:00:00Z`);
    while (cursor <= last) {
      const date = cursor.toISOString().slice(0, 10);
      days.push(postsByDate.get(date) ?? {
        date,
        total: 0,
        merged: 0,
        open: 0,
        remaining: 0,
        slugs: [],
      });
      cursor.setUTCDate(cursor.getUTCDate() + 1);
    }
  }
  return {
    total,
    merged,
    open,
    remaining: Math.max(total - merged - open, 0),
    percent: total > 0 ? Math.round((merged / total) * 1000) / 10 : 0,
    mergedSlugs,
    openSlugs,
    days,
  };
}

export function summarizeChecks(items) {
  const openItems = (items ?? []).filter((item) => item?.pr?.state === 'open');
  const breakdown = { quality: [], seo: [], openCount: openItems.length };
  for (const kind of ['quality', 'seo']) {
    const byName = new Map();
    for (const item of openItems) {
      const report = item?.[kind];
      if (report?.enabled === false || !Array.isArray(report?.checks)) {
        continue;
      }
      for (const check of report.checks) {
        const name = String(check?.text ?? '').split(' — ')[0].trim();
        if (!name) {
          continue;
        }
        const entry = byName.get(name) ?? { name, pass: 0, fail: 0, missing: 0, total: breakdown.openCount };
        if (check?.status === 'pass') {
          entry.pass += 1;
        } else {
          entry.fail += 1;
        }
        byName.set(name, entry);
      }
    }
    for (const entry of byName.values()) {
      entry.missing = Math.max(entry.total - entry.pass - entry.fail, 0);
    }
    breakdown[kind] = [...byName.values()].sort((a, b) => (a.pass - b.pass) || (b.fail - a.fail));
  }
  return breakdown;
}

export function sortByPublishedDate(items, direction = 'desc') {
  const factor = direction === 'asc' ? 1 : -1;
  return [...(items ?? [])].sort((a, b) => {
    const left = String(a?.source?.published_date ?? '');
    const right = String(b?.source?.published_date ?? '');
    if (left !== right) {
      return left < right ? -factor : factor;
    }
    return ((a?.prNumber ?? 0) - (b?.prNumber ?? 0)) * factor;
  });
}

export function summarizeReports(items) {
  return items.reduce((summary, item) => {
    summary.total += 1;
    const state = PULL_STATES.has(item.pr?.state) ? item.pr.state : 'unknown';
    summary[state] += 1;
    if (item.reviewState === 'attention' || item.reviewState === 'pending') {
      summary.attention += 1;
    }
    return summary;
  }, {
    total: 0,
    open: 0,
    merged: 0,
    closed: 0,
    unknown: 0,
    attention: 0,
  });
}
