from pydantic import BaseModel, EmailStr
from datetime import datetime

class NewsletterSubscriberBase(BaseModel):
    email: EmailStr

class NewsletterSubscriberCreate(NewsletterSubscriberBase):
    pass

class NewsletterSubscriberResponse(NewsletterSubscriberBase):
    id: int
    created_date: datetime

    class Config:
        from_attributes = True
