# 特殊学校公益展示网站 · 设计系统

> 方向：温润人文 · 高级杂志诗学  
> 版本：v1.0  
> 适用范围：公众端首页、学校详情、捐赠公示、管理后台登录与数据管理界面

---

## 一、品牌核心

### 1.1 品牌关键词
温暖 · 透明 · 尊严 · 希望 · 专业 · 可信赖

### 1.2 视觉性格
像一本关于爱与成长的公益杂志：克制留白、高级灰调、纸张触感、人文衬线。避免「塑料感」「过度圆角」「紫蓝渐变」等 AI 默认审美。

### 1.3 内容伦理
- 儿童与学校故事以「尊严优先」呈现，避免悲情化或过度暴露隐私。
- 数据真实、来源清晰，捐赠公示强调「可追踪的善意」。
- 图片使用真实授权照片，上线前替换所有 Unsplash / dicebear 占位图。

---

## 二、色彩系统

### 2.1 Primitive Colors

```css
/* 中性色阶 */
--color-ink-900: #1C1A18;
--color-ink-800: #2E2C29;
--color-ink-700: #4A4743;
--color-ink-600: #6B6560;
--color-ink-500: #8D867F;
--color-ink-400: #A09990;
--color-ink-300: #C4BEB6;
--color-ink-200: #DDD7CF;
--color-ink-100: #EDE8E0;
--color-ink-50:  #F7F5F0;
--color-paper:   #FAF8F5;

/* 主色：赤陶赭石 */
--color-terracotta-900: #5C2419;
--color-terracotta-800: #7A2F21;
--color-terracotta-700: #983B2A;
--color-terracotta-600: #A13D2D;  /* 主色 */
--color-terracotta-500: #B85A49;
--color-terracotta-400: #CD7D6E;
--color-terracotta-300: #E2A99E;
--color-terracotta-200: #F0D0CA;
--color-terracotta-100: #F9EBE8;
--color-terracotta-50:  #FDF7F6;

/* 辅色：深苔绿 */
--color-moss-900: #1A2E26;
--color-moss-800: #243F34;
--color-moss-700: #2E4A3E;  /* 辅色 */
--color-moss-600: #3D6353;
--color-moss-500: #527A68;
--color-moss-400: #7A9E8D;
--color-moss-300: #A8C4B8;
--color-moss-200: #D2E2D9;
--color-moss-100: #EAF3EE;
--color-moss-50:  #F5F9F7;

/* 强调：暖金 */
--color-gold-600: #A67C34;
--color-gold-500: #C4943F;
--color-gold-400: #D4A056;  /* 强调 */
--color-gold-300: #E3BE84;
--color-gold-200: #F0DAB2;
--color-gold-100: #F9F0E0;

/* 功能色 */
--color-success: #3D6353;
--color-success-bg: #EAF3EE;
--color-warning: #C4943F;
--color-warning-bg: #F9F0E0;
--color-error: #B85A49;
--color-error-bg: #F9EBE8;
--color-info: #527A68;
--color-info-bg: #F5F9F7;
```

### 2.2 Semantic Colors

```css
/* 背景 */
--bg-page: var(--color-paper);
--bg-section: var(--color-ink-50);
--bg-card: #FFFFFF;
--bg-hero: var(--color-paper);
--bg-footer: var(--color-ink-900);

/* 文字 */
--text-primary: var(--color-ink-900);
--text-secondary: var(--color-ink-600);
--text-muted: var(--color-ink-400);
--text-inverse: #FFFFFF;
--text-link: var(--color-terracotta-700);
--text-link-hover: var(--color-terracotta-900);

/* 主色语义 */
--color-primary: var(--color-terracotta-600);
--color-primary-hover: var(--color-terracotta-700);
--color-primary-active: var(--color-terracotta-800);
--color-primary-bg: var(--color-terracotta-100);
--color-primary-subtle: rgba(161, 61, 45, 0.08);

/* 辅色语义 */
--color-secondary: var(--color-moss-700);
--color-secondary-hover: var(--color-moss-800);
--color-secondary-bg: var(--color-moss-100);
--color-secondary-subtle: rgba(46, 74, 62, 0.08);

/* 强调语义 */
--color-accent: var(--color-gold-400);
--color-accent-bg: var(--color-gold-100);

/* 边框 */
--border-default: var(--color-ink-200);
--border-light: var(--color-ink-100);
--border-inverse: rgba(255, 255, 255, 0.12);
```

### 2.3 Color Usage Rules
- 页面背景使用 `--bg-page`（米白纸感），区块交替使用 `--bg-section` 制造呼吸感。
- 主按钮使用 `--color-primary`，hover 使用 `--color-primary-hover`。
- 成功/完成状态使用 `--color-success`（深苔绿），进行中/警告使用 `--color-accent`（暖金），错误/待处理使用 `--color-error`（赭石）。
- 正文必须保证对比度 ≥ 4.5:1，标题 ≥ 3:1。

---

## 三、字体系统

### 3.1 Font Families

```css
/* 中文标题：思源宋体，人文厚重 */
--font-display: "Noto Serif SC", "Source Han Serif SC", "STSong", Georgia, serif;

/* 中文正文：思源黑体，清晰可读 */
--font-body: "Noto Sans SC", -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;

/* 英文/数据：Inter + JetBrains Mono */
--font-sans: "Inter", "Noto Sans SC", sans-serif;
--font-mono: "JetBrains Mono", "SF Mono", Consolas, monospace;
```

### 3.2 Type Scale

| Token | Size | Line Height | Weight | Usage |
|-------|------|-------------|--------|-------|
| --text-hero | clamp(2.75rem, 5vw, 4.5rem) | 1.15 | 600 | Hero 主标题 |
| --text-h1 | clamp(2rem, 4vw, 3.5rem) | 1.2 | 600 | 页面标题 |
| --text-h2 | clamp(1.5rem, 3vw, 2.5rem) | 1.25 | 600 | 区块标题 |
| --text-h3 | clamp(1.25rem, 2vw, 1.75rem) | 1.3 | 600 | 卡片标题 |
| --text-h4 | 1.125rem | 1.4 | 600 | 小标题 |
| --text-body | 1rem (16px) | 1.75 | 400 | 正文 |
| --text-body-lg | 1.125rem | 1.8 | 400 | 引导段落 |
| --text-body-sm | 0.875rem | 1.6 | 400 | 辅助说明 |
| --text-caption | 0.75rem | 1.5 | 500 | 标签、 eyebrow |
| --text-data | 2rem | 1.1 | 700 | 统计数字 |

### 3.3 Typography Rules
- 标题使用 `--font-display`，正文使用 `--font-body`。
- 数字、金额、状态使用 `--font-mono`，等宽防止布局抖动。
- 中文段落行宽控制在 25-35 字，避免过长。
- 标题 letter-spacing: -0.02em； eyebrow letter-spacing: 0.12em。

---

## 四、间距系统

### 4.1 Spacing Scale (4px base)

```css
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 20px;
--space-6: 24px;
--space-8: 32px;
--space-10: 40px;
--space-12: 48px;
--space-16: 64px;
--space-20: 80px;
--space-24: 96px;
--space-32: 128px;
```

### 4.2 Section Spacing
- 页面区块上下间距：桌面 `--space-24` (96px)，移动端 `--space-16` (64px)。
- Hero 区域：桌面 padding-top 120px，padding-bottom 80px。
- Footer 上方 margin-top: `--space-24`。

### 4.3 Container
```css
--container-max: 1200px;
--container-padding: 24px;  /* 移动端 */
--container-padding-md: 48px;  /* 平板 */
--container-padding-lg: 64px;  /* 桌面 */
```

---

## 五、圆角与阴影

### 5.1 Radius
```css
--radius-sm: 8px;    /* 小标签、输入框 */
--radius-md: 12px;   /* 卡片 */
--radius-lg: 16px;   /* 大卡片、图片 */
--radius-xl: 24px;   /* Hero 图片、modal */
--radius-full: 9999px; /* 按钮、胶囊标签 */
```

### 5.2 Shadow
```css
--shadow-xs: 0 1px 2px rgba(28, 26, 24, 0.04);
--shadow-sm: 0 2px 8px rgba(28, 26, 24, 0.06);
--shadow-md: 0 8px 24px rgba(28, 26, 24, 0.08);
--shadow-lg: 0 16px 48px rgba(28, 26, 24, 0.10);
```
- 默认卡片无阴影或仅 `--shadow-xs`；hover 时过渡到 `--shadow-md`。
- 悬浮统计卡、modal 使用 `--shadow-lg`。

---

## 六、组件规范

### 6.1 Button

**Primary Button**
```css
background: var(--color-primary);
color: #FFFFFF;
border-radius: var(--radius-full);
padding: 14px 28px;
font-weight: 600;
font-size: 0.9375rem;
transition: all 0.2s ease-out;
```
- Hover: background `--color-primary-hover`, translateY(-2px), shadow-md.
- Active: scale(0.98), background `--color-primary-active`.
- Disabled: opacity 0.5, cursor not-allowed.

**Secondary Button**
```css
background: var(--color-ink-100);
color: var(--text-primary);
```
- Hover: background `--color-ink-200`.

**Outline Button**
```css
background: transparent;
border: 1.5px solid var(--border-default);
color: var(--text-primary);
```
- Hover: border-color `--color-primary`, color `--color-primary`.

### 6.2 Card
```css
background: var(--bg-card);
border-radius: var(--radius-lg);
border: 1px solid var(--border-light);
overflow: hidden;
transition: transform 0.25s ease-out, box-shadow 0.25s ease-out;
```
- Hover: translateY(-4px), shadow-md.
- 图片卡片 hover 时图片 scale(1.04)，容器 overflow hidden。

### 6.3 Tag / Badge
```css
/* Default tag */
background: var(--color-primary-subtle);
color: var(--color-primary);
padding: 6px 12px;
border-radius: var(--radius-full);
font-size: 0.8125rem;
font-weight: 500;

/* Status badges */
.status-received { background: var(--color-secondary-bg); color: var(--color-secondary); }
.status-distributing { background: var(--color-accent-bg); color: var(--color-gold-600); }
.status-completed { background: var(--color-success-bg); color: var(--color-success); }
```

### 6.4 Form Inputs
```css
background: var(--bg-card);
border: 1px solid var(--border-default);
border-radius: var(--radius-sm);
padding: 12px 16px;
font-size: 1rem;
color: var(--text-primary);
transition: border-color 0.2s, box-shadow 0.2s;
```
- Focus: border-color `--color-primary`, box-shadow `0 0 0 3px var(--color-primary-subtle)`.
- Label: font-size 0.875rem, font-weight 600, color `--text-secondary`, margin-bottom 8px.
- Error: border-color `--color-error`, 错误文本 `--color-error`.

### 6.5 Navigation
- 桌面：顶部固定导航，高度 72px，背景 `--bg-page` 带底部 1px border。
- 移动端：顶部 56px 汉堡菜单，抽屉从右侧滑入。
- 当前页面导航项：color `--color-primary`，底部 2px indicator。

### 6.6 Table (Admin)
```css
background: var(--bg-card);
border: 1px solid var(--border-light);
border-radius: var(--radius-lg);
overflow: hidden;
```
- 表头：background `--bg-section`, color `--text-secondary`, font-size 0.75rem, uppercase.
- 行 hover：background `--color-ink-50`.
- 操作按钮：小号 outline button。

---

## 七、动效规范

### 7.1 Duration & Easing
```css
--ease-out: cubic-bezier(0.16, 1, 0.3, 1);
--ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
--duration-fast: 150ms;
--duration-normal: 250ms;
--duration-slow: 400ms;
```

### 7.2 Motion Rules
- 微交互（hover、focus）：`--duration-fast` `--ease-out`。
- 卡片悬浮：`--duration-normal`，transform only（不触发重排）。
- 滚动 reveal：`--duration-slow`，opacity + translateY(24px → 0)。
- **必须**支持 `prefers-reduced-motion: reduce`：所有动画直接关闭或变为 opacity-only。

### 7.3 Forbidden Animations
- 禁止滚动劫持、视差、无限循环装饰动画。
- 禁止 animating width/height/top/left（使用 transform）。
- 禁止超过 500ms 的入场动画。

---

## 八、布局与栅格

### 8.1 Grid
- 默认 12 列栅格，gap 24px（桌面），16px（移动）。
- 内容区最大宽度 1200px，居中对齐。

### 8.2 Responsive Breakpoints
```css
--bp-sm: 375px;
--bp-md: 768px;
--bp-lg: 1024px;
--bp-xl: 1440px;
```

### 8.3 Mobile-First Patterns
- 所有区块默认单列，@media (min-width: 768px) 起扩展多列。
- 触控目标最小 48×48px，按钮/输入框高度 ≥ 44px。
- 图片使用 `aspect-ratio` 防止布局偏移。

---

## 九、可访问性规范

### 9.1 Required
- 颜色对比度：正文 ≥ 4.5:1，大文本 ≥ 3:1。
- 所有图片有意义的 `alt` 文本；装饰性图片 `alt=""`。
- 表单 label 与 input 通过 `for`/`id` 绑定。
- 键盘导航可见 focus ring（2px `--color-primary` outline-offset 2px）。
- 标题层级 h1→h6 连续不跳跃。
- 支持 `prefers-reduced-motion`。

### 9.2 Recommended
- 为数据图表提供文本摘要或 table 替代。
- 为视频提供字幕/文稿。
- 使用 `aria-current="page"` 标记当前导航项。

---

## 十、反模式清单（AI Slop 规避）

- ❌ 紫色/蓝紫渐变背景
- ❌ Emoji 作为图标
- ❌ 圆角卡片 + 左侧彩色 border accent 的泛滥
- ❌ 每个标题都配无意义图标
- ❌ SVG 手绘人物/场景替代真实照片
- ❌ 编造统计数据装饰
- ❌ 过度悬浮/阴影造成「塑料感」
- ✅ 克制用色、真实影像、有意义动效、留白呼吸

---

## 十一、页面特殊规范

### 11.1 首页 `/`
- Hero 区域：左侧文字占 5/12，右侧图片占 7/12。
- 统计条：4 列等分，数字使用 `--font-mono`。
- 儿童风采：最多展示 3 张精选故事卡，避免隐私过度曝光。
- 近期捐赠：横向滚动或 5 条列表，状态 badge 清晰。

### 11.2 学校详情 `/school/<id>`
- Hero：全宽 480px 高度头图，渐变遮罩自下而上。
- Tab 按钮：胶囊切换，active 状态白底阴影。
- 侧边栏：sticky top 96px，含学校关键数据与 CTA。

### 11.3 捐赠公示 `/dashboard`
- 顶部 4 个 KPI 卡片，等宽数字。
- 筛选器：学校标签 + 状态下拉 + 排序 + 搜索，移动端折叠为垂直堆叠。
- 捐赠列表：桌面表格，移动端卡片；状态使用 badge。

### 11.4 管理后台 `/admin/*`
- 登录页：极简居中卡片，无侧导航干扰。
- 数据概览：4 个 KPI 卡片 + 最近操作提示。
- 列表/表单：专业化信息密度，表格支持横向滚动。

---

*本设计系统为 Phase 1 输出，后续原型与模板实现须严格引用上述 token，禁止硬编码色值。*
