from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class TaskLogBase(BaseModel):
    message: str


class TaskLogCreate(TaskLogBase):
    task_id: UUID


class TaskLogOut(TaskLogBase):
    id: UUID
    task_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
