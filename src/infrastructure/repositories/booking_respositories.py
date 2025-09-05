from domain.models.ibooking_repositories import IBookingRepository
from domain.models.booking import Booking
from typing import List, Optional
from dotenv import load_dotenv
import os
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from infrastructure.databases import Base
from sqlalchemy.orm import Session
from infrastructure.databases.mssql import session

load_dotenv()

class BookingRepository(IBookingRepository):
    def __init__(self, session: Session = session):
        self._bookings = []
        self._id_counter = 1
        self.session = session

    def add(self, booking: Booking) -> Booking:
        try:
            self.session.add(booking)
            self.session.commit()
            self.session.refresh(booking)
            return booking
        except Exception as e:
            self.session.rollback()
            raise ValueError('Booking not found')
        finally:
            self.session.close()

    def get_by_id(self, booking_id: int) -> Optional[Booking]:
        booking_model = self.session.query(BookingModel).filter_by(id=booking_id).first()
        if booking_model:
            return Booking(
                id=booking_model.id,
                service_id=booking_model.service_id,
                student_id=booking_model.student_id,
                tutor_profile_id=booking_model.tutor_profile_id,
                status=booking_model.status,
                created_at=booking_model.created_at,
                updated_at=booking_model.updated_at,
                total_price=booking_model.total_price
            )
        return None

    def list(self) -> List[Booking]:
        return self._bookings

    def update(self, booking: Booking) -> Booking:
        try:
            booking_model = BookingModel(
                id=booking.id,
                service_id=booking.service_id,
                student_id=booking.student_id,
                tutor_profile_id=booking.tutor_profile_id,
                status=booking.status,
                created_at=booking.created_at,
                updated_at=booking.updated_at,
                total_price=booking.total_price
            )
            self.session.merge(booking_model)
            self.session.commit()
            return booking
        except Exception as e:
            self.session.rollback()
            raise ValueError('Booking not found')
        finally:
            self.session.close()

    def delete(self, booking_id: int) -> None:
        self._bookings = [b for b in self._bookings if b.id != booking_id] 


class BookingModel(Base):
    __tablename__ = 'bookings'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey('service.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tutor_profile_id = Column(Integer, ForeignKey('tutor_profile.id'), nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    total_price = Column(DECIMAL(10, 2), nullable=False)
