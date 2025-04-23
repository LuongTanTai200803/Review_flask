import uuid
from app.extensions import db

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(150), nullable=False) # nullable=False không được để trống
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    user = db.relationship("User", back_populates="posts")