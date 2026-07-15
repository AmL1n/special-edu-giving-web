import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'special-school-charity-2026'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'special_school.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 管理员默认账号（生产环境务必通过环境变量覆盖）
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'admin'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin2026'

    # 上传相关配置
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'img')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'webm', 'mov'}

    # UI 预览开关：仅在测试阶段开启，方便对比多套 UI 风格
    # 设置为 "1"/"true"/"yes" 时，页面右下角显示 UI 切换浮窗
    UI_PREVIEW = os.environ.get('UI_PREVIEW', '').lower() in ('1', 'true', 'yes')


# 安全警告：若使用默认密钥或默认管理员密码，启动时提醒开发者
if not os.environ.get('SECRET_KEY'):
    print(
        '[SECURITY WARNING] 未设置环境变量 SECRET_KEY，当前使用默认密钥。'
        '生产环境请务必通过环境变量设置强密钥！',
        flush=True,
    )

if not os.environ.get('ADMIN_PASSWORD'):
    print(
        '[SECURITY WARNING] 未设置环境变量 ADMIN_PASSWORD，当前使用默认管理员密码。'
        '生产环境请务必修改默认管理员密码！',
        flush=True,
    )
