from fastapi import APIRouter
from . import auth_router, project_router, user_router, column_router, task_router

router = APIRouter()

router.include_router(auth_router.router, prefix="/auth", tags=["auth"])
router.include_router(project_router.router, prefix="/projects", tags=["projects"])
router.include_router(user_router.router, prefix="/users", tags=["users"])
router.include_router(column_router.router, prefix="/columns", tags=["columns"])
router.include_router(task_router.router, prefix="/tasks", tags=["tasks"])