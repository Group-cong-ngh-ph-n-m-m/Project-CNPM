from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ComplainSchema(BaseModel):
    id: Optional[int]
    title: str
    description: str
    status: str
    created_at: datetime
    user_id: Optional[int]

    class Config:
        orm_mode = True
