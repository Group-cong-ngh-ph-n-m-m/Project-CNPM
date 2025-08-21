from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ConversationSchema(BaseModel):
    id: Optional[int]
    topic: str
    created_at: datetime

    class Config:
        orm_mode = True
