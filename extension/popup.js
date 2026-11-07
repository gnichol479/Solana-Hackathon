const DEFAULT_API = 'http://localhost:8000';
const DEFAULT_SITE = 'http://localhost:5173';
const $ = (id) => document.getElementById(id);
const input = $('request-text');
const analyzeButton = $('analyze-button');
const riskLabels = {
  suspicious: 'Suspicious',
  needs_verification: 'Needs verification',
  no_major_warnings_detected: 'No major warnings detected'
};

function normalizeOrigin(value, label) {
  let url;
  try { url = new URL(value.trim()); } catch { throw new Error(`Enter a valid ${label} URL, including http:// or https://.`); }
  if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password) {
    throw new Error(`${label} must be an HTTP or HTTPS URL without credentials.`);
  }
  return url.origin;
}

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
}

function showError(message) {
  const box = $('error-message');
  box.textContent = message;
  box.hidden = false;
}

function clearError() {
  $('error-message').hidden = true;
  $('error-message').textContent = '';
}

function setBusy(busy) {
  analyzeButton.disabled = busy;
  $('selection-button').disabled = busy;
  $('analyze-label').textContent = busy ? 'Checking request…' : 'Analyze request';
  $('analyze-arrow').hidden = busy;
  $('spinner').hidden = !busy;
}

function displayReport(data, siteUrl) {
  const level = riskLabels[data?.risk_level] ? data.risk_level : 'needs_verification';
  const label = riskLabels[level];
  const indicators = Array.isArray(data?.indicators) ? data.indicators : [];
  const details = data?.payment_details && typeof data.payment_details === 'object' ? data.payment_details : {};
  const solana = data?.solana_analysis && typeof data.solana_analysis === 'object' ? data.solana_analysis : {};
  const hasSolana = data?.payment_type === 'solana' || solana.performed;
  const amount = [details.amount, details.currency].filter(value => value !== null && value !== undefined && value !== '').join(' ') || 'Not established';
  const recipient = details.recipient || solana.wallet_address || 'Not verified';
  const report = $('report');
  report.innerHTML = `
    <div class="report-heading"><span class="risk-icon ${escapeHtml(level.replaceAll('_','-'))}">${level === 'suspicious' ? '<svg viewBox="0 0 20 20" fill="none"><path d="M10 6v4m0 3h.01M8.3 3.2 1.6 15.1a1.4 1.4 0 0 0 1.2 2.1h14.4a1.4 1.4 0 0 0 1.2-2.1L11.7 3.2a2 2 0 0 0-3.4 0Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>' : '<svg viewBox="0 0 20 20" fill="none"><path d="M10 2.5 17 5.4v5.1c0 4.1-2.9 6.8-7 8.5-4.1-1.7-7-4.4-7-8.5V5.4l7-2.9Z" stroke="currentColor" stroke-width="1.4"/><path d="m6.8 10.2 2.1 2.1 4.5-4.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'}</span><div><small>OVERALL ASSESSMENT</small><h2>${escapeHtml(label)}</h2></div></div>
    <p class="report-summary">${escapeHtml(data?.summary || 'The service returned a result without a summary.')}</p>
    ${indicators.length ? `<h3 class="findings-title">WHAT DESERVES YOUR ATTENTION</h3>${indicators.slice(0,6).map(item => `<div class="finding"><i class="finding-dot"></i><div><p>${escapeHtml(item.message || item.explanation || item.category || 'Review this signal.')}</p>${item.evidence ? `<p class="evidence">Evidence: ${escapeHtml(item.evidence)}</p>` : ''}</div></div>`).join('')}` : '<p class="uncertainty">No supporting indicators were returned. A low warning level does not prove a payment is safe.</p>'}
    <div class="report-details"><div class="detail"><span>Payment type</span><span>${escapeHtml(data?.payment_type === 'solana' ? 'Solana' : data?.payment_type === 'traditional' ? 'Traditional' : 'Not identified')}</span></div><div class="detail"><span>Amount</span><span>${escapeHtml(amount)}</span></div><div class="detail"><span>Recipient</span><span>${escapeHtml(recipient)}</span></div></div>
    ${hasSolana ? `<p class="solana-note">Solana checks ${solana.performed ? 'used available public blockchain data' : 'were not performed or returned no live evidence'}. Public wallet activity cannot verify a real-world identity.</p>` : ''}
    <p class="uncertainty">Use this as decision support. Confirm payment instructions through a trusted contact you already know.</p>
    <div class="report-links"><a href="${escapeHtml(siteUrl)}" target="_blank" rel="noopener noreferrer">Open Payment Lens website ↗</a><button type="button" id="clear-report">New check</button></div>`;
  report.hidden = false;
  $('clear-report').addEventListener('click', () => { report.hidden = true; input.focus(); });
  report.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
}

async function loadSettings() {
  const { apiUrl = '', siteUrl = '' } = await chrome.storage.local.get(['apiUrl', 'siteUrl']);
  $('api-url').value = apiUrl;
  $('site-url').value = siteUrl;
  $('connection-label').textContent = apiUrl ? `Connected · ${new URL(apiUrl).host}` : 'Backend not configured';
}

$('settings-toggle').addEventListener('click', () => {
  const panel = $('settings');
  panel.hidden = !panel.hidden;
  $('settings-toggle').setAttribute('aria-expanded', String(!panel.hidden));
});
$('settings-close').addEventListener('click', () => {
  $('settings').hidden = true;
  $('settings-toggle').setAttribute('aria-expanded', 'false');
});
$('settings-save').addEventListener('click', async () => {
  clearError();
  try {
    const apiUrl = normalizeOrigin($('api-url').value, 'backend');
    const siteUrl = normalizeOrigin($('site-url').value || DEFAULT_SITE, 'website');
    // Request directly in the click handler so Chrome retains the user gesture.
    const granted = await chrome.permissions.request({ origins: [`${apiUrl}/*`] });
    if (!granted) throw new Error('Permission was not granted. The extension needs access to this backend to submit a request.');
    await chrome.storage.local.set({ apiUrl, siteUrl });
    $('connection-label').textContent = `Connected · ${new URL(apiUrl).host}`;
    $('settings').hidden = true;
    $('settings-toggle').setAttribute('aria-expanded', 'false');
  } catch (error) { showError(error.message); }
});

$('selection-button').addEventListener('click', async () => {
  clearError();
  try {
    const [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
    if (!tab?.id || !/^https?:/.test(tab.url || '')) throw new Error('Open a regular webpage to use selected text.');
    const [result] = await chrome.scripting.executeScript({ target: { tabId: tab.id }, func: () => window.getSelection()?.toString() || '' });
    const selected = result?.result?.trim() || '';
    if (!selected) throw new Error('Select some text on the page first, then choose Use selection.');
    input.value = selected.slice(0, 20000);
    $('char-count').textContent = `${input.value.length.toLocaleString()} / 20,000`;
    input.focus();
  } catch (error) { showError(error.message || 'This page does not allow selected text access.'); }
});

input.addEventListener('input', () => {
  $('char-count').textContent = `${input.value.length.toLocaleString()} / 20,000`;
  clearError();
});

analyzeButton.addEventListener('click', async () => {
  clearError();
  const text = input.value.trim();
  if (!text) { showError('Paste a payment request or use selected text to get started.'); input.focus(); return; }
  setBusy(true);
  try {
    const saved = await chrome.storage.local.get(['apiUrl', 'siteUrl']);
    if (!saved.apiUrl) throw new Error('Connect your team backend first. Open the settings above and enter its URL.');
    const apiUrl = normalizeOrigin(saved.apiUrl, 'backend');
    const permission = await chrome.permissions.contains({ origins: [`${apiUrl}/*`] });
    if (!permission) throw new Error('Backend access permission is missing. Open settings and save the connection again.');
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30000);
    let response;
    try {
      response = await fetch(`${apiUrl}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, source: 'extension' }),
        signal: controller.signal
      });
    } catch (error) {
      if (error.name === 'AbortError') throw new Error('The service timed out. Please try again.');
      throw new Error('Cannot reach your backend. Check that it is running and the URL is correct.');
    } finally { clearTimeout(timeout); }
    let data;
    try { data = await response.json(); } catch { throw new Error('The backend returned an unreadable response.'); }
    if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'The service could not complete this request.');
    displayReport(data, saved.siteUrl || DEFAULT_SITE);
  } catch (error) { showError(error.message || 'Something went wrong. Please try again.'); }
  finally { setBusy(false); }
});

$('brand-home').addEventListener('click', event => {
  event.preventDefault();
  chrome.storage.local.get('siteUrl').then(({ siteUrl }) => chrome.tabs.create({ url: siteUrl || DEFAULT_SITE }));
});

loadSettings().catch(() => { $('connection-label').textContent = 'Could not load settings'; });
