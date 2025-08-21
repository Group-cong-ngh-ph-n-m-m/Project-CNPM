from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from infrastructure.databases.base import Base

class AdminModel(Base):
    __tablename__ = 'admin'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_name = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)