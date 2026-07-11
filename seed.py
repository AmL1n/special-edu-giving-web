# -*- coding: utf-8 -*-
import sys, os, random, json
sys.path.insert(0, os.path.dirname(__file__))
from app import create_app, db
from app.models import School, Post, Donation, Child, AdminUser
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

app = create_app()

S1 = "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=1200&q=85"
S2 = "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1200&q=85"
S3 = "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1200&q=85"

SAMPLE_IMAGES = [
    "https://images.unsplash.com/photo-1509062522246-3755977927d7?w=600&q=80",
    "https://images.unsplash.com/photo-1516627145497-ae6968895b74?w=600&q=80",
    "https://images.unsplash.com/photo-1484820540004-14229fe36ca4?w=600&q=80",
    "https://images.unsplash.com/photo-1544776193-352d25ca82cd?w=600&q=80",
    "https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=600&q=80",
    "https://images.unsplash.com/photo-1560969184-10fe8719e047?w=600&q=80",
]

def make_media(count, sections):
    """生成演示用的媒体 JSON 列表。"""
    media = []
    for i in range(count):
        section = random.choice(sections)
        media.append({
            "type": "image",
            "url": random.choice(SAMPLE_IMAGES),
            "section": section,
            "caption": random.choice(["温暖瞬间", "校园生活", "捐赠现场", "课堂时光", "欢乐活动", ""]),
        })
    return json.dumps(media)

SCHOOL_DATA = [
    {"name": "杭州市启明星特殊教育学校", "description": "杭州市启明星特殊教育学校成立于2008年，是一所为智力障碍、自闭症谱系障碍儿童提供九年义务教育的特殊教育学校。学校秉持「让每一朵花都绽放」的办学理念，设有专业康复训练室、感统训练室、多媒体教学室等功能教室。", "location": "浙江省杭州市西湖区文二西路268号", "cover_image": S1, "student_count": 86, "teacher_count": 32, "founded_year": 2008},
    {"name": "上海市阳光自闭症康复中心", "description": "上海市阳光自闭症康复中心专注于自闭症谱系障碍儿童的早期干预与康复训练。采用ABA、TEACCH等国际认可的干预方法，结合感统训练、语言治疗、社交技能训练等多元课程，已累计帮助超过300名自闭症儿童改善社交沟通能力。", "location": "上海市浦东新区浦东大道1200号", "cover_image": S2, "student_count": 45, "teacher_count": 28, "founded_year": 2015},
    {"name": "广州市启聪聋哑学校", "description": "广州市启聪聋哑学校是一所拥有30年办学历史的特殊教育学校，致力于为听力障碍学生提供优质的义务教育与职业教育。学校设有语言康复部、基础教育部和职业教育部。以「无声世界，有梦同行」为校训，帮助一批又一批听障学生顺利融入社会。", "location": "广州市天河区五山路15号", "cover_image": S3, "student_count": 120, "teacher_count": 45, "founded_year": 1996},
]

CHILDREN_DATA = [
    {"name": "小明", "age": 10, "bio": "热爱绘画的安静小男孩", "quote": "我想画一座桥，让所有人都能走到我心里来。", "tags": "绘画,手工,希望之星"},
    {"name": "小花", "age": 8, "bio": "笑容灿烂的活力小女孩", "quote": "虽然我听不见风，但我可以看见树叶在跳舞。", "tags": "舞蹈,音乐,乐观天使"},
    {"name": "小宇", "age": 12, "bio": "喜欢阅读和写作的少年", "quote": "书本里有另一个世界，那里每个人都一样。", "tags": "阅读,写作,成长"},
    {"name": "小月", "age": 7, "bio": "活泼可爱的小天使", "quote": "每天都要笑一笑，因为微笑是世界上最好看的表情。", "tags": "音乐,运动,开心果"},
    {"name": "小杰", "age": 11, "bio": "擅长手工制作的巧手男孩", "quote": "我做的纸飞机可以飞很远，梦想也是。", "tags": "手工,创造,梦想家"},
    {"name": "小婷", "age": 9, "bio": "记忆力超群的小才女", "quote": "我的心里装着很多很多的故事。", "tags": "记忆,表达,小诗人"},
    {"name": "小峰", "age": 13, "bio": "热爱运动的阳光少年", "quote": "跑起来的时候，我觉得自己可以追上太阳。", "tags": "运动,阳光,追风少年"},
    {"name": "小丽", "age": 6, "bio": "刚入学的小小新生", "quote": "学校里有好多好多的朋友和老师。", "tags": "新生,可爱,小花朵"},
    {"name": "小强", "age": 14, "bio": "厨艺小达人", "quote": "做出好吃的饼干，世界都会变得更甜。", "tags": "烹饪,美食,小厨师"},
    {"name": "小雪", "age": 9, "bio": "安静温柔的小画家", "quote": "每一种颜色都有自己的心情，就像每一个人。", "tags": "绘画,细腻,小画家"},
    {"name": "小龙", "age": 12, "bio": "计算机小天才", "quote": "代码可以创造世界，我也想创造自己的世界。", "tags": "编程,科技,未来之星"},
    {"name": "小慧", "age": 10, "bio": "活泼开朗的小主持人", "quote": "舞台上的灯光会照到我，我也会照亮别人。", "tags": "主持,表达,小明星"},
]

POSTS = [
    {"title": "爱心人士捐赠的冬季校服已全部发放", "content": "感谢社会各界爱心人士的慷慨捐赠，200套冬季校服已全部分发到每一位孩子手中。看到孩子们穿上新校服的笑容，我们知道所有的努力都值得。", "post_type": "distribution"},
    {"title": "春季运动会圆满落幕", "content": "4月20日，学校举办了快乐运动健康成长春季趣味运动会。拔河、接力跑、袋鼠跳……每一个项目孩子们都全心投入，收获了欢笑与友谊。", "post_type": "daily"},
    {"title": "烘焙课上的甜蜜时光", "content": "本周的烘焙课上，孩子们亲手制作了蔓越莓饼干。从称量面粉到装饰成品，每一步都充满认真与期待。烘焙不仅是一门技能，更是一段被爱包裹的时光。", "post_type": "daily"},
    {"title": "多媒体教室设备升级完成", "content": "在爱心企业的大力支持下，学校多媒体教室完成了全面升级。新的投影设备、音响系统和互动白板将为孩子们带来更丰富的学习体验。", "post_type": "distribution"},
    {"title": "六一儿童节文艺汇演精彩纷呈", "content": "6月1日，全校师生齐聚礼堂，共同庆祝六一儿童节。孩子们表演了合唱、舞蹈、诗朗诵等精彩节目，展现了自信与风采。", "post_type": "daily"},
    {"title": "感统训练室器材上新", "content": "新一批感统训练器材已投入使用，包括平衡木、触觉球、摇摆秋千等。专业康复师表示这些器材将有效提升孩子们的感觉统合能力。", "post_type": "distribution"},
    {"title": "家长开放日见证成长的力量", "content": "本学期第一次家长开放日如约而至。家长们走进课堂，近距离感受孩子的学习状态。当看到孩子独立完成手工作品时，许多家长眼中闪着骄傲的泪光。", "post_type": "daily"},
    {"title": "爱心企业捐赠音乐教室乐器", "content": "YAMAHA电子琴、非洲鼓、铃鼓等共计15件乐器已送达学校。音乐老师已经开始为孩子们编排新的音乐课程，让旋律成为传递希望的另一种语言。", "post_type": "distribution"},
    {"title": "秋季校园写生活动", "content": "美术老师带领高年级学生走进校园花园，用画笔记录秋天的色彩。银杏叶的金黄、枫叶的火红，每一幅作品都是孩子们眼中的世界。", "post_type": "daily"},
    {"title": "电脑教室设备全部到位", "content": "10台全新台式电脑已安装完毕并投入使用。信息技术课正式开课，孩子们从认识鼠标键盘开始，一步步走进数字世界的大门。", "post_type": "distribution"},
]

DONORS = ["张女士", "李明远", "王女士", "陈志强", "阿里巴巴公益基金", "腾讯公益基金会", "周博文", "赵女士", "刘建国", "林小姐", "杨女士", "大学生志愿者联盟", "沈先生", "黄女士", "恒生电子企业社", "马万里", "吴女士", "郑先生", "孙女士", "钱阿姨"]
DONATION_ITEMS = [("冬季校服", "加厚棉质冬季校服", "200套", 30000), ("儿童绘本", "精选儿童绘本200册", "200册", 8000), ("美术教具套装", "画笔+颜料+纸张套装", "150套", 12000), ("电子琴", "YAMAHA PSR系列电子琴", "10台", 15000), ("感统训练设备", "综合感统训练器材套件", "1套", 5000), ("多媒体教学设备", "投影仪+音响+白板", "1套", 20000), ("文具用品", "水彩笔+笔记本+铅笔+橡皮", "100套", 6000), ("冬季保暖品", "毛绒手套+围巾+帽子", "200套", 4000), ("投影设备", "高清教学投影仪", "5台", 25000), ("康复器械", "专业康复训练组合器械", "15套", 7500), ("学生校服", "春秋季学生统一校服套装", "30套", 18000), ("空调", "冷暖两用壁挂式空调", "6台", 24000), ("电脑", "台式学习电脑", "10台", 35000), ("图书角", "班级图书角套装", "20套", 40000)]
CLASSES = ["一年级", "二年级", "三年级", "四年级", "五年级", "六年级", "七年级", "八年级", "九年级", "学校统一"]
STATUSES = ["received", "distributing", "completed"]

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()
        schools = []
        for data in SCHOOL_DATA:
            school_data = data.copy()
            school_data['media_json'] = make_media(
                random.randint(3, 6),
                ['gallery', 'activities', 'classroom', 'donation_scene']
            )
            s = School(**school_data)
            db.session.add(s)
            schools.append(s)
        db.session.commit()
        print(f"[OK] {len(schools)} schools")

        for i, cd in enumerate(CHILDREN_DATA):
            db.session.add(Child(school_id=schools[i % len(schools)].id, **cd))
        db.session.commit()
        print(f"[OK] {len(CHILDREN_DATA)} children")

        for i, pd in enumerate(POSTS):
            img = f"https://images.unsplash.com/photo-{1503676260728 + i * 1000}?w=600&q=80"
            post_data = pd.copy()
            post_data['media_json'] = make_media(
                random.randint(0, 4),
                ['gallery', 'featured', 'video_clip']
            )
            db.session.add(Post(
                school_id=schools[i % len(schools)].id,
                image_url=img,
                created_at=datetime.now() - timedelta(days=random.randint(1, 90)),
                **post_data
            ))
        db.session.commit()
        print(f"[OK] {len(POSTS)} posts")

        for i in range(40):
            donor = random.choice(DONORS)
            item = random.choice(DONATION_ITEMS)
            days_ago = random.randint(1, 180)
            status = random.choice(STATUSES)
            dist_at = datetime.now() - timedelta(days=days_ago - random.randint(1, 10)) if status == "completed" else None
            db.session.add(Donation(school_id=random.choice(schools).id, donor_name=donor, item_name=item[0], item_detail=item[1], quantity=item[2], amount=item[3] * random.uniform(0.8, 1.2), received_class=random.choice(CLASSES), status=status, created_at=datetime.now() - timedelta(days=days_ago), distributed_at=dist_at))
        db.session.commit()
        print(f"[OK] 40 donations")

        admin = AdminUser.query.filter_by(
            username=app.config['ADMIN_USERNAME']
        ).first()
        if not admin:
            admin = AdminUser(username=app.config['ADMIN_USERNAME'])
            admin.set_password(app.config['ADMIN_PASSWORD'])
            db.session.add(admin)
            db.session.commit()
            print(f"[OK] default admin user '{admin.username}' created")
        else:
            print(f"[OK] default admin user '{admin.username}' already exists")

        print("DONE - Seed complete!")

if __name__ == "__main__":
    seed()