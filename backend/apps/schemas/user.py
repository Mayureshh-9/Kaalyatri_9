from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    is_admin: bool = False

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_date: datetime

    class Config:
        from_attributes = True
