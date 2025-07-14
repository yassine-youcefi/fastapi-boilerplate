from app.integrations.celery_app import celery_app


def user_created_task(user_email: str):
    print(f"Hi {user_email}")


# Register as a Celery task
task = celery_app.task(user_created_task)
