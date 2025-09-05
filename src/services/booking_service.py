from domain.models.booking import Booking
from domain.models.ibooking_repositories import IBookingRepository
from typing import List, Optional

class BookingService:
    def __init__(self, repository: IBookingRepository):
        self.repository = repository

    def create_booking(
        self,
        service_id: int,
        student_id: int,
        tutor_profile_id: int,
        status: str,
        created_at,
        updated_at,
        total_price
    ) -> Booking:
        booking = Booking(
            id=None,
            service_id=service_id,
            student_id=student_id,
            tutor_profile_id=tutor_profile_id,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            total_price=total_price
        )
        return self.repository.add(booking)

    def get_booking(self, booking_id: int) -> Optional[Booking]:
        return self.repository.get_by_id(booking_id)

    def list_bookings(self) -> List[Booking]:
        return self.repository.list()

    def update_booking(
        self,
        booking_id: int,
        service_id: int,
        student_id: int,
        tutor_profile_id: int,
        status: str,
        created_at,
        updated_at,
        total_price
    ) -> Booking:
        booking = Booking(
            id=booking_id,
            service_id=service_id,
            student_id=student_id,
            tutor_profile_id=tutor_profile_id,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            total_price=total_price
        )
        return self.repository.update(booking)

    def delete_booking(self, booking_id: int) -> None:
        self.repository.delete(booking_id)
