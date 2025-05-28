from pydantic import BaseModel, constr
from uuid import UUID
from datetime import datetime
from typing import Optional


class ProjectBase(BaseModel):
    name: constr(min_length=1, max_length=100)
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectOut(ProjectBase):
    id: UUID
    created_at: datetime
    last_updated_at: datetime

    class Config:
        from_attributes = True
