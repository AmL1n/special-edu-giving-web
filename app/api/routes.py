import json
from flask import Blueprint, request, jsonify
from datetime import datetime
from app.extensions import db
from app.models import School, Post, Donation, Child

api = Blueprint('api', __name__)


@api.route('/api/stats')
def get_stats():
    total_schools = School.query.count()
    total_donations = Donation.query.count()
    total_amount = db.session.query(db.func.sum(Donation.amount)).scalar() or 0
    total_children = Child.query.count()
    return jsonify({
        'total_schools': total_schools,
        'total_donations': total_donations,
        'total_amount': float(total_amount),
        'total_children': total_children,
    })


@api.route('/api/donations')
def get_donations():
    donations = Donation.query.order_by(Donation.created_at.desc()).limit(50).all()
    return jsonify([d.to_dict() for d in donations])


@api.route('/api/import', methods=['POST'])
def import_data():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    imported = {'schools': 0, 'posts': 0, 'donations': 0, 'children': 0}

    for s in data.get('schools', []):
        school = School(
            name=s['name'],
            description=s.get('description', ''),
            location=s.get('location', ''),
            cover_image=s.get('cover_image', ''),
            student_count=s.get('student_count', 0),
            teacher_count=s.get('teacher_count', 0),
            founded_year=s.get('founded_year'),
        )
        db.session.add(school)
        imported['schools'] += 1

    db.session.commit()

    for p in data.get('posts', []):
        post = Post(
            school_id=p['school_id'],
            title=p.get('title', ''),
            content=p.get('content', ''),
            image_url=p.get('image_url', ''),
            post_type=p.get('post_type', 'daily'),
            created_at=datetime.strptime(p['created_at'], '%Y-%m-%d') if 'created_at' in p else datetime.utcnow(),
        )
        db.session.add(post)
        imported['posts'] += 1

    for d in data.get('donations', []):
        donation = Donation(
            school_id=d['school_id'],
            donor_name=d['donor_name'],
            item_name=d['item_name'],
            item_detail=d.get('item_detail', ''),
            quantity=d.get('quantity', ''),
            amount=d.get('amount', 0),
            received_class=d.get('received_class', ''),
            status=d.get('status', 'received'),
            created_at=datetime.strptime(d['created_at'], '%Y-%m-%d') if 'created_at' in d else datetime.utcnow(),
        )
        db.session.add(donation)
        imported['donations'] += 1

    for c in data.get('children', []):
        child = Child(
            school_id=c['school_id'],
            name=c['name'],
            age=c.get('age'),
            bio=c.get('bio', ''),
            quote=c.get('quote', ''),
            avatar=c.get('avatar', ''),
            tags=c.get('tags', ''),
        )
        db.session.add(child)
        imported['children'] += 1

    db.session.commit()
    return jsonify({'message': 'Import successful', 'imported': imported})
