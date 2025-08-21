from datetime import datetime
from infrastructure.db import SessionLocal
from domain.rating import Rating

db = SessionLocal()

def create_rating(score: int, comment: str = None):
    new_rating = Rating(
        score=score,
        comment=comment,
        created_at=datetime.now()
    )
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating

def get_ratings():
    return db.query(Rating).all()

def get_rating(rating_id: int):
    return db.query(Rating).filter_by(id=rating_id).first()

def update_rating(rating_id: int, score: int, comment: str = None):
    rating = db.query(Rating).filter_by(id=rating_id).first()
    if not rating:
        return None
    rating.score = score
    rating.comment = comment
    db.commit()
    db.refresh(rating)
    return rating

def delete_rating(rating_id: int):
    rating = db.query(Rating).filter_by(id=rating_id).first()
    if not rating:
        return False
    db.delete(rating)
    db.commit()
    return True
