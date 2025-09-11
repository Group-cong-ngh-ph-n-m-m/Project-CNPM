from domain.models.itodo_repository import IRatingRepository
from domain.models.todo import Rating
from typing import List, Optional
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from config import Config
from infrastructure.databases import Base
from infrastructure.databases.mssql import session

load_dotenv()

class RatingRepository(IRatingRepository):
    def __init__(self, session: Session = session):
        self._ratings = []
        self._id_counter = 1
        self.session = session

    def add(self, rating: Rating) -> Rating:
        try:
            self.session.add(rating)
            self.session.commit()
            self.session.refresh(rating)
            return rating
        except Exception as e:
            self.session.rollback()
            raise ValueError('Rating could not be added')
        finally:
            self.session.close()

    def get_by_id(self, rating_id: int) -> Optional[Rating]:
        rating_model = self.session.query(RatingModel).filter_by(id=rating_id).first()
        if rating_model:
            return Rating(
                id=rating_model.id,
                user_id=rating_model.user_id,
                item_id=rating_model.item_id,
                score=rating_model.score,
                comment=rating_model.comment,
                created_at=rating_model.created_at,
                updated_at=rating_model.updated_at
            )
        return None

    def list(self) -> List[Rating]:
        return self._ratings

    def update(self, rating: Rating) -> Rating:
        try:
            rating_model = RatingModel(
                id=rating.id,
                user_id=rating.user_id,
                item_id=rating.item_id,
                score=rating.score,
                comment=rating.comment,
                created_at=rating.created_at,
                updated_at=rating.updated_at
            )
            self.session.merge(rating_model)
            self.session.commit()
            return rating
        except Exception as e:
            self.session.rollback()
            raise ValueError('Rating could not be updated')
        finally:
            self.session.close()

    def delete(self, rating_id: int) -> None:
        self._ratings = [r for r in self._ratings if r.id != rating_id]


class RatingModel(Base):
    __tablename__ = 'ratings'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    item_id = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)
    comment = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
