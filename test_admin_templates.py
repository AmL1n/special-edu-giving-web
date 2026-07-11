# -*- coding: utf-8 -*-
"""管理后台模板路由冒烟测试"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import AdminUser

app = create_app()
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False


def _extract_csrf(text):
    m = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', text)
    return m.group(1) if m else None


def main():
    with app.test_client() as client:
        results = []

        # 登录页 GET
        rv = client.get('/admin/login')
        results.append(('GET /admin/login', rv.status_code))
        csrf_token = _extract_csrf(rv.data.decode('utf-8'))

        # 登录页 POST（真实登录）
        if csrf_token:
            rv_login = client.post(
                '/admin/login',
                data={'csrf_token': csrf_token, 'username': 'admin', 'password': 'admin2026'},
                follow_redirects=True,
            )
            results.append(('POST /admin/login', rv_login.status_code))

        protected_gets = [
            '/admin/dashboard',
            '/admin/schools',
            '/admin/posts',
            '/admin/donations',
            '/admin/children',
            '/admin/schools/new',
            '/admin/posts/new',
            '/admin/donations/new',
            '/admin/children/new',
            '/admin/schools/1/edit',
            '/admin/posts/1/edit',
            '/admin/donations/1/edit',
            '/admin/children/1/edit',
        ]

        for path in protected_gets:
            rv = client.get(path)
            results.append((f'GET {path}', rv.status_code))

    failed = [(p, c) for p, c in results if c != 200]
    if failed:
        print('FAILED ROUTES:')
        for path, code in failed:
            print(f'  {path} -> {code}')
        sys.exit(1)

    print('ALL ROUTES OK')
    for path, code in results:
        print(f'  {path} -> {code}')


if __name__ == '__main__':
    main()
