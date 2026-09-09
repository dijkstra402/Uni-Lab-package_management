const state = {
  modules: [],
  selectedIds: [],
  activeId: null,
  query: "",
  category: "",
  view: "all",
  toastTimer: null,
};

const elements = {
  catalogCount: document.querySelector("#catalogCount"),
  categoryCount: document.querySelector("#categoryCount"),
  categoryList: document.querySelector("#categoryList"),
  categorySelect: document.querySelector("#categorySelect"),
  clearFilters: document.querySelector("#clearFilters"),
  configForm: document.querySelector("#configForm"),
  devicePackageButton: document.querySelector("#devicePackageButton"),
  devicePackageLabel: document.querySelector("#devicePackageLabel"),
  detailId: document.querySelector("#detailId"),
  driverMode: document.querySelector("#driverMode"),
  driverModeHelp: document.querySelector("#driverModeHelp"),
  exportButton: document.querySelector("#exportButton"),
  acceptanceBundleButton: document.querySelector("#acceptanceBundleButton"),
  formError: document.querySelector("#formError"),
  moduleDetail: document.querySelector("#moduleDetail"),
  moduleList: document.querySelector("#moduleList"),
  moduleSearch: document.querySelector("#moduleSearch"),
  propertyTotal: document.querySelector("#propertyTotal"),
  resultCount: document.querySelector("#resultCount"),
  selectedCount: document.querySelector("#selectedCount"),
  selectedList: document.querySelector("#selectedList"),
  selectionStatus: document.querySelector("#selectionStatus"),
  sourceTotal: document.querySelector("#sourceTotal"),
  actionTotal: document.querySelector("#actionTotal"),
  toast: document.querySelector("#toast"),
};

const iconClose = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 5l10 10M15 5L5 15" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" /></svg>';

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function getModule(deviceId) {
  return state.modules.find((module) => module.device_id === deviceId);
}

function filteredModules() {
  const query = state.query.trim().toLocaleLowerCase();
  return state.modules.filter((module) => {
    const searchable = [module.device_id, module.displayname, module.category, ...module.category_path]
      .join(" ")
      .toLocaleLowerCase();
    const matchesQuery = !query || searchable.includes(query);
    const matchesCategory = !state.category || module.category_path.join(" > ").startsWith(state.category);
    const matchesView = state.view !== "selected" || state.selectedIds.includes(module.device_id);
    return matchesQuery && matchesCategory && matchesView;
  });
}

function renderCategories() {
  const groups = new Map();
  state.modules.forEach((module) => {
    const topLevel = module.category_path[0] || module.category;
    groups.set(topLevel, (groups.get(topLevel) || 0) + 1);
  });
  const buttons = [
    { value: "", label: "全部模块", count: state.modules.length },
    ...[...groups.entries()]
      .sort(([left], [right]) => left.localeCompare(right, "zh-CN"))
      .map(([label, count]) => ({ value: label, label, count })),
  ];
  elements.categoryList.innerHTML = buttons.map(({ value, label, count }) => `
    <button class="category-button ${state.category === value ? "is-active" : ""}" type="button" data-category="${escapeHtml(value)}" aria-pressed="${state.category === value}">
      <span>${escapeHtml(label)}</span><span>${count}</span>
    </button>
  `).join("");
  elements.categoryCount.textContent = String(groups.size);
  elements.categorySelect.innerHTML = '<option value="">全部分类路径</option>';
  const prefixes = new Set();
  state.modules.forEach((module) => {
    const path = module.category_path || [];
    path.slice(0, 2).forEach((_, index) => {
      prefixes.add(path.slice(0, index + 1).join(" > "));
    });
  });
  [...prefixes]
    .sort((left, right) => left.localeCompare(right, "zh-CN"))
    .forEach((prefix) => {
      const option = document.createElement("option");
      option.value = prefix;
      option.textContent = prefix;
      elements.categorySelect.append(option);
    });
  elements.categorySelect.value = state.category;
}

function renderModules() {
  const modules = filteredModules();
  elements.resultCount.textContent = `${modules.length} 个结果`;
  if (!modules.length) {
    elements.moduleList.innerHTML = `
      <div class="empty-state">
        <div><strong>${state.view === "selected" ? "还没有已选模块" : "没有匹配的模块"}</strong><span>${state.view === "selected" ? "回到全部模块，勾选需要加入设备包的接口。" : "尝试更换关键词或清除分类筛选。"}</span><br /><button type="button" data-action="clear-empty">清除筛选</button></div>
      </div>
    `;
    return;
  }
  elements.moduleList.innerHTML = modules.map((module) => {
    const selected = state.selectedIds.includes(module.device_id);
    const categoryPath = module.category_path.join(" > ");
    return `
      <div class="module-row ${selected ? "is-selected" : ""}">
        <input class="module-check" type="checkbox" data-module-id="${escapeHtml(module.device_id)}" aria-label="选择 ${escapeHtml(module.displayname)}" ${selected ? "checked" : ""} />
        <button class="module-main" type="button" data-detail-id="${escapeHtml(module.device_id)}" aria-label="查看 ${escapeHtml(module.displayname)} 模块合同">
          <span class="module-name">${escapeHtml(module.displayname)}</span>
          <span class="module-meta"><span class="module-category">${escapeHtml(categoryPath)}</span><span class="module-id">${escapeHtml(module.device_id)}</span></span>
        </button>
        <span class="module-contracts"><span>${module.actions.length} actions</span><span>${module.properties.length} props</span></span>
        <button class="detail-button" type="button" data-detail-id="${escapeHtml(module.device_id)}">查看合同</button>
      </div>
    `;
  }).join("");
}

function renderSelected() {
  const selected = state.selectedIds.map(getModule).filter(Boolean);
  elements.selectedCount.textContent = String(selected.length);
  elements.exportButton.disabled = selected.length === 0;
  elements.devicePackageButton.disabled = selected.length === 0;
  elements.acceptanceBundleButton.disabled = selected.length === 0;
  elements.selectionStatus.textContent = selected.length ? "可导出" : "未选择";
  elements.selectionStatus.className = `status-chip ${selected.length ? "status-chip-ready" : "status-chip-neutral"}`;
  elements.actionTotal.textContent = String(selected.reduce((total, module) => total + module.actions.length, 0));
  elements.propertyTotal.textContent = String(selected.reduce((total, module) => total + module.properties.length, 0));
  elements.sourceTotal.textContent = String(selected.filter((module) => module.source_path).length);
  elements.selectedList.innerHTML = selected.length ? selected.map((module) => `
    <div class="selected-item">
      <button class="module-main" type="button" data-detail-id="${escapeHtml(module.device_id)}"><span class="selected-item-name">${escapeHtml(module.displayname)}</span></button>
      <button class="selected-item-remove" type="button" data-remove-id="${escapeHtml(module.device_id)}" aria-label="移除 ${escapeHtml(module.displayname)}">${iconClose}</button>
    </div>
  `).join("") : '<div class="selected-empty">从左侧选择模块，开始组装设备包。</div>';
}

function renderDriverMode() {
  const isOpcUa = elements.driverMode.value === "opcua";
  elements.devicePackageLabel.textContent = isOpcUa ? "生成并下载 OPC UA 设备包" : "生成并下载设备包";
  elements.devicePackageButton.title = isOpcUa ? "生成并下载 OPC UA 真实设备包" : "生成并下载标准设备包";
  elements.driverModeHelp.textContent = isOpcUa
    ? "包含 OPC UA 通信运行时、标准协议点表和可执行的读写动作；部署时注入真实 NodeId。"
    : "标准模板只导出接口，动作会保留为待实现占位。";
}

function renderDetail() {
  const module = getModule(state.activeId);
  if (!module) {
    elements.detailId.textContent = "—";
    elements.moduleDetail.innerHTML = '<div class="detail-empty">点击模块名称查看动作、属性与完整分类路径。</div>';
    return;
  }
  elements.detailId.textContent = module.device_id;
  const renderContract = (contract) => `<div class="contract-item"><strong>${escapeHtml(contract.name)}</strong><span>${escapeHtml(contract.description || contract.parameter_spec || "标准合同")}</span></div>`;
  elements.moduleDetail.innerHTML = `
    <div class="detail-path">${escapeHtml(module.category_path.join(" > "))}</div>
    <p class="detail-description">${escapeHtml(module.category)} · ${escapeHtml(module.displayname)}</p>
    <div class="contract-columns">
      <div class="contract-block"><h4>动作 <span class="contract-count">${module.actions.length}</span></h4><div class="contract-list">${module.actions.map(renderContract).join("") || '<div class="detail-empty">暂无动作</div>'}</div></div>
      <div class="contract-block"><h4>状态属性 <span class="contract-count">${module.properties.length}</span></h4><div class="contract-list">${module.properties.map(renderContract).join("") || '<div class="detail-empty">暂无属性</div>'}</div></div>
    </div>
    <code class="source-path">${escapeHtml(module.source_path)}</code>
  `;
}

function render() {
  renderCategories();
  renderModules();
  renderSelected();
  renderDetail();
  document.querySelectorAll("[data-view]").forEach((button) => button.classList.toggle("is-active", button.dataset.view === state.view));
}

function setActive(deviceId) {
  state.activeId = deviceId;
  renderDetail();
}

function toggleSelection(deviceId, checked) {
  if (checked && !state.selectedIds.includes(deviceId)) state.selectedIds.push(deviceId);
  if (!checked) state.selectedIds = state.selectedIds.filter((id) => id !== deviceId);
  state.activeId = deviceId;
  renderModules();
  renderSelected();
  renderDetail();
}

function clearFilters() {
  state.query = "";
  state.category = "";
  state.view = "all";
  elements.moduleSearch.value = "";
  render();
}

function projectConfig() {
  return {
    distribution_name: document.querySelector("#distributionName").value.trim(),
    package_name: document.querySelector("#packageName").value.trim(),
    version: document.querySelector("#version").value.trim(),
    description: document.querySelector("#description").value.trim(),
    driver_mode: elements.driverMode.value,
    modules: [...state.selectedIds],
  };
}

function validatedProjectConfig() {
  elements.formError.textContent = "";
  if (!elements.configForm.reportValidity()) return null;
  const config = projectConfig();
  if (!config.modules.length) {
    elements.formError.textContent = "至少选择一个设备模块后才能生成或导出。";
    return null;
  }
  return config;
}

function downloadConfig(event) {
  event.preventDefault();
  const config = validatedProjectConfig();
  if (!config) return;
  const blob = new Blob([`${JSON.stringify(config, null, 2)}\n`], { type: "application/json" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `${config.distribution_name || "device-package"}.json`;
  link.click();
  URL.revokeObjectURL(link.href);
  showToast(`已导出 ${config.modules.length} 个模块的配置 JSON`);
}

function downloadFilename(response, fallback) {
  const disposition = response.headers.get("Content-Disposition") || "";
  const match = disposition.match(/filename="([^"]+)"/i);
  return match?.[1] || fallback;
}

async function downloadBundle(kind) {
  const config = validatedProjectConfig();
  if (!config) return;
  const button = kind === "device" ? elements.devicePackageButton : elements.acceptanceBundleButton;
  const endpoint = kind === "device" ? "/api/generate/device-package" : "/api/generate/acceptance-bundle";
  const fallback = kind === "device" ? "device-package.tar.gz" : "acceptance-bundle.tar.gz";
  button.disabled = true;
  button.setAttribute("aria-busy", "true");
  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/gzip" },
      body: JSON.stringify(config),
    });
    if (!response.ok) {
      let message = `HTTP ${response.status}`;
      try {
        const errorPayload = await response.json();
        message = errorPayload.error || message;
      } catch {
        message = `HTTP ${response.status}`;
      }
      throw new Error(message);
    }
    const blob = await response.blob();
    const link = document.createElement("a");
    const objectUrl = URL.createObjectURL(blob);
    link.href = objectUrl;
    link.download = downloadFilename(response, fallback);
    link.click();
    link.remove();
    URL.revokeObjectURL(objectUrl);
    showToast(kind === "device" ? "设备包已生成并开始下载" : "自动验收包已生成并开始下载");
  } catch (error) {
    elements.formError.textContent = `生成失败：${error.message || "请稍后重试"}`;
  } finally {
    button.removeAttribute("aria-busy");
    renderSelected();
  }
}

function showToast(message) {
  elements.toast.textContent = message;
  elements.toast.classList.add("is-visible");
  clearTimeout(state.toastTimer);
  state.toastTimer = setTimeout(() => elements.toast.classList.remove("is-visible"), 2600);
}

async function loadCatalog() {
  try {
    const response = await fetch("/api/catalog", { headers: { Accept: "application/json" } });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const modules = await response.json();
    if (!Array.isArray(modules) || modules.length < 1) throw new Error("目录数量校验失败");
    state.modules = modules;
    state.activeId = modules[0]?.device_id || null;
    elements.catalogCount.textContent = String(modules.length);
    document.querySelector("#catalogTotal").textContent = String(modules.length);
    render();
  } catch (error) {
    elements.moduleList.innerHTML = `<div class="empty-state"><div><strong>模块目录读取失败</strong><span>请确认页面由 <code>unilab-package-builder ui</code> 启动，并重试。</span><br /><button type="button" data-action="retry">重新读取</button></div></div>`;
    elements.resultCount.textContent = "目录不可用";
    console.warn(error);
  }
}

elements.moduleSearch.addEventListener("input", (event) => {
  state.query = event.target.value;
  renderModules();
});
elements.categoryList.addEventListener("click", (event) => {
  const button = event.target.closest("[data-category]");
  if (!button) return;
  state.category = button.dataset.category;
  render();
});
elements.categorySelect.addEventListener("change", (event) => {
  state.category = event.target.value;
  render();
});
elements.clearFilters.addEventListener("click", clearFilters);
elements.moduleList.addEventListener("change", (event) => {
  const checkbox = event.target.closest("[data-module-id]");
  if (checkbox) toggleSelection(checkbox.dataset.moduleId, checkbox.checked);
});
elements.moduleList.addEventListener("click", (event) => {
  const detailButton = event.target.closest("[data-detail-id]");
  const actionButton = event.target.closest("[data-action]");
  if (detailButton) setActive(detailButton.dataset.detailId);
  if (actionButton?.dataset.action === "clear-empty") clearFilters();
  if (actionButton?.dataset.action === "retry") loadCatalog();
});
elements.selectedList.addEventListener("click", (event) => {
  const removeButton = event.target.closest("[data-remove-id]");
  const detailButton = event.target.closest("[data-detail-id]");
  if (removeButton) toggleSelection(removeButton.dataset.removeId, false);
  if (detailButton) setActive(detailButton.dataset.detailId);
});
elements.devicePackageButton.addEventListener("click", () => downloadBundle("device"));
elements.acceptanceBundleButton.addEventListener("click", () => downloadBundle("acceptance"));
elements.driverMode.addEventListener("change", renderDriverMode);
document.querySelectorAll("[data-view]").forEach((button) => button.addEventListener("click", () => {
  state.view = button.dataset.view;
  renderModules();
  document.querySelectorAll("[data-view]").forEach((item) => item.classList.toggle("is-active", item.dataset.view === state.view));
}));
elements.configForm.addEventListener("submit", downloadConfig);
document.addEventListener("keydown", (event) => {
  if (event.key === "/" && document.activeElement?.tagName !== "INPUT") {
    event.preventDefault();
    elements.moduleSearch.focus();
  }
});

loadCatalog();
renderDriverMode();
