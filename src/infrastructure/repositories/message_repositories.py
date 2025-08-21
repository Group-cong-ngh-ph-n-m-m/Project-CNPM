from domain.models.itodo_repository import IMessageRepository
from domain.models.todo import Message
from typing import List, Optional
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Config
from sqlalchemy import Column, Integer, String, DateTime
from infrastructure.databases import Base
from sqlalchemy.orm import Session
from infrastructure.databases.mssql import session

load_dotenv()

class MessageRepository(IMessageRepository):
    def __init__(self, session: Session = session):
        self._todos = []
        self._id_counter = 1
        self.session = session

    def add(self, message: Message) -> Message:
        try:
            self.session.add(message)
            self.session.commit()
            self.session.refresh(message)
            return message
        except Exception as e:
            self.session.rollback()
            raise ValueError('Message not found')
        finally:
            self.session.close()
    #def add(self, todo: Todo) -> Todo:
        #todo.id = self._id_counter
        #self._id_counter += 1
        #self._todos.append(todo)
        #return todo

    def get_by_id(self, message_id: int) -> Optional[Message]:
        message_model = self.session.query(MessageModel).filter_by(id=message_id).first()
        if message_model:
            return Message(
                id=message_model.id,
                content=message_model.content,
                sender_id=message_model.sender_id,
                receiver_id=message_model.receiver_id,
                created_at=message_model.created_at
            )
        return None
    
    #def get_by_id(self, todo_id: int) -> Optional[Todo]:
        #todo_model = self.session.query(TodoModel).filter_by(id=todo_id).first()
        
    #def get_by_id(self, todo_id: int) -> Optional[Todo]:
        #for todo in self._todos:
            #if todo.id == todo_id:
                #return todo
        #return None

    def list(self) -> List[Message]:
        return self._messages

    def update(self, message: Message) -> Message:
        try:
            message = MessageModel(
                id=message.id,
                content=message.content,
                sender_id=message.sender_id,
                receiver_id=message.receiver_id,
                created_at=message.created_at,
                updated_at=message.updated_at
            )
            self.session.merge(message)
            self.session.commit()
            return message
        except Exception as e:
            self.session.rollback()
            raise ValueError('Message not found')
        finally:
            self.session.close()
    #def update(self, todo: Todo) -> Todo:
        #for idx, t in enumerate(self._todos):
            #if t.id == todo.id:
                #self._todos[idx] = todo
                #return todo
        #raise ValueError('Todo not found')

    def delete(self, message_id: int) -> None:
        self._messages = [t for t in self._messages if t.id != message_id] 

class MessageModel(Base):
    __tablename__ = 'messages'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(255), nullable=False)
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)