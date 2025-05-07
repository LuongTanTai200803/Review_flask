from datetime import datetime, timezone
import uuid
from app.extensions import db

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(50), nullable=False) # nullable=False không được để trống
    description = db.Column(db.Text)
    status = db.Column(db.String(20),  default="pending")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    due_date = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    user = db.relationship("User", back_populates="tasks")