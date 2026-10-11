from pydantic import BaseModel
from datetime import datetime

class TourItineraryBase(BaseModel):
    destination_id: int
    day_number: int
    title: str
    description: str

class TourItineraryCreate(TourItineraryBase):
    pass

class TourItineraryResponse(TourItineraryBase):
    id: int
    created_date: datetime

    class Config:
        from_attributes = True
