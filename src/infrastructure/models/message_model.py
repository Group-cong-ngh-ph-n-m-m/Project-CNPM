from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from infrastructure.databases.base import Base

class MessageModel(Base):
    __tablename__ = 'message'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey('conversation.id'), nullable=False)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    message_text = Column(Text, nullable=False)
    attachment_url = Column(String(255), nullable=True)
    sent_at = Column(DateTime, nullable=False)