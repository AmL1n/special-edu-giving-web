# -*- coding: utf-8 -*-
"""管理员后台蓝图

提供基于 Flask session 的登录/登出、数据 CRUD 管理以及媒体上传功能。
所有修改型 POST 路由（除登录外）均要求 session 中存有 csrf_token，
并与请求表单中的 csrf_token 字段比对。
"""
import functools
import json
import os
import secrets
import uuid
from datetime import datetime

from flask import (
    Blueprint, abort, current_app, flash, g, jsonify, redirect,
    render_template, request, session, url_for,
)
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models import AdminUser, Child, Donation, Post, School
from config import Config

admin = Blueprint('admin', __name__, url_prefix='/admin')


# --------------------------------------------------------------------------- #
# 辅助函数
# --------------------------------------------------------------------------- #
def _ensure_default_admin():
    """如果管理员表为空，使用当前配置创建默认管理员账号。"""
    try:
        if AdminUser.query.count() == 0:
            user = AdminUser(username=Config.ADMIN_USERNAME)
            user.set_password(Config.ADMIN_PASSWORD)
            db.session.add(user)
            db.session.commit()
            current_app.logger.warning(
                '已使用默认凭据创建管理员账号：%s', Config.ADMIN_USERNAME
            )
    except Exception:  # 例如数据库表尚未创建时忽略
        db.session.rollback()


@admin.context_processor
def inject_csrf_token():
    """向所有 admin 模板注入 csrf_token。"""
    return {'csrf_token': session.get('csrf_token', '')}


def _valid_csrf():
    """校验请求表单中的 CSRF 令牌是否与 session 中一致。"""
    session_token = session.get('csrf_token')
    form_token = request.form.get('csrf_token')
    return bool(session_token and form_token and session_token == form_token)


def login_required(view):
    """要求管理员已登录。"""
    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        if session.get('admin_id') is None:
            return redirect(url_for('admin.login', next=request.url))
        return view(*args, **kwargs)
    return wrapped


def csrf_protected(view):
    """仅对 POST 请求进行 CSRF 校验的装饰器。"""
    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        if request.method == 'POST' and not _valid_csrf():
            abort(403)
        return view(*args, **kwargs)
    return wrapped


def _int_or_none(value):
    value = (value or '').strip()
    return int(value) if value else None


def _float_or_none(value):
    value = (value or '').strip()
    return float(value) if value else None


def _parse_date(value):
    value = (value or '').strip()
    return datetime.strptime(value, '%Y-%m-%d') if value else None


def _parse_media_json(value):
    """解析前端提交的媒体 JSON，返回标准格式的媒体列表。"""
    try:
        media = json.loads(value or '[]') or []
    except Exception:
        return []
    cleaned = []
    for m in media:
        if not isinstance(m, dict) or not m.get('url'):
            continue
        item = {
            'type': m.get('type', 'image'),
            'url': m.get('url', '').strip(),
            'section': m.get('section', 'gallery').strip(),
            'caption': m.get('caption', '').strip(),
        }
        if item['url']:
            cleaned.append(item)
    return cleaned


# --------------------------------------------------------------------------- #
# 上下文处理
# --------------------------------------------------------------------------- #
@admin.before_request
def load_admin():
    """将当前登录管理员注入 g，方便模板判断登录状态。"""
    admin_id = session.get('admin_id')
    g.admin = AdminUser.query.get(admin_id) if admin_id else None
    g.admin_logged_in = g.admin is not None


# --------------------------------------------------------------------------- #
# 登录 / 登出
# --------------------------------------------------------------------------- #
@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        _ensure_default_admin()

        # 登录表单同样要求 CSRF，但不必预先存在；GET 时会生成并写入 session
        session_token = session.get('csrf_token')
        form_token = request.form.get('csrf_token')
        if not session_token or not form_token or session_token != form_token:
            abort(403)

        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = AdminUser.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['admin_id'] = user.id
            session.permanent = True
            next_url = request.args.get('next')
            if next_url and next_url.startswith('/') and not next_url.startswith('//'):
                return redirect(next_url)
            return redirect(url_for('admin.dashboard'))

        flash('用户名或密码错误', 'error')
        return redirect(url_for('admin.login'))

    # GET：生成 CSRF 令牌供登录表单使用
    session['csrf_token'] = secrets.token_urlsafe(24)
    return render_template('admin/login.html')


@admin.route('/logout', methods=['POST'])
@login_required
@csrf_protected
def logout():
    session.pop('admin_id', None)
    session.pop('csrf_token', None)
    return redirect(url_for('admin.login'))


# --------------------------------------------------------------------------- #
# 后台概览
# --------------------------------------------------------------------------- #
@admin.route('/dashboard')
@login_required
def dashboard():
    counts = {
        'schools': School.query.count(),
        'posts': Post.query.count(),
        'donations': Donation.query.count(),
        'children': Child.query.count(),
    }
    return render_template(
        'admin/dashboard.html',
        school_count=counts['schools'],
        post_count=counts['posts'],
        donation_count=counts['donations'],
        child_count=counts['children'],
    )


# --------------------------------------------------------------------------- #
# 学校管理
# --------------------------------------------------------------------------- #
@admin.route('/schools')
@login_required
def list_schools():
    schools = School.query.order_by(School.created_at.desc()).all()
    return render_template('admin/list_schools.html', schools=schools)


@admin.route('/schools/new', methods=['GET', 'POST'])
@login_required
@csrf_protected
def new_school():
    if request.method == 'POST':
        school = School(
            name=request.form.get('name', '').strip(),
            description=request.form.get('description', '').strip(),
            location=request.form.get('location', '').strip(),
            cover_image=request.form.get('cover_image', '').strip(),
            media_json=json.dumps(_parse_media_json(request.form.get('media_json'))),
            student_count=_int_or_none(request.form.get('student_count')),
            teacher_count=_int_or_none(request.form.get('teacher_count')),
            founded_year=_int_or_none(request.form.get('founded_year')),
            contact_phone=request.form.get('contact_phone', '').strip(),
        )
        db.session.add(school)
        db.session.commit()
        flash('学校已创建', 'success')
        return redirect(url_for('admin.list_schools'))
    return render_template('admin/form_school.html', item=None)


@admin.route('/schools/<int:school_id>/edit', methods=['GET', 'POST'])
@login_required
@csrf_protected
def edit_school(school_id):
    school = School.query.get_or_404(school_id)
    if request.method == 'POST':
        school.name = request.form.get('name', '').strip()
        school.description = request.form.get('description', '').strip()
        school.location = request.form.get('location', '').strip()
        school.cover_image = request.form.get('cover_image', '').strip()
        school.media_json = json.dumps(_parse_media_json(request.form.get('media_json')))
        school.student_count = _int_or_none(request.form.get('student_count'))
        school.teacher_count = _int_or_none(request.form.get('teacher_count'))
        school.founded_year = _int_or_none(request.form.get('founded_year'))
        school.contact_phone = request.form.get('contact_phone', '').strip()
        db.session.commit()
        flash('学校信息已更新', 'success')
        return redirect(url_for('admin.list_schools'))
    return render_template('admin/form_school.html', item=school)


@admin.route('/schools/<int:school_id>/delete', methods=['POST'])
@login_required
@csrf_protected
def delete_school(school_id):
    school = School.query.get_or_404(school_id)
    db.session.delete(school)
    db.session.commit()
    flash('学校已删除', 'success')
    return redirect(url_for('admin.list_schools'))


# --------------------------------------------------------------------------- #
# 动态管理
# --------------------------------------------------------------------------- #
@admin.route('/posts')
@login_required
def list_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    schools = School.query.order_by(School.name).all()
    return render_template('admin/list_posts.html', posts=posts, schools=schools)


@admin.route('/posts/new', methods=['GET', 'POST'])
@login_required
@csrf_protected
def new_post():
    schools = School.query.order_by(School.name).all()
    if request.method == 'POST':
        post = Post(
            school_id=_int_or_none(request.form.get('school_id')),
            title=request.form.get('title', '').strip(),
            content=request.form.get('content', '').strip(),
            image_url=request.form.get('image_url', '').strip(),
            media_json=json.dumps(_parse_media_json(request.form.get('media_json'))),
            post_type=request.form.get('post_type', 'daily').strip(),
        )
        db.session.add(post)
        db.session.commit()
        flash('动态已创建', 'success')
        return redirect(url_for('admin.list_posts'))
    return render_template('admin/form_post.html', item=None, schools=schools)


@admin.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
@csrf_protected
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    schools = School.query.order_by(School.name).all()
    if request.method == 'POST':
        post.school_id = _int_or_none(request.form.get('school_id'))
        post.title = request.form.get('title', '').strip()
        post.content = request.form.get('content', '').strip()
        post.image_url = request.form.get('image_url', '').strip()
        post.media_json = json.dumps(_parse_media_json(request.form.get('media_json')))
        post.post_type = request.form.get('post_type', 'daily').strip()
        db.session.commit()
        flash('动态已更新', 'success')
        return redirect(url_for('admin.list_posts'))
    return render_template('admin/form_post.html', item=post, schools=schools)


@admin.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
@csrf_protected
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('动态已删除', 'success')
    return redirect(url_for('admin.list_posts'))


# --------------------------------------------------------------------------- #
# 捐赠管理
# --------------------------------------------------------------------------- #
@admin.route('/donations')
@login_required
def list_donations():
    donations = Donation.query.order_by(Donation.created_at.desc()).all()
    schools = School.query.order_by(School.name).all()
    return render_template('admin/list_donations.html',
                           donations=donations, schools=schools)


@admin.route('/donations/new', methods=['GET', 'POST'])
@login_required
@csrf_protected
def new_donation():
    schools = School.query.order_by(School.name).all()
    if request.method == 'POST':
        status = request.form.get('status', 'received').strip()
        distributed_at = _parse_date(request.form.get('distributed_at'))
        if status == 'completed' and not distributed_at:
            distributed_at = datetime.utcnow()

        donation = Donation(
            school_id=_int_or_none(request.form.get('school_id')),
            donor_name=request.form.get('donor_name', '').strip(),
            donor_avatar=request.form.get('donor_avatar', '').strip(),
            item_name=request.form.get('item_name', '').strip(),
            item_detail=request.form.get('item_detail', '').strip(),
            quantity=request.form.get('quantity', '').strip(),
            amount=_float_or_none(request.form.get('amount')),
            received_class=request.form.get('received_class', '').strip(),
            status=status,
            distributed_at=distributed_at,
        )
        db.session.add(donation)
        db.session.commit()
        flash('捐赠记录已创建', 'success')
        return redirect(url_for('admin.list_donations'))
    return render_template('admin/form_donation.html',
                           item=None, schools=schools)


@admin.route('/donations/<int:donation_id>/edit', methods=['GET', 'POST'])
@login_required
@csrf_protected
def edit_donation(donation_id):
    donation = Donation.query.get_or_404(donation_id)
    schools = School.query.order_by(School.name).all()
    if request.method == 'POST':
        donation.school_id = _int_or_none(request.form.get('school_id'))
        donation.donor_name = request.form.get('donor_name', '').strip()
        donation.donor_avatar = request.form.get('donor_avatar', '').strip()
        donation.item_name = request.form.get('item_name', '').strip()
        donation.item_detail = request.form.get('item_detail', '').strip()
        donation.quantity = request.form.get('quantity', '').strip()
        donation.amount = _float_or_none(request.form.get('amount'))
        donation.received_class = request.form.get('received_class', '').strip()
        donation.status = request.form.get('status', 'received').strip()
        donation.distributed_at = _parse_date(request.form.get('distributed_at'))
        if donation.status == 'completed' and not donation.distributed_at:
            donation.distributed_at = datetime.utcnow()
        db.session.commit()
        flash('捐赠记录已更新', 'success')
        return redirect(url_for('admin.list_donations'))
    return render_template('admin/form_donation.html',
                           item=donation, schools=schools)


@admin.route('/donations/<int:donation_id>/delete', methods=['POST'])
@login_required
@csrf_protected
def delete_donation(donation_id):
    donation = Donation.query.get_or_404(donation_id)
    db.session.delete(donation)
    db.session.commit()
    flash('捐赠记录已删除', 'success')
    return redirect(url_for('admin.list_donations'))


# --------------------------------------------------------------------------- #
# 学生管理
# --------------------------------------------------------------------------- #
@admin.route('/children')
@login_required
def list_children():
    children = Child.query.order_by(Child.created_at.desc()).all()
    schools = School.query.order_by(School.name).all()
    return render_template('admin/list_children.html',
                           children=children, schools=schools)


@admin.route('/children/new', methods=['GET', 'POST'])
@login_required
@csrf_protected
def new_child():
    schools = School.query.order_by(School.name).all()
    if request.method == 'POST':
        child = Child(
            school_id=_int_or_none(request.form.get('school_id')),
            name=request.form.get('name', '').strip(),
            age=_int_or_none(request.form.get('age')),
            bio=request.form.get('bio', '').strip(),
            quote=request.form.get('quote', '').strip(),
            avatar=request.form.get('avatar', '').strip(),
            tags=request.form.get('tags', '').strip(),
        )
        db.session.add(child)
        db.session.commit()
        flash('学生信息已创建', 'success')
        return redirect(url_for('admin.list_children'))
    return render_template('admin/form_child.html',
                           item=None, schools=schools)


@admin.route('/children/<int:child_id>/edit', methods=['GET', 'POST'])
@login_required
@csrf_protected
def edit_child(child_id):
    child = Child.query.get_or_404(child_id)
    schools = School.query.order_by(School.name).all()
    if request.method == 'POST':
        child.school_id = _int_or_none(request.form.get('school_id'))
        child.name = request.form.get('name', '').strip()
        child.age = _int_or_none(request.form.get('age'))
        child.bio = request.form.get('bio', '').strip()
        child.quote = request.form.get('quote', '').strip()
        child.avatar = request.form.get('avatar', '').strip()
        child.tags = request.form.get('tags', '').strip()
        db.session.commit()
        flash('学生信息已更新', 'success')
        return redirect(url_for('admin.list_children'))
    return render_template('admin/form_child.html',
                           item=child, schools=schools)


@admin.route('/children/<int:child_id>/delete', methods=['POST'])
@login_required
@csrf_protected
def delete_child(child_id):
    child = Child.query.get_or_404(child_id)
    db.session.delete(child)
    db.session.commit()
    flash('学生信息已删除', 'success')
    return redirect(url_for('admin.list_children'))


# --------------------------------------------------------------------------- #
# 文件上传
# --------------------------------------------------------------------------- #
@admin.route('/upload', methods=['POST'])
@login_required
@csrf_protected
def upload():
    """上传图片到 app/static/img/，返回可被前端直接使用的相对路径。"""
    if 'file' not in request.files:
        return jsonify({'error': '未找到文件'}), 400

    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'error': '未选择文件'}), 400

    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if ext not in Config.ALLOWED_EXTENSIONS:
        return jsonify({'error': '不支持的文件类型'}), 400

    media_type = 'video' if ext in {'mp4', 'webm', 'mov'} else 'image'
    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    save_path = os.path.join(upload_folder, unique_name)
    file.save(save_path)

    return jsonify({
        'url': url_for('static', filename=f'img/{unique_name}'),
        'filename': unique_name,
        'type': media_type,
    })
