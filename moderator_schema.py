from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ModeratorSchema(BaseModel):
    id: Optional[int]
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
