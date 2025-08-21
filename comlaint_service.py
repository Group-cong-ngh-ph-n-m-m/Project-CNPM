from infrastructure.db import SessionLocal
from domain.complain import Complain
from datetime import datetime

db = SessionLocal()

def create_complain(title: str, description: str, user_id: int):
    new_complain = Complain(
        title=title,
        description=description,
        status="pending",
        created_at=datetime.now(),
        user_id=user_id
    )
    db.add(new_complain)
    db.commit()
    db.refresh(new_complain)
    return new_complain

def get_complains():
    return db.query(Complain).all()
