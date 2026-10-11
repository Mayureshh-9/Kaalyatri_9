from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ContactMessageBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    subject: Optional[str] = None
    message: str
    is_read: bool = False

class ContactMessageCreate(ContactMessageBase):
    pass

class ContactMessageResponse(ContactMessageBase):
    id: int
    created_date: datetime

    class Config:
        from_attributes = True
