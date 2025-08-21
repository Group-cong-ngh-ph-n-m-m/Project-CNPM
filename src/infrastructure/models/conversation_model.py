from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, DECIMAL
from infrastructure.databases.base import Base

class ConversationModel(Base):
    __tablename__ = 'conversation'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('booking.id'), nullable=False)
    created_at = Column(DateTime, nullable=False)