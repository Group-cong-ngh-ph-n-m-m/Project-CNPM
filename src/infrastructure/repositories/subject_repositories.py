from domain.models.itodo_repository import ISubjectRepository
from domain.models.todo import Subject
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

class SubjectRepository(ISubjectRepository):
    def __init__(self, session: Session = session):
        self._subjects = []
        self._id_counter = 1
        self.session = session

    def add(self, subject: Subject) -> Subject:
        try:
            self.session.add(subject)
            self.session.commit()
            self.session.refresh(subject)
            return subject
        except Exception as e:
            self.session.rollback()
            raise ValueError('Subject not found')
        finally:
            self.session.close()
    #def add(self, todo: Todo) -> Todo:
        #todo.id = self._id_counter
        #self._id_counter += 1
        #self._todos.append(todo)
        #return todo

    def get_by_id(self, subject_id: int) -> Optional[Subject]:
        subject_model = self.session.query(SubjectModel).filter_by(id=subject_id).first()
        if subject_model:
            return Subject(
                id=subject_model.id,
                name=subject_model.name,
                description=subject_model.description
            )
        return None
    
    #def get_by_id(self, todo_id: int) -> Optional[Todo]:
        #todo_model = self.session.query(TodoModel).filter_by(id=todo_id).first()
        
    #def get_by_id(self, todo_id: int) -> Optional[Todo]:
        #for todo in self._todos:
            #if todo.id == todo_id:
                #return todo
        #return None

    def list(self) -> List[Subject]:
        return self._subjects

    def update(self, subject: Subject) -> Subject:
        try:
            subject = SubjectModel(
                id=subject.id,
                name=subject.name,
                description=subject.description
            )
            self.session.merge(subject)
            self.session.commit()
            return subject
        except Exception as e:
            self.session.rollback()
            raise ValueError('Subject not found')
        finally:
            self.session.close()
    #def update(self, todo: Todo) -> Todo:
        #for idx, t in enumerate(self._todos):
            #if t.id == todo.id:
                #self._todos[idx] = todo
                #return todo
        #raise ValueError('Todo not found')

    def delete(self, subject_id: int) -> None:
        self._subjects = [t for t in self._subjects if t.id != subject_id] 

class SubjectModel(Base):
    __tablename__ = 'subjects'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)

    def __init__(self, id: int, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description 