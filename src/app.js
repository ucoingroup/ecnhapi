const FIT_LABELS = {
  best: "✅ Best Fit",
  good: "⚡ Good Fit",
  low: "➖ Low Fit",
};

const I18N = {
  en: {
    eyebrow: "API Ecosystem Guide",
    heroTitle: "Global APIs × eCNH",
    heroCopy:
      "Complete guide to Top 10 Social APIs + Top 10 AI APIs. What's free? How are they priced? Which are best for eCNH?",
    exploreGuide: "Explore guide",
    viewStack: "View eCNH stack",
    socialApis: "Social APIs",
    aiApis: "AI APIs",
    freeTier: "Have Free Tier",
    bestFit: "Best Fit eCNH",
    compareEyebrow: "Decision dashboard",
    compareTitle: "API ecosystem comparison",
    searchLabel: "Search APIs",
    all: "All",
    socialTab: "💬 Social APIs",
    aiTab: "🤖 AI APIs",
    emptyState: "No APIs match your search.",
    socialTable: "📊 Social API Comparison Table",
    aiTable: "🤖 AI API Comparison Table",
    platform: "Platform",
    free: "Free?",
    freeLimit: "Free Limit",
    startingPrice: "Starting Price",
    ecnhFit: "eCNH Fit",
    stackEyebrow: "eCNH Stack",
    stackTitle: "Recommended launch architecture",
    footerNote: "Data sourced from official platform docs (2025-2026) · Prices may change, verify at official sites.",
    paidPlans: "Paid plans & use cases",
    searchPlaceholder: "Search...",
  },
  zh: {
    eyebrow: "API 生态指南",
    heroTitle: "全球 API × eCNH",
    heroCopy: "完整梳理 Top 10 社交 API + Top 10 AI API：哪些免费？如何计费？哪些最适合 eCNH？",
    exploreGuide: "查看指南",
    viewStack: "查看 eCNH 架构",
    socialApis: "社交 API",
    aiApis: "AI API",
    freeTier: "提供免费层",
    bestFit: "最适合 eCNH",
    compareEyebrow: "决策看板",
    compareTitle: "API 生态对比",
    searchLabel: "搜索 API",
    all: "全部",
    socialTab: "💬 社交 API",
    aiTab: "🤖 AI API",
    emptyState: "没有匹配的 API。",
    socialTable: "📊 社交 API 对比表",
    aiTable: "🤖 AI API 对比表",
    platform: "平台",
    free: "免费？",
    freeLimit: "免费额度",
    startingPrice: "起始价格",
    ecnhFit: "eCNH 适配度",
    stackEyebrow: "eCNH 技术栈",
    stackTitle: "推荐启动架构",
    footerNote: "数据参考官方平台文档（2025-2026）· 价格可能变化，请以官方网站为准。",
    paidPlans: "付费方案与使用场景",
    searchPlaceholder: "搜索...",
  },
};

const state = {
  apis: [],
  stack: [],
  filter: "all",
  search: "",
  locale: "en",
};

const elements = {
  apiGrid: document.querySelector("#api-grid"),
  emptyState: document.querySelector("#empty-state"),
  socialTable: document.querySelector("#social-table-body"),
  aiTable: document.querySelector("#ai-table-body"),
  stackGrid: document.querySelector("#stack-grid"),
  search: document.querySelector("#search-input"),
  tabs: document.querySelectorAll(".tab"),
  languageToggle: document.querySelector("#language-toggle"),
  navToggle: document.querySelector(".nav-toggle"),
  navLinks: document.querySelector("#nav-links"),
};

async function loadApiData() {
  const response = await fetch("data/api-ecosystem.json");
  if (!response.ok) {
    throw new Error(`Unable to load API data: ${response.status}`);
  }
  return response.json();
}

function renderStats() {
  const socialApis = state.apis.filter((api) => api.category === "social");
  const aiApis = state.apis.filter((api) => api.category === "ai");
  document.querySelector("#social-count").textContent = socialApis.length;
  document.querySelector("#ai-count").textContent = aiApis.length;
  document.querySelector("#free-count").textContent = state.apis.filter((api) => api.free).length;
  document.querySelector("#best-fit-count").textContent = state.apis.filter((api) => api.fit === "best").length;
}

function filteredApis() {
  const query = state.search.trim().toLowerCase();
  return state.apis.filter((api) => {
    const matchesFilter = state.filter === "all" || api.category === state.filter || api.fit === state.filter;
    const haystack = [api.name, api.type, api.freeLimit, api.note, api.ecnhValue, ...api.useCases]
      .join(" ")
      .toLowerCase();
    return matchesFilter && (!query || haystack.includes(query));
  });
}

function createApiCard(api) {
  const article = document.createElement("article");
  article.className = `api-card ${api.fit}`;
  article.innerHTML = `
    <div class="card-top">
      <div class="api-title">
        <span class="api-icon" aria-hidden="true">${api.icon}</span>
        <div>
          <h3>${api.name}</h3>
          <span class="badge">${api.type}</span>
        </div>
      </div>
      <div class="badges">
        <span class="badge ${api.fit}">${FIT_LABELS[api.fit]}</span>
        <span class="badge">${api.category === "social" ? "Social" : "AI"}</span>
      </div>
    </div>
    <p class="free-line">Free: ${api.freeLimit}</p>
    <p>${api.note}</p>
    <p>${api.ecnhValue}</p>
    <details>
      <summary>${I18N[state.locale].paidPlans}</summary>
      <ul class="use-cases">
        <li><strong>Starting price:</strong> ${api.startingPrice}</li>
        ${api.useCases.map((item) => `<li>${item}</li>`).join("")}
      </ul>
    </details>
  `;
  return article;
}

function renderCards() {
  const apis = filteredApis();
  elements.apiGrid.replaceChildren(...apis.map(createApiCard));
  elements.emptyState.hidden = apis.length > 0;
}

function createTableRow(api) {
  const row = document.createElement("tr");
  row.innerHTML = `
    <td>${api.icon} ${api.name}</td>
    <td>${api.free ? "✅" : "❌"}</td>
    <td>${api.freeLimit}</td>
    <td>${api.startingPrice}</td>
    <td>${FIT_LABELS[api.fit].split(" ")[0]}</td>
  `;
  return row;
}

function renderTables() {
  elements.socialTable.replaceChildren(...state.apis.filter((api) => api.category === "social").map(createTableRow));
  elements.aiTable.replaceChildren(...state.apis.filter((api) => api.category === "ai").map(createTableRow));
}

function renderStack() {
  const cards = state.stack.map((item) => {
    const card = document.createElement("article");
    card.className = "stack-card";
    card.innerHTML = `
      <h3>${item.title}</h3>
      <p><strong>${item.apis.join(" + ")}</strong></p>
      <p>${item.description}</p>
    `;
    return card;
  });
  elements.stackGrid.replaceChildren(...cards);
}

function applyTranslations() {
  const dictionary = I18N[state.locale];
  document.documentElement.lang = state.locale === "zh" ? "zh-Hans" : "en";
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    const key = node.dataset.i18n;
    if (dictionary[key]) {
      node.textContent = dictionary[key];
    }
  });
  elements.search.placeholder = dictionary.searchPlaceholder;
  elements.languageToggle.textContent = state.locale === "en" ? "🇬🇧 EN" : "🇨🇳 中文";
}

function bindEvents() {
  elements.search.addEventListener("input", (event) => {
    state.search = event.target.value;
    renderCards();
  });

  elements.tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      state.filter = tab.dataset.filter;
      elements.tabs.forEach((item) => {
        const selected = item === tab;
        item.classList.toggle("is-active", selected);
        item.setAttribute("aria-selected", String(selected));
      });
      renderCards();
    });
  });

  elements.languageToggle.addEventListener("click", () => {
    state.locale = state.locale === "en" ? "zh" : "en";
    applyTranslations();
    renderCards();
  });

  elements.navToggle.addEventListener("click", () => {
    const isOpen = elements.navLinks.classList.toggle("is-open");
    elements.navToggle.setAttribute("aria-expanded", String(isOpen));
  });
}

function renderAll() {
  applyTranslations();
  renderStats();
  renderCards();
  renderTables();
  renderStack();
}

async function init() {
  try {
    const data = await loadApiData();
    state.apis = data.apis;
    state.stack = data.stack;
    bindEvents();
    renderAll();
  } catch (error) {
    elements.apiGrid.innerHTML = `<p class="empty-state">${error.message}</p>`;
  }
}

init();
