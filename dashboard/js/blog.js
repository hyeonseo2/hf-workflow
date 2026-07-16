const BLOG_INDEX_URL = 'https://raw.githubusercontent.com/huggingface/blog/main/_blog.yml';
const API_VERSION = '2022-11-28';
const CACHE_SCHEMA_VERSION = 1;
const CACHE_STALE_AFTER_MS = 3_600_000;
const EXCLUDED_TAGS = new Set(['community', 'enterprise']);

const MONTHS = new Map([
  ['january', 1], ['february', 2], ['march', 3], ['april', 4], ['may', 5], ['june', 6],
  ['july', 7], ['august', 8], ['september', 9], ['october', 10], ['november', 11], ['december', 12],
  ['jan', 1], ['feb', 2], ['mar', 3], ['apr', 4], ['jun', 6],
  ['jul', 7], ['aug', 8], ['sep', 9], ['sept', 9], ['oct', 10], ['nov', 11], ['dec', 12],
]);

function isObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

function isTimestamp(value) {
  return typeof value === 'string' && Number.isFinite(Date.parse(value));
}

function pad(value) {
  return String(value).padStart(2, '0');
}

export function parseBlogDate(raw) {
  if (typeof raw !== 'string') {
    return null;
  }
  const value = raw.trim().replace(/^['"]|['"]$/g, '').trim();
  const iso = value.match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (iso) {
    return `${iso[1]}-${iso[2]}-${iso[3]}`;
  }
  const written = value.match(/^([A-Za-z]+)\.?\s*(\d{1,2})?(?:st|nd|rd|th)?\s*,?\s*(\d{4})$/);
  if (!written) {
    return null;
  }
  const month = MONTHS.get(written[1].toLowerCase());
  const day = written[2] === undefined ? 1 : Number(written[2]);
  if (!month || !Number.isInteger(day) || day < 1 || day > 31) {
    return null;
  }
  return `${written[3]}-${pad(month)}-${pad(day)}`;
}

export function parseBlogIndex(text) {
  const posts = [];
  let current = null;
  for (const rawLine of String(text).split('\n')) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#')) {
      continue;
    }
    const slugMatch = line.match(/^- local:\s*(\S+)\s*$/);
    if (slugMatch) {
      current = { slug: slugMatch[1], date: null, tags: [] };
      posts.push(current);
      continue;
    }
    if (!current) {
      continue;
    }
    if (line.startsWith('date:')) {
      current.date = parseBlogDate(line.slice('date:'.length));
    } else if (/^- [^:]+$/.test(line)) {
      current.tags.push(line.slice(2).trim());
    }
  }
  return posts;
}

export function eligibleBlogPosts(posts, { baselineDate, excludedTags = EXCLUDED_TAGS } = {}) {
  if (!Array.isArray(posts) || typeof baselineDate !== 'string' || !baselineDate) {
    return [];
  }
  return posts.filter((post) => (
    typeof post?.date === 'string'
    && post.date >= baselineDate
    && !post.tags?.some((tag) => excludedTags.has(String(tag).toLowerCase()))
  ));
}

export async function fetchBlogIndex({ fetchImpl = globalThis.fetch } = {}) {
  const response = await fetchImpl(BLOG_INDEX_URL);
  if (!response?.ok) {
    throw new Error(`blog index request failed with status ${response?.status ?? 0}`);
  }
  const posts = parseBlogIndex(await response.text());
  if (posts.length === 0) {
    throw new TypeError('blog index contains no posts');
  }
  return posts;
}

export async function fetchFirstPullCreatedAt({ repository, fetchImpl = globalThis.fetch } = {}) {
  const parts = typeof repository === 'string' ? repository.split('/') : [];
  if (parts.length !== 2 || parts.some((part) => part.length === 0)) {
    throw new TypeError('repository must be an owner/repo string');
  }
  const query = new URLSearchParams({ state: 'all', sort: 'created', direction: 'asc', per_page: '1' });
  const url = `https://api.github.com/repos/${encodeURIComponent(parts[0])}/${encodeURIComponent(parts[1])}/pulls?${query}`;
  const response = await fetchImpl(url, {
    headers: {
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': API_VERSION,
    },
  });
  if (!response?.ok) {
    throw new Error(`first pull request lookup failed with status ${response?.status ?? 0}`);
  }
  const pulls = await response.json();
  const createdAt = Array.isArray(pulls) ? pulls[0]?.created_at : null;
  if (!isTimestamp(createdAt)) {
    throw new TypeError('first pull request creation date is unavailable');
  }
  return createdAt;
}

function isValidPost(value) {
  return isObject(value)
    && typeof value.slug === 'string'
    && value.slug.length > 0
    && (value.date === null || /^\d{4}-\d{2}-\d{2}$/.test(value.date))
    && Array.isArray(value.tags)
    && value.tags.every((tag) => typeof tag === 'string');
}

export function readCachedBlogStats({ storage = globalThis.localStorage, key = 'hf-krew-blog-stats', repository, now = Date.now } = {}) {
  try {
    const stored = storage?.getItem(key);
    if (stored === null || stored === undefined) {
      return null;
    }
    const snapshot = JSON.parse(stored);
    if (!isObject(snapshot)
      || snapshot.schemaVersion !== CACHE_SCHEMA_VERSION
      || snapshot.repository !== repository
      || !isTimestamp(snapshot.fetchedAt)
      || !isTimestamp(snapshot.baselineAt)
      || !Array.isArray(snapshot.posts)
      || snapshot.posts.length === 0
      || !snapshot.posts.every(isValidPost)) {
      return null;
    }
    const currentTime = typeof now === 'function' ? now() : now;
    if (!Number.isFinite(currentTime)) {
      return null;
    }
    return {
      posts: snapshot.posts,
      baselineAt: snapshot.baselineAt,
      stale: currentTime - Date.parse(snapshot.fetchedAt) > CACHE_STALE_AFTER_MS,
    };
  } catch {
    return null;
  }
}

export function writeCachedBlogStats({
  storage = globalThis.localStorage,
  key = 'hf-krew-blog-stats',
  repository,
  fetchedAt,
  baselineAt,
  posts,
} = {}) {
  if (typeof repository !== 'string'
    || !isTimestamp(fetchedAt)
    || !isTimestamp(baselineAt)
    || !Array.isArray(posts)
    || posts.length === 0
    || !posts.every(isValidPost)) {
    return false;
  }
  if (!storage || typeof storage.setItem !== 'function') {
    return false;
  }
  try {
    storage.setItem(key, JSON.stringify({
      schemaVersion: CACHE_SCHEMA_VERSION,
      repository,
      fetchedAt,
      baselineAt,
      posts,
    }));
    return true;
  } catch {
    return false;
  }
}
