from typing import List, Optional, Dict, Any
from domain.admin import Admin
from infrastructure.repositories.admin_repository import AdminRepository
class AdminUseCase:
    def __init__(self, repository: AdminRepository):
        self.repository = repository
    def get_all(self) -> List[Admin]:
        return self.repository.get_all()
    def get_by_id(self, admin_id: int) -> Optional[Admin]:
        return self.repository.get_by_id(admin_id)
    def create(self, data: Dict[str, Any]) -> Admin:
        if "email" not in data or not data["email"]:
            raise ValueError("Email is required")
        return self.repository.create(data)
    def update(self, admin_id: int, data: Dict[str, Any]) -> Optional[Admin]:
        return self.repository.update(admin_id, data)
    def delete(self, admin_id: int) -> bool:
        return self.repository.delete(admin_id)
