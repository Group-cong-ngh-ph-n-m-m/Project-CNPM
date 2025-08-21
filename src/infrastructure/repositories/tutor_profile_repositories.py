from domain.models.itodo_repository import ITutorProfileRepository
from domain.models.todo import TutorProfile
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

class TutorProfileRepository(ITutorProfileRepository):
    def __init__(self, session: Session = session):
        self._tutor_profiles = []
        self._id_counter = 1
        self.session = session

    def add(self, tutor_profile: TutorProfile) -> TutorProfile:
        try:
            self.session.add(tutor_profile)
            self.session.commit()
            self.session.refresh(tutor_profile)
            return tutor_profile
        except Exception as e:
            self.session.rollback()
            raise ValueError('TutorProfile not found')
        finally:
            self.session.close()
    #def add(self, todo: Todo) -> Todo:
        #todo.id = self._id_counter
        #self._id_counter += 1
        #self._todos.append(todo)
        #return todo

    def get_by_id(self, profile_id: int) -> Optional[TutorProfile]:
        todo_model = self.session.query(TutorProfileModel).filter_by(id=profile_id).first()
        if todo_model:  
            return TutorProfile(
                id=todo_model.id,
                name=todo_model.name,
                email=todo_model.email,
                phone=todo_model.phone
            )
        return None
    
    #def get_by_id(self, todo_id: int) -> Optional[Todo]:
        #todo_model = self.session.query(TodoModel).filter_by(id=todo_id).first()
        
    #def get_by_id(self, todo_id: int) -> Optional[Todo]:
        #for todo in self._todos:
            #if todo.id == todo_id:
                #return todo
        #return None

    def list(self) -> List[TutorProfile]:
        return self._tutor_profiles

    def update(self, tutor_profile: TutorProfile) -> TutorProfile:
        try:
            tutor_profile = TutorProfileModel(
                id=tutor_profile.id,
                name=tutor_profile.name,
                email=tutor_profile.email,
                phone=tutor_profile.phone
            )
            self.session.merge(tutor_profile)
            self.session.commit()
            return tutor_profile
        except Exception as e:
            self.session.rollback()
            raise ValueError('Tutor profile not found')
        finally:
            self.session.close()
    #def update(self, todo: Todo) -> Todo:
        #for idx, t in enumerate(self._todos):
            #if t.id == todo.id:
                #self._todos[idx] = todo
                #return todo
        #raise ValueError('Todo not found')

    def delete(self, tutor_profile_id: int) -> None:
        self._tutor_profiles = [t for t in self._tutor_profiles if t.id != tutor_profile_id] 

class TutorProfileModel(Base):
    __tablename__ = 'tutor_profiles'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=True) 