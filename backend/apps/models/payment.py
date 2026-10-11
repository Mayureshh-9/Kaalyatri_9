import datetime
from .BaseEntity import BaseEntity
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Payment(Base, BaseEntity):
    __tablename__ = "payments"
    __table_args__ = {'schema': 'admin'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("admin.bookings.id"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    status = Column(String(50), default="Pending")
    transaction_id = Column(String(100), unique=True, nullable=True)

    booking = relationship("Booking", backref="payment")
