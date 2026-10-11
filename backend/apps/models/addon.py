from .BaseEntity import BaseEntity
from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class TemporalAddon(Base, BaseEntity):
    __tablename__ = "temporal_addons"
    __table_args__ = {'schema': 'admin'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    category = Column(String(50), default="Gear")
    description = Column(Text, nullable=True)
    price_inr = Column(Numeric(12, 2), nullable=False)
    icon = Column(String(20), default="🛡️")
    is_mandatory = Column(Boolean, default=False)

class BookingAddon(Base, BaseEntity):
    __tablename__ = "booking_addons"
    __table_args__ = {'schema': 'admin'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("admin.bookings.id"), nullable=False)
    addon_id = Column(Integer, ForeignKey("admin.temporal_addons.id"), nullable=False)
    quantity = Column(Integer, default=1)
    price_at_booking = Column(Numeric(12, 2), nullable=False)

    addon = relationship("TemporalAddon")
