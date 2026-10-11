import datetime
from .BaseEntity import BaseEntity
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Review(Base, BaseEntity):
    __tablename__ = "reviews"
    __table_args__ = {'schema': 'admin'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    destination_id = Column(Integer, ForeignKey("admin.destinations.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)

    destination = relationship("Destination", backref="reviews")
