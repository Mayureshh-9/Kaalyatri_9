from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DestinationBase(BaseModel):
    name: str
    era: str
    year_label: str
    short_description: str
    description: str
    price_inr: float
    duration_days: int = 7
    difficulty: str = "Moderate"
    image_emoji: str = "🌍"
    accent_color: str = "#7c4dff"
    highlights: Optional[str] = None
    is_featured: bool = False

class DestinationCreate(DestinationBase):
    pass

class DestinationResponse(DestinationBase):
    id: int
    created_date: datetime

    class Config:
        from_attributes = True
