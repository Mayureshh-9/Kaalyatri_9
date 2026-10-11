import datetime
from .BaseEntity import BaseEntity
from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean
from db import Base

class Destination(Base, BaseEntity):
    __tablename__ = "destinations"
    __table_args__ = {'schema': 'admin'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    era = Column(String(100), nullable=False)
    year_label = Column(String(50), nullable=False)
    short_description = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price_inr = Column(Numeric(12, 2), nullable=False)
    duration_days = Column(Integer, nullable=False, default=7)
    difficulty = Column(String(50), default="Moderate")
    image_emoji = Column(String(20), default="🌍")
    accent_color = Column(String(20), default="#7c4dff")
    highlights = Column(Text)
    is_featured = Column(Boolean, default=False)
