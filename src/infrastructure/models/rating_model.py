from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from infrastructure.databases.base import Base

class RatingModel(Base):
    __tablename__ = 'rating'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('booking.id'), nullable=False)
    student_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tutor_user_id = Column(Integer, ForeignKey('tutor_profile.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False)