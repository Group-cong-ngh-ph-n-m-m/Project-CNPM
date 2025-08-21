from domain.models.user import User
from domain.models.iuser_repository import IUserRepository
from typing import List, Optional

class UserService:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def create_user(self, username: str, email: str, password: str, role: str, created_at, updated_at) -> User:
        user = User(id=None, username=username, email=email, password=password, role=role, created_at=created_at, updated_at=updated_at)
        return self.repository.add(user)

    def get_user(self, user_id: int) -> Optional[User]:
        return self.repository.get_by_id(user_id)

    def list_user(self) -> List[User]:
        return self.repository.list()

    def update_user(self, user_id: int, username: str, email: str, password: str, role: str, created_at, updated_at) -> User:
        user = User(id=user_id, username=username, email=email, password=password, role=role, created_at=created_at, updated_at=updated_at)
        return self.repository.update(user)

    def delete_user(self, user_id: int) -> None:
        self.repository.delete(user_id) 