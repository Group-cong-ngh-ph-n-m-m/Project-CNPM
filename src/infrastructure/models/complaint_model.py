from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from infrastructure.databases.base import Base

class ComplaintModel(Base):
    __tablename__ = 'complaint'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)
    filed_by_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    target_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    booking_id = Column(Integer, ForeignKey('booking.id'), nullable=False)
    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default='pending')  # Trạng thái của khiếu nại
    created_at = Column(DateTime, nullable=False)
    resolved_at = Column(DateTime, nullable=True)  # Thời gian giải quyết khiếu nại, có thể null nếu chưa giải quyết