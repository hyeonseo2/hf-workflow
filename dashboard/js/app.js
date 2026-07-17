import {
  eligibleBlogPosts,
  fetchBlogIndex,
  fetchFirstBlogAgentPullCreatedAt,
  readCachedBlogStats,
  writeCachedBlogStats,
} from './blog.js';
import {
  createSingleFlight,
  fetchPullStatuses,
  readCachedSnapshot,
  writeCachedSnapshot,
} from './github.js';
import { computeProgress, filterReports, joinReports, sortByPublishedDate, summarizeChecks, summarizeReports } from './model.js';
import { renderCheckStats, renderDetails, renderProgress, renderRows, renderSummary } from './view.js';

const REPOSITORY = 'Hugging-Face-KREW/hugging-face-krew.github.io';
const CACHE_KEY = 'hf-krew-pr-snapshot';
const BLOG_CACHE_KEY = 'hf-krew-blog-stats';

const apiStatus = document.querySelector('#api-status');
const apiStatusText = document.querySelector('#api-status-text');
const syncedAt = document.querySelector('#synced-at');
const refreshButton = document.querySelector('#refresh-button');
const summary = document.querySelector('#summary');
const progress = document.querySelector('#progress');
const checkStats = document.querySelector('#check-stats');
const searchInput = document.querySelector('#search-input');
const prStateControls = document.querySelector('#pr-state-controls');
const reviewState = document.querySelector('#review-state');
const reportRows = document.querySelector('#report-rows');
const sortDateButton = document.querySelector('#sort-date');
const detailsDialog = document.querySelector('#details-dialog');
const detailsContent = document.querySelector('#details-content');
const detailsClose = document.querySelector('#details-close');

refreshButton.disabled = true;

let reports = [];
let pulls = new Map();
let renderedItems = [];
let lastSyncedAt = null;
let filters = { query: '', prState: 'all', reviewState: 'all' };
let dateSort = 'desc';
let reportsReady = false;
let blogStats = null;

function isValidReport(report) {
  return report
    && typeof report === 'object'
    && Number.isInteger(report.prNumber)
    && report.prNumber > 0
    && report.source
    && typeof report.source === 'object'
    && typeof report.source.title === 'string'
    && typeof report.source.slug === 'string'
    && report.translation
    && report.translation.target_repo === REPOSITORY;
}

function setApiStatus(message, tone = 'ok') {
  apiStatusText.textContent = message;
  apiStatus.dataset.tone = tone;
}

function formatTime(value) {
  return new Date(value).toLocaleString('ko-KR');
}

function formatRelativeTime(value) {
  const elapsed = Date.now() - new Date(value).getTime();
  if (!Number.isFinite(elapsed) || elapsed < 0) {
    return formatTime(value);
  }
  const minutes = Math.floor(elapsed / 60_000);
  if (minutes < 1) {
    return '방금 전';
  }
  if (minutes < 60) {
    return `${minutes}분 전`;
  }
  const hours = Math.floor(minutes / 60);
  return hours < 24 ? `${hours}시간 전` : formatTime(value);
}

function renderSyncedAt() {
  if (!lastSyncedAt) {
    return;
  }
  syncedAt.textContent = `동기화 ${formatRelativeTime(lastSyncedAt)}`;
  syncedAt.title = formatTime(lastSyncedAt);
}

function setSyncedAt(value) {
  lastSyncedAt = value;
  if (!value) {
    syncedAt.textContent = '동기화: 아직 없음';
    syncedAt.removeAttribute('title');
    return;
  }
  renderSyncedAt();
}

function activeSummaryFilter({ prState, reviewState: review }) {
  if (prState === 'all' && review === 'all') {
    return 'all';
  }
  if (review === 'all') {
    return prState;
  }
  return prState === 'all' && review === 'needs-review' ? 'needs-review' : 'none';
}

function progressModel(items) {
  if (!blogStats?.posts || !blogStats?.baselineAt) {
    return null;
  }
  const baselineDate = String(blogStats.baselineAt).slice(0, 10);
  const eligible = eligibleBlogPosts(blogStats.posts, { baselineDate });
  return { ...computeProgress(eligible, items), baselineDate };
}

function render() {
  const items = joinReports(reports, pulls);
  renderedItems = sortByPublishedDate(filterReports(items, filters), dateSort);
  summary.innerHTML = renderSummary(summarizeReports(items), activeSummaryFilter(filters));
  progress.innerHTML = renderProgress(progressModel(items));
  checkStats.innerHTML = renderCheckStats(summarizeChecks(items));
  reportRows.innerHTML = renderRows(renderedItems);
}

async function refreshBlogStats() {
  const cached = readCachedBlogStats({ key: BLOG_CACHE_KEY, repository: REPOSITORY });
  if (cached) {
    blogStats = cached;
    if (!cached.stale) {
      return;
    }
  }
  try {
    const [posts, baselineAt] = await Promise.all([
      fetchBlogIndex(),
      blogStats?.baselineAt ?? fetchFirstBlogAgentPullCreatedAt({ repository: REPOSITORY }),
    ]);
    blogStats = { posts, baselineAt };
    writeCachedBlogStats({
      key: BLOG_CACHE_KEY,
      repository: REPOSITORY,
      fetchedAt: new Date().toISOString(),
      baselineAt,
      posts,
    });
  } catch {
    // 블로그 목록 갱신 실패 시 이전(캐시) 진행률을 유지한다.
  }
}

function renderFatalLoadError() {
  reportsReady = false;
  reports = [];
  pulls = new Map();
  lastSyncedAt = null;
  render();
  setApiStatus('보고서 로드 오류: 데이터 파일을 확인하세요.', 'error');
  syncedAt.textContent = '동기화: 불가';
  refreshButton.disabled = true;
}

async function loadReports() {
  const response = await fetch('./data/reports.json');
  if (!response.ok) {
    throw new Error(`report snapshot request failed with status ${response.status}`);
  }
  const snapshot = await response.json();
  if (!snapshot || !Array.isArray(snapshot.reports) || !snapshot.reports.every(isValidReport)) {
    throw new TypeError('report snapshot is invalid');
  }
  return snapshot.reports;
}

function statusWithRateLimit(prefix, rateLimit) {
  return rateLimit?.remaining === null || rateLimit?.remaining === undefined
    ? prefix
    : `${prefix} · 남은 요청 ${rateLimit.remaining}회`;
}

const refresh = createSingleFlight(async () => {
  if (!reportsReady) {
    return;
  }
  refreshButton.disabled = true;
  setApiStatus('GitHub 상태를 확인하는 중입니다.', 'busy');
  await refreshBlogStats();

  try {
    const snapshot = await fetchPullStatuses({
      repository: REPOSITORY,
      numbers: reports.map((report) => report.prNumber),
    });
    pulls = snapshot.pulls;
    setSyncedAt(snapshot.syncedAt);
    writeCachedSnapshot({
      key: CACHE_KEY,
      repository: REPOSITORY,
      syncedAt: snapshot.syncedAt,
      rateLimit: snapshot.rateLimit,
      pulls: snapshot.pulls,
    });
    setApiStatus(statusWithRateLimit('GitHub 상태가 동기화되었습니다', snapshot.rateLimit));
    render();
  } catch (error) {
    const preservedTime = lastSyncedAt ? ` 마지막 동기화: ${formatTime(lastSyncedAt)}.` : '';
    setApiStatus(`GitHub 상태를 갱신하지 못했습니다. 표시 중인 데이터를 유지합니다.${preservedTime}`, 'error');
    render();
  } finally {
    refreshButton.disabled = false;
  }
});

function openDetails(prNumber) {
  const item = renderedItems.find((candidate) => candidate.prNumber === prNumber);
  if (!item) {
    return;
  }
  detailsContent.innerHTML = renderDetails(item);
  detailsDialog.showModal();
}

function syncFilterControls() {
  for (const control of prStateControls.querySelectorAll('button[data-pr-state]')) {
    control.setAttribute('aria-pressed', String(control.dataset.prState === filters.prState));
  }
  reviewState.value = filters.reviewState;
}

function applyPrState(button) {
  filters = { ...filters, prState: button.dataset.prState };
  syncFilterControls();
  render();
}

function resetFilters() {
  filters = { query: '', prState: 'all', reviewState: 'all' };
  searchInput.value = '';
  syncFilterControls();
  render();
}

function applySummaryFilter(value) {
  const next = activeSummaryFilter(filters) === value ? 'all' : value;
  if (next === 'needs-review') {
    filters = { ...filters, prState: 'all', reviewState: 'needs-review' };
  } else {
    filters = { ...filters, prState: next === 'all' ? 'all' : next, reviewState: 'all' };
  }
  syncFilterControls();
  render();
}

function registerControls() {
  refreshButton.addEventListener('click', () => { void refresh(); });
  searchInput.addEventListener('input', () => {
    filters = { ...filters, query: searchInput.value };
    render();
  });
  prStateControls.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-pr-state]');
    if (button && prStateControls.contains(button)) {
      applyPrState(button);
    }
  });
  summary.addEventListener('click', (event) => {
    const tile = event.target.closest('button[data-summary-filter]');
    if (tile && summary.contains(tile)) {
      applySummaryFilter(tile.dataset.summaryFilter);
    }
  });
  reviewState.addEventListener('change', () => {
    filters = { ...filters, reviewState: reviewState.value };
    render();
  });
  sortDateButton.addEventListener('click', () => {
    dateSort = dateSort === 'desc' ? 'asc' : 'desc';
    sortDateButton.dataset.dir = dateSort;
    render();
  });
  reportRows.addEventListener('click', (event) => {
    if (event.target.closest('button[data-action="reset-filters"]')) {
      resetFilters();
      return;
    }
    const row = event.target.closest('tr[data-pr-number]');
    if (row && reportRows.contains(row)) {
      openDetails(Number(row.dataset.prNumber));
    }
  });
  reportRows.addEventListener('keydown', (event) => {
    if (event.key !== 'Enter' && event.key !== ' ') {
      return;
    }
    const row = event.target.closest('tr[data-pr-number]');
    if (row && reportRows.contains(row)) {
      event.preventDefault();
      openDetails(Number(row.dataset.prNumber));
    }
  });
  detailsClose.addEventListener('click', () => { detailsDialog.close(); });
  detailsDialog.addEventListener('click', (event) => {
    if (event.target === detailsDialog) {
      detailsDialog.close();
    }
  });
  detailsDialog.addEventListener('cancel', () => {});
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
      void refresh();
    }
  });
  window.addEventListener('online', () => { void refresh(); });
  window.setInterval(() => {
    if (document.visibilityState !== 'visible') {
      return;
    }
    void refresh();
  }, 300_000);
  window.setInterval(renderSyncedAt, 60_000);
}

async function start() {
  try {
    reports = await loadReports();
    const cached = readCachedSnapshot({ key: CACHE_KEY, repository: REPOSITORY });
    if (cached) {
      pulls = cached.pulls;
      setSyncedAt(cached.syncedAt);
      setApiStatus(cached.stale ? '캐시 상태를 표시합니다. 최신 상태를 확인하는 중입니다.' : '캐시 상태를 표시합니다.');
    } else {
      setApiStatus('GitHub 상태를 확인하는 중입니다.');
    }
    render();
    reportsReady = true;
    void refresh();
  } catch (error) {
    renderFatalLoadError(error);
  }
}

registerControls();
void start();
