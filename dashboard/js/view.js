const PULL_STATE_LABELS = {
  open: '열림',
  merged: '병합',
  closed: '닫힘',
  unknown: '미확인',
};

const REVIEW_STATE_LABELS = {
  complete: '검토 완료',
  pending: '검토 대기',
  attention: '확인 필요',
};

const REPORT_STATUS_LABELS = {
  pass: '통과',
  warning: '경고',
  fail: '실패',
  missing: '미생성',
};

const KNOWN_STATUS_STATES = new Set([
  ...Object.keys(PULL_STATE_LABELS),
  ...Object.keys(REVIEW_STATE_LABELS),
  ...Object.keys(REPORT_STATUS_LABELS),
]);

function stringValue(value) {
  return value === null || value === undefined ? '' : String(value);
}

function recordValue(record, key) {
  return record && typeof record === 'object' ? record[key] : undefined;
}

function stateLabel(labels, state, fallback) {
  return labels[state] ?? fallback;
}

export function statusClass(state) {
  const value = stringValue(state);
  return KNOWN_STATUS_STATES.has(value) ? value : 'unknown';
}

function numberValue(value) {
  return Number.isFinite(value) ? String(value) : '0';
}

function externalLink(url, label) {
  const safeUrl = safeExternalUrl(url);
  const safeLabel = escapeHtml(label);
  if (safeUrl === '#') {
    return `<a href="#" aria-disabled="true" tabindex="-1">${safeLabel} (안전하지 않은 링크)</a>`;
  }
  return `<a href="${escapeHtml(safeUrl)}" target="_blank" rel="noopener noreferrer">${safeLabel} ↗</a>`;
}

function reportStatus(report) {
  const status = recordValue(report, 'status');
  return stateLabel(REPORT_STATUS_LABELS, status, '미생성');
}

function reportFileBlock(report) {
  const safeReport = report && typeof report === 'object' ? report : {};
  const content = stringValue(safeReport.content);
  const fileName = stringValue(safeReport.fileName) || 'report.md';
  if (!content) {
    return '<p class="report-file-missing">결과 파일이 없습니다.</p>';
  }
  return `<details class="report-file">
    <summary>파일 보기 <span class="path">${escapeHtml(fileName)}</span></summary>
    <pre tabindex="0"><code>${escapeHtml(content)}</code></pre>
  </details>`;
}

function reportBlock(label, report) {
  const safeReport = report && typeof report === 'object' ? report : {};
  const status = stringValue(safeReport.status);
  const checks = Array.isArray(safeReport.checks) ? safeReport.checks : [];
  const metrics = safeReport.metrics && typeof safeReport.metrics === 'object' ? safeReport.metrics : {};
  const checkItems = checks.length > 0
    ? checks.map((check) => {
      const checkStatus = stringValue(recordValue(check, 'status'));
      const labelText = stateLabel(REPORT_STATUS_LABELS, checkStatus, '미생성');
      return `<li><span class="status status-${statusClass(checkStatus)}">${escapeHtml(labelText)}</span> ${escapeHtml(recordValue(check, 'text'))}</li>`;
    }).join('')
    : '<li>세부 검토 항목이 없습니다.</li>';
  const metricItems = Object.entries(metrics).map(([key, value]) => (
    `<div><dt>${escapeHtml(key)}</dt><dd>${escapeHtml(value)}</dd></div>`
  )).join('');

  return `<section class="detail-report" aria-label="${escapeHtml(label)} 보고서">
    <h3>${escapeHtml(label)}</h3>
    <p><span class="status status-${statusClass(status)}">${escapeHtml(reportStatus(safeReport))}</span></p>
    <ul class="check-list">${checkItems}</ul>
    ${metricItems ? `<dl class="metrics">${metricItems}</dl>` : ''}
    ${reportFileBlock(safeReport)}
  </section>`;
}

export function escapeHtml(value) {
  return stringValue(value).replace(/[&<>"']/g, (character) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  })[character]);
}

export function safeExternalUrl(value) {
  try {
    const url = new URL(stringValue(value));
    return url.protocol === 'https:' ? stringValue(value) : '#';
  } catch {
    return '#';
  }
}

function safePercent(value) {
  return Number.isFinite(value) && value > 0 ? Math.min(value, 100) : 0;
}

export function renderProgress(progress = null) {
  if (!progress || !Number.isFinite(progress.total)) {
    return '<p class="progress-empty">huggingface.co/blog 글 목록을 불러오는 중입니다.</p>';
  }
  const total = Math.max(Number(progress.total) || 0, 0);
  const merged = Math.max(Number(progress.merged) || 0, 0);
  const open = Math.max(Number(progress.open) || 0, 0);
  const remaining = Math.max(Number(progress.remaining) || 0, 0);
  const percent = safePercent(progress.percent);
  const mergedWidth = safePercent(total > 0 ? (merged / total) * 100 : 0);
  const openWidth = safePercent(total > 0 ? (open / total) * 100 : 0);
  const baselineDate = escapeHtml(progress.baselineDate ?? '');

  return `<div class="progress-head">
    <p class="progress-percent"><strong>${percent}%</strong> 병합 완료</p>
    <p class="progress-count">대상 ${total}편 중 ${merged}편 병합</p>
  </div>
  <div class="progress-track" role="img" aria-label="대상 ${total}편 중 병합 ${merged}편, 번역 진행 중 ${open}편">
    ${merged > 0 ? `<div class="progress-fill progress-fill-merged" style="width: ${mergedWidth}%"></div>` : ''}
    ${open > 0 ? `<div class="progress-fill progress-fill-open" style="width: ${openWidth}%"></div>` : ''}
  </div>
  <p class="progress-legend">
    <span class="legend-item"><span class="legend-chip chip-merged" aria-hidden="true"></span>병합 ${merged}편</span>
    <span class="legend-item"><span class="legend-chip chip-open" aria-hidden="true"></span>진행 중 ${open}편</span>
    <span class="legend-item"><span class="legend-chip chip-remaining" aria-hidden="true"></span>남은 글 ${remaining}편</span>
  </p>
  <p class="progress-note">기준: HuggingFace Blog Agent 적용일(${baselineDate}) 이후 huggingface.co/blog 공식 글 · community/enterprise 글 제외</p>`;
}

function renderCheckRate(label, stats = {}) {
  const total = Math.max(Number(stats.total) || 0, 0);
  if (total === 0) {
    return '<p class="check-empty">집계할 검토 항목이 아직 없습니다.</p>';
  }
  const pass = Math.max(Number(stats.pass) || 0, 0);
  const reviewNeeded = Math.max(Number(stats.reviewNeeded) || 0, 0);
  const passPercent = safePercent(Number(stats.passPercent));
  const passWidth = safePercent(total > 0 ? (pass / total) * 100 : 0);
  const reviewWidth = safePercent(total > 0 ? (reviewNeeded / total) * 100 : 0);
  const safeLabel = escapeHtml(label);

  return `<div class="check-rate">
    <div class="check-rate-head">
      <span>현재 PR ${total}건</span>
      <strong>통과율 ${passPercent}%</strong>
    </div>
    <div class="check-bar check-rate-bar" role="img" aria-label="${safeLabel}: 현재 PR ${total}건 중 통과 ${pass}건, 검토필요 ${reviewNeeded}건">
      ${pass > 0 ? `<span class="check-seg check-seg-pass" style="width: ${passWidth}%"></span>` : ''}
      ${reviewNeeded > 0 ? `<span class="check-seg check-seg-review" style="width: ${reviewWidth}%"></span>` : ''}
    </div>
    <p class="check-rate-counts">
      <span><strong>통과</strong> ${pass}건</span>
      <span><strong>검토필요</strong> ${reviewNeeded}건</span>
    </p>
  </div>`;
}

export function renderCheckStats(stats = {}) {
  const groups = [
    ['품질 기준', stats.quality],
    ['SEO 기준', stats.seo],
  ];
  return groups.map(([label, checkStats]) => (
    `<section class="check-group" aria-label="${label} 현황">
      <h3>${label}</h3>
      ${renderCheckRate(label, checkStats)}
    </section>`
  )).join('');
}

export function renderSummary(summary = {}, activeFilter = 'all') {
  const tiles = [
    ['전체', 'total', 'neutral', 'all'],
    ['열림', 'open', 'open', 'open'],
    ['병합', 'merged', 'merged', 'merged'],
    ['닫힘', 'closed', 'closed', 'closed'],
    ['확인 필요', 'attention', 'attention', 'needs-review'],
  ];
  return tiles.map(([label, key, color, filter]) => {
    const value = numberValue(recordValue(summary, key));
    const alert = color === 'attention' && value !== '0' ? ' summary-alert' : '';
    return `<button type="button" class="summary-tile summary-${color}${alert}" data-summary-filter="${filter}"
      aria-pressed="${activeFilter === filter}" aria-label="${label} ${value}건 필터">
      <span>${label}</span><strong>${value}</strong>
    </button>`;
  }).join('');
}

export function renderRows(items = []) {
  if (!Array.isArray(items) || items.length === 0) {
    return '<tr class="empty-row"><td colspan="6">표시할 번역 보고서가 없습니다.</td></tr>';
  }

  return items.map((item) => {
    const source = recordValue(item, 'source') ?? {};
    const translation = recordValue(item, 'translation') ?? {};
    const pull = recordValue(item, 'pr') ?? {};
    const prState = stringValue(recordValue(pull, 'state'));
    const reviewState = stringValue(recordValue(item, 'reviewState'));
    const prNumber = recordValue(item, 'prNumber');
    const title = recordValue(item, 'title') || recordValue(source, 'title');
    const slug = recordValue(item, 'slug') || recordValue(source, 'slug');
    const pullUrl = recordValue(pull, 'htmlUrl') || recordValue(translation, 'pr_url');
    const reviewLabel = stateLabel(REVIEW_STATE_LABELS, reviewState, '미확인');
    const qualityLabel = reportStatus(recordValue(item, 'quality'));
    const seoLabel = reportStatus(recordValue(item, 'seo'));
    const filePath = stringValue(recordValue(translation, 'file_path'));
    const fileName = filePath.split('/').pop();

    return `<tr>
      <td data-label="PR">${externalLink(pullUrl, `#${prNumber}`)}</td>
      <td data-label="원문">${externalLink(recordValue(source, 'url'), title)}<br><span class="path">${escapeHtml(slug)}</span></td>
      <td data-label="PR 상태"><span class="status status-${statusClass(prState)}">${escapeHtml(stateLabel(PULL_STATE_LABELS, prState, '미확인'))}</span></td>
      <td data-label="검토"><span class="status status-${statusClass(reviewState)}">${escapeHtml(reviewLabel)}</span><br><span class="report-summary">품질 ${escapeHtml(qualityLabel)} · SEO ${escapeHtml(seoLabel)}</span></td>
      <td data-label="번역 경로"><span class="path" title="${escapeHtml(filePath)}">${escapeHtml(fileName)}</span></td>
      <td data-label="상세"><button type="button" class="detail-button" data-action="details" data-pr-number="${escapeHtml(prNumber)}">상세</button></td>
    </tr>`;
  }).join('');
}

export function renderDetails(item = {}) {
  const source = recordValue(item, 'source') ?? {};
  const translation = recordValue(item, 'translation') ?? {};
  const pull = recordValue(item, 'pr') ?? {};
  const prState = stringValue(recordValue(pull, 'state'));
  const reviewState = stringValue(recordValue(item, 'reviewState'));
  const title = recordValue(item, 'title') || recordValue(source, 'title');
  const prNumber = recordValue(item, 'prNumber');
  const pullUrl = recordValue(pull, 'htmlUrl') || recordValue(translation, 'pr_url');

  return `<div class="detail-content">
    <p class="eyebrow">PR #${escapeHtml(prNumber)}</p>
    <h2 id="details-title">${escapeHtml(title)}</h2>
    <p><span class="status status-${statusClass(prState)}">${escapeHtml(stateLabel(PULL_STATE_LABELS, prState, '미확인'))}</span> <span class="status status-${statusClass(reviewState)}">${escapeHtml(stateLabel(REVIEW_STATE_LABELS, reviewState, '미확인'))}</span></p>
    <dl class="detail-meta">
      <div><dt>원문</dt><dd>${externalLink(recordValue(source, 'url'), recordValue(source, 'slug') || '원문 보기')}</dd></div>
      <div><dt>번역 브랜치</dt><dd class="path">${escapeHtml(recordValue(translation, 'branch'))}</dd></div>
      <div><dt>번역 파일</dt><dd class="path">${escapeHtml(recordValue(translation, 'file_path'))}</dd></div>
      <div><dt>PR</dt><dd>${externalLink(pullUrl, 'GitHub PR 보기')}</dd></div>
      <div><dt>작성자</dt><dd>${escapeHtml(recordValue(pull, 'author')) || '정보 없음'}</dd></div>
    </dl>
    ${reportBlock('품질 검사', recordValue(item, 'quality'))}
    ${reportBlock('SEO 검사', recordValue(item, 'seo'))}
  </div>`;
}
