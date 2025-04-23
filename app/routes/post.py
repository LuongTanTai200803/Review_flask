from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extensions import db

from app.models.user import User
from app.models.post import Post
from app.routes import check_user

post_bp = Blueprint("post", __name__)

# Create post
@post_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    user_id = get_jwt_identity()
    user = check_user(user_id)

    post = Post(
        title = data['title'],
        content = data['content'],
        user_id = user.id
    )

    db.session.add(post)
    db.session.commit()
    return jsonify({"msg": "Post created success"}), 201


@post_bp.route('/', methods=['GET'])
@jwt_required()
def get_post():
    user_id = get_jwt_identity()
    check_user(user_id)

    # Lấy tất cả post của user
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.id.asc()).all()
    
      # Chuyển đổi dữ liệu task
    posts_data = [
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "users_id": post.user_id,
        }
        for post in posts
    ]

    return jsonify(posts_data), 200

@post_bp.route('/<string:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    # Kiểm tra đúng user
    check_user(user_id)

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
        return jsonify({"msg": "Post Not Found"}), 400
    
    db.session.delete(post)
    db.session.commit()
    return jsonify({"msg": "Post delete success"}), 200
