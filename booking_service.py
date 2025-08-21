from infrastructure.db import SessionLocal
from domain.booking import Booking

db = SessionLocal()

def create_booking(status: str, total_price: float):
    new_booking = Booking(
        status=status,
        created_at=datetime.now(),
        updated_at=None,
        total_price=total_price
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

def get_bookings():
    return db.query(Booking).all()
