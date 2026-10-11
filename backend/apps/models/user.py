import datetime
from .BaseEntity import BaseEntity
from sqlalchemy import Column, Integer, String, Boolean
from db import Base

class User(Base, BaseEntity):
    __tablename__ = "users"
    __table_args__ = {'schema': 'admin'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(150), unique=True, nullable=False)
    full_name = Column(String(120), nullable=False)
    phone = Column(String(30), nullable=True)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
