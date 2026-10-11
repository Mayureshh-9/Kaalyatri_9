import datetime
from sqlalchemy import Column, DateTime, String, Integer

class BaseEntity:
    created_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    created_by = Column(String, nullable=True)
    updated_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)
    updated_by = Column(String, nullable=True)
    user_id = Column(Integer, nullable=True)
