import assert from 'node:assert/strict';
import test from 'node:test';

import {
  escapeHtml,
  renderCheckStats,
  renderDetails,
  renderProgress,
  renderRows,
  renderSummary,
  safeExternalUrl,
  statusClass,
} from '../js/view.js';

const item = {
  prNumber: 168,
  title: 'Profiling in PyTorch',
  slug: 'torch-attention-profile',
  source: {
    url: 'https://huggingface.co/blog/torch-attention-profile',
    published_date: '2026-07-10',
  },
  translation: {
    branch: 'translate/torch-attention-profile',
    file_path: '_posts/2026-07-10-torch-attention-profile.md',
    pr_url: 'https://github.com/Hugging-Face-KREW/hugging-face-krew.github.io/pull/168',
  },
  pr: { state: 'open', htmlUrl: 'https://github.com/Hugging-Face-KREW/hugging-face-krew.github.io/pull/168', author: 'krew' },
  reviewState: 'pending',
  quality: {
    status: 'pass',
    enabled: true,
    available: true,
    fileName: 'quality-report.md',
    content: '# Quality Report\n\n## Checks\n\n- PASS: translation body is not empty',
    checks: [{ status: 'pass', text: 'translation body is not empty' }],
  },
  seo: {
    status: 'missing',
    enabled: true,
    available: false,
    fileName: 'seo-report.md',
    content: '',
    checks: [],
  },
};

test('escapes every untrusted archive and GitHub string in rows and details', () => {
  const dangerous = {
    ...item,
    title: '<img src=x onerror=alert(1)>',
    slug: 'slug&value',
    source: { ...item.source, url: 'javascript:alert(1)' },
    translation: {
      branch: '<script>alert(1)</script>',
      file_path: '" onmouseover="alert(1)',
      pr_url: 'data:text/html,boom',
    },
    pr: { state: 'closed', htmlUrl: 'javascript:alert(1)', author: '<b>attacker</b>' },
    quality: { status: 'fail', enabled: true, available: true, checks: [{ status: 'fail', text: '<svg onload=alert(1)>' }] },
  };

  const html = `${renderRows([dangerous])}${renderDetails(dangerous)}`;

  assert.doesNotMatch(html, /<img|<script|<svg/i);
  assert.match(html, /&lt;img/);
  assert.match(html, /&lt;script&gt;/);
  assert.match(html, /&lt;svg/);
  assert.match(html, /href="#" aria-disabled="true" tabindex="-1"/);
  assert.match(html, /닫힘/);
  assert.match(html, /실패/);
  assert.match(html, /미생성/);
});

test('renders summary tiles and an explicit empty table state', () => {
  const summary = renderSummary({ total: 7, open: 2, merged: 3, closed: 1, attention: 4 });

  assert.match(summary, /전체/);
  assert.match(summary, /열림/);
  assert.match(summary, /병합/);
  assert.match(summary, /닫힘/);
  assert.match(summary, /확인 필요/);
  assert.match(summary, />7</);
  assert.match(renderRows([]), /표시할 번역 보고서가 없습니다/);
});

test('renders summary tiles as filter buttons with a pressed active tile', () => {
  const summary = renderSummary({ total: 7, open: 2, merged: 3, closed: 1, attention: 4 }, 'open');

  assert.match(summary, /<button type="button" class="summary-tile summary-neutral"/);
  assert.match(summary, /data-summary-filter="all"/);
  assert.match(summary, /data-summary-filter="open"[\s\S]*?aria-pressed="true"/);
  assert.match(summary, /data-summary-filter="merged"[\s\S]*?aria-pressed="false"/);
  assert.match(summary, /data-summary-filter="needs-review"/);
  assert.match(summary, /summary-attention summary-alert/);
  assert.doesNotMatch(
    renderSummary({ total: 1, open: 1, merged: 0, closed: 0, attention: 0 }),
    /summary-alert/,
  );
});

test('renders blog progress as a date heatmap with per-day cells and Blog Agent baseline note', () => {
  const html = renderProgress({
    total: 4,
    merged: 1,
    open: 1,
    remaining: 2,
    percent: 25,
    baselineDate: '2026-04-28',
    days: [
      { date: '2026-07-10', total: 2, merged: 1, open: 1, remaining: 0, slugs: ['torch-profiler', 'torch-attention-profile'] },
      { date: '2026-07-11', total: 0, merged: 0, open: 0, remaining: 0, slugs: [] },
      { date: '2026-07-12', total: 1, merged: 0, open: 0, remaining: 1, slugs: ['untranslated-post'] },
      { date: '2026-07-13', total: 1, merged: 0, open: 0, remaining: 1, slugs: ['closed-post'] },
    ],
  });

  assert.match(html, />25<small>%<\/small>/);
  assert.match(html, /대상 4편 중 1편 병합 \(25%\)/);
  assert.match(html, /aria-label="날짜별 번역 진행률: 대상 4편 중 병합 1편, 번역 진행 중 1편, 남은 글 2편"/);
  assert.equal((html.match(/class="heat-cell/g) ?? []).length, 4);
  assert.match(html, /class="heat-cell heat-cell-mixed heat-cell-density-2" data-tip="2026-07-10 · 2편 · 병합 1 · 진행 1 · 미번역 0 · torch-profiler, torch-attention-profile"/);
  assert.match(html, /class="heat-cell heat-cell-empty" data-tip="2026-07-11 · 글 없음"/);
  assert.match(html, /class="heat-cell heat-cell-remaining heat-cell-density-1" data-tip="2026-07-12 · 1편 · 병합 0 · 진행 0 · 미번역 1 · untranslated-post"/);
  assert.match(html, /병합 1편/);
  assert.match(html, /번역 진행 중 1편/);
  assert.match(html, /남은 글 2편/);
  assert.match(html, /2026-04-28/);
  assert.match(html, /HuggingFace Blog Agent 적용일/);
  assert.match(html, /community\/enterprise 글 제외/);
  assert.doesNotMatch(
    renderProgress({ total: 0, merged: 0, open: 0, remaining: 0, percent: 0, baselineDate: '2026-04-28', days: [] }),
    /heat-cell-/,
  );
  assert.match(renderProgress(null), /불러오는 중/);
  assert.match(renderProgress({ percent: 50 }), /불러오는 중/);
});

test('renders per-check pass rates for open PRs with a priority marker on the worst check', () => {
  const html = renderCheckStats({
    quality: [
      { name: 'code fences are balanced', pass: 1, total: 3 },
      { name: 'contains Korean prose', pass: 3, total: 3 },
      { name: 'unmapped custom check', pass: 3, total: 3 },
    ],
    seo: [],
    openCount: 3,
  });

  assert.match(html, /<section class="check-column" aria-label="품질 통과율">/);
  assert.match(html, /<section class="check-column" aria-label="SEO 통과율">/);
  assert.match(html, /<h3>품질<\/h3>/);
  assert.match(html, /<h3>SEO<\/h3>/);
  assert.match(html, /check-worst">코드 펜스 균형/);
  assert.doesNotMatch(html, /check-worst">한국어 본문 포함/);
  assert.match(html, /unmapped custom check/);
  assert.match(html, /check-bar-low/);
  assert.match(html, /aria-label="코드 펜스 균형 통과 1\/3"/);
  assert.match(html, /1\/3/);
  assert.match(html, /3\/3/);
  assert.match(html, /현재 열린 PR에 SEO 보고서가 없습니다/);
  const empty = renderCheckStats({ quality: [], seo: [], openCount: 0 });
  assert.match(empty, /현재 열린 PR에 품질 보고서가 없습니다/);
  assert.match(empty, /현재 열린 PR에 SEO 보고서가 없습니다/);
});

test('renders raw quality and SEO report files behind file-view controls', () => {
  const html = renderDetails({
    ...item,
    seo: {
      status: 'pass',
      enabled: true,
      available: true,
      fileName: 'seo-report.md',
      content: '# SEO Report\n\n<script>alert(1)</script>\n\n- PASS: title exists',
      checks: [{ status: 'pass', text: 'title exists' }],
    },
  });

  assert.match(html, /품질 검사/);
  assert.match(html, /quality-report\.md/);
  assert.match(html, /SEO 검사/);
  assert.match(html, /seo-report\.md/);
  assert.match(html, /파일 보기/);
  assert.match(html, /# Quality Report/);
  assert.match(html, /# SEO Report/);
  assert.doesNotMatch(html, /<script>alert\(1\)<\/script>/);
  assert.match(html, /&lt;script&gt;alert\(1\)&lt;\/script&gt;/);
});

test('escapes HTML and permits only HTTPS external URLs', () => {
  assert.equal(escapeHtml(`<&>"'`), '&lt;&amp;&gt;&quot;&#39;');
  assert.equal(safeExternalUrl('https://github.com/Hugging-Face-KREW'), 'https://github.com/Hugging-Face-KREW');
  assert.equal(safeExternalUrl('javascript:alert(1)'), '#');
  assert.equal(safeExternalUrl('http://example.com'), '#');
  assert.equal(safeExternalUrl('//example.com'), '#');
});

test('uses only known state names for status CSS classes', () => {
  const knownStates = [
    'open', 'merged', 'closed', 'unknown',
    'complete', 'pending', 'attention',
    'pass', 'warning', 'fail', 'missing',
  ];

  assert.deepEqual(knownStates.map(statusClass), knownStates);
  assert.equal(statusClass('not-a-state'), 'unknown');
  assert.equal(statusClass('open evil'), 'unknown');
  assert.equal(statusClass('" onmouseover="alert(1)'), 'unknown');
});
