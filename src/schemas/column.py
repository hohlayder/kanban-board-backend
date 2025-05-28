from pydantic import BaseModel, constr
from uuid import UUID
from datetime import datetime
from typing import Optional, List

from src.schemas.task import TaskOut


class ColumnBase(BaseModel):
    name: constr(min_length=1, max_length=50)
    description: Optional[str] = None
    order: Optional[int] = None


class ColumnCreate(ColumnBase):
    project_id: UUID


class ColumnUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=50)] = None
    description: Optional[str] = None
    order: Optional[int] = None


class ColumnOut(ColumnBase):
    id: UUID
    project_id: UUID
    created_at: datetime
    last_updated_at: datetime
    tasks: List[TaskOut] = []

    class Config:
        from_attributes = True
