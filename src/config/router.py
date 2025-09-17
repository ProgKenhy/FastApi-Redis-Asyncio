from fastapi import APIRouter
from tasks.router import task_router

api_router = APIRouter()

api_router.include_router(task_router, prefix='/task', tags=["tasks"])
