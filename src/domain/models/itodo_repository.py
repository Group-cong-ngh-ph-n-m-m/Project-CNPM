from abc import ABC, abstractmethod
from .todo import Todo, Subject, TutorProfile, Message
from typing import List, Optional

class ITodoRepository(ABC):
    @abstractmethod
    def add(self, todo: Todo) -> Todo:
        pass

    @abstractmethod
    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        pass

    @abstractmethod
    def list(self) -> List[Todo]:
        pass

    @abstractmethod
    def update(self, todo: Todo) -> Todo:
        pass

    @abstractmethod
    def delete(self, todo_id: int) -> None:
        pass 
    
class ISubjectRepository(ABC):
    @abstractmethod
    def add(self, subject: 'Subject') -> 'Subject':
        pass

    @abstractmethod
    def get_by_id(self, subject_id: int) -> Optional['Subject']:
        pass

    @abstractmethod
    def list(self) -> List['Subject']:
        pass

    @abstractmethod
    def update(self, subject: 'Subject') -> 'Subject':
        pass

    @abstractmethod
    def delete(self, subject_id: int) -> None:
        pass

class ITutorProfileRepository(ABC):
    @abstractmethod
    def add(self, profile: TutorProfile) -> TutorProfile:
        pass

    @abstractmethod
    def get_by_id(self, profile_id: int) -> Optional[TutorProfile]:
        pass

    @abstractmethod
    def list(self) -> List[TutorProfile]:
        pass

    @abstractmethod
    def update(self, profile: TutorProfile) -> TutorProfile:
        pass

    @abstractmethod
    def delete(self, profile_id: int) -> None:
        pass

class IMessageRepository(ABC):
    @abstractmethod
    def add(self, message: 'Message') -> 'Message':
        pass

    @abstractmethod
    def get_by_id(self, message_id: int) -> Optional['Message']:
        pass

    @abstractmethod
    def list(self) -> List['Message']:
        pass

    @abstractmethod
    def update(self, message: 'Message') -> 'Message':
        pass

    @abstractmethod
    def delete(self, message_id: int) -> None:
        pass
