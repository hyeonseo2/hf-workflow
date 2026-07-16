import assert from 'node:assert/strict';
import test from 'node:test';

import { computeProgress, filterReports, joinReports, summarizeChecks, summarizeReports } from '../js/model.js';

const reportWithoutSeo = {
  prNumber: 168,
  source: { slug: 'torch-attention-profile', title: 'Profiling in PyTorch' },
  quality: { enabled: true, available: true, status: 'pass' },
  seo: { enabled: true, available: false, status: 'missing' },
};
const openPull = { number: 168, state: 'open', title: 'Open translation PR' };

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
    { slug: 'open-post', date: '2026-07-11', tags: [] },
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
  });
  assert.deepEqual(computeProgress([], items), {
    total: 0,
    merged: 0,
    open: 0,
    remaining: 0,
    percent: 0,
  });
});

test('aggregates quality and SEO check outcomes by criterion', () => {
  const items = [
    {
      quality: { checks: [{ status: 'pass', text: 'no TODO marker remains' }, { status: 'fail', text: 'code fences are balanced' }] },
      seo: { checks: [{ status: 'pass', text: 'frontmatter title exists' }] },
    },
    {
      quality: { checks: [{ status: 'warning', text: 'no TODO marker remains' }, { status: 'unknown', text: 'ignored status' }, { status: 'pass', text: '' }] },
      seo: { checks: [] },
    },
    { quality: null, seo: undefined },
  ];

  assert.deepEqual(summarizeChecks(items), {
    quality: [
      { text: 'no TODO marker remains', pass: 1, warning: 1, fail: 0, total: 2 },
      { text: 'code fences are balanced', pass: 0, warning: 0, fail: 1, total: 1 },
    ],
    seo: [
      { text: 'frontmatter title exists', pass: 1, warning: 0, fail: 0, total: 1 },
    ],
  });
  assert.deepEqual(summarizeChecks([]), { quality: [], seo: [] });
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
