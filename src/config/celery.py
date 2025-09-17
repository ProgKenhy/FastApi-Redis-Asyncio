from celery import Celery
from .settings import settings

celery_app = Celery("myapp")

celery_config = settings.celery_config
celery_app.conf.update(
    broker_url=celery_config.BROKER_URL,
    result_backend=celery_config.RESULT_BACKEND,
    task_serializer=celery_config.TASK_SERIALIZER,
    accept_content=celery_config.ACCEPT_CONTENT,
    result_serializer=celery_config.RESULT_SERIALIZER,
    timezone=celery_config.TIMEZONE,
    enable_utc=celery_config.ENABLE_UTC,
    task_track_started=celery_config.TASK_TRACK_STARTED,
    task_time_limit=celery_config.TASK_TIME_LIMIT,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_soft_time_limit=celery_config.TASK_SOFT_TIME_LIMIT,
    # include=['myapp.tasks']
)

celery_app.autodiscover_tasks()
