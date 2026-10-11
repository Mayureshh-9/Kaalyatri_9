from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentBase(BaseModel):
    booking_id: int
    amount: float
    status: str = "Pending"
    transaction_id: Optional[str] = None

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: int
    created_date: datetime

    class Config:
        from_attributes = True
