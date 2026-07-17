const PULL_STATES = new Set(['open', 'merged', 'closed', 'unknown']);
const REPORT_STATUSES = new Set(['pass', 'warning', 'fail']);

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

export function joinReports(reports, pulls = new Map()) {
  if (!Array.isArray(reports)) {
    return [];
  }
  return reports.map((report) => {
    const prNumber = report?.prNumber;
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
  return {
    total,
    merged,
    open,
    remaining: Math.max(total - merged - open, 0),
    percent: total > 0 ? Math.round((merged / total) * 1000) / 10 : 0,
    mergedSlugs,
    openSlugs,
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
        const entry = byName.get(name) ?? { name, pass: 0, total: 0 };
        entry.total += 1;
        if (check?.status === 'pass') {
          entry.pass += 1;
        }
        byName.set(name, entry);
      }
    }
    breakdown[kind] = [...byName.values()].sort((a, b) => (a.pass / a.total) - (b.pass / b.total));
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
