import datetime
from .BaseEntity import BaseEntity
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class TemporalPass(Base, BaseEntity):
    __tablename__ = "temporal_passes"
    __table_args__ = {'schema': 'admin'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("admin.bookings.id"), nullable=False, unique=True)
    pass_code = Column(String(50), nullable=False, unique=True)
    qr_hash = Column(String(100), nullable=False)
    status = Column(String(30), default="ACTIVE")
    issued_at = Column(DateTime, default=datetime.datetime.utcnow)

    booking = relationship("Booking", backref="pass_ticket")
