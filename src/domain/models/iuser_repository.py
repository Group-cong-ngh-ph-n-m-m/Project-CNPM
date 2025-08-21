from abc import ABC, abstractmethod
from .user import User, Admin
from typing import List, Optional

class IUserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def list(self) -> List[User]:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass 

class IAdminRepository(ABC):
    @abstractmethod
    def add(self, admin: Admin) -> Admin:
        pass

    @abstractmethod
    def get_by_id(self, admin_id: int) -> Optional[Admin]:
        pass

    @abstractmethod
    def list(self) -> List[Admin]:
        pass

    @abstractmethod
    def update(self, admin: Admin) -> Admin:
        pass

    @abstractmethod
    def delete(self, admin_id: int) -> None:
        pass