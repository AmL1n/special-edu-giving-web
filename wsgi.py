# -*- coding: utf-8 -*-
"""生产环境 WSGI 入口。"""
from app import create_app

app = create_app()
