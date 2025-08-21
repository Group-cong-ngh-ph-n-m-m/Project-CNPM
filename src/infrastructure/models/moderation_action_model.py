from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from infrastructure.databases.base import Base

class Moderation_actionModel(Base):
    __tablename__ = 'moderation_action'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)
    moderation_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    target_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    complaint_id = Column(Integer, ForeignKey('complaint.id'), nullable=False)
    action_type = Column(String(50), nullable=False)  # Ví dụ: 'ban
    action_deltail = Column(Text, nullable=True)  # Chi tiết về hành động
    action_at = Column(DateTime, nullable=False)  # Thời gian thực hiện hành động