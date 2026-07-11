// ===== Special School · PC端交互脚本 =====

document.addEventListener("DOMContentLoaded", () => {
  initScrollAnimations();
  initTabSwitching();
  initMobileNav();
  initAdminUploadPreview();
  initSchoolDetailStatusFilter();
  initMediaGallery();
});

// --- 移动端导航 ---
function initMobileNav() {
  if (document.querySelector(".mobile-top-bar")) return;

  const sideNav = document.querySelector(".side-nav");
  const main = document.querySelector(".main-content");
  if (!sideNav) return;

  const topBar = document.createElement("div");
  topBar.className = "mobile-top-bar";
  topBar.innerHTML = `
    <span class="brand">特殊学校公益平台</span>
    <button class="mobile-nav-toggle" aria-label="切换导航" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  `;
  document.body.insertBefore(topBar, sideNav);

  const overlay = document.createElement("div");
  overlay.className = "mobile-nav-overlay";
  if (main) {
    document.body.insertBefore(overlay, main);
  } else {
    document.body.appendChild(overlay);
  }

  const toggle = topBar.querySelector(".mobile-nav-toggle");

  function setOpen(open) {
    sideNav.classList.toggle("mobile-nav-open", open);
    toggle.classList.toggle("active", open);
    overlay.classList.toggle("active", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  }

  toggle.addEventListener("click", () => setOpen(!sideNav.classList.contains("mobile-nav-open")));
  overlay.addEventListener("click", () => setOpen(false));

  sideNav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => setOpen(false));
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 768) setOpen(false);
  });
}

// --- 单图 / 单文件上传回填 ---
function initAdminUploadPreview() {
  document.querySelectorAll(".image-upload-input").forEach((input) => {
    input.addEventListener("change", async () => {
      const file = input.files[0];
      if (!file) return;

      const form = input.closest("form");
      const csrfToken = form?.querySelector('input[name="csrf_token"]')?.value;
      if (!csrfToken) {
        alert("缺少 CSRF 令牌，无法上传");
        return;
      }

      const targetId = input.dataset.target;
      const urlInput = targetId
        ? document.getElementById(targetId)
        : input.closest(".form-group")?.querySelector(".image-url-input");
      const preview = urlInput
        ? document.getElementById("preview_" + (targetId || urlInput.id))
        : null;

      const data = new FormData();
      data.append("file", file);
      data.append("csrf_token", csrfToken);

      try {
        input.disabled = true;
        const response = await fetch(window.UPLOAD_URL || "/admin/upload", {
          method: "POST",
          body: data,
        });
        const result = await response.json();
        if (!response.ok || !result.url) {
          throw new Error(result.error || "上传失败");
        }

        if (urlInput) urlInput.value = result.url;
        if (preview) {
          preview.src = result.url;
          preview.style.display = "block";
        }
      } catch (err) {
        alert("上传失败：" + err.message);
      } finally {
        input.disabled = false;
        input.value = "";
      }
    });
  });
}

// --- 多媒体画廊管理器 ---
function initMediaGallery() {
  const container = document.querySelector(".media-gallery-group");
  if (!container) return;

  const listEl = container.querySelector("#media_list");
  const emptyEl = container.querySelector("#media_empty");
  const inputEl = container.querySelector("#media_json");
  const uploadInput = container.querySelector("#media_upload_input");
  const sectionSelect = container.querySelector("#new_media_section");
  const sections = window.MEDIA_SECTIONS || { gallery: "相册" };

  let items = [];
  try {
    items = JSON.parse(inputEl?.value || "[]") || [];
  } catch (e) {
    items = [];
  }

  function save() {
    if (inputEl) inputEl.value = JSON.stringify(items);
    render();
  }

  function render() {
    if (!listEl) return;
    listEl.innerHTML = "";
    if (emptyEl) emptyEl.style.display = items.length ? "none" : "block";

    items.forEach((item, index) => {
      const el = document.createElement("div");
      el.className = "media-item";
      el.draggable = true;
      el.dataset.index = index;

      const isVideo = item.type === "video";
      const preview = isVideo
        ? `<video src="${item.url}" controls class="media-thumb"></video>`
        : `<img src="${item.url}" alt="" class="media-thumb" onerror="this.style.display='none'">`;

      const sectionOptions = Object.entries(sections)
        .map(
          ([key, label]) =>
            `<option value="${key}" ${item.section === key ? "selected" : ""}>${label}</option>`
        )
        .join("");

      el.innerHTML = `
        <div class="media-drag-handle" title="拖拽排序">⋮⋮</div>
        <div class="media-preview">${preview}</div>
        <div class="media-fields">
          <select class="form-control form-control-sm media-section" data-index="${index}">${sectionOptions}</select>
          <input type="text" class="form-control form-control-sm media-caption" value="${escapeHtml(item.caption || "")}" placeholder="说明文字" data-index="${index}">
        </div>
        <div class="media-actions">
          <button type="button" class="btn btn-sm btn-secondary media-move-up" data-index="${index}" ${index === 0 ? "disabled" : ""}>↑</button>
          <button type="button" class="btn btn-sm btn-secondary media-move-down" data-index="${index}" ${index === items.length - 1 ? "disabled" : ""}>↓</button>
          <button type="button" class="btn btn-sm btn-outline media-delete" data-index="${index}">删除</button>
        </div>
      `;

      listEl.appendChild(el);
    });

    bindItemEvents();
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  function bindItemEvents() {
    container.querySelectorAll(".media-section").forEach((sel) => {
      sel.onchange = (e) => {
        const idx = parseInt(e.target.dataset.index);
        items[idx].section = e.target.value;
        save();
      };
    });

    container.querySelectorAll(".media-caption").forEach((inp) => {
      inp.onchange = (e) => {
        const idx = parseInt(e.target.dataset.index);
        items[idx].caption = e.target.value;
        save();
      };
    });

    container.querySelectorAll(".media-delete").forEach((btn) => {
      btn.onclick = (e) => {
        const idx = parseInt(e.target.dataset.index);
        if (confirm("确定删除该媒体？")) {
          items.splice(idx, 1);
          save();
        }
      };
    });

    container.querySelectorAll(".media-move-up").forEach((btn) => {
      btn.onclick = (e) => {
        const idx = parseInt(e.target.dataset.index);
        if (idx > 0) {
          [items[idx], items[idx - 1]] = [items[idx - 1], items[idx]];
          save();
        }
      };
    });

    container.querySelectorAll(".media-move-down").forEach((btn) => {
      btn.onclick = (e) => {
        const idx = parseInt(e.target.dataset.index);
        if (idx < items.length - 1) {
          [items[idx], items[idx + 1]] = [items[idx + 1], items[idx]];
          save();
        }
      };
    });

    // 拖拽排序
    let dragSrcIndex = null;
    container.querySelectorAll(".media-item").forEach((el) => {
      el.addEventListener("dragstart", (e) => {
        dragSrcIndex = parseInt(el.dataset.index);
        el.classList.add("dragging");
      });
      el.addEventListener("dragend", () => {
        el.classList.remove("dragging");
        dragSrcIndex = null;
      });
      el.addEventListener("dragover", (e) => {
        e.preventDefault();
        const target = e.target.closest(".media-item");
        if (!target || target === el) return;
        target.classList.add("drag-over");
      });
      el.addEventListener("dragleave", () => {
        el.classList.remove("drag-over");
      });
      el.addEventListener("drop", (e) => {
        e.preventDefault();
        const target = e.target.closest(".media-item");
        if (!target || dragSrcIndex === null) return;
        const targetIndex = parseInt(target.dataset.index);
        const [moved] = items.splice(dragSrcIndex, 1);
        items.splice(targetIndex, 0, moved);
        save();
      });
    });
  }

  async function uploadFiles(files) {
    const form = container.closest("form");
    const csrfToken = form?.querySelector('input[name="csrf_token"]')?.value;
    if (!csrfToken) {
      alert("缺少 CSRF 令牌，无法上传");
      return;
    }

    const section = sectionSelect?.value || "gallery";

    for (const file of files) {
      const data = new FormData();
      data.append("file", file);
      data.append("csrf_token", csrfToken);

      try {
        const response = await fetch(window.UPLOAD_URL || "/admin/upload", {
          method: "POST",
          body: data,
        });
        const result = await response.json();
        if (!response.ok || !result.url) {
          throw new Error(result.error || "上传失败");
        }
        items.push({
          type: result.type || "image",
          url: result.url,
          section: section,
          caption: "",
        });
      } catch (err) {
        alert(`"${file.name}" 上传失败：${err.message}`);
      }
    }
    save();
  }

  if (uploadInput) {
    uploadInput.addEventListener("change", () => {
      if (uploadInput.files?.length) {
        uploadFiles(Array.from(uploadInput.files));
        uploadInput.value = "";
      }
    });
  }

  render();
}

// --- 学校详情页捐赠状态筛选 ---
function initSchoolDetailStatusFilter() {
  const group = document.querySelector(".donation-filter-hint");
  if (!group) return;

  const tags = group.querySelectorAll("[data-filter]");
  const items = document.querySelectorAll(".donation-item[data-status]");
  if (!tags.length || !items.length) return;

  tags.forEach((tag) => {
    tag.addEventListener("click", () => {
      const filter = tag.dataset.filter;

      tags.forEach((t) => t.classList.remove("filter-active"));
      tag.classList.add("filter-active");

      items.forEach((item) => {
        if (filter === "all" || item.dataset.status === filter) {
          item.style.display = "";
        } else {
          item.style.display = "none";
        }
      });
    });
  });
}

// --- 滚动触发动画 ---
function initScrollAnimations() {
  // Respect reduced motion preference: content stays visible.
  // Also disable scroll-driven reveals for headless/automated browsers
  // so that screenshots, crawlers, and tests see fully rendered content.
  if (
    window.matchMedia("(prefers-reduced-motion: reduce)").matches ||
    navigator.webdriver
  ) {
    return;
  }

  const elements = document.querySelectorAll(".scroll-animate");
  if (elements.length === 0) return;

  // Enable CSS-driven reveal animations
  document.documentElement.classList.add("js-scroll-animations-enabled");

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("animate-in");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: "0px 0px -40px 0px" }
  );

  elements.forEach((el) => {
    // Elements already in viewport on load should be visible immediately
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight && rect.bottom > 0) {
      el.classList.add("animate-in");
    } else {
      observer.observe(el);
    }
  });
}

// --- Tab 切换 ---
function initTabSwitching() {
  document.querySelectorAll("[data-tab-group]").forEach((group) => {
    const tabs = group.querySelectorAll(".detail-tab");

    tabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        tabs.forEach((t) => t.classList.remove("active"));
        tab.classList.add("active");

        const target = tab.dataset.tab;
        const allContents = group.querySelectorAll("[data-tab-content]");

        allContents.forEach((content) => {
          if (content.dataset.tabContent === target) {
            content.style.display = "block";
            content.style.opacity = "1";
          } else {
            content.style.display = "none";
            content.style.opacity = "0";
          }
        });
      });
    });
  });
}

// --- 数字滚动动画 ---
function animateNumber(el, target, duration = 1600) {
  const start = 0;
  const startTime = performance.now();

  function update(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    // ease-out-expo
    const eased = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
    const current = Math.floor(start + (target - start) * eased);
    el.textContent = current.toLocaleString();

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      el.textContent = target.toLocaleString();
    }
  }

  requestAnimationFrame(update);
}

const numberObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const target = parseInt(entry.target.dataset.target);
        if (target && target > 0) {
          animateNumber(entry.target, target);
          numberObserver.unobserve(entry.target);
        }
      }
    });
  },
  { threshold: 0.05, rootMargin: "0px 0px 300px 0px" }
);

document.querySelectorAll("[data-target]").forEach((el) => {
  numberObserver.observe(el);
});
