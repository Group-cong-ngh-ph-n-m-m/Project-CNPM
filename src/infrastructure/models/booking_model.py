from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, DECIMAL
from infrastructure.databases.base import Base

class BookingModel(Base):
    __tablename__ = 'booking'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)
    servicce_id = Column(Integer, ForeignKey('service.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tutor_profile_id = Column(Integer, ForeignKey('tutor_profile.id'), nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    total_price = Column(DECIMAL(10, 2), nullable=False)