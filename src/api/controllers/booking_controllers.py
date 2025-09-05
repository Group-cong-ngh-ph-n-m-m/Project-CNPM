from flask import Blueprint, request, jsonify
from services.booking_service import BookingService
from infrastructure.repositories.booking_respositories import BookingRepository
from api.schemas.booking import BookingRequestSchema, BookingResponseSchema
from datetime import datetime
from infrastructure.databases.mssql import session

bp = Blueprint('booking', __name__, url_prefix='/bookings')

# Khởi tạo service và repository (dùng memory, chưa kết nối DB thật)
booking_service = BookingService(BookingRepository(session))

request_schema = BookingRequestSchema()
response_schema = BookingResponseSchema()

@bp.route('/', methods=['GET'])
def list_bookings():
    """
    Get all bookings
    ---
    get:
      summary: Get all bookings
      tags:
        - Bookings
      responses:
        200:
          description: List of bookings
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/BookingResponse'
    """
    bookings = booking_service.list_bookings()
    return jsonify(response_schema.dump(bookings, many=True)), 200

@bp.route('/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    """
    Get a booking by ID
    ---
    get:
      summary: Get a booking by ID
      tags:
        - Bookings
      parameters:
        - in: path
          name: booking_id
          required: true
          schema:
            type: integer
          description: The ID of the booking to retrieve
      responses:
        200:
          description: Booking found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BookingResponse'
        404:
          description: Booking not found
    """
    booking = booking_service.get_booking(booking_id)
    if not booking:
        return jsonify({'message': 'Booking not found'}), 404
    return jsonify(response_schema.dump(booking)), 200

@bp.route('/', methods=['POST'])
def create_booking():
    """
    Create a new booking
    ---
    post:
      summary: Create a new booking
      tags:
        - Bookings
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BookingRequest'
      responses:
        201:
          description: Booking created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BookingResponse'
        400:
          description: Invalid input
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    now = datetime.utcnow()
    booking = booking_service.create_booking(
        student_id=data['student_id'],
        tutor_id=data['tutor_id'],
        subject_id=data['subject_id'],
        start_time=data['start_time'],
        end_time=data['end_time'],
        status=data['status'],
        created_at=now,
        updated_at=now
    )
    return jsonify(response_schema.dump(booking)), 201

@bp.route('/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    """
    Update an existing booking
    ---
    put:
      summary: Update an existing booking
      tags:
        - Bookings
      parameters:
        - in: path
          name: booking_id
          required: true
          schema:
            type: integer
          description: The ID of the booking to update
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BookingRequest'
      responses:
        200:
          description: Booking updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BookingResponse'
        400:
          description: Invalid input
        404:
          description: Booking not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    booking = booking_service.update_booking(
        booking_id=booking_id,
        student_id=data['student_id'],
        tutor_id=data['tutor_id'],
        subject_id=data['subject_id'],
        start_time=data['start_time'],
        end_time=data['end_time'],
        status=data['status'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    return jsonify(response_schema.dump(booking)), 200

@bp.route('/<int:booking_id>', methods=['PATCH'])
def patch_booking(booking_id):
    """
    Patch an existing booking
    ---
    patch:
      summary: Patch an existing booking
      tags:
        - Bookings
      parameters:
        - in: path
          name: booking_id
          required: true
          schema:
            type: integer
          description: The ID of the booking to patch
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BookingRequest'
      responses:
        200:
          description: Booking patched successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BookingResponse'
        400:
          description: Invalid input
        404:
          description: Booking not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    booking = booking_service.patch_booking(
        booking_id=booking_id,
        student_id=data.get('student_id'),
        tutor_id=data.get('tutor_id'),
        subject_id=data.get('subject_id'),
        start_time=data.get('start_time'),
        end_time=data.get('end_time'),
        status=data.get('status'),
        updated_at=datetime.utcnow()
    )
    return jsonify(response_schema.dump(booking)), 200

@bp.route('/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    """
    Delete a booking
    ---
    delete:
      summary: Delete a booking
      tags:
        - Bookings
      parameters:
        - in: path
          name: booking_id
          required: true
          schema:
            type: integer
          description: The ID of the booking to delete
      responses:
        204:
          description: Booking deleted successfully
        404:
          description: Booking not found
    """
    booking = booking_service.get_booking(booking_id)
    if not booking:
        return jsonify({'message': 'Booking not found'}), 404
    booking_service.delete_booking(booking_id)
    return '', 204
