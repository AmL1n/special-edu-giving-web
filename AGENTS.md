# 特殊学校公益展示网站 —— 项目指南

本文件供 AI 编码代理阅读。当前项目是一个面向特殊教育学校的公益展示平台，采用 Python Flask 构建，主要展示合作学校、受助儿童、捐赠公示与校园动态。

> 重要提示：本项目为大创实践演示项目，当前所有数据（`seed.py` 注入的数据）均为虚拟演示内容，不应作为真实公益机构数据直接使用。

---

## 1. 项目概述

- **项目名称**：特殊学校公益展示网站
- **项目定位**：公益机构前端展示与捐赠透明公示平台
- **技术栈**：
  - 后端：Python 3 + Flask 3.1.1
  - ORM：Flask-SQLAlchemy 3.1.1
  - 数据库迁移：Flask-Migrate 4.1.0
  - 跨域：Flask-CORS 5.0.1
  - 数据库：SQLite（默认）
  - 前端：原生 HTML + CSS + JavaScript，模板引擎 Jinja2
- **代码仓库**：根目录为 Git 仓库，`.venv` 为本地 Python 虚拟环境（已存在，勿提交）
- **入口文件**：`run.py`

### 主要页面

- `/`：首页，展示平台口号、统计数据、合作学校、受助儿童、最新动态与近期捐赠。
- `/school/<int:school_id>`：学校详情页，含学校简介、日常动态、捐赠公示、学生风采四个 Tab。
- `/dashboard`：捐赠透明公示 / 数据大屏，展示所有捐赠记录与汇总数据。
- `/admin/login`：管理后台登录页。
- `/admin/dashboard` 及各 `/admin/<model>/*` 路由：后台数据管理（学校、动态、捐赠、儿童、管理员账号）。

### 数据模型

- `School`：合作特殊教育学校信息。
- `Post`：校园动态 / 捐赠分发图文记录。
- `Donation`：捐赠记录，含捐赠人、物品、数量、金额、接收班级、状态（received / distributing / completed）。
- `Child`：受助儿童信息，含姓名、年龄、简介、语录、兴趣标签。
- `AdminUser`：管理员账号，用于后台登录与数据管理。

---

## 2. 项目结构

```text
特殊学校公益展示网站/
├── app/                          # Flask 应用包
│   ├── __init__.py               # 应用工厂 create_app()，注册扩展与蓝图
│   ├── extensions.py             # db（SQLAlchemy）、migrate（Migrate）实例
│   ├── models.py                 # 数据模型：School / Post / Donation / Child / AdminUser
│   ├── views.py                  # 页面蓝图 main：首页、学校详情、捐赠公示
│   ├── admin/                    # 管理后台蓝图（登录、数据 CRUD）
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates/admin/      # 后台模板（login / dashboard / list_* / form_*）
│   ├── api/
│   │   ├── __init__.py           # 空文件
│   │   └── routes.py             # API 蓝图：/api/stats /api/donations /api/import
│   ├── templates/                # Jinja2 模板
│   │   ├── base.html             # 新顶部固定导航 + 主内容 + 页脚
│   │   ├── index.html            # 首页
│   │   ├── school_detail.html    # 学校详情页
│   │   ├── dashboard.html        # 捐赠公示数据大屏
│   │   ├── partials/             # 可复用片段（如 UI 预览切换浮窗）
│   │   └── ui_variants/          # 测试阶段 UI 风格变体（上线前删除）
│   └── static/                   # 静态资源
│       ├── css/app.css           # 全局样式（温润人文杂志诗学、暖色调、响应式）
│       ├── css/ui_variants/      # 各变体独立样式（上线前随 ui_variants 删除）
│       ├── js/app.js             # 滚动动画、Tab 切换、数字滚动动画、移动端抽屉
│       └── media/ui_variants/    # 变体本地图片与视频素材（上线前删除）
├── config.py                     # Flask 配置类
├── run.py                        # 启动脚本：创建应用、建表、运行开发服务器
├── seed.py                       # 初始化/重置并注入演示数据
├── design-system.md              # 新版设计系统文档（设计方向、Token、组件规范）
├── prototypes/                   # 高保真原型 HTML（首页/学校/捐赠公示）
├── screenshots/                  # 验收截图（桌面 + 移动端）
├── DEPLOY.md                     # 上线准备与部署指南
├── requirements.txt              # Python 依赖
├── tests/                        # 测试目录（当前为 UI 变体冒烟测试）
│   └── test_ui_variants.py
└── instance/
    └── special_school.db         # SQLite 数据库文件（默认位置，git 忽略）
```

---

## 3. 环境准备与运行

### 3.1 创建/激活虚拟环境

项目已存在 `.venv`，可直接激活：

```bash
# Windows (Git Bash)
source .venv/Scripts/activate

# Windows (CMD / PowerShell)
.venv\Scripts\activate
```

若需新建虚拟环境：

```bash
python -m venv .venv
```

### 3.2 安装依赖

```bash
pip install -r requirements.txt
```

`requirements.txt` 内容：

```text
flask==3.1.1
flask-sqlalchemy==3.1.1
flask-migrate==4.1.0
flask-cors==5.0.1
```

### 3.3 初始化数据库

首次运行或需要重置数据库时，执行：

```bash
python seed.py
```

该脚本会：

1. 删除并重新创建所有表（`db.drop_all()` / `db.create_all()`）。
2. 注入 3 所演示学校、12 名儿童、10 条动态、40 条捐赠记录。
3. 创建默认管理员账号（如尚不存在），账号/密码由 `config.Config.ADMIN_USERNAME` / `ADMIN_PASSWORD` 决定。

仅想建表不注入数据时，可在 `run.py` 启动时自动执行 `db.create_all()`，或进入 Flask shell 手动执行。

### 3.4 启动开发服务器

```bash
python run.py
```

默认监听 `0.0.0.0:5000`，Debug 模式开启。浏览器访问：

```text
http://localhost:5000
```

### 3.5 Flask 迁移命令（可选）

项目已集成 Flask-Migrate，但当前未使用 Alembic 版本目录。如需启用：

```bash
flask db init      # 初始化 migrations 目录
flask db migrate   # 生成迁移脚本
flask db upgrade   # 执行迁移
```

当前更常见的操作是直接运行 `seed.py` 重置数据，或依赖 `run.py` 中的 `db.create_all()`。

---

## 4. 代码组织

### 4.1 应用工厂

`app/__init__.py` 中的 `create_app(config_class=Config)` 是统一入口：

- 初始化 Flask 应用并加载 `config.Config`。
- 初始化 `db`、`migrate`、`CORS`。
- 注册蓝图：
  - `main`（`app.views`）：页面路由。
  - `api`（`app.api.routes`）：JSON API。
- 在应用上下文中导入 `models`，确保 SQLAlchemy 注册模型。

### 4.2 蓝图与路由

| 蓝图 | 文件 | 前缀 | 用途 |
|------|------|------|------|
| `main` | `app/views.py` | `/` | HTML 页面 |
| `api` | `app/api/routes.py` | `/api` | JSON 接口 |

### 4.3 主要 API

- `GET /api/stats`：返回学校总数、捐赠总数、累计金额、受助儿童总数。
- `GET /api/donations`：返回最近 50 条捐赠记录。
- `POST /api/import`：批量导入 JSON 数据（支持 schools / posts / donations / children）。

示例导入格式：

```json
{
  "schools": [...],
  "posts": [{"school_id": 1, "title": "...", ...}],
  "donations": [{"school_id": 1, "donor_name": "...", ...}],
  "children": [{"school_id": 1, "name": "...", ...}]
}
```

导入接口未做字段校验与权限控制，仅在可信内网或本地使用。

### 4.4 UI 风格变体（测试阶段）

项目当前包含 5 套参考国际公益平台的 UI 风格变体，用于设计方向比选。通过 `?ui=<variant>` 查询参数切换：

| 变体 | 参考风格 | 首页 | 学校详情页 | 捐赠公示页 |
|------|----------|------|------------|------------|
| `charitywater` | Charity: Water | `/?ui=charitywater` | `/school/1?ui=charitywater` | `/dashboard?ui=charitywater` |
| `justgiving` | JustGiving（萤火特刊） | `/?ui=justgiving` | `/school/1?ui=justgiving` | `/dashboard?ui=justgiving` |
| `donorsee` | DonorSee | `/?ui=donorsee` | `/school/1?ui=donorsee` | `/dashboard?ui=donorsee` |
| `wwf` | WWF 年度报告 | `/?ui=wwf` | `/school/1?ui=wwf` | `/dashboard?ui=wwf` |
| `gofundme` | GoFundMe | `/?ui=gofundme` | `/school/1?ui=gofundme` | `/dashboard?ui=gofundme` |

- 模板：`app/templates/ui_variants/<variant>.html`（首页）、`<variant>_school.html`（学校详情）、`<variant>_dashboard.html`（捐赠公示）。
- 样式：`app/static/css/ui_variants/<variant>.css`。
- 本地媒体：`app/static/media/ui_variants/<variant>/images/` 与 `videos/`，通过 `variant_asset()` 辅助函数引用；缺失时回退到远程占位 URL。
- 媒体下载脚本：`download_media.py` 用于从 Pexels / Mixkit 拉取演示素材（仅供开发预览）。
- 清理方式：上线前删除 `app/templates/ui_variants`、`app/static/css/ui_variants`、`app/static/media/ui_variants`、`download_media.py`，并移除 `app/views.py` 中的变体路由逻辑，保留默认模板。

---

## 5. 配置说明

`config.py`：

```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'special-school-charity-2026'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'special_school.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'admin'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin2026'
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'img')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
```

- `SECRET_KEY`：生产环境务必通过环境变量 `SECRET_KEY` 覆盖默认值。
- `DATABASE_URL`：可通过环境变量切换为 MySQL / PostgreSQL 等生产数据库。
- `ADMIN_USERNAME` / `ADMIN_PASSWORD`：管理员默认账号。生产环境务必通过环境变量覆盖，切勿使用默认值。
- `UPLOAD_FOLDER`：上传图片保存目录，当前由后台 `/admin/upload` 使用（需配合 admin 蓝图）。
- `MAX_CONTENT_LENGTH`：请求体大小限制 16 MB。
- `ALLOWED_EXTENSIONS`：允许上传的图片扩展名白名单。

---

## 6. 设计系统

新版 UI 采用「温润人文 · 高级杂志诗学」方向，强调信任感、透明度与克制的高级审美。详细规范见 `design-system.md`，核心要点如下：

### 6.1 设计方向

- **关键词**：温润、信任、杂志感、诗学留白、手工质感。
- **情绪板**：牛皮纸、陶土、苔藓、手写字、胶卷边缘、自然光线。
- **避免**：高饱和渐变、卡通圆角、浮窗广告、密集表格、默认 Bootstrap 风格。

### 6.2 三层 Token 架构

- **原始层（Primitive）**：`--color-*`、`--font-*`、`--space-*`、`--radius-*`、`--shadow-*`、`--duration-*`。
- **语义层（Semantic）**：`--text-primary`、`--surface-elevated`、`--border-default`。
- **组件层（Component）**：`--btn-primary-bg`、`--card-bg`、`--input-border`。

### 6.3 色彩

| 角色 | 色值 | 用途 |
|------|------|------|
| 主色 | `#A13D2D`（赤陶赭石） | CTA、强调、状态高亮 |
| 辅色 | `#2E4A3E`（深苔绿） | 成功状态、图表、链接悬停 |
| 强调 | `#D4A056`（暖金） | 数据、标签、hover 反馈 |
| 背景 | `#F8F5F2`（暖白） | 页面底色 |
| 表面 | `#FFFFFF` | 卡片、浮层 |
| 文字主色 | `#2B2118` | 标题、正文 |
| 文字次要 | `#6B5E51` | 说明、辅助文案 |

### 6.4 字体

- **标题**：`Noto Serif SC`（思源宋体）
- **正文**：`Noto Sans SC`（思源黑体）
- **数据 / 等宽**：`JetBrains Mono`
- **西文辅助**：`Inter`

### 6.5 组件与交互

- **按钮**：主按钮使用实心主色 + 白色文字；次按钮使用描边；幽灵按钮用于深色背景。
- **卡片**：大圆角（`--radius-xl`）、柔和阴影、1px 边框，hover 时轻微上浮。
- **表格**：轻量表格，斑马纹 + 悬停高亮；移动端自动切换为卡片列表。
- **动画**：滚动 reveal 与数字递增动画默认启用；尊重 `prefers-reduced-motion`，无 JS 时内容默认可见；headless / 自动化环境自动禁用动画保证截图完整。

### 6.6 响应式断点

- 桌面：`>=1024px`
- 平板：`768px - 1023px`
- 手机：`<768px`
- 超小屏：`<=420px`（导航品牌缩短为「公益平台」）

---

## 7. 代码风格与约定

- **语言**：中文是项目注释、模板文案与文档的主要语言，新增代码中的用户可见文案保持中文。
- **编码**：模板与 Python 文件使用 UTF-8；`seed.py` 显式声明 `# -*- coding: utf-8 -*-`。
- **缩进**：Python 代码 4 空格缩进；CSS 2 空格缩进。
- **模型**：每个模型定义 `__tablename__` 与 `to_dict()` 方法，API 序列化直接调用。
- **字段状态常量**：以字符串枚举形式存储，如 `post_type` 为 `daily` / `distribution`，`status` 为 `received` / `distributing` / `completed`。
- **模板继承**：所有页面继承 `base.html`，通过 `{% block content %}` 填充主体。
- **样式变量**：CSS 使用 `:root` 定义设计令牌（颜色、圆角、阴影、字体），保持统一。
- **可访问性约定**：
  - 每个页面有唯一 `<h1>`，标题层级连续不跳级。
  - 图片必须提供有意义的 `alt`；装饰性图标使用 `aria-hidden="true"`。
  - 表单控件必须关联 `<label>` 或 `aria-label`。
  - 提供「跳转到主要内容」链接、`<main>` 地标、`<nav>` 地标。
  - 动画遵循 `prefers-reduced-motion`，无 JS 时内容保持可见。

---

## 8. 测试策略

当前已配置基础冒烟测试：

- `tests/test_ui_variants.py`：使用标准库 `unittest` 验证默认路由与 5 套 UI 变体的首页、学校详情页、捐赠公示页均能返回 HTTP 200，并校验页面引用的 `/static/` 图片在本地真实存在。
- 运行方式：

```bash
python -m unittest discover -s tests -v
```

建议后续继续补充：

- 使用 `pytest` + `pytest-flask` 针对 `/api/stats`、`/api/donations`、`/api/import` 编写接口断言。
- 针对后台 `/admin/*` 路由补充登录与权限测试。

---

## 9. 安全注意事项

- **默认 SECRET_KEY**：当前为硬编码字符串，生产环境必须通过环境变量 `SECRET_KEY` 覆盖默认值。
- **默认管理员凭据**：`ADMIN_USERNAME` / `ADMIN_PASSWORD` 在未设置环境变量时使用默认值，启动时会打印安全警告；生产环境务必通过环境变量修改。
- **SQLite 默认路径**：数据库文件位于 `instance/special_school.db`，需确保不被外部直接下载；生产环境建议切换到 MySQL / PostgreSQL。
- **后台认证**：`/admin/*` 已使用 session 登录保护，但 `/api/import` 目前未做管理员权限校验，应仅在内网或受控环境暴露，或额外增加认证装饰器。
- **无输入校验**：`import_data` 未校验字段类型与必填项，直接接收外部 JSON 写入数据库，生产环境需补充校验与权限检查。
- **演示数据**：`seed.py` 中的学校、儿童、捐赠记录全部为虚构内容，部署前需替换为真实数据或清空。
- **演示图片**：模板与原型中使用的 Unsplash 占位图仅用于开发预览，上线前必须替换为已获得授权的真实素材。
- **跨域**：`CORS(app)` 默认允许所有来源，生产环境应配置白名单（如 `CORS(app, resources={r"/api/*": {"origins": "https://your-domain.com"}})`）。
- **上传功能**：`UPLOAD_FOLDER` 已预留；若启用上传，需校验文件类型、限制大小，重命名文件名并防止目录遍历。

---

## 10. 部署建议

### 10.1 环境变量清单（生产必填）

```bash
export SECRET_KEY="<至少 32 字节的随机字符串>"
export DATABASE_URL="mysql+pymysql://user:pass@host/db"   # 或 PostgreSQL
export ADMIN_USERNAME="<自定义管理员账号>"
export ADMIN_PASSWORD="<强密码>"
```

### 10.2 启动方式

- **开发**：使用 `python run.py`（Debug 模式，不要用于生产）。
- **生产**：使用 Gunicorn / uWSGI 等 WSGI 服务器，并关闭 Debug 模式：

```bash
gunicorn -w 4 -b 127.0.0.1:5000 "app:create_app()"
```

### 10.3 Nginx 配置要点

- 反向代理到 Gunicorn，并设置 `proxy_set_header Host / X-Forwarded-For / X-Forwarded-Proto`。
- 直接由 Nginx 托管 `app/static/`：

```nginx
location /static/ {
    alias /path/to/特殊学校公益展示网站/app/static/;
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

### 10.4 上线前检查清单

- [ ] 修改 `SECRET_KEY`、`ADMIN_USERNAME`、`ADMIN_PASSWORD`。
- [ ] 将 SQLite 替换为 MySQL / PostgreSQL 并备份旧数据。
- [ ] 清空或替换 `seed.py` 中的虚拟学校、儿童、捐赠数据。
- [ ] 删除测试阶段 UI 变体：`app/templates/ui_variants`、`app/static/css/ui_variants`、`app/static/media/ui_variants`、`download_media.py`，并还原 `app/views.py` 默认路由。
- [ ] 替换所有 Unsplash / 占位图片为真实授权素材，并补充 `alt` 文本。
- [ ] 限制 `/api/import` 访问（建议仅允许已登录管理员）。
- [ ] 配置 CORS 白名单，关闭跨域全开。
- [ ] 关闭 Debug 模式，使用 Gunicorn + Nginx（或同类方案）。
- [ ] 启用 HTTPS，配置 HSTS、安全 Cookie。
- [ ] 运行自动化截图 / 可访问性检查，确认桌面与移动端效果。

---

## 11. 常见操作速查

| 操作 | 命令 |
|------|------|
| 安装依赖 | `pip install -r requirements.txt` |
| 重置并填充演示数据 | `python seed.py` |
| 启动开发服务器 | `python run.py` |
| 进入 Flask Shell | `flask shell` |
| 初始化迁移 | `flask db init` |
| 开启 UI 风格预览（默认页显示切换浮窗） | `set UI_PREVIEW=1`（Windows CMD）或 `export UI_PREVIEW=1`（Bash） |
| 预览 Charity: Water 风格 | `http://localhost:5000/?ui=charitywater` |
| 预览 JustGiving / DonorSee / WWF / GoFundMe 风格 | `?ui=justgiving`、`?ui=donorsee`、`?ui=wwf`、`?ui=gofundme` |

---

*本文件基于项目当前实际代码生成，后续若新增测试、部署流程或安全机制，应同步更新本指南。*
