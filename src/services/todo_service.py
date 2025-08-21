from domain.models.todo import Todo, Subject, TutorProfile, Message
from domain.models.itodo_repository import ITodoRepository, ISubjectRepository, ITutorProfileRepository, IMessageRepository
from typing import List, Optional

class TodoService:
    def __init__(self, repository: ITodoRepository):
        self.repository = repository

    def create_todo(self, title: str, description: str, status: str, created_at, updated_at) -> Todo:
        todo = Todo(id=None, title=title, description=description, status=status, created_at=created_at, updated_at=updated_at)
        return self.repository.add(todo)

    def get_todo(self, todo_id: int) -> Optional[Todo]:
        return self.repository.get_by_id(todo_id)

    def list_todos(self) -> List[Todo]:
        return self.repository.list()

    def update_todo(self, todo_id: int, title: str, description: str, status: str, created_at, updated_at) -> Todo:
        todo = Todo(id=todo_id, title=title, description=description, status=status, created_at=created_at, updated_at=updated_at)
        return self.repository.update(todo)

    def delete_todo(self, todo_id: int) -> None:
        self.repository.delete(todo_id) 

class SubjectService:
    def __init__(self, repository: ISubjectRepository):
        self.repository = repository

    def create_subject(self, name: str, description: str) -> Subject:
        subject = Subject(id=None, name=name, description=description)
        return self.repository.add(subject)

    def get_subject(self, subject_id: int) -> Optional[Subject]:
        return self.repository.get_by_id(subject_id)

    def list_subjects(self) -> List[Subject]:
        return self.repository.list()

    def update_subject(self, subject_id: int, name: str, description: str) -> Subject:
        subject = Subject(id=subject_id, name=name, description=description)
        return self.repository.update(subject)

    def delete_subject(self, subject_id: int) -> None:
        self.repository.delete(subject_id)

class TutorProfileService:
    def __init__(self, repository: ITutorProfileRepository):
        self.repository = repository

    def create_profile(self, name: str, email: str, phone: str) -> TutorProfile:
        profile = TutorProfile(id=None, name=name, email=email, phone=phone)
        return self.repository.add(profile)

    def get_profile(self, profile_id: int) -> Optional[TutorProfile]:
        return self.repository.get_by_id(profile_id)

    def list_profiles(self) -> List[TutorProfile]:
        return self.repository.list()

    def update_profile(self, profile_id: int, name: str, email: str, phone: str) -> TutorProfile:
        profile = TutorProfile(id=profile_id, name=name, email=email, phone=phone)
        return self.repository.update(profile)

    def delete_profile(self, profile_id: int) -> None:
        self.repository.delete(profile_id)

class MessageService:
    def __init__(self, repository: IMessageRepository):
        self.repository = repository

    def create_message(self, content: str, sender_id: int, receiver_id: int, created_at, updated_at) -> Message:
        message = Message(id=None, content=content, sender_id=sender_id, receiver_id=receiver_id, created_at=created_at, updated_at=updated_at)
        return self.repository.add(message)

    def get_message(self, message_id: int) -> Optional[Message]:
        return self.repository.get_by_id(message_id)

    def list_messages(self) -> List[Message]:
        return self.repository.list()

    def update_message(self, message_id: int, content: str, sender_id: int, receiver_id: int, created_at, updated_at) -> Message:
        message = Message(id=message_id, content=content, sender_id=sender_id, receiver_id=receiver_id, created_at=created_at, updated_at=updated_at)
        return self.repository.update(message)

    def delete_message(self, message_id: int) -> None:
        self.repository.delete(message_id)