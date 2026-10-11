from .BaseEntity import BaseEntity
from sqlalchemy import Column, Integer, String, Text
from db import Base

class Era(Base, BaseEntity):
    __tablename__ = "eras"
    __table_args__ = {'schema': 'admin'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    icon = Column(String(20), default="⏳")
    description = Column(Text, nullable=True)
    accent_color = Column(String(30), default="#7c4dff")
