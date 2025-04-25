
from datetime import datetime
import time
from app.celery_worker import celery
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extensions import db
from app.models.task import Task
from app.models.user import User

task_bp = Blueprint("taks", __name__)

@task_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"msg": "Not User"}), 400
    
    task = Task(
        title = data['title'],
        status = data['status'],
        due_date=datetime.strptime(data['due_date'], '%Y-%m-%d') if data.get('due_date') else None,
        user_id = user.id
    )
    task.description = data.get('description', 'No description')

    db.session.add(task)
    db.session.commit()
    return jsonify({"msg": "Task created"}), 201


@task_bp.route('/', methods=['GET'])
@jwt_required()
def get_task():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"msg": "Not User"}), 400
    
    # Lấy tất cả task của user
    tasks = Task.query.filter_by(user_id=user_id).order_by(Task.id.asc()).all()
    
      # Chuyển đổi dữ liệu task
    tasks_data = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "users_id": task.user_id,
            "username": user.username,
            "due_date": task.due_date
        }
        for task in tasks
    ]

    return jsonify(tasks_data), 200

@task_bp.route('/', methods=['PUT'])
@jwt_required()
def update_task():
    user_id = get_jwt_identity()
    data = request.get_json()

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"msg": "Not Found User"}), 400
    task_id = data['id']

    task = Task.query.filter_by(id=task_id).first()

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)

    if data.get('due_date'):
        try:
            # Giả sử định dạng ngày bạn gửi là "YYYY-MM-DD"
            task.due_date = datetime.strptime(data.get('due_date'), '%Y-%m-%d')
        except ValueError:
            return jsonify({"msg": "Invalid date format for due_date, expected YYYY-MM-DD"}), 400
    elif data.get('due_date') is None:
        task.due_date = None 

    db.session.commit()
    return jsonify({"msg": "Task update success"}), 200

@task_bp.route('/', methods=['DELETE'])
@jwt_required()
def delete_task():
    user_id = get_jwt_identity()
    data = request.get_json()

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"msg": "User Not Found"}), 400
    
    task_id = data['id']
    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return jsonify({"msg": "User Not Found"}), 400
    
    db.session.delete(task)
    db.session.commit()
    return jsonify({"msg": "Task delete success"}), 200

@celery.task
def send_email(to_email, subject, body):
    # Giả lập delay gửi email
    time.sleep(5)
    print(f"Sent email to {to_email} with subject '{subject}'")
    return True