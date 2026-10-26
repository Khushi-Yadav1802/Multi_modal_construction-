/* ═══════════════════════════════════════════════════════════════════════════
   app.js — Multimodal Construction Intelligence Platform
   Handles all tab logic, API calls, UI rendering
   ═══════════════════════════════════════════════════════════════════════════ */

const API = 'http://localhost:8000';

/* ════════════════════════════════════════════════ STATE ══ */
const state = {
  apiKey: '',
  chatHistory: [],
  currentWeather: 'Normal Conditions',
  planningResult: null,
};

/* ════════════════════════════════════════════════ INIT ═══ */
document.addEventListener('DOMContentLoaded', () => {
  setupSidebar();
  setupTabs();
  setupSafetyTab();
  setupCrackTab();
  setupPlanningTab();
  setupAssistantTab();
  loadWeatherAdvisory('Normal Conditions');
});

/* ════════════════════════════════════════════════ SIDEBAR ══ */
function setupSidebar() {
  const input = document.getElementById('apiKeyInput');
  const status = document.getElementById('apiStatus');
  const badge  = document.getElementById('modeBadge');
  const menuBtn = document.getElementById('menuBtn');
  const sidebar = document.getElementById('sidebar');
  const main = document.querySelector('.main-content');

  input.addEventListener('input', () => {
    state.apiKey = input.value.trim();
    if (state.apiKey) {
      status.textContent = '✓ Live AI Mode';
      status.className = 'api-status live';
      badge.textContent = '✓ Live AI Mode';
      badge.className = 'header-badge live';
    } else {
      status.textContent = '⚡ Demo Mode';
      status.className = 'api-status demo';
      badge.textContent = '⚡ Demo Mode';
      badge.className = 'header-badge';
    }
  });

  menuBtn.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
    main.classList.toggle('full');
  });

  // Sidebar nav buttons mirror tab buttons
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      switchTab(btn.dataset.tab);
      document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });
}

/* ════════════════════════════════════════════════ TABS ═══ */
function setupTabs() {
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => switchTab(btn.dataset.tab));
  });
}

function switchTab(tabId) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.toggle('active', b.dataset.tab === tabId));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.toggle('active', b.dataset.tab === tabId));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.toggle('active', p.id === `tab-${tabId}`));
}

/* ════════════════════════════════════════════════ HELPERS ══ */
function headers() {
  const h = { 'X-API-Key': state.apiKey };
  return h;
}

function showLoading(id) { document.getElementById(id).classList.remove('hidden'); }
function hideLoading(id) { document.getElementById(id).classList.add('hidden'); }
function showEl(id)  { document.getElementById(id).classList.remove('hidden'); }
function hideEl(id)  { document.getElementById(id).classList.add('hidden'); }

function setupDropzone(zoneId, fileInputId, previewId, onFile) {
  const zone  = document.getElementById(zoneId);
  const input = document.getElementById(fileInputId);

  zone.addEventListener('click', () => input.click());
  zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('dragover'); });
  zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
  zone.addEventListener('drop', e => {
    e.preventDefault();
    zone.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file, previewId, zone, onFile);
  });
  input.addEventListener('change', () => {
    if (input.files[0]) handleFile(input.files[0], previewId, zone, onFile);
  });
}

function handleFile(file, previewId, zone, onFile) {
  const reader = new FileReader();
  reader.onload = e => {
    const preview = document.getElementById(previewId);
    preview.innerHTML = `<img src="${e.target.result}" alt="Preview" />`;
    preview.classList.remove('hidden');
    zone.style.display = 'none';
  };
  reader.readAsDataURL(file);
  onFile(file);
}

function downloadJSON(data, filename) {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  a.click();
}

function severityColor(sev) {
  return { Critical: '#dc2626', High: '#ef4444', Medium: '#f59e0b', Low: '#3b82f6' }[sev] || '#3b82f6';
}
function severityPill(sev) {
  const cls = { Critical: 'pill-critical', High: 'pill-danger', Medium: 'pill-warning', Low: 'pill-info' }[sev] || 'pill-info';
  return `<span class="pill ${cls}">${sev}</span>`;
}
function scorePillClass(score) {
  if (score >= 80) return 'pill-safe';
  if (score >= 60) return 'pill-warning';
  if (score >= 40) return 'pill-danger';
  return 'pill-critical';
}
function scoreColor(score) {
  if (score >= 80) return '#34d399';
  if (score >= 60) return '#fbbf24';
  if (score >= 40) return '#f87171';
  return '#dc2626';
}

/* ════════════════════════════════════════════════ TAB 1: SAFETY ══ */
let safetyFile = null;
let safetyResult = null;

function setupSafetyTab() {
  setupDropzone('safetyUploadZone', 'safetyFile', 'safetyPreview', f => { safetyFile = f; });
  document.getElementById('runSafetyBtn').addEventListener('click', runSafetyAudit);
}

async function runSafetyAudit() {
  const btn = document.getElementById('runSafetyBtn');
  btn.disabled = true;
  showLoading('safetyLoading');
  hideEl('safetyResults');

  try {
    const formData = new FormData();
    if (safetyFile) formData.append('file', safetyFile);

    const res = await fetch(`${API}/api/safety-audit`, {
      method: 'POST',
      headers: headers(),
      body: formData,
    });
    safetyResult = await res.json();
    renderSafetyResults(safetyResult);
  } catch (err) {
    alert('API error: ' + err.message + '\n\nMake sure the backend server is running.');
  } finally {
    hideLoading('safetyLoading');
    btn.disabled = false;
  }
}

function renderSafetyResults(r) {
  const sc = r.safety_score ?? 0;
  const st = r.overall_status ?? 'UNKNOWN';
  const ppe = r.ppe_detection ?? {};
  const hazards = r.site_hazards ?? [];
  const detectedCount = Object.values(ppe).filter(v => v.detected).length;
  const highCount = hazards.filter(h => ['Critical','High'].includes(h.severity)).length;

  const ppeLabels = {
    hard_hat: '🪖 Hard Hat', high_vis_vest: '🦺 High-Vis Vest',
    steel_toe_boots: '👢 Steel-Toe Boots', safety_harness: '🔗 Safety Harness',
    safety_gloves: '🧤 Safety Gloves', eye_protection: '🥽 Eye Protection',
  };

  const ppeHTML = Object.entries(ppeLabels).map(([key, label]) => {
    const item = ppe[key] || { detected: false, compliance: 'Unknown' };
    return `
      <div class="ppe-item">
        <span class="ppe-name">${label}</span>
        <div class="ppe-right">
          <div class="${item.detected ? 'ppe-status-ok' : 'ppe-status-bad'}">
            ${item.detected ? '✓ Detected' : '✗ Missing'}
          </div>
          <div class="ppe-compliance">${item.compliance || ''}</div>
        </div>
      </div>`;
  }).join('');

  const hazardsHTML = hazards.map(h => {
    const col = severityColor(h.severity);
    return `
      <div class="hazard-card" style="border-left-color:${col};">
        <div class="hazard-title">
          ${h.hazard}
          ${severityPill(h.severity)}
        </div>
        <div class="hazard-remedy">🔧 ${h.remedy}</div>
      </div>`;
  }).join('');

  const stdsHTML = (r.standards_referenced || []).map(s =>
    `<span class="pill pill-info">📘 ${s}</span>`
  ).join('');

  const el = document.getElementById('safetyResults');
  el.innerHTML = `
    <!-- Metrics -->
    <div class="metric-grid">
      <div class="metric-card">
        <div class="metric-label">Safety Score</div>
        <div class="metric-value" style="color:${scoreColor(sc)}">${sc}</div>
        <div class="metric-delta">out of 100</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">PPE Detected</div>
        <div class="metric-value">${detectedCount}/${Object.keys(ppe).length}</div>
        <div class="metric-delta">items compliant</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">High+ Hazards</div>
        <div class="metric-value" style="color:#f87171">${highCount}</div>
        <div class="metric-delta">requiring action</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Overall Status</div>
        <div style="margin-top:0.6rem">
          <span class="pill ${scorePillClass(sc)}">${st}</span>
        </div>
      </div>
    </div>

    <!-- PPE + Hazards -->
    <div class="result-panels">
      <div class="result-panel">
        <div class="panel-title">🦺 PPE Compliance Checklist</div>
        ${ppeHTML}
      </div>
      <div class="result-panel">
        <div class="panel-title">⚠️ Identified Site Hazards</div>
        ${hazardsHTML || '<p style="color:var(--text-dim);font-size:0.85rem;">No hazards detected.</p>'}
      </div>
    </div>

    <!-- Standards -->
    <div class="section-header"><div class="section-title">📋 Standards & Recommendations</div></div>
    <div class="standards-row">${stdsHTML}</div>
    <div class="info-box">💡 <strong>Recommendation:</strong> ${r.recommendations || 'N/A'}</div>

    <!-- Download -->
    <button class="btn-download" id="dlSafetyBtn">⬇️ Download JSON Report</button>
  `;

  document.getElementById('dlSafetyBtn').addEventListener('click', () => {
    downloadJSON(r, `ppe_audit_${Date.now()}.json`);
  });

  el.classList.remove('hidden');
}

/* ════════════════════════════════════════════════ TAB 2: CRACK ══ */
let crackFile = null;
let crackResult = null;

function setupCrackTab() {
  setupDropzone('crackUploadZone', 'crackFile', 'crackPreview', f => { crackFile = f; });
  document.getElementById('runCrackBtn').addEventListener('click', runCrackAnalysis);
}

async function runCrackAnalysis() {
  const btn = document.getElementById('runCrackBtn');
  btn.disabled = true;
  showLoading('crackLoading');
  hideEl('crackResults');

  try {
    const formData = new FormData();
    if (crackFile) formData.append('file', crackFile);

    const res = await fetch(`${API}/api/crack-analysis`, {
      method: 'POST',
      headers: headers(),
      body: formData,
    });
    crackResult = await res.json();
    renderCrackResults(crackResult);
  } catch (err) {
    alert('API error: ' + err.message + '\n\nMake sure the backend server is running.');
  } finally {
    hideLoading('crackLoading');
    btn.disabled = false;
  }
}

function renderCrackResults(r) {
  const sev = r.severity || 'Medium';
  const sevColor = severityColor(sev);

  const causesHTML = (r.root_causes || []).map(c => `
    <div class="hazard-card" style="border-left-color:#f59e0b;">
      <div class="hazard-remedy">🔎 ${c}</div>
    </div>`).join('');

  const repairsHTML = (r.recommended_repairs || []).map((rp, i) => `
    <div class="hazard-card" style="border-left-color:#3b82f6;">
      <div class="hazard-title">#${i+1} ${rp.method}</div>
      <div class="hazard-remedy">${rp.detail}</div>
    </div>`).join('');

  const stdsHTML = (r.standards || []).map(s => `<span class="pill pill-info">📘 ${s}</span>`).join('');

  const el = document.getElementById('crackResults');
  el.innerHTML = `
    <div class="metric-grid">
      <div class="metric-card">
        <div class="metric-label">Defect Type</div>
        <div class="metric-sub">${r.defect_type || 'Unknown'}</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Crack Width</div>
        <div class="metric-value" style="color:${sevColor}">${r.crack_width_mm ?? '—'}</div>
        <div class="metric-delta">millimetres</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Severity</div>
        <div style="margin-top:0.6rem">${severityPill(sev)}</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Urgency</div>
        <div class="metric-sub" style="color:#fbbf24">${r.urgency || 'Assessment Required'}</div>
      </div>
    </div>

    <div class="result-panels">
      <div class="result-panel">
        <div class="panel-title">🔍 Pattern & Root Causes</div>
        <div class="info-box" style="margin-bottom:1rem">
          <strong>Pattern:</strong> ${r.pattern || 'N/A'}<br>
          <strong>Est. Length:</strong> ${r.crack_length_estimate || 'N/A'}
        </div>
        ${causesHTML}
        <div style="margin-top:1rem" class="standards-row">${stdsHTML}</div>
      </div>
      <div class="result-panel">
        <div class="panel-title">🔧 Recommended Engineering Repairs</div>
        ${repairsHTML}
        ${r.monitoring ? `
          <div class="info-box" style="margin-top:0.8rem; background:rgba(59,130,246,0.07); color:#bfdbfe; border-color:rgba(59,130,246,0.3)">
            📏 <strong>Monitoring:</strong> ${r.monitoring}
          </div>` : ''}
      </div>
    </div>

    <button class="btn-download" id="dlCrackBtn">⬇️ Download Crack Report</button>
  `;

  document.getElementById('dlCrackBtn').addEventListener('click', () => {
    downloadJSON(r, `crack_report_${Date.now()}.json`);
  });

  el.classList.remove('hidden');
}

/* ════════════════════════════════════════════════ TAB 3: PLANNING ══ */
function setupPlanningTab() {
  const slider = document.getElementById('completion');
  const val    = document.getElementById('completionVal');
  slider.addEventListener('input', () => { val.textContent = slider.value; });

  document.getElementById('calcBtn').addEventListener('click', runPlanning);
  document.getElementById('genRenderBtn').addEventListener('click', generateRender);
}

async function runPlanning() {
  const btn = document.getElementById('calcBtn');
  btn.disabled = true;
  btn.textContent = '⏳ Calculating...';

  const body = {
    structure_type: document.getElementById('structType').value,
    sqft: parseFloat(document.getElementById('sqft').value),
    location: document.getElementById('location').value,
    completion: parseInt(document.getElementById('completion').value),
    project_name: document.getElementById('projName').value,
  };

  try {
    const res = await fetch(`${API}/api/planning`, {
      method: 'POST',
      headers: { ...headers(), 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const r = await res.json();
    state.planningResult = r;
    renderPlanningResults(r);
  } catch (err) {
    alert('API error: ' + err.message);
  } finally {
    btn.disabled = false;
    btn.textContent = '📊 Calculate & Analyse';
  }
}

function renderPlanningResults(r) {
  const milestonesHTML = (r.milestones || []).map(m => `
    <div class="milestone-item">
      <div class="milestone-header">
        <span>${m.complete ? '✅' : (r.completion > (m.threshold - 20) ? '🔄' : '⏳')} ${m.name}</span>
        <span class="milestone-pct ${m.complete ? 'done' : ''}">${Math.min(100, m.progress)}%</span>
      </div>
      <div class="progress-track">
        <div class="progress-fill-bar" style="width:${Math.min(100, m.progress)}%"></div>
      </div>
    </div>`).join('');

  document.getElementById('planningResults').innerHTML = `
    <div class="card">
      <div class="card-title">📊 Financial Metrics — ${r.project_name}</div>
      <div class="metric-grid" style="grid-template-columns:repeat(3,1fr); margin-bottom:1rem">
        <div class="metric-card">
          <div class="metric-label">Total Budget</div>
          <div class="metric-value" style="font-size:1.4rem">${r.total_budget}</div>
          <div class="metric-delta">@ ₹${Number(r.cost_per_sqft).toLocaleString()}/sqft</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">CapEx Incurred</div>
          <div class="metric-value" style="font-size:1.4rem;color:#fbbf24">${r.capex_incurred}</div>
          <div class="metric-delta">${r.completion}% complete</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">Market Asset Value</div>
          <div class="metric-value" style="font-size:1.4rem;color:#34d399">${r.market_value}</div>
          <div class="metric-delta">Current market rate</div>
        </div>
      </div>
      <div class="metric-grid" style="grid-template-columns:1fr 1fr; margin-bottom:1.2rem">
        <div class="metric-card">
          <div class="metric-label">Steel Required</div>
          <div class="metric-value" style="font-size:1.5rem">${Number(r.steel_kg).toLocaleString()}</div>
          <div class="metric-delta">kg &nbsp;(${r.steel_mt} MT)</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">Cement Required</div>
          <div class="metric-value" style="font-size:1.5rem">${Number(r.cement_bags).toLocaleString()}</div>
          <div class="metric-delta">bags of 50 kg</div>
        </div>
      </div>

      <div class="section-title" style="margin-bottom:0.8rem">🏗️ Milestone Progress</div>
      <div class="milestone-list">${milestonesHTML}</div>
    </div>
  `;
}

async function generateRender() {
  const btn = document.getElementById('genRenderBtn');
  const status = document.getElementById('renderStatus');
  const output = document.getElementById('renderOutput');

  btn.disabled = true;
  btn.textContent = '⏳ Generating...';
  status.textContent = 'Calling Pollinations AI... (~10–20s)';
  status.classList.remove('hidden');

  const structType = document.getElementById('structType').value;
  const location   = document.getElementById('location').value.split('(')[0].trim();
  const style      = document.getElementById('renderStyle').value;
  const projName   = document.getElementById('projName').value;

  const prompt = encodeURIComponent(
    `Photorealistic ${style} architectural concept render of a ${structType}, ` +
    `located in ${location} India. Modern contemporary design with glass facade, ` +
    `landscaping, steel structure, golden hour lighting, ultra-detailed 3D CGI, ` +
    `8K quality, professional architectural visualization, dramatic sky, premium real estate`
  );

  const imgUrl = `https://image.pollinations.ai/prompt/${prompt}?width=1024&height=576&seed=42&nologo=true`;

  try {
    const img = new Image();
    img.onload = () => {
      output.innerHTML = `
        <div class="render-card">
          <img src="${imgUrl}" alt="3D Render" style="width:100%;border-radius:var(--radius);border:1px solid var(--border);" />
          <div class="render-caption">🏗️ ${projName} — ${style} | Pollinations AI</div>
        </div>
        <a href="${imgUrl}" download="render_${Date.now()}.jpg" class="btn-download" style="margin-top:0.7rem;display:inline-flex">
          ⬇️ Download Render
        </a>
      `;
      status.classList.add('hidden');
      btn.disabled = false;
      btn.textContent = '🎨 Generate 3D Render';
    };
    img.onerror = () => {
      status.textContent = '❌ Render failed — try again';
      btn.disabled = false;
      btn.textContent = '🎨 Generate 3D Render';
    };
    img.src = imgUrl;
  } catch (e) {
    status.textContent = '❌ Error: ' + e.message;
    btn.disabled = false;
    btn.textContent = '🎨 Generate 3D Render';
  }
}

/* ════════════════════════════════════════════════ TAB 4: ASSISTANT ══ */
function setupAssistantTab() {
  // Weather buttons
  document.querySelectorAll('.weather-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.weather-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      loadWeatherAdvisory(btn.dataset.weather);
    });
  });

  // Quick prompts
  document.querySelectorAll('.quick-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.getElementById('chatInput').value = btn.dataset.q;
      sendChat();
    });
  });

  // Send button & Enter key
  document.getElementById('sendBtn').addEventListener('click', sendChat);
  document.getElementById('chatInput').addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendChat(); }
  });

  // Clear chat
  document.getElementById('clearChatBtn').addEventListener('click', () => {
    state.chatHistory = [];
    const msgs = document.getElementById('chatMessages');
    msgs.innerHTML = `
      <div class="chat-msg assistant">
        <div class="msg-bubble">
          👋 Conversation cleared. How can I help you today?
        </div>
      </div>`;
  });
}

async function loadWeatherAdvisory(condition) {
  state.currentWeather = condition;
  const el = document.getElementById('weatherAdvisory');
  el.innerHTML = '<div style="color:var(--text-dim);font-size:0.82rem;">Loading...</div>';

  try {
    const key = condition.replace(/\s*\(.*?\)\s*/g, '').trim().replace(/\s+/g,'_');
    const res = await fetch(`${API}/api/weather/${encodeURIComponent(key)}`, { headers: headers() });
    const data = await res.json();
    renderWeatherAdvisory(data);
  } catch {
    renderWeatherAdvisory(getFallbackWeather(condition));
  }
}

function renderWeatherAdvisory(data) {
  const el = document.getElementById('weatherAdvisory');
  const levelClass = { warning: 'warning', danger: 'danger', info: 'info', success: '' }[data.level] || '';
  el.className = `weather-advisory ${levelClass}`;
  el.innerHTML = `
    <div class="advisory-title">${data.icon} ${data.title}</div>
    ${(data.alerts || []).map(a => `<div class="advisory-alert">• ${a}</div>`).join('')}
  `;
}

function getFallbackWeather(condition) {
  const map = {
    'Normal Conditions':       { icon:'☀️', level:'success', title:'Standard Operations — All Clear', alerts:['Normal site operations. Run pre-shift toolbox talk.','Verify daily PPE compliance checklist.','Good concrete curing conditions — maintain moist curing 7 days.'] },
    'High Wind (>50 km/h)':   { icon:'💨', level:'warning', title:'High Wind — Elevated Risk', alerts:['Suspend crane and hoist operations above 50 km/h.','Secure loose materials and scaffolding boards.','Re-permit crane ops only after 30 min sustained calm.'] },
    'Heavy Rain / Flooding':  { icon:'🌧️', level:'info',    title:'Heavy Rain Advisory', alerts:['De-energise temporary power boards immediately.','Halt all excavation — slope stability at risk.','Suspend concrete pours if rain rate >10 mm/hr.'] },
    'Extreme Heat (>42°C)':   { icon:'🌡️', level:'danger',  title:'Extreme Heat Stress Advisory', alerts:['1 litre cool water per worker per hour — mandatory.','Reschedule heavy work before 10 AM / after 4 PM.','Halt if WBGT exceeds 35°C (ACGIH TLV).'] },
  };
  return map[condition] || map['Normal Conditions'];
}

function appendChatMsg(role, text) {
  const msgs = document.getElementById('chatMessages');
  const div  = document.createElement('div');
  div.className = `chat-msg ${role}`;
  div.innerHTML = `<div class="msg-bubble">${formatMD(text)}</div>`;
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

function formatMD(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code style="font-family:monospace;background:rgba(255,255,255,0.08);padding:1px 5px;border-radius:3px">$1</code>')
    .replace(/\n- /g, '<br>• ')
    .replace(/\n/g, '<br>');
}

async function sendChat() {
  const input = document.getElementById('chatInput');
  const msg   = input.value.trim();
  if (!msg) return;

  input.value = '';
  appendChatMsg('user', msg);
  state.chatHistory.push({ role: 'user', content: msg });

  showEl('chatLoading');
  document.getElementById('sendBtn').disabled = true;

  try {
    const res = await fetch(`${API}/api/chat`, {
      method: 'POST',
      headers: { ...headers(), 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg, history: state.chatHistory.slice(-8) }),
    });
    const data = await res.json();
    const reply = data.reply || 'Sorry, no response.';
    appendChatMsg('assistant', reply);
    state.chatHistory.push({ role: 'assistant', content: reply });
  } catch (err) {
    appendChatMsg('assistant', '❌ Could not reach the server. Make sure the backend is running at localhost:8000.');
  } finally {
    hideEl('chatLoading');
    document.getElementById('sendBtn').disabled = false;
  }
}
