import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

function ruleBody(css, selector) {
  return css.match(new RegExp(`${selector}\\s*\\{([\\s\\S]*?)\\}`, 'i'))?.[1] ?? '';
}

test('index contains the monitor landmarks and module entrypoint', async () => {
  const html = await readFile(new URL('../index.html', import.meta.url), 'utf8');

  assert.match(html, /<main/);
  assert.match(html, /id="report-table"/);
  assert.match(html, /id="summary"/);
  assert.match(html, /id="api-status"[^>]*aria-live="polite"/);
  assert.match(html, /id="details-dialog"/);
  assert.match(html, /type="module" src="\.\/js\/app\.js"/);
  assert.match(html, /src="\.\/assets\/hf-krew\.png"/);
  assert.match(html, /rel="icon"[^>]*href="\.\/assets\/hf-krew\.png"/);
  assert.match(html, /id="api-status-text"/);
  assert.match(html, /option value="needs-review"/);
  assert.match(html, /id="progress"/);
  assert.match(html, /id="check-stats"/);
  assert.match(html, /현재 PR별 통과율/);
});

test('bundled organization image is a PNG', async () => {
  const image = await readFile(new URL('../assets/hf-krew.png', import.meta.url));
  assert.deepEqual([...image.subarray(0, 8)], [137, 80, 78, 71, 13, 10, 26, 10]);
});

test('styles include responsive records, focus, and reduced motion support', async () => {
  const css = await readFile(new URL('../styles.css', import.meta.url), 'utf8');
  const tableHeader = ruleBody(css, 'thead');

  assert.match(css, /@media\s*\(max-width:\s*760px\)/);
  assert.match(css, /data-label/);
  assert.match(css, /td:nth-child\(n\)[^{]*\{[^}]*width\s*:\s*auto/i);
  assert.doesNotMatch(tableHeader, /display\s*:\s*none/i);
  assert.match(tableHeader, /position\s*:\s*absolute/i);
  assert.match(tableHeader, /width\s*:\s*1px/i);
  assert.match(tableHeader, /height\s*:\s*1px/i);
  assert.match(tableHeader, /overflow\s*:\s*hidden/i);
  assert.match(tableHeader, /white-space\s*:\s*nowrap/i);
  assert.match(tableHeader, /clip(?:-path)?\s*:/i);
  assert.match(css, /:focus-visible/);
  assert.match(css, /prefers-reduced-motion:\s*reduce/);
  assert.doesNotMatch(css, /gradient/i);
  assert.doesNotMatch(css, /border-radius\s*:\s*(?:9|[1-9]\d+)px/i);
  assert.doesNotMatch(css, /font-size\s*:[^;{}]*(?:vw|vh|vmin|vmax)/i);
});

test('app lifecycle loads cached reports, safely refreshes GitHub state, and wires controls', async () => {
  const app = await readFile(new URL('../js/app.js', import.meta.url), 'utf8');

  assert.match(app, /from '\.\/blog\.js'/);
  assert.match(app, /from '\.\/github\.js'/);
  assert.match(app, /from '\.\/model\.js'/);
  assert.match(app, /from '\.\/view\.js'/);
  assert.match(app, /fetch\('\.\/data\/reports\.json'\)/);
  assert.match(app, /readCachedSnapshot\(/);
  assert.match(app, /writeCachedSnapshot\(/);
  assert.match(app, /createSingleFlight\(/);
  assert.match(app, /fetchPullStatuses\(/);
  assert.match(app, /renderRows\(/);
  assert.match(app, /renderSummary\(/);
  assert.match(app, /renderProgress\(/);
  assert.match(app, /renderCheckStats\(/);
  assert.match(app, /fetchBlogIndex\(/);
  assert.match(app, /fetchFirstBlogAgentPullCreatedAt\(/);
  assert.match(app, /eligibleBlogPosts\(/);
  assert.match(app, /readCachedBlogStats\(/);
  assert.match(app, /writeCachedBlogStats\(/);
  assert.match(app, /setInterval\([^,]+,\s*300_000\)/);
  assert.match(app, /document\.visibilityState\s*!==\s*'visible'/);
  assert.match(app, /visibilitychange/);
  assert.match(app, /window\.addEventListener\('online'/);
  assert.match(app, /refreshButton\.disabled\s*=\s*true/);
  assert.match(app, /finally/);
  assert.match(app, /searchInput\.addEventListener\('input'/);
  assert.match(app, /prStateControls\.addEventListener\('click'/);
  assert.match(app, /summary\.addEventListener\('click'/);
  assert.match(app, /setAttribute\('aria-pressed'/);
  assert.match(app, /reviewState\.addEventListener\('change'/);
  assert.match(app, /reportRows\.addEventListener\('click'/);
  assert.match(app, /renderDetails\(/);
  assert.match(app, /detailsDialog\.showModal\(\)/);
  assert.match(app, /detailsClose\.addEventListener\('click'/);
  assert.match(app, /detailsDialog\.addEventListener\('cancel'/);
  assert.match(app, /catch\s*\([^)]*\)\s*\{[\s\S]*?render\(/);
  assert.doesNotMatch(app, /method\s*:\s*['"](?:POST|PUT|PATCH|DELETE)['"]/i);
});

test('app refresh waits for a valid report snapshot before touching GitHub state', async () => {
  const app = await readFile(new URL('../js/app.js', import.meta.url), 'utf8');
  const readinessGuard = app.indexOf('if (!reportsReady)');

  assert.match(app, /let reportsReady = false;/);
  assert.match(app, /const refresh = createSingleFlight\(async \(\) => \{\s*if \(!reportsReady\) \{\s*return;\s*\}/);
  assert.ok(readinessGuard < app.indexOf('await fetchPullStatuses'));
  assert.ok(readinessGuard < app.indexOf('writeCachedSnapshot({'));
  assert.match(app, /reports = await loadReports\(\);[\s\S]*?render\(\);\s*reportsReady = true;\s*void refresh\(\);/);
  assert.match(app, /function renderFatalLoadError\(\) \{\s*reportsReady = false;/);
});
