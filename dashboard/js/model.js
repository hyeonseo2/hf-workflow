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
  let merged = 0;
  let open = 0;
  for (const post of posts) {
    const state = states.get(post?.slug);
    if (state === 'merged') {
      merged += 1;
    } else if (state === 'open') {
      open += 1;
    }
  }
  const total = posts.length;
  return {
    total,
    merged,
    open,
    remaining: Math.max(total - merged - open, 0),
    percent: total > 0 ? Math.round((merged / total) * 1000) / 10 : 0,
  };
}

function emptyCheckSummary() {
  return { pass: 0, reviewNeeded: 0, total: 0, passPercent: 0 };
}

function reportPassState(report) {
  if (report?.enabled === false) {
    return 'excluded';
  }
  return report?.available === true && report?.status === 'pass' ? 'pass' : 'reviewNeeded';
}

function withPassPercent(summary) {
  return {
    ...summary,
    passPercent: summary.total > 0 ? Math.round((summary.pass / summary.total) * 1000) / 10 : 0,
  };
}

export function summarizeChecks(items) {
  const groups = { quality: emptyCheckSummary(), seo: emptyCheckSummary() };
  for (const item of items ?? []) {
    for (const kind of ['quality', 'seo']) {
      const state = reportPassState(item?.[kind]);
      if (state === 'excluded') {
        continue;
      }
      groups[kind].total += 1;
      groups[kind][state] += 1;
    }
  }
  return {
    quality: withPassPercent(groups.quality),
    seo: withPassPercent(groups.seo),
  };
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
