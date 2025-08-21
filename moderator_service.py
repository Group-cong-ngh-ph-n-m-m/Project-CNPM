from infrastructure.db import SessionLocal
from domain.moderator import Moderator
from datetime import datetime

db = SessionLocal()

def create_moderator(username: str, email: str):
    new_moderator = Moderator(
        username=username,
        email=email,
        created_at=datetime.now()
    )
    db.add(new_moderator)
    db.commit()
    db.refresh(new_moderator)
    return new_moderator

def get_moderators():
    return db.query(Moderator).all()
