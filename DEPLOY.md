# 特殊学校公益展示网站 · 上线准备与部署指南

> 本文档面向运维与项目负责人。本地开发请继续参考 `AGENTS.md`。

---

## 1. 上线前必须完成的安全配置

| 配置项 | 开发默认值 | 生产要求 |
|--------|-----------|----------|
| `SECRET_KEY` | 硬编码字符串 | 环境变量覆盖，≥32 字节随机字符串 |
| `ADMIN_USERNAME` / `ADMIN_PASSWORD` | `admin` / `admin2026` | 环境变量覆盖为强账号密码 |
| `DATABASE_URL` | SQLite (`instance/special_school.db`) | MySQL / PostgreSQL |
| `CORS` | 允许所有来源 | 配置白名单 |
| `/api/import` | 无鉴权 | 限制为已登录管理员或关闭 |

### 1.1 环境变量示例（Linux / macOS）

```bash
export SECRET_KEY="$(openssl rand -hex 32)"
export DATABASE_URL="mysql+pymysql://user:password@host/special_school"
export ADMIN_USERNAME="your_admin"
export ADMIN_PASSWORD="$(openssl rand -base64 24)"
```

### 1.2 环境变量示例（Windows PowerShell）

```powershell
$env:SECRET_KEY = -join ((1..32) | ForEach-Object { Get-Random -Maximum 16 | ForEach-Object { "{0:X}" -f $_ } })
$env:DATABASE_URL = "mysql+pymysql://user:password@host/special_school"
$env:ADMIN_USERNAME = "your_admin"
$env:ADMIN_PASSWORD = -join ((1..24) | ForEach-Object { [char](Get-Random -Minimum 33 -Maximum 126) })
```

---

## 2. 生产部署步骤

### 2.1 准备服务器

- 安装 Python 3.11+、Nginx、MySQL / PostgreSQL。
- 克隆代码到 `/var/www/special-school`（路径可自定义）。
- 创建并激活虚拟环境：

```bash
cd /var/www/special-school
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# 生产环境额外安装 gunicorn
pip install gunicorn
```

### 2.2 初始化生产数据库

```bash
flask db init      # 若首次使用迁移
flask db migrate -m "init"
flask db upgrade
```

> 不建议在生产环境使用 `python seed.py`，因为会 `drop_all()` 清空数据。

### 2.3 启动 Gunicorn

```bash
source .venv/bin/activate
export SECRET_KEY="..."
export DATABASE_URL="..."
export ADMIN_USERNAME="..."
export ADMIN_PASSWORD="..."

gunicorn -w 4 -b 127.0.0.1:5000 "app:create_app()"
```

推荐使用 systemd 或 supervisor 守护进程：

```ini
# /etc/systemd/system/special-school.service
[Unit]
Description=Special School Charity Website
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/special-school
Environment="SECRET_KEY=..."
Environment="DATABASE_URL=..."
Environment="ADMIN_USERNAME=..."
Environment="ADMIN_PASSWORD=..."
ExecStart=/var/www/special-school/.venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 "app:create_app()"
Restart=always

[Install]
WantedBy=multi-user.target
```

### 2.4 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location /static/ {
        alias /var/www/special-school/app/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 3. 数据与素材替换

- 在后台 `/admin/schools`、`/admin/children`、`/admin/donations`、`/admin/posts` 中替换虚拟数据。
- 上传图片建议保存到 `app/static/img/` 或对象存储（如 OSS / S3），并在模板中使用对应 URL。
- 所有 Unsplash 占位图必须替换为真实授权照片，且为儿童肖像补充监护人授权与隐私脱敏处理。

---

## 4. 上线前检查清单

- [ ] 环境变量 `SECRET_KEY`、`DATABASE_URL`、`ADMIN_USERNAME`、`ADMIN_PASSWORD` 已设置。
- [ ] Debug 模式已关闭（`FLASK_DEBUG=0` 或未设置）。
- [ ] 使用 Gunicorn + Nginx / 同类生产服务器。
- [ ] 已启用 HTTPS 与 HSTS。
- [ ] 数据库已迁移，无 `drop_all` 操作。
- [ ] `seed.py` 虚拟数据已清空或替换。
- [ ] 所有占位图片已替换并补充 `alt` 文本。
- [ ] `/api/import` 已做鉴权或已关闭公网访问。
- [ ] CORS 已配置白名单。
- [ ] 已在 1280px+ 与 390px 宽度下截图验收。
- [ ] 已通过键盘 Tab 操作与屏幕阅读器（或浏览器可访问性检查）验证主要流程。
- [ ] 测试阶段 UI 变体已清理：删除 `app/templates/ui_variants/`、`app/static/css/ui_variants/`、`app/templates/partials/_ui_switcher.html`，并确保未设置 `UI_PREVIEW`。

---

## 5. 回滚与备份

- 数据库：配置每日自动备份（`mysqldump` / `pg_dump`）。
- 静态文件：上传前保留旧版本，必要时通过对象存储版本控制回滚。
- 代码：上线前打 Git tag，出现问题可 `git checkout <tag>` 回滚。

---

## 6. 联系我们 / 维护

- 项目入口：`run.py`
- 应用工厂：`app/__init__.py`
- 设计系统：`design-system.md`
- 后台路由：`app/admin/routes.py`
- 数据模型：`app/models.py`
