from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models.user import User


auth_bp = Blueprint("auth", __name__)
@auth_bp.route('/singup', methods=['POST'])
def singup():
    data = request.get_json()
    user = User(username = data['username'])
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Bad credentials"}), 401

