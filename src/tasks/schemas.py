from datetime import datetime

from pydantic import BaseModel, Field


class TaskInfo(BaseModel):
    id: str = Field(description="ID задачи")
    assignee: str = Field(description="Исполнитель задачи")
    task_name: str = Field(max_length=255, description="Название задачи")
    created_at: datetime = Field(description="Дата и время создания задачи")


class TaskCreate(BaseModel):
    assignee: str = Field(description="Исполнитель задачи")
    task_name: str = Field(max_length=255, description="Название задачи")


# class TaskAssigneeGet(BaseModel):
#     assignee: str = Field(description="Исполнитель задачи")
#     timeout: int = Field(gt=0, description="Время ожидания задачи")

class TaskCreateResponse(BaseModel):
    id: str = Field(description="ID задачи")


class TaskInfoResponse(BaseModel):
    assignee: str = Field(description="Исполнитель задачи")
    task_name: str = Field(description="Название задачи")
    created_at: datetime = Field(description="Дата и время создания задачи")
