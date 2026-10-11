import datetime
from .BaseEntity import BaseEntity
from sqlalchemy import Column, Integer, String
from db import Base

class NewsletterSubscriber(Base, BaseEntity):
    __tablename__ = "newsletter_subscribers"
    __table_args__ = {'schema': 'admin'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(150), unique=True, nullable=False)
