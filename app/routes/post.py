from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.exceptions import BadRequestException, NotFoundException
from app.extensions import db, cache

from app.models.user import User
from app.models.post import Post
from app.routes import check_user, make_cache_key
from app.celery_worker import send_email

post_bp = Blueprint("post", __name__)
import logging

logger = logging.getLogger(__name__)  # __name__ tự động lấy tên module hiện tại

# Create post
@post_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    user_id = get_jwt_identity()
    user = check_user(user_id)

    if not any(field in data and data[field].strip() for field in ['title', 'content']):
        return jsonify({"msg": "At least one of title or content must be provided and not empty"}), 400
    
    post = Post(
        title = data['title'],
        content = data['content'],
        user_id = user.id
    )

    db.session.add(post)
    db.session.commit()
    # Gửi email thông báo bất đồng bộ
    #send_email.delay('user@example.com', "New post created", 'This is test email')

    return jsonify({
        "msg": "Post created success",
        "post_id": post.id
        }), 201


@post_bp.route('/', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60, key_prefix=make_cache_key)
def get_post():
    user_id = get_jwt_identity()
    check_user(user_id)

    # Lấy tham số phân trang và tìm kiếm
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    keyword = request.args.get('q', '', type=str)

    # Lấy post theo user
    query = Post.query.filter_by(user_id=user_id).order_by(Post.id.desc())
    
    # Nếu có từ khóa tìm kiếm 
    if keyword:
        query = query.filter(Post.title.ilike(f"%{keyword}%"))

    # Phân trang
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # Chuyển đổi dữ liệu task
    posts_data = [
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "user_id": post.user_id,
        }
        for post in pagination.items
    ]

    return jsonify({
        "post": posts_data,
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    }), 200

@post_bp.route('/<string:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    # Kiểm tra đúng user
    check_user(user_id)

    if not data:
        return jsonify({"msg": "Request body is empty"}), 400

    if not any(field in data and data[field].strip() for field in ['title', 'content']):
        return jsonify({"msg": "At least one of title or content must be provided and not empty"}), 400
    
    post = Post.query.filter_by(id=post_id, user_id=user_id).first()
   
    if not post:
        return jsonify({"msg": "Post not found or unauthorized"}), 404
    
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)

    db.session.commit()
    return jsonify({"msg": "Post update success"}), 200

@post_bp.route('/<string:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    user_id = get_jwt_identity()
    # Kiểm tra đúng user
    check_user(user_id)

    post = Post.query.filter_by(id=post_id).first()
    if not post:
        raise NotFoundException("Post Not Found")
    
    db.session.delete(post)
    db.session.commit()
    return jsonify({"msg": "Post delete success"}), 200
