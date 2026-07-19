import assert from 'node:assert/strict';
import test from 'node:test';

import { computeProgress, filterReports, joinReports, sortByPublishedDate, summarizeChecks, summarizeReports } from '../js/model.js';

const reportWithoutSeo = {
  prNumber: 168,
  source: { slug: 'torch-attention-profile', title: 'Profiling in PyTorch' },
  quality: { enabled: true, available: true, status: 'pass' },
  seo: { enabled: true, available: false, status: 'missing' },
};
const openPull = { number: 168, state: 'open', title: 'Translate Hugging Face blog post: Profiling in PyTorch' };

test('gives warnings and failures review attention before missing reports', () => {
  const items = joinReports([
    reportWithoutSeo,
    { ...reportWithoutSeo, prNumber: 169, quality: { enabled: true, available: true, status: 'warning' }, seo: { enabled: true, available: false, status: 'missing' } },
    { ...reportWithoutSeo, prNumber: 170, quality: { enabled: true, available: true, status: 'fail' }, seo: { enabled: false, available: false, status: 'missing' } },
    { ...reportWithoutSeo, prNumber: 171, quality: { enabled: true, available: true, status: 'pass' }, seo: { enabled: false, available: false, status: 'missing' } },
  ], new Map([[168, openPull]]));
  assert.deepEqual(items.map((item) => item.reviewState), ['pending', 'attention', 'attention', 'complete']);
});

test('treats incomplete enabled report data as pending before complete', () => {
  const reports = [
    { ...reportWithoutSeo, prNumber: 1, quality: { enabled: true }, seo: { enabled: false } },
    { ...reportWithoutSeo, prNumber: 2, quality: null, seo: { enabled: false } },
    { ...reportWithoutSeo, prNumber: 3, quality: { enabled: true, available: true }, seo: { enabled: false } },
    { ...reportWithoutSeo, prNumber: 4, quality: { enabled: true, available: false, status: 'warning' }, seo: { enabled: false } },
    { ...reportWithoutSeo, prNumber: 5, quality: { enabled: true, available: true, status: 'fail' }, seo: { enabled: false } },
    { ...reportWithoutSeo, prNumber: 6, quality: { enabled: true, available: true, status: 'pass' }, seo: { enabled: false } },
  ];

  assert.deepEqual(joinReports(reports).map((item) => item.reviewState), [
    'pending', 'pending', 'pending', 'attention', 'attention', 'complete',
  ]);
});

test('keeps absent GitHub data unknown rather than closed', () => {
  const [item] = joinReports([reportWithoutSeo], new Map());
  assert.equal(item.pr.state, 'unknown');
  assert.equal(item.prNumber, 168);
});

test('adds open pull requests that are missing from the report snapshot', () => {
  const items = joinReports([reportWithoutSeo], new Map([
    [168, { number: 168, state: 'open', title: 'Translate Hugging Face blog post: Profiling in PyTorch' }],
    [173, {
      number: 173,
      state: 'open',
      title: 'Translate Hugging Face blog post: Security incident disclosure — July 2026',
      htmlUrl: 'https://github.com/Hugging-Face-KREW/hugging-face-krew.github.io/pull/173',
      sourceUrl: 'https://huggingface.co/blog/security-incident-july-2026',
      createdAt: '2026-07-17T03:34:38Z',
    }],
    [170, {
      number: 170,
      state: 'open',
      title: 'Workflow security boundary update',
      htmlUrl: 'https://github.com/Hugging-Face-KREW/hugging-face-krew.github.io/pull/170',
      createdAt: '2026-07-13T13:55:34Z',
    }],
  ]));

  assert.deepEqual(items.map((item) => item.prNumber), [168, 173]);
  assert.equal(items[1].title, 'Security incident disclosure — July 2026');
  assert.equal(items[1].slug, 'security-incident-july-2026');
  assert.equal(items[1].source.url, 'https://huggingface.co/blog/security-incident-july-2026');
  assert.equal(items[1].source.published_date, '2026-07-17');
  assert.equal(items[1].translation.pr_url, 'https://github.com/Hugging-Face-KREW/hugging-face-krew.github.io/pull/173');
  assert.equal(items[1].quality.status, 'missing');
  assert.equal(items[1].seo.status, 'missing');
  assert.equal(items[1].reviewState, 'pending');
});

test('excludes tracked reports when the GitHub pull title is not a blog translation PR', () => {
  const items = joinReports([
    reportWithoutSeo,
    {
      ...reportWithoutSeo,
      prNumber: 170,
      source: { slug: 'workflow-security-boundary', title: 'Workflow security boundary update' },
    },
  ], new Map([
    [168, openPull],
    [170, { number: 170, state: 'open', title: 'Workflow security boundary update' }],
  ]));

  assert.deepEqual(items.map((item) => item.prNumber), [168]);
});

test('counts missing reports as review attention', () => {
  const items = joinReports([reportWithoutSeo], new Map([[168, openPull]]));
  assert.deepEqual(summarizeReports(items), {
    total: 1,
    open: 1,
    merged: 0,
    closed: 0,
    unknown: 0,
    attention: 1,
  });
});

test('summarizes all separate pull states', () => {
  const reports = ['merged', 'closed', 'unknown'].map((state, index) => ({ ...reportWithoutSeo, prNumber: index + 1, seo: { enabled: false, available: false, status: 'missing' } }));
  const pulls = new Map([
    [1, { number: 1, state: 'merged' }],
    [2, { number: 2, state: 'closed' }],
    [3, { number: 3, state: 'unknown' }],
  ]);
  assert.deepEqual(summarizeReports(joinReports(reports, pulls)), {
    total: 3,
    open: 0,
    merged: 1,
    closed: 1,
    unknown: 1,
    attention: 0,
  });
});

test('filters by query, pull request state, and review state', () => {
  const items = joinReports([
    reportWithoutSeo,
    { ...reportWithoutSeo, prNumber: 169, source: { slug: 'different-post', title: 'Different title' }, seo: { enabled: false, available: false, status: 'missing' } },
  ], new Map([[168, openPull], [169, { number: 169, state: 'closed' }]]));
  assert.deepEqual(filterReports(items, { query: 'torch', prState: 'open', reviewState: 'pending' }).map((item) => item.prNumber), [168]);
  assert.deepEqual(filterReports(items, { query: '', prState: 'all', reviewState: 'complete' }).map((item) => item.prNumber), [169]);
});

test('computes blog progress from merged and open tracked slugs', () => {
  const posts = [
    { slug: 'torch-attention-profile', date: '2026-07-10', tags: [] },
    { slug: 'open-post', date: '2026-07-10', tags: [] },
    { slug: 'untranslated-post', date: '2026-07-12', tags: [] },
    { slug: 'closed-post', date: '2026-07-13', tags: [] },
  ];
  const items = joinReports([
    reportWithoutSeo,
    { ...reportWithoutSeo, prNumber: 169, source: { slug: 'open-post', title: 'Open post' } },
    { ...reportWithoutSeo, prNumber: 170, source: { slug: 'closed-post', title: 'Closed post' } },
    { ...reportWithoutSeo, prNumber: 171, source: { slug: 'not-in-blog', title: 'Untracked slug' } },
  ], new Map([
    [168, { number: 168, state: 'merged' }],
    [169, openPull],
    [170, { number: 170, state: 'closed' }],
    [171, { number: 171, state: 'merged' }],
  ]));

  assert.deepEqual(computeProgress(posts, items), {
    total: 4,
    merged: 1,
    open: 1,
    remaining: 2,
    percent: 25,
    mergedSlugs: ['torch-attention-profile'],
    openSlugs: ['open-post'],
    days: [
      {
        date: '2026-07-10',
        total: 2,
        merged: 1,
        open: 1,
        remaining: 0,
        slugs: ['torch-attention-profile', 'open-post'],
      },
      {
        date: '2026-07-11',
        total: 0,
        merged: 0,
        open: 0,
        remaining: 0,
        slugs: [],
      },
      {
        date: '2026-07-12',
        total: 1,
        merged: 0,
        open: 0,
        remaining: 1,
        slugs: ['untranslated-post'],
      },
      {
        date: '2026-07-13',
        total: 1,
        merged: 0,
        open: 0,
        remaining: 1,
        slugs: ['closed-post'],
      },
    ],
  });
  assert.deepEqual(computeProgress([], items), {
    total: 0,
    merged: 0,
    open: 0,
    remaining: 0,
    percent: 0,
    mergedSlugs: [],
    openSlugs: [],
    days: [],
  });
});

test('aggregates per-check pass rates over open PRs with the worst check first', () => {
  const items = [
    {
      pr: { state: 'open' },
      quality: { enabled: true, checks: [
        { status: 'pass', text: 'contains Korean prose' },
        { status: 'fail', text: 'code fences are balanced' },
      ] },
      seo: { enabled: true, checks: [] },
    },
    {
      pr: { state: 'open' },
      quality: { enabled: true, checks: [
        { status: 'pass', text: 'contains Korean prose — 2 untranslated blocks' },
        { status: 'pass', text: 'code fences are balanced' },
      ] },
      seo: { enabled: false, checks: [{ status: 'fail', text: 'excluded because seo is disabled' }] },
    },
    {
      pr: { state: 'open' },
      quality: { enabled: true, available: false },
      seo: { enabled: true, available: false },
    },
    {
      pr: { state: 'merged' },
      quality: { enabled: true, checks: [{ status: 'fail', text: 'contains Korean prose' }] },
      seo: { enabled: true, checks: [{ status: 'pass', text: 'title length' }] },
    },
  ];

  assert.deepEqual(summarizeChecks(items), {
    quality: [
      { name: 'code fences are balanced', pass: 1, fail: 1, missing: 1, total: 3 },
      { name: 'contains Korean prose', pass: 2, fail: 0, missing: 1, total: 3 },
    ],
    seo: [],
    openCount: 3,
  });
  assert.deepEqual(summarizeChecks([]), { quality: [], seo: [], openCount: 0 });
});

test('sorts report items by published date with PR number tiebreak', () => {
  const items = [
    { prNumber: 1, source: { published_date: '2026-06-01' } },
    { prNumber: 3, source: { published_date: '2026-07-01' } },
    { prNumber: 2, source: { published_date: '2026-06-01' } },
    { prNumber: 4, source: {} },
  ];

  assert.deepEqual(sortByPublishedDate(items, 'desc').map((item) => item.prNumber), [3, 2, 1, 4]);
  assert.deepEqual(sortByPublishedDate(items, 'asc').map((item) => item.prNumber), [4, 1, 2, 3]);
});

test('filters needs-review as attention or pending combined', () => {
  const items = joinReports([
    reportWithoutSeo,
    { ...reportWithoutSeo, prNumber: 169, quality: { enabled: true, available: true, status: 'fail' }, seo: { enabled: false, available: false, status: 'missing' } },
    { ...reportWithoutSeo, prNumber: 170, quality: { enabled: true, available: true, status: 'pass' }, seo: { enabled: false, available: false, status: 'missing' } },
  ], new Map([[168, openPull]]));

  assert.deepEqual(
    filterReports(items, { reviewState: 'needs-review' }).map((item) => item.prNumber),
    [168, 169],
  );
});
