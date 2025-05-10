from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from app.models.user import User


def check_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"msg": "Not Found User"}), 400
    return user
# Tạo key theo params
def make_cache_key(*args, **kwargs):
    user_id = get_jwt_identity()
    path = request.path
    args = str(hash(frozenset(request.args.items())))
    return f"{path} | user:{user_id} | params:{args}"

# Bảo mật hash key cache
""" def make_secure_cache_key(*args, **kwargs):
    user_id = get_jwt_identity()
    path = request.path
    params_str = str(sorted(request.args.items()))
    raw_key = f"{path}|user:{user_id}|params:{params_str}|salt:{SECRET_SALT}"
    hashed_key = hashlib.sha256(raw_key.encode()).hexdigest()
    return f"flask_cache_{hashed_key}" """