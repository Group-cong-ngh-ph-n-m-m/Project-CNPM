from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from infrastructure.databases.base import Base

class VideoModel(Base):
    __tablename__ = 'video'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    url = Column(String(255), nullable=False)
    tutor_profile_id = Column(Integer, ForeignKey('tutor_profile.id'), nullable=False)
    is_public = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False)