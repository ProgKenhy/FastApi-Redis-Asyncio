from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class TaskInfo(BaseModel):
    id: str = Field(description="ID задачи")
    assignee: str = Field(description="Исполнитель задачи")
    task_name: str = Field(max_length=255, description="Название задачи")
    created_at: datetime = Field(description="Дата и время создания задачи")
    model_config = ConfigDict(from_attributes=True)


class TaskCreate(BaseModel):
    assignee: str = Field(description="Исполнитель задачи")
    task_name: str = Field(max_length=255, description="Название задачи")
    model_config = ConfigDict(from_attributes=True)


# class TaskAssigneeGet(BaseModel):
#     assignee: str = Field(description="Исполнитель задачи")
#     timeout: int = Field(gt=0, description="Время ожидания задачи")
#     model_config = ConfigDict(from_attributes=True)

class TaskCreateResponse(BaseModel):
    id: str = Field(description="ID задачи")
    model_config = ConfigDict(from_attributes=True)


class TaskInfoResponse(BaseModel):
    assignee: str = Field(description="Исполнитель задачи")
    task_name: str = Field(description="Название задачи")
    created_at: datetime = Field(description="Дата и время создания задачи")
    model_config = ConfigDict(from_attributes=True)
