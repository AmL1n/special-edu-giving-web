from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class School(db.Model):
    __tablename__ = 'schools'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(500))
    cover_image = db.Column(db.String(500))
    media_json = db.Column(db.Text)  # JSON: [{type, url, section, caption}, ...]
    student_count = db.Column(db.Integer, default=0)
    teacher_count = db.Column(db.Integer, default=0)
    founded_year = db.Column(db.Integer)
    contact_phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship('Post', backref='school', lazy='dynamic')
    donations = db.relationship('Donation', backref='school', lazy='dynamic')
    children = db.relationship('Child', backref='school', lazy='dynamic')

    def get_media(self):
        """解析 media_json 为媒体列表。"""
        import json
        try:
            return json.loads(self.media_json or '[]') or []
        except Exception:
            return []

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'location': self.location,
            'cover_image': self.cover_image,
            'student_count': self.student_count,
            'teacher_count': self.teacher_count,
            'founded_year': self.founded_year,
        }


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    title = db.Column(db.String(300))
    content = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    media_json = db.Column(db.Text)  # JSON: [{type, url, section, caption}, ...]
    post_type = db.Column(db.String(20), default='daily')  # daily / distribution
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_media(self):
        """解析 media_json 为媒体列表。"""
        import json
        try:
            return json.loads(self.media_json or '[]') or []
        except Exception:
            return []

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'image_url': self.image_url,
            'post_type': self.post_type,
            'created_at': self.created_at.strftime('%Y-%m-%d'),
        }


class Donation(db.Model):
    __tablename__ = 'donations'
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    donor_name = db.Column(db.String(100), nullable=False)
    donor_avatar = db.Column(db.String(500))
    item_name = db.Column(db.String(200), nullable=False)
    item_detail = db.Column(db.Text)
    quantity = db.Column(db.String(100))
    amount = db.Column(db.Float)
    received_class = db.Column(db.String(100))
    status = db.Column(db.String(20), default='received')  # received / distributing / completed
    distributed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'donor_name': self.donor_name,
            'item_name': self.item_name,
            'item_detail': self.item_detail,
            'quantity': self.quantity,
            'amount': self.amount,
            'received_class': self.received_class,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d'),
            'distributed_at': self.distributed_at.strftime('%Y-%m-%d') if self.distributed_at else None,
        }


class Child(db.Model):
    __tablename__ = 'children'
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    bio = db.Column(db.Text)
    quote = db.Column(db.String(500))
    avatar = db.Column(db.String(500))
    tags = db.Column(db.String(500))  # JSON string of tags
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'bio': self.bio,
            'quote': self.quote,
            'avatar': self.avatar,
            'tags': self.tags.split(',') if self.tags else [],
        }


class AdminUser(db.Model):
    __tablename__ = 'admin_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

