from sqlalchemy import Column, Integer, String, DateTime
from infrastructure.db import Base
from datetime import datetime

class Moderator(Base):
    __tablename__ = "moderators"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
