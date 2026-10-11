// SevaGuide - Interactive Client Controller

let allServices = [];
let currentChecklist = null;
let currentService = null;
let checkedDocs = new Set();

document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  loadServices();
  setupEventListeners();
});

function initTheme() {
  const savedTheme = localStorage.getItem("sevaguide_theme") || "light";
  document.documentElement.setAttribute("data-theme", savedTheme);
  updateThemeButton(savedTheme);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme") || "light";
  const target = current === "light" ? "dark" : "light";
  document.documentElement.setAttribute("data-theme", target);
  localStorage.setItem("sevaguide_theme", target);
  updateThemeButton(target);
}

function updateThemeButton(theme) {
  const btn = document.getElementById("theme-toggle-btn");
  if (btn) {
    btn.innerHTML = theme === "light" ? "🌙 Dark Mode" : "☀️ Light Mode";
  }
}

async function loadServices(category = "", search = "") {
  const grid = document.getElementById("services-grid");
  grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--text-muted);">
    <p>Loading certificate services...</p>
  </div>`;

  try {
    let url = "/api/v1/services";
    const params = new URLSearchParams();
    if (category) params.append("category", category);
    if (search) params.append("search", search);
    if (params.toString()) url += `?${params.toString()}`;

    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to load services");
    const data = await res.json();
    allServices = data;
    renderServices(data);
  } catch (err) {
    console.error(err);
    grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: #ef4444;">
      <p>Error connecting to SevaGuide API backend. Make sure the FastAPI server is running.</p>
    </div>`;
  }
}

function renderServices(services) {
  const grid = document.getElementById("services-grid");
  if (services.length === 0) {
    grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--text-muted);">
      <p>No certificate services found matching your criteria.</p>
    </div>`;
    return;
  }

  grid.innerHTML = services.map(svc => `
    <div class="service-card" data-slug="${svc.slug}">
      <div class="card-header">
        <div class="card-category">${svc.category}</div>
        <h3 class="card-title">${svc.title}</h3>
      </div>
      <p class="card-desc">${svc.short_description}</p>

      <div class="meta-info">
        <div class="meta-item">
          <span class="meta-label">Est. Time</span>
          <span class="meta-value">${svc.estimated_processing_days} Days</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Fee</span>
          <span class="meta-value">₹${svc.fee.amount}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Validity</span>
          <span class="meta-value">${svc.validity_period}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Authority</span>
          <span class="meta-value">${svc.department.split('(')[0].trim()}</span>
        </div>
      </div>

      <div class="card-actions">
        <button class="btn btn-primary" onclick="openChecklistModal('${svc.slug}')">
          <span>📋 View Checklist & Guide</span>
        </button>
      </div>
    </div>
  `).join("");
}

async function openChecklistModal(slug) {
  const modal = document.getElementById("modal-backdrop");
  modal.classList.add("active");
  document.body.style.overflow = "hidden";

  document.getElementById("modal-title").innerText = "Loading Guide...";
  document.getElementById("modal-content-area").innerHTML = "<p>Fetching document checklist and steps...</p>";

  try {
    const [svcRes, chkRes] = await Promise.all([
      fetch(`/api/v1/services/${slug}`),
      fetch(`/api/v1/services/${slug}/checklist`)
    ]);

    if (!svcRes.ok || !chkRes.ok) throw new Error("Failed to load details");
    currentService = await svcRes.json();
    currentChecklist = await chkRes.json();

    document.getElementById("modal-title").innerText = currentService.title;
    document.getElementById("modal-dept").innerText = currentService.department;

    // Reset checked docs or load from session
    checkedDocs = new Set(JSON.parse(sessionStorage.getItem(`checked_${slug}`) || "[]"));

    switchTab('documents');
  } catch (err) {
    console.error(err);
    document.getElementById("modal-content-area").innerHTML = "<p style='color:red;'>Could not load checklist data.</p>";
  }
}

function closeModal() {
  const modal = document.getElementById("modal-backdrop");
  modal.classList.remove("active");
  document.body.style.overflow = "auto";
}

function switchTab(tab) {
  document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
  const targetBtn = document.querySelector(`.tab-btn[data-tab="${tab}"]`);
  if (targetBtn) targetBtn.classList.add("active");

  const container = document.getElementById("modal-content-area");

  if (tab === "documents") {
    renderDocumentsTab(container);
  } else if (tab === "steps") {
    renderStepsTab(container);
  } else if (tab === "eligibility") {
    renderEligibilityTab(container);
  } else if (tab === "ai-eligibility") {
    renderAiEligibilityTab(container);
  } else if (tab === "faqs") {
    renderFaqsTab(container);
  }
}

function updateProgress() {
  const total = currentChecklist.documents_required.length;
  const count = checkedDocs.size;
  const pct = total > 0 ? Math.round((count / total) * 100) : 0;

  const bar = document.getElementById("progress-fill");
  const text = document.getElementById("progress-text");
  if (bar) bar.style.width = `${pct}%`;
  if (text) text.innerText = `${pct}% Prepared (${count}/${total} documents ready)`;

  // Save state
  sessionStorage.setItem(`checked_${currentService.slug}`, JSON.stringify(Array.from(checkedDocs)));
}

function toggleDoc(docName) {
  if (checkedDocs.has(docName)) {
    checkedDocs.delete(docName);
  } else {
    checkedDocs.add(docName);
  }
  updateProgress();
}

function renderDocumentsTab(container) {
  const total = currentChecklist.documents_required.length;
  const count = checkedDocs.size;
  const pct = total > 0 ? Math.round((count / total) * 100) : 0;

  let html = `
    <div class="progress-box">
      <div class="progress-header">
        <span>Citizen Readiness Tracker</span>
        <span id="progress-text">${pct}% Prepared (${count}/${total} documents ready)</span>
      </div>
      <div class="progress-bar-bg">
        <div class="progress-bar-fill" id="progress-fill" style="width: ${pct}%;"></div>
      </div>
    </div>

    <h3 style="margin-bottom: 1rem;">Required Documents Checklist</h3>
    <div class="checklist-group">
  `;

  currentChecklist.documents_required.forEach((doc, idx) => {
    const isChecked = checkedDocs.has(doc.document_name);
    html += `
      <div class="checklist-item">
        <input type="checkbox" class="checklist-checkbox" id="doc-${idx}" ${isChecked ? 'checked' : ''} onchange="toggleDoc('${doc.document_name.replace(/'/g, "\\'")}')" />
        <div class="checklist-info">
          <div class="doc-name">${doc.document_name}</div>
          <div class="doc-meta">
            <span class="badge ${doc.is_mandatory ? 'badge-mandatory' : 'badge-category'}">
              ${doc.is_mandatory ? 'Mandatory' : 'Optional'}
            </span>
            <span class="badge badge-category">${doc.category}</span>
          </div>
          <p style="font-size: 0.9rem; color: var(--text-muted);">${doc.description || ''}</p>
          ${doc.accepted_options && doc.accepted_options.length ? `
            <div class="accepted-options">
              <strong>Accepted proofs:</strong> ${doc.accepted_options.join(", ")}
            </div>
          ` : ''}
          ${doc.format_guidelines ? `
            <div style="font-size: 0.8rem; color: var(--accent-orange); margin-top: 0.3rem;">
              ℹ️ ${doc.format_guidelines}
            </div>
          ` : ''}
        </div>
      </div>
    `;
  });

  html += `</div>`;
  container.innerHTML = html;
}

function renderStepsTab(container) {
  let html = `<div class="timeline">`;
  currentChecklist.application_steps.forEach(step => {
    html += `
      <div class="step-card">
        <div class="step-number">${step.step_number}</div>
        <div class="step-details">
          <h4>${step.title}</h4>
          <span style="font-size: 0.8rem; background: var(--accent-indigo-light); color: var(--accent-indigo); padding: 0.15rem 0.5rem; border-radius: 4px; font-weight: 600;">
            ${step.phase} • ⏱️ ${step.estimated_time} • 🌐 ${step.online_or_offline}
          </span>
          <p style="margin-top: 0.5rem; font-size: 0.95rem; color: var(--text-muted);">${step.description}</p>
          ${step.action_items && step.action_items.length ? `
            <ul class="step-action-list">
              ${step.action_items.map(a => `<li>${a}</li>`).join("")}
            </ul>
          ` : ''}
        </div>
      </div>
    `;
  });
  html += `</div>`;
  container.innerHTML = html;
}

function renderEligibilityTab(container) {
  let html = `
    <h3 style="margin-bottom: 0.75rem;">Eligibility Criteria</h3>
    <ul style="padding-left: 1.5rem; margin-bottom: 2rem;">
      ${(currentService.eligibility_criteria || []).map(e => `<li style="margin-bottom: 0.5rem;">${e}</li>`).join("")}
    </ul>

    <h3 style="margin-bottom: 0.75rem; color: #dc2626;">⚠️ Common Mistakes & Rejection Traps</h3>
    <ul style="padding-left: 1.5rem; margin-bottom: 2rem; color: var(--text-muted);">
      ${(currentChecklist.common_mistakes || []).map(m => `<li style="margin-bottom: 0.5rem;">${m}</li>`).join("")}
    </ul>

    <h3 style="margin-bottom: 0.75rem; color: #059669;">💡 Expert Pro-Tips</h3>
    <ul style="padding-left: 1.5rem; color: var(--text-muted);">
      ${(currentChecklist.helpful_tips || []).map(t => `<li style="margin-bottom: 0.5rem;">${t}</li>`).join("")}
    </ul>
  `;
  container.innerHTML = html;
}

function renderFaqsTab(container) {
  if (!currentChecklist.faqs || currentChecklist.faqs.length === 0) {
    container.innerHTML = "<p>No FAQs available.</p>";
    return;
  }

  let html = `<div style="display: flex; flex-direction: column; gap: 1rem;">`;
  currentChecklist.faqs.forEach(faq => {
    html += `
      <div style="padding: 1.25rem; background: var(--bg-primary); border-radius: var(--radius-md); border: 1px solid var(--border-color);">
        <h4 style="margin-bottom: 0.4rem; color: var(--text-main);">❓ ${faq.question}</h4>
        <p style="color: var(--text-muted); font-size: 0.95rem;">${faq.answer}</p>
      </div>
    `;
  });
  html += `</div>`;
  container.innerHTML = html;
}

function renderAiEligibilityTab(container) {
  container.innerHTML = `
    <div style="background: var(--bg-primary); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 1.5rem; margin-bottom: 1.5rem;">
      <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
        <span style="font-size: 1.3rem;">🤖</span>
        <h4 style="font-size: 1.1rem;">Ask Gemini AI About Your Eligibility</h4>
      </div>
      <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1rem;">
        Describe your personal background, income, family situation, or doubts regarding <strong>${currentService.title}</strong>. Our backend Gemini AI will cross-reference your query with official criteria.
      </p>

      <textarea id="ai-query-input" rows="3" style="width: 100%; border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 0.75rem; background: var(--bg-secondary); color: var(--text-main); font-family: inherit; font-size: 0.95rem; resize: vertical; margin-bottom: 0.75rem;" placeholder="e.g. My family earns ₹6,50,000 per year and my father is a farmer. Am I eligible, and which documents will I need?"></textarea>

      <div style="display: flex; justify-content: flex-end;">
        <button class="btn btn-primary" id="ai-check-btn" onclick="askAiEligibility()">
          ✨ Evaluate My Eligibility
        </button>
      </div>
    </div>

    <div id="ai-eval-result" style="display: none; padding: 1.5rem; border-radius: var(--radius-md); background: var(--bg-secondary); border: 1px solid var(--border-color);">
      <!-- AI result populated here -->
    </div>
  `;
}

async function askAiEligibility() {
  const queryInput = document.getElementById("ai-query-input");
  const query = queryInput ? queryInput.value.trim() : "";
  if (!query) {
    alert("Please enter your question or situation.");
    return;
  }

  const btn = document.getElementById("ai-check-btn");
  const resultDiv = document.getElementById("ai-eval-result");
  btn.disabled = true;
  btn.innerText = "Analyzing Criteria...";

  resultDiv.style.display = "block";
  resultDiv.innerHTML = `<p style="color: var(--text-muted); text-align: center;">Consulting government guidelines and evaluating your eligibility...</p>`;

  try {
    const res = await fetch("/api/v1/ai/check-eligibility", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        service_slug: currentService.slug,
        user_query: query
      })
    });

    if (!res.ok) throw new Error("Evaluation request failed");
    const data = await res.json();

    const badgeColor = data.assessment.includes("Likely Eligible") ? "#059669" : (data.assessment.includes("Ineligible") ? "#dc2626" : "#d97706");
    const badgeBg = data.assessment.includes("Likely Eligible") ? "#ecfdf5" : (data.assessment.includes("Ineligible") ? "#fef2f2" : "#fffbeb");

    resultDiv.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <h4 style="font-size: 1.1rem;">Eligibility Assessment</h4>
        <span style="background: ${badgeBg}; color: ${badgeColor}; font-weight: 700; font-size: 0.85rem; padding: 0.25rem 0.75rem; border-radius: 9999px;">
          ${data.assessment}
        </span>
      </div>

      <p style="font-size: 0.95rem; margin-bottom: 1.25rem; line-height: 1.6;">${data.reasoning}</p>

      ${data.required_documents_highlight && data.required_documents_highlight.length ? `
        <div style="margin-bottom: 1rem;">
          <strong style="font-size: 0.85rem; text-transform: uppercase; color: var(--text-light);">Key Documents You Must Prepare:</strong>
          <ul style="margin-top: 0.35rem; padding-left: 1.2rem; font-size: 0.9rem;">
            ${data.required_documents_highlight.map(d => `<li>${d}</li>`).join("")}
          </ul>
        </div>
      ` : ''}

      <div style="background: var(--bg-primary); padding: 0.75rem 1rem; border-radius: var(--radius-sm); border-left: 3px solid var(--accent-orange); margin-bottom: 1rem;">
        <strong>Recommended Next Step:</strong> <span style="color: var(--text-muted); font-size: 0.9rem;">${data.suggested_action}</span>
      </div>

      <div style="font-size: 0.75rem; color: var(--text-light); border-top: 1px solid var(--border-color); padding-top: 0.5rem;">
        ${data.disclaimer} • <span style="text-transform: capitalize;">Engine: ${data.source}</span>
      </div>
    `;
  } catch (err) {
    console.error(err);
    resultDiv.innerHTML = `<p style="color: #ef4444;">Could not evaluate eligibility. Please verify backend connection.</p>`;
  } finally {
    btn.disabled = false;
    btn.innerText = "✨ Evaluate My Eligibility";
  }
}

async function explainQuickTerm(term) {
  document.getElementById("term-input").value = term;
  await fetchTermExplanation(term);
}

async function explainCustomTerm() {
  const input = document.getElementById("term-input");
  const term = input ? input.value.trim() : "";
  if (!term) return;
  await fetchTermExplanation(term);
}

async function fetchTermExplanation(term) {
  const resultCard = document.getElementById("term-result-card");
  resultCard.style.display = "block";
  resultCard.innerHTML = `<p style="color: var(--text-muted); text-align: center;">Explaining "${term}" in simple citizen terms...</p>`;

  try {
    const res = await fetch("/api/v1/ai/explain-term", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ term: term })
    });

    if (!res.ok) throw new Error("Failed to explain term");
    const data = await res.json();

    resultCard.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
        <h3 style="font-size: 1.2rem; color: var(--accent-orange);">${data.term}</h3>
        <span style="font-size: 0.75rem; background: var(--bg-secondary); padding: 0.2rem 0.5rem; border-radius: 4px; color: var(--text-muted);">
          Source: ${data.source === 'gemini' ? 'Google Gemini AI' : 'Verified Knowledge Base'}
        </span>
      </div>
      <p style="font-size: 1rem; line-height: 1.6; margin-bottom: 1rem;">${data.simplified_explanation}</p>

      <div style="background: var(--bg-secondary); padding: 1rem; border-radius: var(--radius-sm); margin-bottom: 0.75rem; border: 1px solid var(--border-color);">
        <strong style="color: var(--accent-blue); font-size: 0.9rem;">📌 Real-World Example:</strong>
        <p style="font-size: 0.9rem; color: var(--text-muted); margin-top: 0.25rem;">${data.real_world_example}</p>
      </div>

      <div style="background: var(--accent-orange-light); padding: 1rem; border-radius: var(--radius-sm); border: 1px solid rgba(234, 88, 12, 0.2);">
        <strong style="color: var(--accent-orange); font-size: 0.9rem;">💡 Citizen Action Tip:</strong>
        <p style="font-size: 0.9rem; color: var(--text-main); margin-top: 0.25rem;">${data.actionable_tip}</p>
      </div>
    `;
  } catch (err) {
    console.error(err);
    resultCard.innerHTML = `<p style="color: #ef4444;">Failed to fetch explanation. Please ensure the backend is running.</p>`;
  }
}

function setupEventListeners() {
  // Theme Toggle
  const themeBtn = document.getElementById("theme-toggle-btn");
  if (themeBtn) themeBtn.addEventListener("click", toggleTheme);

  // Term input enter key
  const termInput = document.getElementById("term-input");
  if (termInput) {
    termInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") explainCustomTerm();
    });
  }

  // Search Input debounce
  const searchInput = document.getElementById("search-input");
  let debounceTimeout;
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      clearTimeout(debounceTimeout);
      debounceTimeout = setTimeout(() => {
        const activePill = document.querySelector(".pill.active");
        const category = activePill ? activePill.getAttribute("data-cat") : "";
        loadServices(category === "All" ? "" : category, e.target.value.trim());
      }, 300);
    });
  }

  // Category Pills
  document.querySelectorAll(".pill").forEach(pill => {
    pill.addEventListener("click", () => {
      document.querySelectorAll(".pill").forEach(p => p.classList.remove("active"));
      pill.classList.add("active");
      const cat = pill.getAttribute("data-cat");
      const searchVal = document.getElementById("search-input") ? document.getElementById("search-input").value.trim() : "";
      loadServices(cat === "All" ? "" : cat, searchVal);
    });
  });

  // Modal Backdrop click to close
  const modal = document.getElementById("modal-backdrop");
  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) closeModal();
    });
  }
}
