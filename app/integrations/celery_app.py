from celery import Celery

from app.config.config import settings

celery_app = Celery(
    "fastapi_boilerplate",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks"],  # You can create this module for your celery tasks
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
