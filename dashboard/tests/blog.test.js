import assert from 'node:assert/strict';
import test from 'node:test';

import {
  eligibleBlogPosts,
  fetchBlogIndex,
  fetchFirstBlogAgentPullCreatedAt,
  parseBlogDate,
  parseBlogIndex,
  readCachedBlogStats,
  writeCachedBlogStats,
} from '../js/blog.js';

const SAMPLE_INDEX = `# comment line
- local: how-to-train
  date: February 14, 2020
  tags:
    - guide
    - nlp

- local: month-only
  date: March, 2020
  tags:
    - research

- local: torch-attention-profile
  date: July 10, 2026
  tags:
    - guide

- local: community-story
  date: July 11, 2026
  tags:
    - Community

- local: enterprise-notes
  date: July 12, 2026
  tags:
    - enterprise

- local: broken-date
  date: someday soon
  tags:
    - guide
`;

function memoryStorage(initial = {}) {
  const data = new Map(Object.entries(initial));
  return {
    getItem: (key) => (data.has(key) ? data.get(key) : null),
    setItem: (key, value) => { data.set(key, String(value)); },
    data,
  };
}

test('parses blog dates across the written formats used by _blog.yml', () => {
  assert.equal(parseBlogDate('February 14, 2020'), '2020-02-14');
  assert.equal(parseBlogDate('Sep 10, 2020'), '2020-09-10');
  assert.equal(parseBlogDate('March, 2020'), '2020-03-01');
  assert.equal(parseBlogDate('November 09, 2020'), '2020-11-09');
  assert.equal(parseBlogDate('"July 3, 2020"'), '2020-07-03');
  assert.equal(parseBlogDate('2026-07-10'), '2026-07-10');
  assert.equal(parseBlogDate('someday soon'), null);
  assert.equal(parseBlogDate(undefined), null);
});

test('parses the blog index into slug, date, and tag records', () => {
  const posts = parseBlogIndex(SAMPLE_INDEX);

  assert.equal(posts.length, 6);
  assert.deepEqual(posts[0], { slug: 'how-to-train', date: '2020-02-14', tags: ['guide', 'nlp'] });
  assert.deepEqual(posts[2], { slug: 'torch-attention-profile', date: '2026-07-10', tags: ['guide'] });
  assert.equal(posts[5].date, null);
});

test('keeps only dated official posts on or after the baseline date', () => {
  const posts = parseBlogIndex(SAMPLE_INDEX);
  const eligible = eligibleBlogPosts(posts, { baselineDate: '2024-09-18' });

  assert.deepEqual(eligible.map((post) => post.slug), ['torch-attention-profile']);
  assert.deepEqual(eligibleBlogPosts(posts, {}), []);
  assert.deepEqual(eligibleBlogPosts(null, { baselineDate: '2024-09-18' }), []);
});

test('fetches and validates the blog index over HTTPS', async () => {
  const posts = await fetchBlogIndex({
    fetchImpl: async (url) => {
      assert.match(url, /^https:\/\/raw\.githubusercontent\.com\/huggingface\/blog\/main\/_blog\.yml$/);
      return { ok: true, text: async () => SAMPLE_INDEX };
    },
  });
  assert.equal(posts.length, 6);

  await assert.rejects(fetchBlogIndex({ fetchImpl: async () => ({ ok: false, status: 500 }) }), /500/);
  await assert.rejects(fetchBlogIndex({ fetchImpl: async () => ({ ok: true, text: async () => '' }) }), TypeError);
});

test('fetches the earliest Blog Agent pull request creation date read-only', async () => {
  const requests = [];
  const createdAt = await fetchFirstBlogAgentPullCreatedAt({
    repository: 'Hugging-Face-KREW/hugging-face-krew.github.io',
    fetchImpl: async (url, options) => {
      requests.push(url);
      assert.match(url, /^https:\/\/api\.github\.com\/repos\/Hugging-Face-KREW\/hugging-face-krew\.github\.io\/pulls\?/);
      assert.match(url, /direction=asc/);
      assert.match(url, /per_page=100/);
      assert.equal(options.method, undefined);
      const page = new URL(url).searchParams.get('page');
      return {
        ok: true,
        json: async () => (page === '1'
          ? [
            ...Array.from({ length: 100 }, (_, index) => ({
              number: index + 1,
              title: `Maintenance PR ${index + 1}`,
              created_at: '2024-09-18T11:32:57Z',
            })),
          ]
          : [
            {
              number: 101,
              title: 'Translate Hugging Face blog post: torch-attention-profile',
              created_at: '2026-07-10T09:00:00Z',
            },
          ]),
      };
    },
  });
  assert.equal(createdAt, '2026-07-10T09:00:00Z');
  assert.equal(requests.length, 2);

  await assert.rejects(fetchFirstBlogAgentPullCreatedAt({ repository: 'bad' }), TypeError);
  await assert.rejects(fetchFirstBlogAgentPullCreatedAt({
    repository: 'a/b',
    fetchImpl: async () => ({ ok: true, json: async () => [] }),
  }), TypeError);
});

test('round-trips the blog cache and rejects invalid snapshots', () => {
  const storage = memoryStorage();
  const posts = [{ slug: 'torch-attention-profile', date: '2026-07-10', tags: ['guide'] }];
  const written = writeCachedBlogStats({
    storage,
    repository: 'a/b',
    fetchedAt: new Date().toISOString(),
    baselineAt: '2024-09-18T11:32:57Z',
    posts,
  });
  assert.equal(written, true);

  const cached = readCachedBlogStats({ storage, repository: 'a/b' });
  assert.deepEqual(cached.posts, posts);
  assert.equal(cached.baselineAt, '2024-09-18T11:32:57Z');
  assert.equal(cached.stale, false);

  const stale = readCachedBlogStats({ storage, repository: 'a/b', now: () => Date.now() + 7_200_000 });
  assert.equal(stale.stale, true);

  assert.equal(readCachedBlogStats({ storage, repository: 'other/repo' }), null);
  assert.equal(readCachedBlogStats({ storage: memoryStorage({ 'hf-krew-blog-stats': '{"broken"' }), repository: 'a/b' }), null);
  assert.equal(writeCachedBlogStats({ storage, repository: 'a/b', fetchedAt: 'not-a-date', baselineAt: '2024-09-18T11:32:57Z', posts }), false);
  assert.equal(writeCachedBlogStats({ storage, repository: 'a/b', fetchedAt: new Date().toISOString(), baselineAt: '2024-09-18T11:32:57Z', posts: [] }), false);
});
