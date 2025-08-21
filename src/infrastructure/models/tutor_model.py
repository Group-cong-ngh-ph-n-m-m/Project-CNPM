from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from infrastructure.databases.base import Base

class TutorModel(Base):
    __tablename__ = 'tutor'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    tutor_profile_id = Column(Integer, ForeignKey('tutor_profile.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subject.id'), nullable=False)
    proficiency_level = Column(String(50), nullable=False)