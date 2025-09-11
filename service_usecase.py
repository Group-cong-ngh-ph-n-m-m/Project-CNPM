from typing import List, Optional, Dict, Any
from domain.service import Service
from infrastructure.repositories.service_repository import ServiceRepository

class ServiceUseCase:
    def __init__(self, repository: ServiceRepository):
        self.repository = repository
    def get_all(self) -> List[Service]:
        return self.repository.get_all()
    def get_by_id(self, service_id: int) -> Optional[Service]:
        return self.repository.get_by_id(service_id)
    def create(self, data: Dict[str, Any]) -> Service:
        if "name" not in data or not data["name"]:
            raise ValueError("Service name is required")
        if "price" in data and data["price"] is not None and data["price"] < 0:
            raise ValueError("Price must be non-negative")
        return self.repository.create(data)
    def update(self, service_id: int, data: Dict[str, Any]) -> Optional[Service]:
        return self.repository.update(service_id, data)
    def delete(self, service_id: int) -> bool:
        return self.repository.delete(service_id)



