import assert from 'node:assert/strict';
import test from 'node:test';

import {
  escapeHtml,
  renderDetails,
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
