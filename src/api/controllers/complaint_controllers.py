# api/routes/complaint.py
from flask import Blueprint, request, jsonify
from services.complaint_service import ComplaintService
from infrastructure.repositories.complaint_respository import ComplaintRepository
from api.schemas.complaint import ComplaintRequestSchema, ComplaintResponseSchema
from datetime import datetime
from infrastructure.databases.mssql import session

bp = Blueprint('complaint', __name__, url_prefix='/complaints')

complaint_service = ComplaintService(ComplaintRepository(session))

request_schema = ComplaintRequestSchema()
response_schema = ComplaintResponseSchema()

@bp.route('/', methods=['GET'])
def list_complaints():
    """
    Get all complaints
    ---
    get:
      summary: Get all complaints
      tags:
        - Complaints
      responses:
        200:
          description: List of complaints
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ComplaintResponse'
    """
    complaints = complaint_service.list_complaints()
    return jsonify(response_schema.dump(complaints, many=True)), 200

@bp.route('/<int:complaint_id>', methods=['GET'])
def get_complaint(complaint_id):
    """
    Get a complaint by ID
    ---
    get:
      summary: Get a complaint by ID
      tags:
        - Complaints
      parameters:
        - in: path
          name: complaint_id
          required: true
          schema:
            type: integer
          description: The ID of the complaint to retrieve
      responses:
        200:
          description: Complaint found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ComplaintResponse'
        404:
          description: Complaint not found
    """
    complaint = complaint_service.get_complaint(complaint_id)
    if not complaint:
        return jsonify({'message': 'Complaint not found'}), 404
    return jsonify(response_schema.dump(complaint)), 200

@bp.route('/', methods=['POST'])
def create_complaint():
    """
    Create a new complaint
    ---
    post:
      summary: Create a new complaint
      tags:
        - Complaints
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ComplaintRequest'
      responses:
        201:
          description: Complaint created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ComplaintResponse'
        400:
          description: Invalid input
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    now = datetime.utcnow()
    complaint = complaint_service.create_complaint(
        filed_by_user_id=data['filed_by_user_id'],
        target_user_id=data['target_user_id'],
        booking_id=data['booking_id'],
        subject=data['subject'],
        description=data['description'],
        status=data['status'],
        created_at=now
    )
    return jsonify(response_schema.dump(complaint)), 201

@bp.route('/<int:complaint_id>', methods=['PUT'])
def update_complaint(complaint_id):
    """
    Update an existing complaint
    ---
    put:
      summary: Update an existing complaint
      tags:
        - Complaints
      parameters:
        - in: path
          name: complaint_id
          required: true
          schema:
            type: integer
          description: The ID of the complaint to update
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ComplaintRequest'
      responses:
        200:
          description: Complaint updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ComplaintResponse'
        400:
          description: Invalid input
        404:
          description: Complaint not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    complaint = complaint_service.get_complaint(complaint_id)
    if not complaint:
        return jsonify({'message': 'Complaint not found'}), 404

    complaint.subject = data['subject']
    complaint.description = data['description']
    complaint.status = data['status']
    complaint.resolved_at = data.get('resolved_at', complaint.resolved_at)

    updated_complaint = complaint_service.update_complaint(complaint)
    return jsonify(response_schema.dump(updated_complaint)), 200

@bp.route('/<int:complaint_id>', methods=['DELETE'])
def delete_complaint(complaint_id):
    """
    Delete a complaint
    ---
    delete:
      summary: Delete a complaint
      tags:
        - Complaints
      parameters:
        - in: path
          name: complaint_id
          required: true
          schema:
            type: integer
          description: The ID of the complaint to delete
      responses:
        204:
          description: Complaint deleted successfully
        404:
          description: Complaint not found
    """
    complaint = complaint_service.get_complaint(complaint_id)
    if not complaint:
        return jsonify({'message': 'Complaint not found'}), 404
    complaint_service.delete_complaint(complaint_id)
    return '', 204
