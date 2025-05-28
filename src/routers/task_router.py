from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user import UserOut
from src.schemas.task import TaskCreate, TaskUpdate, TaskOut
from src.schemas.task_log import TaskLogOut
from src.core.database import get_db
from src.security import get_current_user
from src.models.models import User
from src.crud import task as task_crud

router = APIRouter()


@router.post("/", response_model=TaskOut)
async def create_task(
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await task_crud.create_task(session, task_data)


@router.get("/{task_id}", response_model=TaskOut)
async def get_task(
    task_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = await task_crud.get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/column/{column_id}", response_model=List[TaskOut])
async def get_tasks_by_column(
    column_id: UUID,
    name_contains: Optional[str] = Query(None),
    user_id: Optional[UUID] = Query(None),
    sort_by_create_time: Optional[str] = Query(None, regex="^(asc|desc)$"),
    sort_by_update_time: Optional[str] = Query(None,regex="^(asc|desc)$"),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await task_crud.get_tasks_by_column(
        session,
        column_id,
        name_contains=name_contains,
        user_id=user_id,
        sort_by_create_time=sort_by_create_time,
        sort_by_update_time=sort_by_update_time
    )


@router.put("/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = await task_crud.update_task(session, task_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}")
async def delete_task(
    task_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await task_crud.delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted successfully"}


@router.post("/{task_id}/users/{user_id}")
async def add_user_to_task(
    task_id: UUID,
    user_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await task_crud.add_user_to_task(session, task_id, user_id)
    return {"detail": "User added to task"}


@router.delete("/{task_id}/users/{user_id}")
async def remove_user_from_task(
    task_id: UUID,
    user_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await task_crud.remove_user_from_task(session, task_id, user_id)
    return {"detail": "User removed from task"}


@router.get("/{task_id}/logs", response_model=List[TaskLogOut])
async def get_logs_for_task(
    task_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await task_crud.get_task_logs(session, task_id)


@router.get("/{task_id}/users", response_model=list[UserOut])
async def get_task_users(
    task_id: UUID,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    users = await task_crud.get_users_by_task(session, task_id)
    return users