from flask import Blueprint, request, jsonify
from services.booking_service import create_booking, get_bookings

bp = Blueprint("bookings", __name__, url_prefix="/bookings")

@bp.route("/", methods=["GET"])
def list_bookings():
    bookings = get_bookings()
    return jsonify([{
        "id": b.id,
        "status": b.status,
        "created_at": b.created_at,
        "updated_at": b.updated_at,
        "total_price": float(b.total_price)
    } for b in bookings])

@bp.route("/", methods=["POST"])
def add_booking():
    data = request.get_json()
    booking = create_booking(
        status=data["status"],
        total_price=data["total_price"]
    )
    return jsonify({
        "id": booking.id,
        "status": booking.status,
        "created_at": booking.created_at,
        "updated_at": booking.updated_at,
        "total_price": float(booking.total_price)
    }), 201
