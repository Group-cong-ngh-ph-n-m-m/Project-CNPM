# domain/models/complaint.py
class Complaint:
    def __init__(
        self,
        id: int,
        filed_by_user_id: int,
        target_user_id: int,
        booking_id: int,
        subject: str,
        description: str,
        status: str,
        created_at,
        resolved_at=None
    ):
        self.id = id
        self.filed_by_user_id = filed_by_user_id
        self.target_user_id = target_user_id
        self.booking_id = booking_id
        self.subject = subject
        self.description = description
        self.status = status
        self.created_at = created_at
        self.resolved_at = resolved_at
