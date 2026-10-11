import datetime
from .BaseEntity import BaseEntity
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class TourItinerary(Base, BaseEntity):
    __tablename__ = "tour_itineraries"
    __table_args__ = {'schema': 'admin'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    destination_id = Column(Integer, ForeignKey("admin.destinations.id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)

    destination = relationship("Destination", backref="itineraries")
