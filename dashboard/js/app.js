import {
  createSingleFlight,
  fetchPullStatuses,
  readCachedSnapshot,
  writeCachedSnapshot,
} from './github.js';
import { filterReports, joinReports, summarizeReports } from './model.js';
import { renderDetails, renderRows, renderSummary } from './view.js';

const REPOSITORY = 'Hugging-Face-KREW/hugging-face-krew.github.io';
const CACHE_KEY = 'hf-krew-pr-snapshot';

const apiStatus = document.querySelector('#api-status');
const syncedAt = document.querySelector('#synced-at');
const refreshButton = document.querySelector('#refresh-button');
const summary = document.querySelector('#summary');
const searchInput = document.querySelector('#search-input');
const prStateControls = document.querySelector('#pr-state-controls');
const reviewState = document.querySelector('#review-state');
const reportRows = document.querySelector('#report-rows');
const detailsDialog = document.querySelector('#details-dialog');
const detailsContent = document.querySelector('#details-content');
const detailsClose = document.querySelector('#details-close');

refreshButton.disabled = true;

let reports = [];
let pulls = new Map();
let renderedItems = [];
let lastSyncedAt = null;
let filters = { query: '', prState: 'all', reviewState: 'all' };
let reportsReady = false;

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

function setApiStatus(message) {
  apiStatus.textContent = message;
}

function formatTime(value) {
  return new Date(value).toLocaleString('ko-KR');
}

function setSyncedAt(value) {
  lastSyncedAt = value;
  syncedAt.textContent = value ? `동기화: ${formatTime(value)}` : '동기화: 아직 없음';
}

function render() {
  const items = joinReports(reports, pulls);
  renderedItems = filterReports(items, filters);
  summary.innerHTML = renderSummary(summarizeReports(items));
  reportRows.innerHTML = renderRows(renderedItems);
}

function renderFatalLoadError() {
  reportsReady = false;
  reports = [];
  pulls = new Map();
  render();
  setApiStatus('보고서 로드 오류: 데이터 파일을 확인하세요.');
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
  setApiStatus('GitHub 상태를 확인하는 중입니다.');

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
    setApiStatus(`GitHub 상태를 갱신하지 못했습니다. 표시 중인 데이터를 유지합니다.${preservedTime}`);
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

function applyPrState(button) {
  filters = { ...filters, prState: button.dataset.prState };
  for (const control of prStateControls.querySelectorAll('button[data-pr-state]')) {
    control.setAttribute('aria-pressed', String(control === button));
  }
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
  reviewState.addEventListener('change', () => {
    filters = { ...filters, reviewState: reviewState.value };
    render();
  });
  reportRows.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-action="details"]');
    if (button && reportRows.contains(button)) {
      openDetails(Number(button.dataset.prNumber));
    }
  });
  detailsClose.addEventListener('click', () => { detailsDialog.close(); });
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
