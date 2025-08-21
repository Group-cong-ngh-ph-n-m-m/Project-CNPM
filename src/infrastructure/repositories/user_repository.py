from domain.models.iuser_repository import IUserRepository
from domain.models.user import User
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

class UserRepository(IUserRepository):
    def __init__(self, session: Session = session):
        self._users = []
        self._id_counter = 1
        self.session = session

    def add(self, user: User) -> User:
        try:
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except Exception as e:
            self.session.rollback()
            raise ValueError('User not found')
        finally:
            self.session.close()
    #def add(self, todo: Todo) -> Todo:
        #todo.id = self._id_counter
        #self._id_counter += 1
        #self._todos.append(todo)
        #return todo

    def get_by_id(self, user_id: int) -> Optional[User]:
        user_model = self.session.query(UserModel).filter_by(id=user_id).first()
        if user_model:
            return User(
                id=user_model.id,
                username=user_model.username,
                email=user_model.email,
                created_at=user_model.created_at,
                updated_at=user_model.updated_at
            )
        return None
    
    #def get_by_id(self, todo_id: int) -> Optional[Todo]:
        #todo_model = self.session.query(TodoModel).filter_by(id=todo_id).first()
        
    #def get_by_id(self, todo_id: int) -> Optional[Todo]:
        #for todo in self._todos:
            #if todo.id == todo_id:
                #return todo
        #return None

    def list(self) -> List[User]:
        user_models = self.session.query(UserModel).all()
        return [
            User(
                id=user_model.id,
                username=user_model.username,
                email=user_model.email,
                created_at=user_model.created_at,
                updated_at=user_model.updated_at
            ) for user_model in user_models
        ]

    def update(self, user: User) -> User:
        try:
            self.session.query(UserModel).filter_by(id=user.id).update({
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }
            )
            self.session.merge(user)
            self.session.commit()
            return user
        except Exception as e:
            self.session.rollback()
            raise ValueError('User not found')
        finally:
            self.session.close()
    #def update(self, todo: Todo) -> Todo:
        #for idx, t in enumerate(self._todos):
            #if t.id == todo.id:
                #self._todos[idx] = todo
                #return todo
        #raise ValueError('Todo not found')

    def delete(self, users_id: int) -> None:
        self._users = [t for t in self._users if t.id != users_id] 

class UserModel(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime, nullable=True) 