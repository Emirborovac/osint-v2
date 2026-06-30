// OSINT V2 — front-end shell. Vanilla JS. Sidebar collapse + tab switching.

const TITLES = { search: "Search", sources: "Supported Sources" };
const VIEWS = ["search", "sources"];

function el(id) {
  return document.getElementById(id);
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

/* ---- Boot ----------------------------------------------------------- */

initSidebar();
initNav();
showView("search");
