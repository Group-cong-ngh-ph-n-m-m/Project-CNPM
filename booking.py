from sqlalchemy import Column, Integer, String, DateTime, DECIMAL
from infrastructure.db import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    total_price = Column(DECIMAL(10, 2), nullable=False)
