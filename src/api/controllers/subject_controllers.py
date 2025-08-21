from flask import Blueprint, request, jsonify
from services.todo_service import SubjectService
from infrastructure.repositories.subject_repositories import SubjectRepository
from api.schemas.todo import SubjectRequestSchema, SubjectResponseSchema
from datetime import datetime
from infrastructure.databases.mssql import session

bp = Blueprint('subject', __name__, url_prefix='/subjects')

# Khởi tạo service và repository (dùng memory, chưa kết nối DB thật)
subject_service = SubjectService(SubjectRepository(session))

request_schema = SubjectRequestSchema()
response_schema = SubjectResponseSchema()

@bp.route('/', methods=['GET'])
def list_subjects():
    """
    Get all subjects
    ---
    get:
      summary: Get all subjects
      tags:
        - Subjects
      responses:
        200:
          description: List of subjects
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/SubjectResponse'
    """
    subjects = subject_service.list_subjects()
    return jsonify(response_schema.dump(subjects, many=True)), 200

@bp.route('/<int:subject_id>', methods=['GET'])
def get_subject(subject_id):
    """ Get a subject by ID
    ---
    get:
      summary: Get a subject by ID
      tags:
        - Subjects
      parameters:
        - in: path
          name: subject_id
          required: true
          schema:
            type: integer
          description: The ID of the subject to retrieve
      responses:
        200:
          description: Subject found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SubjectResponse'
        404:
          description: Subject not found
    """
    subject = subject_service.get_subject(subject_id)
    if not subject:
        return jsonify({'message': 'Subject not found'}), 404
    return jsonify(response_schema.dump(subject)), 200

@bp.route('/', methods=['POST'])
def create_subject():
    """ Create a new subject
    ---
    post:
      summary: Create a new subject
      tags:
        - Subjects
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SubjectRequest'
      responses:
        201:
          description: Subject created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SubjectResponse'
        400:
          description: Invalid input
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    subject = subject_service.create_subject(
        name=data['name'],
        description=data['description']
    )
    return jsonify(response_schema.dump(subject)), 201

@bp.route('/<int:subject_id>', methods=['PUT'])
def update_todo(subject_id):
    """ Update an existing subject
    ---
    put:
      summary: Update an existing subject
      tags:
        - Subjects
      parameters:
        - in: path
          name: subject_id
          required: true
          schema:
            type: integer
          description: The ID of the subject to update
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SubjectRequest'
      responses:
        200:
          description: Subject updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SubjectResponse'
        400:
          description: Invalid input
        404:
          description: Subject not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    subject = subject_service.update_subject(
        subject_id=subject_id,
        name=data['name'],
        description=data['description']
    )
    return jsonify(response_schema.dump(subject)), 200

@bp.route('/<int:subject_id>', methods=['PATCH'])
def patch_subject(subject_id):
    """ Patch an existing subject
    ---
    patch:
      summary: Patch an existing subject
      tags:
        - Subjects
      parameters:
        - in: path
          name: subject_id
          required: true
          schema:
            type: integer
          description: The ID of the subject to patch
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SubjectRequest'
      responses:
        200:
          description: Subject patched successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SubjectResponse'
        404:
          description: Subject not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    subject = subject_service.update_subject(
        subject_id=subject_id,
        name=data.get('name', ''),
        description=data.get('description', '')
    )
    return jsonify(response_schema.dump(subject)), 200

@bp.route('/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    """ Delete a subject
    ---
    delete:
      summary: Delete a subject
      tags:
        - Subjects
      parameters:
        - in: path
          name: subject_id
          required: true
          schema:
            type: integer
          description: The ID of the subject to delete
      responses:
        204:
          description: Subject deleted successfully
        404:
          description: Subject not found
    """
    subject_service.delete_subject(subject_id)
    return '', 204 