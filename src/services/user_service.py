from domain.models.user import User, Admin
from domain.models.iuser_repository import IUserRepository, IAdminRepository
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

class AdminService:
    def __init__(self, repository: IAdminRepository):
        self.repository = repository

    def create_admin(self, user_id: int, username: str, email: str) -> Admin:
        admin = Admin(id=None, user_id=user_id, username=username, email=email)
        return self.repository.add(admin)

    def get_admin(self, admin_id: int) -> Optional[Admin]:
        return self.repository.get_by_id(admin_id)

    def list_admins(self) -> List[Admin]:
        return self.repository.list()

    def update_admin(self, admin_id: int, user_id: int, username: str, email: str) -> Admin:
        admin = Admin(id=admin_id, user_id=user_id, username=username, email=email)
        return self.repository.update(admin)

    def delete_admin(self, admin_id: int) -> None:
        self.repository.delete(admin_id)