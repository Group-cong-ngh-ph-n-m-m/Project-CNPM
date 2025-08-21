from datetime import datetime
from infrastructure.db import SessionLocal
from domain.review import Review

db = SessionLocal()

def create_review(content: str):
    new_review = Review(
        content=content,
        created_at=datetime.now()
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

def get_reviews():
    return db.query(Review).all()

def get_review(review_id: int):
    return db.query(Review).filter_by(id=review_id).first()

def update_review(review_id: int, content: str):
    review = db.query(Review).filter_by(id=review_id).first()
    if not review:
        return None
    review.content = content
    db.commit()
    db.refresh(review)
    return review

def delete_review(review_id: int):
    review = db.query(Review).filter_by(id=review_id).first()
    if not review:
        return False
    db.delete(review)
    db.commit()
    return True
