from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReviewSchema(BaseModel):
    id: Optional[int]
    content: str
    created_at: datetime

    class Config:
        orm_mode = True
