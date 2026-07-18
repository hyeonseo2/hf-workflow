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

const CHECK_NAME_LABELS = {
  'translation body is not empty': '번역 본문 존재',
  'no TODO marker remains': 'TODO 마커 없음',
  'code fences are balanced': '코드 펜스 균형',
  'contains Korean prose': '한국어 본문 포함',
  'source attribution exists': '출처 표기',
  'frontmatter title exists': '제목(frontmatter) 존재',
  'frontmatter slug exists': '슬러그(frontmatter) 존재',
  'categories exists': '카테고리 존재',
  'source_url exists': '원문 URL 존재',
  'has H1': 'H1 헤딩 존재',
  'has at least three section headings': '섹션 헤딩 3개 이상',
  'has source attribution sentence': '출처 문장 포함',
};

export function checkNameLabel(name) {
  return CHECK_NAME_LABELS[name] ?? name;
}

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
      return `<li><span class="status status-${statusClass(checkStatus)}">${escapeHtml(labelText)}</span> <span>${escapeHtml(checkNameLabel(stringValue(recordValue(check, 'text'))))}</span></li>`;
    }).join('')
    : '<li>세부 검토 항목이 없습니다.</li>';
  const metricItems = Object.entries(metrics).map(([key, value]) => (
    `<div><dt>${escapeHtml(key)}</dt><dd>${escapeHtml(value)}</dd></div>`
  )).join('');

  return `<section class="detail-report" aria-label="${escapeHtml(label)} 보고서">
    <h3>${escapeHtml(label)} <span class="status status-${statusClass(status)}">${escapeHtml(reportStatus(safeReport))}</span></h3>
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

function heatCellClass(day) {
  if (!day?.total) {
    return 'heat-cell-empty';
  }
  const states = [
    day.merged > 0 ? 'merged' : '',
    day.open > 0 ? 'open' : '',
    day.remaining > 0 ? 'remaining' : '',
  ].filter(Boolean);
  return states.length === 1 ? `heat-cell-${states[0]}` : 'heat-cell-mixed';
}

function heatCellTip(day) {
  if (!day?.total) {
    return `${day?.date ?? ''} · 글 없음`;
  }
  const slugs = Array.isArray(day.slugs) && day.slugs.length > 0 ? ` · ${day.slugs.join(', ')}` : '';
  return `${day.date} · ${day.total}편 · 병합 ${day.merged} · 진행 ${day.open} · 미번역 ${day.remaining}${slugs}`;
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
  const baselineDate = escapeHtml(progress.baselineDate ?? '');
  const days = Array.isArray(progress.days) ? progress.days : [];
  const cells = days.map((day) => {
    const density = Math.min(Math.max(Number(day?.total) || 0, 0), 4);
    const densityClass = density > 0 ? ` heat-cell-density-${density}` : '';
    return `<i class="heat-cell ${heatCellClass(day)}${densityClass}" data-tip="${escapeHtml(heatCellTip(day))}"></i>`;
  }).join('');

  return `<div class="waffle-head">
    <strong class="waffle-percent">${Math.round(percent)}<small>%</small></strong>
    <span class="waffle-count">대상 ${total}편 중 ${merged}편 병합 (${percent}%)</span>
  </div>
  <div class="heatmap" role="img" aria-label="날짜별 번역 진행률: 대상 ${total}편 중 병합 ${merged}편, 번역 진행 중 ${open}편, 남은 글 ${remaining}편">${cells}</div>
  <p class="progress-legend">
    <span class="legend-item"><span class="legend-chip chip-merged" aria-hidden="true"></span>병합 ${merged}편</span>
    <span class="legend-item"><span class="legend-chip chip-open" aria-hidden="true"></span>번역 진행 중 ${open}편</span>
    <span class="legend-item"><span class="legend-chip chip-remaining" aria-hidden="true"></span>남은 글 ${remaining}편</span>
  </p>
  <p class="progress-note">기준: HuggingFace Blog Agent 적용일(${baselineDate}) 이후 huggingface.co/blog 공식 글 · community/enterprise 글 제외</p>`;
}

function renderCheckRow(entry, isWorst) {
  const total = Math.max(Number(entry?.total) || 0, 0);
  const pass = Math.max(Number(entry?.pass) || 0, 0);
  const percent = total > 0 ? (pass / total) * 100 : 0;
  const tone = percent === 100 ? '' : percent >= 70 ? ' check-bar-mid' : ' check-bar-low';
  const name = checkNameLabel(stringValue(entry?.name));
  return `<div class="check-row">
    <span class="check-name${isWorst ? ' check-worst' : ''}">${escapeHtml(name)}</span>
    <span class="check-bar${tone}" role="img" aria-label="${escapeHtml(name)} 통과 ${pass}/${total}"><b style="width: ${percent}%"></b></span>
    <span class="check-counts">${pass}/${total}</span>
  </div>`;
}

export function renderCheckStats(stats = {}) {
  const groups = [
    ['품질', stats.quality],
    ['SEO', stats.seo],
  ];
  return groups.map(([label, entries]) => {
    const heading = `<section class="check-column" aria-label="${label} 통과율"><h3>${label}</h3>`;
    if (!Array.isArray(entries) || entries.length === 0) {
      return `${heading}<p class="check-empty">현재 열린 PR에 ${label} 보고서가 없습니다. 워크플로가 보고서를 생성하면 여기에 집계됩니다.</p></section>`;
    }
    return heading + entries.map((entry, index) => (
      renderCheckRow(entry, index === 0 && entry.pass < entry.total)
    )).join('') + '</section>';
  }).join('');
}

export function renderSummary(summary = {}, activeFilter = 'all') {
  const tiles = [
    ['전체', 'total', 'neutral', 'all', '모든 번역 PR'],
    ['열림', 'open', 'open', 'open', '번역 진행 중'],
    ['병합', 'merged', 'merged', 'merged', '게시 완료'],
    ['닫힘', 'closed', 'closed', 'closed', '철회·중복'],
    ['확인 필요', 'attention', 'attention', 'needs-review', '검토 대기·막힘'],
  ];
  return tiles.map(([label, key, color, filter, description]) => {
    const value = numberValue(recordValue(summary, key));
    const alert = color === 'attention' && value !== '0' ? ' summary-alert' : '';
    return `<button type="button" class="summary-tile summary-${color}${alert}" data-summary-filter="${filter}"
      aria-pressed="${activeFilter === filter}" aria-label="${label} ${value}건 필터">
      <span>${label}</span><strong>${value}</strong><em>${description}</em>
    </button>`;
  }).join('');
}

export function renderRows(items = []) {
  if (!Array.isArray(items) || items.length === 0) {
    return `<tr class="empty-row"><td colspan="6">표시할 번역 보고서가 없습니다.<br>
      <button type="button" class="reset-button" data-action="reset-filters">필터 초기화</button></td></tr>`;
  }

  return items.map((item) => {
    const source = recordValue(item, 'source') ?? {};
    const pull = recordValue(item, 'pr') ?? {};
    const prState = stringValue(recordValue(pull, 'state'));
    const reviewState = stringValue(recordValue(item, 'reviewState'));
    const prNumber = recordValue(item, 'prNumber');
    const title = recordValue(item, 'title') || recordValue(source, 'title');
    const slug = recordValue(item, 'slug') || recordValue(source, 'slug');
    const reviewLabel = stateLabel(REVIEW_STATE_LABELS, reviewState, '미확인');
    const quality = recordValue(item, 'quality');
    const seo = recordValue(item, 'seo');
    const publishedDate = stringValue(recordValue(source, 'published_date'));

    return `<tr tabindex="0" role="button" data-pr-number="${escapeHtml(prNumber)}" aria-label="PR ${escapeHtml(prNumber)} 상세 보기">
      <td class="pr-cell" data-label="PR">#${escapeHtml(prNumber)}</td>
      <td data-label="원문">${escapeHtml(title)}<span class="path">${escapeHtml(slug)}</span></td>
      <td data-label="PR 상태"><span class="status status-${statusClass(prState)}">${escapeHtml(stateLabel(PULL_STATE_LABELS, prState, '미확인'))}</span></td>
      <td data-label="검토"><span class="status status-${statusClass(reviewState)}">${escapeHtml(reviewLabel)}</span></td>
      <td class="date-cell" data-label="게시일">${escapeHtml(publishedDate) || '—'}</td>
      <td data-label="품질 / SEO"><span class="status status-${statusClass(stringValue(recordValue(quality, 'status')))}">${escapeHtml(reportStatus(quality))}</span> <span class="status status-${statusClass(stringValue(recordValue(seo, 'status')))}">${escapeHtml(reportStatus(seo))}</span></td>
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
  const publishedDate = stringValue(recordValue(source, 'published_date'));

  return `<div class="detail-content">
    <p class="eyebrow"><mark>PR #${escapeHtml(prNumber)}</mark>${publishedDate ? ` · ${escapeHtml(publishedDate)} 게시` : ''}</p>
    <h2 id="details-title">${escapeHtml(title)}</h2>
    <p class="detail-badges"><span class="status status-${statusClass(prState)}">${escapeHtml(stateLabel(PULL_STATE_LABELS, prState, '미확인'))}</span> <span class="status status-${statusClass(reviewState)}">${escapeHtml(stateLabel(REVIEW_STATE_LABELS, reviewState, '미확인'))}</span></p>
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
