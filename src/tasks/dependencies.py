from config.database import redis_client
from .service import TaskService


def get_task_service():
    return TaskService(redis_client)
