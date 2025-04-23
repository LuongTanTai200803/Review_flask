from flask import jsonify
from app.models.user import User


def check_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"msg": "Not User"}), 400
    return user