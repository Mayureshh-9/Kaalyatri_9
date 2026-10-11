from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    destination_id: int
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    created_date: datetime

    class Config:
        from_attributes = True
