import datetime
from .BaseEntity import BaseEntity
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Booking(Base, BaseEntity):
    __tablename__ = "bookings"
    __table_args__ = {'schema': 'admin'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    destination_id = Column(Integer, ForeignKey("admin.destinations.id"), nullable=False)
    full_name = Column(String(120), nullable=False)
    email = Column(String(150), nullable=False)
    phone = Column(String(30), nullable=False)
    travelers = Column(Integer, nullable=False, default=1)
    travel_date = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)
    status = Column(String(30), default="pending")

    destination = relationship("Destination", backref="bookings")
