# domain/models/icomp_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from .complaint import Complaint

class IComplaintRepository(ABC):
    @abstractmethod
    def add(self, complaint: Complaint) -> Complaint:
        pass

    @abstractmethod
    def get_by_id(self, complaint_id: int) -> Optional[Complaint]:
        pass

    @abstractmethod
    def list(self) -> List[Complaint]:
        pass

    @abstractmethod
    def update(self, complaint: Complaint) -> Complaint:
        pass

    @abstractmethod
    def delete(self, complaint_id: int) -> None:
        pass
