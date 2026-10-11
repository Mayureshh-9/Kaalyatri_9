import datetime
from .BaseEntity import BaseEntity
from sqlalchemy import Column, Integer, String, Text, Boolean
from db import Base

class ContactMessage(Base, BaseEntity):
    __tablename__ = "contact_messages"
    __table_args__ = {'schema': 'admin'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    email = Column(String(150), nullable=False)
    phone = Column(String(30), nullable=True)
    subject = Column(String(200), nullable=True)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
