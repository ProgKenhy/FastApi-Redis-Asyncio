import uuid
from datetime import datetime, UTC
from typing import Optional

from redis.asyncio import Redis

from tasks.schemas import TaskCreate, TaskInfoResponse, TaskInfo, TaskCreateResponse


class TaskService:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    async def create_task(self, task_data: TaskCreate) -> TaskCreateResponse:
        task_id = str(uuid.uuid4())
        task_info = TaskInfo(
            id=task_id,
            task_name=task_data.task_name,
            assignee=task_data.assignee,
            created_at=datetime.now(UTC),
        )
        await self.redis.set(
            f"task:{task_id}",
            task_info.model_dump_json(),
        )

        await self.redis.lpush(f"queue:{task_data.assignee}", task_id)

        return TaskCreateResponse(id=task_id)

    async def get_assignee_task(self, assignee: str, timeout: int = 30) -> Optional[TaskInfoResponse]:
        result = await self.redis.brpop([f"queue:{assignee}"], timeout=timeout)

        if not result:
            return None

        _list_name, task_id = result
        if isinstance(task_id, bytes):
            task_id = task_id.decode()

        task_key = f"task:{task_id}"

        task_json = await self.redis.get(task_key)
        if not task_json:
            return None

        return TaskInfoResponse.model_validate_json(task_json)
