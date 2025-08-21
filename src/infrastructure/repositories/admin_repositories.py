from domain.models.iuser_repository import IAdminRepository
from domain.models.user import Admin
from typing import List, Optional
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Config
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from infrastructure.databases import Base
from sqlalchemy.orm import Session
from infrastructure.databases.mssql import session

load_dotenv()

class AdminRepository(IAdminRepository):
    def __init__(self, session: Session = session):
        self._messages = []
        self._id_counter = 1
        self.session = session

    def add(self, admin: Admin) -> Admin:
        try:
            self.session.add(admin)
            self.session.commit()
            self.session.refresh(admin)
            return admin
        except Exception as e:
            self.session.rollback()
            raise ValueError('Admin not found')
        finally:
            self.session.close()
    #def add(self, todo: Todo) -> Todo:
        #todo.id = self._id_counter
        #self._id_counter += 1
        #self._todos.append(todo)
        #return todo

    def get_by_id(self, admin_id: int) -> Optional[Admin]:
        admin_model = self.session.query(AdminModel).filter_by(id=admin_id).first()
        if admin_model:
            return Admin(
                id=admin_model.id,
                user_id=admin_model.user_id,
                username=admin_model.user_name,
                email=admin_model.email
            )
        return None
    
    #def get_by_id(self, todo_id: int) -> Optional[Todo]:
        #todo_model = self.session.query(TodoModel).filter_by(id=todo_id).first()
        
    #def get_by_id(self, todo_id: int) -> Optional[Todo]:
        #for todo in self._todos:
            #if todo.id == todo_id:
                #return todo
        #return None

    def list(self) -> List[Admin]:
        return self._messages

    def update(self, admin: Admin) -> Admin:
        try:
            admin = AdminModel(
                id=admin.id,
                user_id=admin.user_id,
                user_name=admin.username,
                email=admin.email
            )
            self.session.merge(admin)
            self.session.commit()
            return admin
        except Exception as e:
            self.session.rollback()
            raise ValueError('Admin not found')
        finally:
            self.session.close()
    #def update(self, todo: Todo) -> Todo:
        #for idx, t in enumerate(self._todos):
            #if t.id == todo.id:
                #self._todos[idx] = todo
                #return todo
        #raise ValueError('Todo not found')

    def delete(self, admin_id: int) -> None:
        self._admins = [t for t in self._admins if t.id != admin_id] 

class AdminModel(Base):
    __tablename__ = 'admins'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_name = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)