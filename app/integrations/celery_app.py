from celery import Celery
from kombu import Queue

from app.config.config import settings


def create_celery_app() -> Celery:
    celery = Celery(
        "fastapi_boilerplate",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND,
        include=["app.user.tasks.user_tasks"],
    )
    celery.conf.task_queues = (
        Queue("auth-queue"),
        Queue("user-queue"),
    )
    celery.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        beat_scheduler="celery.beat:PersistentScheduler",
        beat_schedule={},
    )
    return celery
