from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, DECIMAL
from infrastructure.databases.base import Base

class ServiceModel(Base):
    __tablename__ = 'service'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    price_per_hour = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)