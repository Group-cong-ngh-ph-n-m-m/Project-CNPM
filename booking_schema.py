from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookingSchema(BaseModel):
    id: Optional[int]
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    total_price: float

    class Config:
        orm_mode = True  # để đọc được từ SQLAlchemy model
