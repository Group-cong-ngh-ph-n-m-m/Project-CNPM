from domain.models.itodo_repository import IReviewRepository
from domain.models.todo import Review
from typing import List, Optional
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from config import Config
from infrastructure.databases import Base
from infrastructure.databases.mssql import session

load_dotenv()

class ReviewRepository(IReviewRepository):
    def __init__(self, session: Session = session):
        self._reviews = []
        self._id_counter = 1
        self.session = session

    def add(self, review: Review) -> Review:
        try:
            self.session.add(review)
            self.session.commit()
            self.session.refresh(review)
            return review
        except Exception as e:
            self.session.rollback()
            raise ValueError('Review could not be added')
        finally:
            self.session.close()

    def get_by_id(self, review_id: int) -> Optional[Review]:
        review_model = self.session.query(ReviewModel).filter_by(id=review_id).first()
        if review_model:
            return Review(
                id=review_model.id,
                user_id=review_model.user_id,
                item_id=review_model.item_id,
                title=review_model.title,
                content=review_model.content,
                rating=review_model.rating,
                created_at=review_model.created_at,
                updated_at=review_model.updated_at
            )
        return None

    def list(self) -> List[Review]:
        return self._reviews

    def update(self, review: Review) -> Review:
        try:
            review_model = ReviewModel(
                id=review.id,
                user_id=review.user_id,
                item_id=review.item_id,
                title=review.title,
                content=review.content,
                rating=review.rating,
                created_at=review.created_at,
                updated_at=review.updated_at
            )
            self.session.merge(review_model)
            self.session.commit()
            return review
        except Exception as e:
            self.session.rollback()
            raise ValueError('Review could not be updated')
        finally:
            self.session.close()

    def delete(self, review_id: int) -> None:
        self._reviews = [r for r in self._reviews if r.id != review_id]


class ReviewModel(Base):
    __tablename__ = 'reviews'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    item_id = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
    rating = Column(Float, nullable=True)
    created_at = Column(DateTime, nullable=False)
