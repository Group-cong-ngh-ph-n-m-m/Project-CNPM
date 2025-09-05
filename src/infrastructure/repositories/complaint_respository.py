# infrastructure/repositories/complaint_repository.py
from domain.models.icomplaint import IComplaintRepository
from domain.models.complaint import Complaint
from typing import List, Optional
from infrastructure.databases.mssql import session
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from infrastructure.databases.base import Base

class ComplaintRepository(IComplaintRepository):
    def __init__(self, session: Session = session):
        self.session = session

    def add(self, complaint: Complaint) -> Complaint:
        complaint_model = ComplaintModel(
            filed_by_user_id=complaint.filed_by_user_id,
            target_user_id=complaint.target_user_id,
            booking_id=complaint.booking_id,
            subject=complaint.subject,
            description=complaint.description,
            status=complaint.status,
            created_at=complaint.created_at,
            resolved_at=complaint.resolved_at
        )
        self.session.add(complaint_model)
        self.session.commit()
        self.session.refresh(complaint_model)
        return Complaint(
            id=complaint_model.id,
            filed_by_user_id=complaint_model.filed_by_user_id,
            target_user_id=complaint_model.target_user_id,
            booking_id=complaint_model.booking_id,
            subject=complaint_model.subject,
            description=complaint_model.description,
            status=complaint_model.status,
            created_at=complaint_model.created_at,
            resolved_at=complaint_model.resolved_at
        )

    def get_by_id(self, complaint_id: int) -> Optional[Complaint]:
        complaint_model = self.session.query(ComplaintModel).filter_by(id=complaint_id).first()
        if complaint_model:
            return Complaint(
                id=complaint_model.id,
                filed_by_user_id=complaint_model.filed_by_user_id,
                target_user_id=complaint_model.target_user_id,
                booking_id=complaint_model.booking_id,
                subject=complaint_model.subject,
                description=complaint_model.description,
                status=complaint_model.status,
                created_at=complaint_model.created_at,
                resolved_at=complaint_model.resolved_at
            )
        return None

    def list(self) -> List[Complaint]:
        complaints = self.session.query(ComplaintModel).all()
        return [
            Complaint(
                id=c.id,
                filed_by_user_id=c.filed_by_user_id,
                target_user_id=c.target_user_id,
                booking_id=c.booking_id,
                subject=c.subject,
                description=c.description,
                status=c.status,
                created_at=c.created_at,
                resolved_at=c.resolved_at
            ) for c in complaints
        ]

    def update(self, complaint: Complaint) -> Complaint:
        complaint_model = self.session.query(ComplaintModel).filter_by(id=complaint.id).first()
        if not complaint_model:
            raise ValueError("Complaint not found")
        complaint_model.subject = complaint.subject
        complaint_model.description = complaint.description
        complaint_model.status = complaint.status
        complaint_model.resolved_at = complaint.resolved_at
        self.session.commit()
        return complaint

    def delete(self, complaint_id: int) -> None:
        complaint_model = self.session.query(ComplaintModel).filter_by(id=complaint_id).first()
        if complaint_model:
            self.session.delete(complaint_model)
            self.session.commit()

class ComplaintModel(Base):
    __tablename__ = 'complaint'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    filed_by_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    target_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    booking_id = Column(Integer, ForeignKey('booking.id'), nullable=False)
    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default='pending')
    created_at = Column(DateTime, nullable=False)
    resolved_at = Column(DateTime, nullable=True)
