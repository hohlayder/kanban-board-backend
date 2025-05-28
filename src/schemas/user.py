from pydantic import BaseModel, EmailStr, constr
from uuid import UUID
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: constr(min_length=1, max_length=50)
    description: Optional[constr(min_length=1, max_length=1000)]
    email: EmailStr


class UserCreate(UserBase):
    password: constr(min_length=6, max_length=100)

class UserUpdate(BaseModel):
    username: Optional[constr(min_length=1, max_length=50)] = None
    description: Optional[constr(min_length=1, max_length=1000)] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=6, max_length=100)] = None

class UserOut(UserBase):
    id: UUID
    created_at: datetime
    last_updated_at: datetime

    class Config:
        from_attributes = True
