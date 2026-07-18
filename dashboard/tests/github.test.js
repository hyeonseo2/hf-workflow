import assert from 'node:assert/strict';
import test from 'node:test';

import {
  GitHubApiError,
  createSingleFlight,
  fetchOpenPulls,
  fetchPullStatuses,
  normalizePull,
  readCachedSnapshot,
  writeCachedSnapshot,
} from '../js/github.js';

const REPOSITORY = 'owner/repo';

function pull(number, state = 'open', overrides = {}) {
  return {
    number,
    state,
    title: `Pull ${number}`,
    html_url: `https://github.com/${REPOSITORY}/pull/${number}`,
    created_at: '2026-07-01T00:00:00Z',
    updated_at: '2026-07-02T00:00:00Z',
    merged_at: null,
    ...overrides,
  };
}

function response({ status = 200, body = [], headers = {} } = {}) {
  return {
    ok: status >= 200 && status < 300,
    status,
    headers: new Headers(headers),
    json: async () => body,
  };
}

function storage(initial = {}) {
  const values = new Map(Object.entries(initial));
  return {
    getItem: (key) => values.get(key) ?? null,
    setItem: (key, value) => values.set(key, value),
    value: (key) => values.get(key),
  };
}

test('normalizes open, merged, and closed pull request states', () => {
  assert.equal(normalizePull(pull(1)).state, 'open');
  assert.equal(normalizePull(pull(2, 'closed', { merged_at: '2026-07-03T00:00:00Z' })).state, 'merged');
  assert.equal(normalizePull(pull(3, 'closed')).state, 'closed');
});

test('normalizes pull request title and source URL metadata', () => {
  const normalized = normalizePull(pull(10, 'open', {
    title: 'Translate Hugging Face blog post: New model',
    body: 'Source: https://huggingface.co/blog/new-model\n\nDraft translation.',
  }));

  assert.equal(normalized.title, 'Translate Hugging Face blog post: New model');
  assert.equal(normalized.sourceUrl, 'https://huggingface.co/blog/new-model');
});

test('normalizes malformed pull request data as unknown', () => {
  assert.equal(normalizePull({ number: 7, state: 'closed', merged_at: 'invalid' }).state, 'closed');
  assert.equal(normalizePull({ number: 7, state: 'unexpected' }).state, 'unknown');
  assert.equal(normalizePull({ number: '7', state: 'open' }).state, 'unknown');
});

test('fetches requested pull requests across pages and records rate-limit metadata', async () => {
  const requests = [];
  const result = await fetchPullStatuses({
    repository: REPOSITORY,
    numbers: [168, 42],
    fetchImpl: async (url, options) => {
      requests.push({ url, options });
      const page = new URL(url).searchParams.get('page');
      return page === '1'
        ? response({ body: [pull(168), ...Array.from({ length: 99 }, (_, index) => pull(index + 500))] })
        : response({ body: [pull(42)], headers: { 'x-ratelimit-remaining': '59', 'x-ratelimit-reset': '1782864000' } });
    },
  });

  assert.deepEqual([...result.pulls.keys()].sort((a, b) => a - b), [42, 168]);
  assert.equal(requests.length, 2);
  assert.equal(requests[0].url, 'https://api.github.com/repos/owner/repo/pulls?state=all&sort=created&direction=desc&per_page=100&page=1');
  assert.deepEqual(requests[0].options.headers, {
    Accept: 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
  });
  assert.deepEqual(result.rateLimit, { remaining: 59, resetAt: '2026-07-01T00:00:00.000Z' });
});

test('fetches only open translation pull requests across pages', async () => {
  const requests = [];
  const result = await fetchOpenPulls({
    repository: REPOSITORY,
    fetchImpl: async (url, options) => {
      requests.push({ url, options });
      const page = new URL(url).searchParams.get('page');
      return page === '1'
        ? response({ body: [
          pull(3, 'open', { title: 'Translate Hugging Face blog post: Third' }),
          pull(4, 'open', { title: 'Maintenance PR' }),
          ...Array.from({ length: 99 }, (_, index) => pull(index + 100)),
        ] })
        : response({
          body: [pull(2, 'open', { title: 'Translate Hugging Face blog post: Second' })],
          headers: { 'x-ratelimit-remaining': '57' },
        });
    },
  });

  assert.deepEqual([...result.pulls.keys()].sort((a, b) => a - b), [2, 3]);
  assert.equal(requests.length, 2);
  assert.equal(requests[0].url, 'https://api.github.com/repos/owner/repo/pulls?state=open&sort=created&direction=desc&per_page=100&page=1');
  assert.deepEqual(requests[0].options.headers, {
    Accept: 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
  });
  assert.deepEqual(result.rateLimit, { remaining: 57, resetAt: null });
});

test('continues beyond five full pages to find requested pull requests', async () => {
  const fullPage = Array.from({ length: 100 }, (_, index) => pull(index + 1));
  let calls = 0;
  const result = await fetchPullStatuses({
    repository: REPOSITORY,
    numbers: [777],
    fetchImpl: async (url) => {
      calls += 1;
      const page = Number(new URL(url).searchParams.get('page'));
      return response({ body: page === 8 ? [pull(777)] : fullPage });
    },
  });

  assert.equal(calls, 8);
  assert.equal(result.pulls.get(777).state, 'open');
});

test('marks requested but unresolved pull requests as unknown after a short page', async () => {
  const result = await fetchPullStatuses({
    repository: REPOSITORY,
    numbers: [168, 42],
    fetchImpl: async () => response({ body: [pull(168)] }),
  });

  assert.equal(result.pulls.get(42).state, 'unknown');
  assert.equal(result.pulls.get(42).number, 42);
  assert.deepEqual(result.rateLimit, { remaining: null, resetAt: null });
});

test('throws typed errors for non-success responses', async () => {
  await assert.rejects(
    fetchPullStatuses({
      repository: REPOSITORY,
      numbers: [168],
      fetchImpl: async () => response({ status: 403, headers: { 'x-ratelimit-remaining': '0' } }),
    }),
    (error) => error instanceof GitHubApiError && error.status === 403 && error.rateLimit.remaining === 0,
  );
});

test('preserves network errors and rejects malformed successful responses', async () => {
  const networkError = new Error('offline');
  await assert.rejects(
    fetchPullStatuses({ repository: REPOSITORY, numbers: [168], fetchImpl: async () => { throw networkError; } }),
    networkError,
  );
  await assert.rejects(
    fetchPullStatuses({ repository: REPOSITORY, numbers: [168], fetchImpl: async () => response({ body: {} }) }),
    /array/i,
  );
});

test('fails rather than returning a partial result when a later page fails', async () => {
  let calls = 0;
  await assert.rejects(
    fetchPullStatuses({
      repository: REPOSITORY,
      numbers: [168, 42],
      fetchImpl: async () => {
        calls += 1;
        return calls === 1 ? response({ body: [pull(168), ...Array.from({ length: 99 }, (_, index) => pull(index + 500))] }) : response({ status: 500 });
      },
    }),
    GitHubApiError,
  );
});

test('reads only valid cache envelopes and marks snapshots older than five minutes stale', () => {
  const now = Date.parse('2026-07-12T12:00:00Z');
  const valid = {
    schemaVersion: 2,
    repository: REPOSITORY,
    syncedAt: '2026-07-12T11:55:01Z',
    rateLimit: { remaining: 42, resetAt: '2026-07-12T13:00:00Z' },
    pulls: [normalizePull(pull(168))],
  };
  const current = readCachedSnapshot({ storage: storage({ snapshot: JSON.stringify(valid) }), key: 'snapshot', repository: REPOSITORY, now });
  assert.equal(current.stale, false);
  assert.equal(current.pulls.get(168).state, 'open');

  valid.syncedAt = '2026-07-12T11:54:00Z';
  assert.equal(readCachedSnapshot({ storage: storage({ snapshot: JSON.stringify(valid) }), key: 'snapshot', repository: REPOSITORY, now }).stale, true);
  assert.equal(readCachedSnapshot({ storage: storage({ snapshot: '{oops' }), key: 'snapshot', repository: REPOSITORY, now }), null);
  assert.equal(readCachedSnapshot({ storage: storage({ snapshot: JSON.stringify({ ...valid, repository: 'other/repo' }) }), key: 'snapshot', repository: REPOSITORY, now }), null);
});

test('rejects malformed cache values and tolerates storage read errors', () => {
  const now = Date.parse('2026-07-12T12:00:00Z');
  const invalidEntries = [
    { schemaVersion: 3, repository: REPOSITORY, syncedAt: '2026-07-12T11:59:00Z', pulls: [] },
    { schemaVersion: 2, repository: REPOSITORY, syncedAt: 'invalid', pulls: [] },
    { schemaVersion: 2, repository: REPOSITORY, syncedAt: '2026-07-12T11:59:00Z', pulls: [{ number: '168', state: 'open' }] },
  ];
  for (const value of invalidEntries) {
    assert.equal(readCachedSnapshot({ storage: storage({ snapshot: JSON.stringify(value) }), key: 'snapshot', repository: REPOSITORY, now }), null);
  }
  assert.equal(readCachedSnapshot({ storage: { getItem() { throw new Error('blocked'); } }, key: 'snapshot', repository: REPOSITORY, now }), null);
});

test('rejects cache envelopes without an owned rate-limit field', () => {
  const snapshot = {
    schemaVersion: 2,
    repository: REPOSITORY,
    syncedAt: '2026-07-12T11:59:00Z',
    pulls: [normalizePull(pull(168))],
  };
  assert.equal(readCachedSnapshot({
    storage: storage({ snapshot: JSON.stringify(snapshot) }),
    key: 'snapshot',
    repository: REPOSITORY,
    now: Date.parse('2026-07-12T12:00:00Z'),
  }), null);
});

test('writes valid cache envelopes and tolerates storage write errors', () => {
  const localStorage = storage();
  const written = writeCachedSnapshot({
    storage: localStorage,
    key: 'snapshot',
    repository: REPOSITORY,
    syncedAt: '2026-07-12T12:00:00Z',
    rateLimit: { remaining: 50, resetAt: null },
    pulls: new Map([[168, normalizePull(pull(168))]]),
  });
  assert.equal(written, true);
  assert.deepEqual(JSON.parse(localStorage.value('snapshot')).pulls.map((item) => item.number), [168]);
  assert.equal(writeCachedSnapshot({ storage: { setItem() { throw new Error('quota'); } }, key: 'snapshot', repository: REPOSITORY, syncedAt: '2026-07-12T12:00:00Z', pulls: new Map() }), false);
  assert.equal(writeCachedSnapshot({ storage: {}, key: 'snapshot', repository: REPOSITORY, syncedAt: '2026-07-12T12:00:00Z', pulls: new Map() }), false);
});

test('returns false when cache storage is null or unavailable by default', () => {
  const snapshot = {
    key: 'snapshot',
    repository: REPOSITORY,
    syncedAt: '2026-07-12T12:00:00Z',
    pulls: new Map(),
  };
  assert.equal(writeCachedSnapshot({ ...snapshot, storage: null }), false);
  assert.equal(writeCachedSnapshot(snapshot), false);
});

test('shares concurrent work and permits a new call after settlement', async () => {
  let calls = 0;
  let release;
  const gate = new Promise((resolve) => { release = resolve; });
  const singleFlight = createSingleFlight(async () => {
    calls += 1;
    await gate;
    return { calls };
  });
  const first = singleFlight();
  const second = singleFlight();
  assert.strictEqual(first, second);
  release();
  assert.deepEqual(await first, { calls: 1 });
  assert.deepEqual(await singleFlight(), { calls: 2 });
});

test('clears rejected work so a later single-flight call can succeed', async () => {
  let attempts = 0;
  const singleFlight = createSingleFlight(() => {
    attempts += 1;
    return attempts === 1 ? Promise.reject(new Error('offline')) : Promise.resolve('recovered');
  });

  await assert.rejects(singleFlight(), /offline/);
  assert.equal(await singleFlight(), 'recovered');
  assert.equal(attempts, 2);
});
