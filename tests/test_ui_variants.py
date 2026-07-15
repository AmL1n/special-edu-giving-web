# -*- coding: utf-8 -*-
"""UI 变体冒烟测试。

验证 5 套首页、学校详情页、捐赠公示页均能正常渲染，且页面中引用的
本地图片静态文件真实存在。
"""
import os
import unittest
from html.parser import HTMLParser

from app import create_app
from app.extensions import db


class ImgSrcParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.srcs = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            attrs = dict(attrs)
            src = attrs.get("src", "").strip()
            if src:
                self.srcs.append(src)


class UiVariantSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        cls.app_context.pop()

    def _local_path_for_static(self, src):
        if src.startswith("/static/"):
            rel = src[len("/static/"):]
            return os.path.join(self.app.static_folder, *rel.split("/"))
        return None

    def test_default_home(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)

    def test_default_school_detail(self):
        resp = self.client.get("/school/1")
        self.assertEqual(resp.status_code, 200)

    def test_default_dashboard(self):
        resp = self.client.get("/dashboard")
        self.assertEqual(resp.status_code, 200)

    def test_all_variant_pages_render(self):
        variants = ("charitywater", "justgiving", "donorsee", "wwf", "gofundme")
        for variant in variants:
            with self.subTest(variant=variant, page="index"):
                resp = self.client.get(f"/?ui={variant}")
                self.assertEqual(resp.status_code, 200)
            with self.subTest(variant=variant, page="school"):
                resp = self.client.get(f"/school/1?ui={variant}")
                self.assertEqual(resp.status_code, 200)
            with self.subTest(variant=variant, page="dashboard"):
                resp = self.client.get(f"/dashboard?ui={variant}")
                self.assertEqual(resp.status_code, 200)

    def test_variant_images_are_local_or_reachable(self):
        """页面引用的 /static/ 图片必须在 static 目录中存在（媒体素材已下载时）。"""
        media_root = os.path.join(self.app.static_folder, "media", "ui_variants")
        if not os.path.isdir(media_root):
            self.skipTest(f"本地媒体目录不存在：{media_root}，请先运行 python download_media.py 下载素材")
        variants = ("charitywater", "justgiving", "donorsee", "wwf", "gofundme")
        missing = []
        for variant in variants:
            for path in (f"/?ui={variant}", "/school/1?ui={variant}", "/dashboard?ui={variant}"):
                resp = self.client.get(path)
                html = resp.get_data(as_text=True)
                parser = ImgSrcParser()
                parser.feed(html)
                for src in parser.srcs:
                    if src.startswith("/static/"):
                        local = self._local_path_for_static(src)
                        if local and not os.path.exists(local):
                            missing.append((path, src, local))
        if missing:
            self.fail("以下图片文件缺失：\n" + "\n".join(f"  {p} -> {s}" for p, s, _ in missing))


if __name__ == "__main__":
    unittest.main()
