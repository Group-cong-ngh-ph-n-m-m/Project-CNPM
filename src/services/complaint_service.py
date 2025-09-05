# services/complaint_service.py
from domain.models.complaint import Complaint
from domain.models.icomplaint import IComplaintRepository
from typing import List, Optional
from datetime import datetime

class ComplaintService:
    def __init__(self, repository: IComplaintRepository):
        self.repository = repository

    def create_complaint(
        self,
        filed_by_user_id: int,
        target_user_id: int,
        booking_id: int,
        subject: str,
        description: str,
        status: str,
        created_at=datetime.utcnow(),
        resolved_at=None
    ) -> Complaint:
        complaint = Complaint(
            id=None,
            filed_by_user_id=filed_by_user_id,
            target_user_id=target_user_id,
            booking_id=booking_id,
            subject=subject,
            description=description,
            status=status,
            created_at=created_at,
            resolved_at=resolved_at
        )
        return self.repository.add(complaint)

    def get_complaint(self, complaint_id: int) -> Optional[Complaint]:
        return self.repository.get_by_id(complaint_id)

    def list_complaints(self) -> List[Complaint]:
        return self.repository.list()

    def update_complaint(self, complaint: Complaint) -> Complaint:
        return self.repository.update(complaint)

    def delete_complaint(self, complaint_id: int) -> None:
        self.repository.delete(complaint_id)
