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

test('renders blog progress as a stacked bar with counts and Blog Agent baseline note', () => {
  const html = renderProgress({
    total: 190, merged: 3, open: 2, remaining: 185, percent: 1.6, baselineDate: '2024-09-18',
  });

  assert.match(html, />1\.6%<\/strong>/);
  assert.match(html, /대상 190편 중 3편 병합/);
  assert.match(html, /aria-label="대상 190편 중 병합 3편, 번역 진행 중 2편"/);
  assert.match(html, /progress-fill-merged/);
  assert.match(html, /progress-fill-open/);
  assert.match(html, /병합 3편/);
  assert.match(html, /진행 중 2편/);
  assert.match(html, /남은 글 185편/);
  assert.match(html, /2024-09-18/);
  assert.match(html, /HuggingFace Blog Agent 적용일/);
  assert.match(html, /community\/enterprise 글 제외/);
  assert.doesNotMatch(renderProgress({ total: 4, merged: 0, open: 0, remaining: 4, percent: 0, baselineDate: '2024-09-18' }), /progress-fill/);
  assert.match(renderProgress(null), /불러오는 중/);
  assert.match(renderProgress({ percent: 50 }), /불러오는 중/);
});

test('renders quality and SEO pass rates against current PR reports', () => {
  const html = renderCheckStats({
    quality: { pass: 4, reviewNeeded: 5, total: 9, passPercent: 44.4 },
    seo: { pass: 3, reviewNeeded: 6, total: 9, passPercent: 33.3 },
  });

  assert.match(html, /품질 기준/);
  assert.match(html, /SEO 기준/);
  assert.match(html, /현재 PR 9건/);
  assert.match(html, /통과율 44\.4%/);
  assert.match(html, /통과 4건/);
  assert.match(html, /검토필요 5건/);
  assert.match(html, /aria-label="품질 기준: 현재 PR 9건 중 통과 4건, 검토필요 5건"/);
  assert.match(html, /check-seg-pass/);
  assert.match(html, /check-seg-review/);
  assert.match(renderCheckStats({ quality: { pass: 0, reviewNeeded: 0, total: 0, passPercent: 0 } }), /집계할 검토 항목이 아직 없습니다/);
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
