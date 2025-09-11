from domain.models.itodo_repository import IConversationRepository
from domain.models.todo import Conversation
from typing import List, Optional
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from config import Config
from infrastructure.databases import Base
from infrastructure.databases.mssql import session

load_dotenv()

class ConversationRepository(IConversationRepository):
    def __init__(self, session: Session = session):
        self._conversations = []
        self._id_counter = 1
        self.session = session

    def add(self, conversation: Conversation) -> Conversation:
        try:
            self.session.add(conversation)
            self.session.commit()
            self.session.refresh(conversation)
            return conversation
        except Exception as e:
            self.session.rollback()
            raise ValueError('Conversation could not be added')
        finally:
            self.session.close()

    def get_by_id(self, conversation_id: int) -> Optional[Conversation]:
        conversation_model = self.session.query(ConversationModel).filter_by(id=conversation_id).first()
        if conversation_model:
            return Conversation(
                id=conversation_model.id,
                sender_id=conversation_model.sender_id,
                receiver_id=conversation_model.receiver_id,
                message=conversation_model.message,
                created_at=conversation_model.created_at,
                updated_at=conversation_model.updated_at
            )
        return None

    def list(self) -> List[Conversation]:
        return self._conversations

    def update(self, conversation: Conversation) -> Conversation:
        try:
            conversation_model = ConversationModel(
                id=conversation.id,
                sender_id=conversation.sender_id,
                receiver_id=conversation.receiver_id,
                message=conversation.message,
                created_at=conversation.created_at,
                updated_at=conversation.updated_at
            )
            self.session.merge(conversation_model)
            self.session.commit()
            return conversation
        except Exception as e:
            self.session.rollback()
            raise ValueError('Conversation could not be updated')
        finally:
            self.session.close()

    def delete(self, conversation_id: int) -> None:
        self._conversations = [c for c in self._conversations if c.id != conversation_id]


class ConversationModel(Base):
    __tablename__ = 'conversations'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)
    message = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
