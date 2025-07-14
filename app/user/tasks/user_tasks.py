from celery import shared_task


@shared_task(bind=True, queue="user-queue", max_retries=3, default_retry_delay=10)
def user_created_task(self, user_email: str):
    try:
        print(f"Hi {user_email}")
    except Exception as exc:
        raise self.retry(exc=exc)
