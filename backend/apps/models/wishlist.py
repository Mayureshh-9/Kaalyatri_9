from .BaseEntity import BaseEntity
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class UserWishlist(Base, BaseEntity):
    __tablename__ = "user_wishlists"
    __table_args__ = {'schema': 'admin'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("admin.users.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("admin.destinations.id"), nullable=False)

    destination = relationship("Destination")
