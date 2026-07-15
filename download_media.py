# -*- coding: utf-8 -*-
"""
下载免费图库媒体到本地，供 UI 变体演示使用。
图片：Pexels（Pexels License，无需署名，可免费商用）
视频：Mixkit（Mixkit License）
仅作演示，使用前请遵守各平台许可条款。
"""
import os
import ssl
import time
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POOL_DIR = os.path.join(BASE_DIR, 'app', 'static', 'media', 'ui_variants', '_pool')
VARIANTS = ['charitywater', 'justgiving', 'donorsee', 'wwf', 'gofundme']

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# Pexels 图片 ID 列表（主题：特殊教育、课堂、儿童、学校、包容）
PEXELS_IDS = [
    7395291,   # 宽敞教室
    30703604,  # 安静教室自然光
    34655955,  # 彩色学校走廊
    5428014,   # 小学生课堂
    6936379,   # 专注的学生
    10638224,  # 孩子们一起读书
    6936087,   # 多样化儿童课桌学习
    7105618,   # 孩子指向书中文字
    8617945,   # 孩子们课堂写字
    18870250,  # 女孩在课桌写字
    31864396,  # 孩子玩教育玩具
    35581970,  # 女孩们坐在教室里
    35107613,  # 快乐学校孩子户外举牌
    35107611,  # 快乐学童户外庆祝
    13812360,  # 学童户外游戏
    28389321,  # 文化学校活动传统服饰
    20556421,  # 微笑女孩和男孩坐在字母墙下
    8088232,   # 老师和孩子们
    3231358,   # 印度女学生课堂听讲
    3231359,   # 印度女学生校服听讲
    6936006,   # 包容课堂
    6981085,   # 视障男士使用电脑
    8501770,   # 图书馆艺术创作
    8456130,   # 三个孩子背书包
    20660400,  # 男孩背书包
    4887244,   # 书包里的泰迪熊
    31864391,  # 女孩学习地理印度地图
    35558791,  # 印度农村学校儿童学习
]

# 每个变体对应一段 Mixkit 视频（ID）
MIXKIT_VIDEOS = {
    'charitywater': 5887,    # Young children at school
    'justgiving': 35954,     # Classroom with children raising hands
    'donorsee': 28326,       # Student writing in notebook
    'wwf': 46064,            # Friends studying/working outdoors
    'gofundme': 13298,       # Student hi-fives tutor
}


def fetch(url, timeout=60):
    req = urllib.request.Request(url, headers={
        'User-Agent': USER_AGENT,
        'Accept': '*/*',
    })
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        return resp.read()


def download_pexels_image(photo_id, dest_path, width=1400):
    url = f'https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.jpeg?auto=compress&cs=tinysrgb&w={width}'
    data = fetch(url, timeout=60)
    with open(dest_path, 'wb') as f:
        f.write(data)


def download_mixkit_video(video_id, dest_path):
    url = f'https://assets.mixkit.co/videos/{video_id}/{video_id}-720.mp4'
    data = fetch(url, timeout=180)
    with open(dest_path, 'wb') as f:
        f.write(data)


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def main():
    ensure_dir(POOL_DIR)

    # 下载图片池
    downloaded_images = []
    for idx, photo_id in enumerate(PEXELS_IDS, start=1):
        dest = os.path.join(POOL_DIR, f'pool-{idx:03d}.jpg')
        if os.path.exists(dest):
            print(f'图片已存在，跳过 {photo_id}')
            downloaded_images.append(dest)
            continue
        try:
            print(f'下载图片 {idx}/{len(PEXELS_IDS)}: Pexels {photo_id}')
            download_pexels_image(photo_id, dest)
            downloaded_images.append(dest)
            time.sleep(0.4)
        except Exception as e:
            print(f'  [error] 下载失败 {photo_id}: {e}')

    # 下载视频池
    downloaded_videos = {}
    for variant, vid in MIXKIT_VIDEOS.items():
        dest = os.path.join(POOL_DIR, f'{variant}-video.mp4')
        if os.path.exists(dest):
            print(f'视频已存在，跳过 {variant} ({vid})')
            downloaded_videos[variant] = dest
            continue
        try:
            print(f'下载视频 {variant}: Mixkit {vid}')
            download_mixkit_video(vid, dest)
            downloaded_videos[variant] = dest
            time.sleep(0.5)
        except Exception as e:
            print(f'  [error] 视频下载失败 {vid}: {e}')

    # 复制到各变体目录
    for variant in VARIANTS:
        variant_img_dir = os.path.join(BASE_DIR, 'app', 'static', 'media', 'ui_variants', variant, 'images')
        variant_vid_dir = os.path.join(BASE_DIR, 'app', 'static', 'media', 'ui_variants', variant, 'videos')
        ensure_dir(variant_img_dir)
        ensure_dir(variant_vid_dir)

        mapping = []
        if len(downloaded_images) >= 3:
            mapping.extend([
                ('school-1.jpg', downloaded_images[0]),
                ('school-2.jpg', downloaded_images[1]),
                ('school-3.jpg', downloaded_images[2]),
            ])
        # 儿童肖像 12 张
        for i in range(1, 13):
            src = downloaded_images[(i + 2) % len(downloaded_images)] if len(downloaded_images) > 3 else downloaded_images[i % len(downloaded_images)]
            mapping.append((f'child-{i}.jpg', src))
        # 场景图：剩余图片
        scene_start = 15
        for i in range(scene_start, len(downloaded_images) + 1):
            src = downloaded_images[i - 1]
            mapping.append((f'scene-{i - scene_start + 1}.jpg', src))

        for name, src in mapping:
            dest = os.path.join(variant_img_dir, name)
            if not os.path.exists(dest):
                with open(src, 'rb') as fsrc, open(dest, 'wb') as fdst:
                    fdst.write(fsrc.read())

        if variant in downloaded_videos:
            src = downloaded_videos[variant]
            dest = os.path.join(variant_vid_dir, 'hero-video.mp4')
            if not os.path.exists(dest):
                with open(src, 'rb') as fsrc, open(dest, 'wb') as fdst:
                    fdst.write(fsrc.read())

    print('完成。媒体资源已同步到各变体目录。')


if __name__ == '__main__':
    main()
