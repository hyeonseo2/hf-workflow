const API_VERSION = '2022-11-28';
const CACHE_SCHEMA_VERSION = 2;
const CACHE_STALE_AFTER_MS = 300_000;
const PULL_STATES = new Set(['open', 'merged', 'closed', 'unknown']);
const BLOG_TRANSLATION_PREFIX = 'Translate Hugging Face blog post:';

export class GitHubApiError extends Error {
  constructor(status, rateLimit) {
    super(`GitHub API request failed with status ${status}`);
    this.name = 'GitHubApiError';
    this.status = status;
    this.rateLimit = rateLimit;
  }
}

function isObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

function isTimestamp(value) {
  return typeof value === 'string' && Number.isFinite(Date.parse(value));
}

function optionalTimestamp(value) {
  return isTimestamp(value) ? value : null;
}

function optionalString(value) {
  return typeof value === 'string' && value.length > 0 ? value : null;
}

function sourceUrlFromBody(value) {
  const match = typeof value === 'string' ? value.match(/^Source:\s*(https:\/\/\S+)/m) : null;
  return match ? match[1] : null;
}

function isTranslationPull(pull) {
  return typeof pull?.title === 'string' && pull.title.startsWith(BLOG_TRANSLATION_PREFIX);
}

function validPullNumber(value) {
  return Number.isInteger(value) && value > 0;
}

function parseRateLimit(headers) {
  const remainingHeader = headers?.get?.('x-ratelimit-remaining');
  const resetHeader = headers?.get?.('x-ratelimit-reset');
  const remaining = remainingHeader === null || remainingHeader === undefined ? NaN : Number(remainingHeader);
  const resetSeconds = resetHeader === null || resetHeader === undefined ? NaN : Number(resetHeader);
  return {
    remaining: Number.isInteger(remaining) && remaining >= 0 ? remaining : null,
    resetAt: Number.isFinite(resetSeconds) && resetSeconds > 0
      ? new Date(resetSeconds * 1000).toISOString()
      : null,
  };
}

function isValidRateLimit(value) {
  return value === null || (
    isObject(value)
    && (value.remaining === null || (Number.isInteger(value.remaining) && value.remaining >= 0))
    && (value.resetAt === null || isTimestamp(value.resetAt))
  );
}

function isValidPullSnapshot(value) {
  return isObject(value)
    && validPullNumber(value.number)
    && PULL_STATES.has(value.state)
    && typeof value.draft === 'boolean'
    && (value.title === null || typeof value.title === 'string')
    && (value.sourceUrl === null || typeof value.sourceUrl === 'string')
    && (value.htmlUrl === null || typeof value.htmlUrl === 'string')
    && (value.author === null || typeof value.author === 'string')
    && (value.createdAt === null || isTimestamp(value.createdAt))
    && (value.updatedAt === null || isTimestamp(value.updatedAt))
    && (value.closedAt === null || isTimestamp(value.closedAt))
    && (value.mergedAt === null || isTimestamp(value.mergedAt));
}

function unknownPull(number) {
  return {
    number,
    state: 'unknown',
    draft: false,
    title: null,
    sourceUrl: null,
    htmlUrl: null,
    author: null,
    createdAt: null,
    updatedAt: null,
    closedAt: null,
    mergedAt: null,
  };
}

export function normalizePull(pull) {
  if (!isObject(pull) || !validPullNumber(pull.number)) {
    return unknownPull(null);
  }

  const mergedAt = optionalTimestamp(pull.merged_at ?? pull.mergedAt);
  const githubState = pull.state;
  const state = mergedAt
    ? 'merged'
    : githubState === 'open' || githubState === 'closed'
      ? githubState
      : 'unknown';

  return {
    number: pull.number,
    state,
    draft: Boolean(pull.draft),
    title: optionalString(pull.title),
    sourceUrl: optionalString(pull.sourceUrl ?? sourceUrlFromBody(pull.body)),
    htmlUrl: optionalString(pull.html_url ?? pull.htmlUrl),
    author: optionalString(pull.user?.login ?? pull.author),
    createdAt: optionalTimestamp(pull.created_at ?? pull.createdAt),
    updatedAt: optionalTimestamp(pull.updated_at ?? pull.updatedAt),
    closedAt: optionalTimestamp(pull.closed_at ?? pull.closedAt),
    mergedAt,
  };
}

function parseRepository(repository) {
  if (typeof repository !== 'string') {
    throw new TypeError('repository must be an owner/repo string');
  }
  const parts = repository.split('/');
  if (parts.length !== 2 || parts.some((part) => part.length === 0)) {
    throw new TypeError('repository must be an owner/repo string');
  }
  return parts;
}

export async function fetchPullStatuses({ repository, numbers, fetchImpl = globalThis.fetch, now = Date.now } = {}) {
  const [owner, repo] = parseRepository(repository);
  if (typeof fetchImpl !== 'function') {
    throw new TypeError('fetchImpl must be a function');
  }

  const requested = new Set(numbers ?? []);
  if ([...requested].some((number) => !validPullNumber(number))) {
    throw new TypeError('numbers must contain positive integers');
  }

  const pulls = new Map();
  let rateLimit = { remaining: null, resetAt: null };
  let page = 1;

  while (requested.size > 0) {
    const query = new URLSearchParams({
      state: 'all',
      sort: 'created',
      direction: 'desc',
      per_page: '100',
      page: String(page),
    });
    const url = `https://api.github.com/repos/${encodeURIComponent(owner)}/${encodeURIComponent(repo)}/pulls?${query}`;
    const response = await fetchImpl(url, {
      headers: {
        Accept: 'application/vnd.github+json',
        'X-GitHub-Api-Version': API_VERSION,
      },
    });
    rateLimit = parseRateLimit(response?.headers);
    if (!response?.ok) {
      throw new GitHubApiError(response?.status ?? 0, rateLimit);
    }

    const pagePulls = await response.json();
    if (!Array.isArray(pagePulls)) {
      throw new TypeError('GitHub pull response must be an array');
    }

    for (const rawPull of pagePulls) {
      const normalized = normalizePull(rawPull);
      if (requested.has(normalized.number)) {
        pulls.set(normalized.number, normalized);
        requested.delete(normalized.number);
      }
    }
    if (requested.size === 0 || pagePulls.length < 100) {
      break;
    }
    page += 1;
  }

  for (const number of requested) {
    pulls.set(number, unknownPull(number));
  }

  return {
    pulls,
    syncedAt: new Date(now()).toISOString(),
    rateLimit,
  };
}

export async function fetchOpenPulls({ repository, fetchImpl = globalThis.fetch, now = Date.now } = {}) {
  const [owner, repo] = parseRepository(repository);
  if (typeof fetchImpl !== 'function') {
    throw new TypeError('fetchImpl must be a function');
  }

  const pulls = new Map();
  let rateLimit = { remaining: null, resetAt: null };
  let page = 1;

  while (true) {
    const query = new URLSearchParams({
      state: 'open',
      sort: 'created',
      direction: 'desc',
      per_page: '100',
      page: String(page),
    });
    const url = `https://api.github.com/repos/${encodeURIComponent(owner)}/${encodeURIComponent(repo)}/pulls?${query}`;
    const response = await fetchImpl(url, {
      headers: {
        Accept: 'application/vnd.github+json',
        'X-GitHub-Api-Version': API_VERSION,
      },
    });
    rateLimit = parseRateLimit(response?.headers);
    if (!response?.ok) {
      throw new GitHubApiError(response?.status ?? 0, rateLimit);
    }

    const pagePulls = await response.json();
    if (!Array.isArray(pagePulls)) {
      throw new TypeError('GitHub pull response must be an array');
    }
    for (const rawPull of pagePulls) {
      const normalized = normalizePull(rawPull);
      if (normalized.state === 'open' && isTranslationPull(normalized)) {
        pulls.set(normalized.number, normalized);
      }
    }
    if (pagePulls.length < 100) {
      break;
    }
    page += 1;
  }

  return {
    pulls,
    syncedAt: new Date(now()).toISOString(),
    rateLimit,
  };
}

export function readCachedSnapshot({ storage = globalThis.localStorage, key = 'hf-krew-pr-snapshot', repository, now = Date.now() } = {}) {
  try {
    const stored = storage?.getItem(key);
    if (stored === null || stored === undefined) {
      return null;
    }
    const snapshot = JSON.parse(stored);
    if (!isObject(snapshot)
      || snapshot.schemaVersion !== CACHE_SCHEMA_VERSION
      || snapshot.repository !== repository
      || !isTimestamp(snapshot.syncedAt)
      || !Object.prototype.hasOwnProperty.call(snapshot, 'rateLimit')
      || !isValidRateLimit(snapshot.rateLimit)
      || !Array.isArray(snapshot.pulls)
      || !snapshot.pulls.every(isValidPullSnapshot)) {
      return null;
    }
    const syncedAt = Date.parse(snapshot.syncedAt);
    const currentTime = typeof now === 'function' ? now() : now;
    if (!Number.isFinite(currentTime)) {
      return null;
    }
    return {
      pulls: new Map(snapshot.pulls.map((pull) => [pull.number, pull])),
      syncedAt: snapshot.syncedAt,
      rateLimit: snapshot.rateLimit ?? null,
      stale: currentTime - syncedAt > CACHE_STALE_AFTER_MS,
    };
  } catch {
    return null;
  }
}

export function writeCachedSnapshot({
  storage = globalThis.localStorage,
  key = 'hf-krew-pr-snapshot',
  repository,
  syncedAt,
  rateLimit = null,
  pulls,
} = {}) {
  const entries = pulls instanceof Map ? [...pulls.values()] : null;
  if (typeof repository !== 'string'
    || !isTimestamp(syncedAt)
    || !isValidRateLimit(rateLimit)
    || !entries
    || !entries.every(isValidPullSnapshot)) {
    return false;
  }
  if (!storage || typeof storage.setItem !== 'function') {
    return false;
  }

  try {
    storage.setItem(key, JSON.stringify({
      schemaVersion: CACHE_SCHEMA_VERSION,
      repository,
      syncedAt,
      rateLimit,
      pulls: entries,
    }));
    return true;
  } catch {
    return false;
  }
}

export function createSingleFlight(task) {
  if (typeof task !== 'function') {
    throw new TypeError('task must be a function');
  }
  let inFlight;

  return (...args) => {
    if (inFlight) {
      return inFlight;
    }
    const current = Promise.resolve().then(() => task(...args));
    inFlight = current;
    current.then(
      () => { if (inFlight === current) inFlight = undefined; },
      () => { if (inFlight === current) inFlight = undefined; },
    );
    return current;
  };
}
