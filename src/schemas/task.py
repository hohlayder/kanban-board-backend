from pydantic import BaseModel, constr
from uuid import UUID
from typing import Optional, List
from datetime import datetime

from src.schemas.task_log import TaskLogOut
from src.schemas.user import UserOut


class TaskBase(BaseModel):
    title: constr(min_length=1, max_length=100)
    description: Optional[str] = None
    status: Optional[str] = "Active"
    priority: Optional[int] = 5


class TaskCreate(TaskBase):
    column_id: UUID


class TaskUpdate(BaseModel):
    title: Optional[constr(min_length=1, max_length=100)] = None
    description: Optional[str] = None
    column_id: Optional[UUID] = None
    status: Optional[str] = None
    priority: Optional[int] = None


class TaskOut(TaskBase):
    id: UUID
    column_id: UUID
    created_at: datetime
    last_updated_at: datetime
    users: List[UserOut] = []
    logs: List[TaskLogOut] = []

    class Config:
        from_attributes = True
