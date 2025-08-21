from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from infrastructure.databases.base import Base

class Tutor_profile_Model(Base):
    __tablename__ = 'tutor_profile'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=True)