from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

class BookingBase(BaseModel):
    destination_id: int
    full_name: str
    email: EmailStr
    phone: str
    travelers: int = 1
    travel_date: date
    notes: Optional[str] = None
    status: str = "pending"

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: int
    created_date: datetime

    class Config:
        from_attributes = True
