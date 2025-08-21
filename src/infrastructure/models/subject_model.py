from sqlalchemy import Column, Integer, String, DateTime
from infrastructure.databases.base import Base

class SubjectModel(Base):
    __tablename__ = 'subject'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)