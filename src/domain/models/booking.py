# domain/models/booking.py

class Booking:
    def __init__(
        self,
        id,
        service_id,
        student_id,
        tutor_profile_id,
        status,
        created_at,
        total_price,
        updated_at=None
    ):
        self.id = id
        self.service_id = service_id
        self.student_id = student_id
        self.tutor_profile_id = tutor_profile_id
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.total_price = total_price
