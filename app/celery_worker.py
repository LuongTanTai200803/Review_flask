import time
from celery import Celery
from app.config import Config  # hoặc từ config chung nếu config đặt nơi khác

celery = Celery(
    'app',
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND
)
celery.conf.update(
    task_track_started=True,
    task_serializer='json',
)

@celery.task
def send_email(to_email, subject, body):
    time.sleep(5)
    print(f"Sent email to {to_email} with subject '{subject}'")
    return True