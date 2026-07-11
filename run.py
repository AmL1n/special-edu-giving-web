import os
from app import create_app, db
from app.models import School, Post, Donation, Child, AdminUser

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    if not os.environ.get('ADMIN_PASSWORD'):
        print(
            f"[ADMIN] 默认管理员账号: {app.config['ADMIN_USERNAME']} / "
            f"默认密码: {app.config['ADMIN_PASSWORD']}"
        )
        print(
            '[SECURITY] 生产环境请通过环境变量 ADMIN_USERNAME 和 ADMIN_PASSWORD '
            '修改默认凭据，并设置强 SECRET_KEY。'
        )
    app.run(debug=True, host='0.0.0.0', port=5000)

