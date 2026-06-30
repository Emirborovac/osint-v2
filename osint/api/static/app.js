// OSINT V2 — front-end shell. Vanilla JS. Sidebar collapse + tab switching + search.

const TITLES = { search: "Search", sources: "Supported Sources" };
const VIEWS = ["search", "sources"];

function el(id) {
  return document.getElementById(id);
}
function escapeHtml(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

/* ---- View switching ------------------------------------------------- */

function showView(view) {
  document.querySelectorAll(".nav-item").forEach((a) => {
    a.classList.toggle("active", a.dataset.view === view);
  });
  el("page-title").textContent = (TITLES[view] || view).toUpperCase();
  VIEWS.forEach((v) => {
    const node = el("view-" + v);
    if (node) node.hidden = v !== view;
  });
}

function initNav() {
  el("nav").addEventListener("click", (e) => {
    const a = e.target.closest(".nav-item");
    if (!a) return;
    e.preventDefault();
    showView(a.dataset.view);
  });
}

/* ---- Sidebar collapse (persisted) ----------------------------------- */

function initSidebar() {
  const layout = el("layout");
  const toggle = el("toggle");
  const collapsed = localStorage.getItem("sidebarCollapsed") === "1";
  layout.classList.toggle("collapsed", collapsed);
  toggle.setAttribute("aria-expanded", String(!collapsed));
  toggle.addEventListener("click", () => {
    const now = layout.classList.toggle("collapsed");
    localStorage.setItem("sidebarCollapsed", now ? "1" : "0");
    toggle.setAttribute("aria-expanded", String(!now));
  });
}

/* ---- Search (link harvesting) --------------------------------------- */

function resultHtml(link, idx) {
  const title = escapeHtml(link.title || link.url);
  const url = escapeHtml(link.url);
  return (
    `<div class="result">` +
    `<div class="r-title"><span class="r-idx">${idx}</span>${title}</div>` +
    `<a class="r-url" href="${url}" target="_blank" rel="noopener">${url}</a>` +
    `</div>`
  );
}

function renderResults(data) {
  const box = el("search-results");
  const links = data.links || [];
  if (!links.length) {
    const note = data.note ? escapeHtml(data.note) : "No links found.";
    box.innerHTML = `<div class="results-empty">${note}</div>`;
  } else {
    box.innerHTML =
      `<div class="results-head">${links.length} links harvested for &ldquo;${escapeHtml(data.query)}&rdquo;</div>` +
      links.map((l, i) => resultHtml(l, i + 1)).join("");
  }
  box.hidden = false;
}

async function runSearch(query) {
  const progress = el("search-progress");
  const results = el("search-results");
  const btn = el("search-btn");

  results.hidden = true;
  results.innerHTML = "";
  progress.hidden = false;
  btn.disabled = true;

  try {
    const r = await fetch("/api/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(data.detail || "Search failed");
    renderResults(data);
  } catch (err) {
    results.innerHTML = `<div class="results-empty">${escapeHtml(err.message || "Search failed")}</div>`;
    results.hidden = false;
  } finally {
    progress.hidden = true;
    btn.disabled = false;
  }
}

function initSearch() {
  el("search-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const q = el("q").value.trim();
    if (q) runSearch(q);
  });
}

/* ---- Boot ----------------------------------------------------------- */

initSidebar();
initNav();
initSearch();
showView("search");
