from flask import Blueprint, render_template, request, current_app, url_for
from urllib.parse import urlencode, parse_qs, urlparse, urlunparse
import os
from app.extensions import db
from app.models import School, Post, Donation, Child

main = Blueprint('main', __name__)

# 测试阶段 UI 变体白名单，对应 app/templates/ui_variants/<key>.html
UI_VARIANTS = ('charitywater', 'justgiving', 'donorsee', 'wwf', 'gofundme')


def _variant_template_exists(template):
    """检查变体模板文件是否存在。"""
    parts = template.split('/')
    path = os.path.join(current_app.root_path, 'templates', *parts)
    return os.path.exists(path)


@main.app_context_processor
def inject_schools():
    return {'schools': School.query.all()}


@main.app_context_processor
def inject_ui_helpers():
    """注入 UI 变体测试所需的辅助函数。"""

    def ui_switch_url(variant):
        """保留当前路径与参数，仅替换 ui=<variant>。"""
        url = urlparse(request.url)
        qs = parse_qs(url.query, keep_blank_values=True)
        qs['ui'] = [variant]
        new_query = urlencode(qs, doseq=True)
        return urlunparse(url._replace(query=new_query))

    def variant_asset(variant, rel_path, fallback=None):
        """优先返回本地变体静态资源；不存在则返回 fallback。"""
        static_path = '/'.join(['media', 'ui_variants', variant, rel_path])
        full_path = os.path.join(current_app.static_folder, *static_path.split('/'))
        if os.path.exists(full_path):
            return url_for('static', filename=static_path)
        return fallback or ''

    return {'ui_switch_url': ui_switch_url, 'variant_asset': variant_asset}


@main.route('/')
def index():
    schools = School.query.all()
    children = Child.query.limit(6).all()
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(6).all()
    recent_donations = Donation.query.order_by(Donation.created_at.desc()).limit(8).all()
    total_donations = db.session.query(db.func.count(Donation.id)).scalar() or 0
    total_amount = db.session.query(db.func.sum(Donation.amount)).scalar() or 0

    ui = request.args.get('ui', '').strip().lower()
    if ui in UI_VARIANTS:
        return render_template(f'ui_variants/{ui}.html',
                               schools=schools,
                               children=children,
                               recent_posts=recent_posts,
                               recent_donations=recent_donations,
                               total_donations=total_donations,
                               total_amount=total_amount,
                               ui_variant=ui)

    return render_template('index.html',
                           schools=schools,
                           children=children,
                           recent_posts=recent_posts,
                           recent_donations=recent_donations,
                           total_donations=total_donations,
                           total_amount=total_amount)


@main.route('/school/<int:school_id>')
def school_detail(school_id):
    school = School.query.get_or_404(school_id)
    posts = Post.query.filter_by(school_id=school_id).order_by(Post.created_at.desc()).all()
    donations = Donation.query.filter_by(school_id=school_id).order_by(Donation.created_at.desc()).all()
    children = Child.query.filter_by(school_id=school_id).all()
    all_schools = School.query.order_by(School.created_at.desc()).all()

    ui = request.args.get('ui', '').strip().lower()
    if ui in UI_VARIANTS:
        template = f'ui_variants/{ui}_school.html'
        if _variant_template_exists(template):
            return render_template(template,
                                   school=school,
                                   posts=posts,
                                   donations=donations,
                                   children=children,
                                   all_schools=all_schools,
                                   ui_variant=ui)

    return render_template('school_detail.html',
                           school=school,
                           posts=posts,
                           donations=donations,
                           children=children,
                           all_schools=all_schools)


@main.route('/dashboard')
def dashboard():
    schools = School.query.all()

    # 查询参数
    school_id = request.args.get('school_id', type=int)
    status = request.args.get('status', '').strip()
    q = request.args.get('q', '').strip()
    sort = request.args.get('sort', 'date_desc').strip()

    # 构造查询
    query = Donation.query
    if school_id:
        query = query.filter_by(school_id=school_id)
    if status in ('received', 'distributing', 'completed'):
        query = query.filter_by(status=status)
    if q:
        query = query.filter(
            db.or_(
                Donation.donor_name.ilike(f'%{q}%'),
                Donation.item_name.ilike(f'%{q}%'),
                Donation.item_detail.ilike(f'%{q}%')
            )
        )

    # 排序
    if sort == 'date_asc':
        query = query.order_by(Donation.created_at.asc())
    elif sort == 'amount_desc':
        query = query.order_by(Donation.amount.desc().nulls_last())
    elif sort == 'amount_asc':
        query = query.order_by(Donation.amount.asc().nulls_last())
    else:  # date_desc
        query = query.order_by(Donation.created_at.desc())

    donations = query.all()

    # 统计数据基于当前筛选结果
    total_count = len(donations)
    total_amount = sum(d.amount or 0 for d in donations)
    completed_count = sum(1 for d in donations if d.status == 'completed')

    # 人次：按捐赠人去重计数
    donor_count = len({d.donor_name for d in donations})

    ui = request.args.get('ui', '').strip().lower()
    if ui in UI_VARIANTS:
        template = f'ui_variants/{ui}_dashboard.html'
        if _variant_template_exists(template):
            return render_template(template,
                                   schools=schools,
                                   donations=donations,
                                   total_count=total_count,
                                   total_amount=total_amount,
                                   completed_count=completed_count,
                                   donor_count=donor_count,
                                   school_id=school_id,
                                   status=status,
                                   q=q,
                                   sort=sort,
                                   ui_variant=ui)

    return render_template('dashboard.html',
                           schools=schools,
                           donations=donations,
                           total_count=total_count,
                           total_amount=total_amount,
                           completed_count=completed_count,
                           donor_count=donor_count,
                           school_id=school_id,
                           status=status,
                           q=q,
                           sort=sort)
