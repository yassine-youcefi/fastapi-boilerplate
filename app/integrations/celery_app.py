from celery import Celery
from kombu import Queue

from app.config.config import settings

celery_app = Celery(
    "fastapi_boilerplate",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.user.tasks.user_tasks"],  # Updated to point to the correct task module
)

# Remove default queue, define two named queues: auth-queue and user-queue
celery_app.conf.task_queues = (
    Queue("auth-queue"),
    Queue("user-queue"),
)

# Optional: Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_scheduler="celery.beat:PersistentScheduler",
    beat_schedule={},  # You can add periodic tasks here
)
