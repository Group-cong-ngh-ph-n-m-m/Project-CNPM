from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db import Base
from datetime import datetime

class Complain(Base):
    __tablename__ = "complains"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    # Ví dụ: complain do user gửi -> liên kết user_id
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="complains")
