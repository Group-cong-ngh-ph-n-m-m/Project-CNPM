from pydantic import BaseModel
from typing import Optional

class RatingSchema(BaseModel):
    id: Optional[int]
    score: int
    comment: Optional[str]

    class Config:
        orm_mode = True
