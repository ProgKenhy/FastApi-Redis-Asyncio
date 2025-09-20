from fastapi import APIRouter, Depends, HTTPException

from config.auth import get_current_user
from tasks.schemas import TaskCreate, TaskCreateResponse, TaskInfoResponse
from tasks.service import TaskService
from .dependencies import get_task_service

task_router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    dependencies=[Depends(get_current_user)]
)


@task_router.post('', response_model=TaskCreateResponse)
async def create_task(body: TaskCreate, task_service: TaskService = Depends(get_task_service)):
    new_task = await task_service.create_task(task_data=body)
    return new_task


@task_router.get('/{assignee}', response_model=TaskInfoResponse)
async def get_assignee_task(assignee: str, timeout: int, task_service: TaskService = Depends(get_task_service)):
    try:
        task = await task_service.get_assignee_task(assignee=assignee, timeout=timeout)
        if not task:
            raise HTTPException(
                status_code=404,
                detail="Задачи нет для данного исполнителя"
            )
        return TaskInfoResponse(
            assignee=task.assignee,
            task_name=task.task_name,
            created_at=task.created_at,
        )


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
