from flask import Blueprint, request, jsonify
from services.todo_service import TutorProfileService
from infrastructure.repositories.tutor_profile_repositories import TutorProfileRepository
from api.schemas.todo import TutorProfileRequestSchema, TutorProfileResponseSchema
from datetime import datetime
from infrastructure.databases.mssql import session

bp = Blueprint('tutor_profile', __name__, url_prefix='/tutor_profiles')

# Khởi tạo service và repository (dùng memory, chưa kết nối DB thật)
tutor_profile_service = TutorProfileService(TutorProfileRepository(session))

request_schema = TutorProfileRequestSchema()
response_schema = TutorProfileResponseSchema()

@bp.route('/', methods=['GET'])
def list_tutor_profiles():
    """
    Get all tutor profiles
    ---
    get:
      summary: Get all tutor profiles
      tags:
        - Tutor Profiles
      responses:
        200:
          description: List of tutor profiles
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/TutorProfileResponse'
    """
    tutor_profiles = tutor_profile_service.list_tutor_profiles()
    return jsonify(response_schema.dump(tutor_profiles, many=True)), 200

@bp.route('/<int:tutor_profile_id>', methods=['GET'])
def get_tutor_profile(tutor_profile_id):
    """ Get a tutor profile by ID
    ---
    get:
      summary: Get a tutor profile by ID
      tags:
        - Tutor Profiles
      parameters:
        - in: path
          name: tutor_profile_id
          required: true
          schema:
            type: integer
          description: The ID of the tutor profile to retrieve
      responses:
        200:
          description: Tutor profile found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TutorProfileResponse'
        404:
          description: Tutor profile not found
    """
    tutor_profile = tutor_profile_service.get_tutor_profile(tutor_profile_id)
    if not tutor_profile:
        return jsonify({'message': 'Tutor profile not found'}), 404
    return jsonify(response_schema.dump(tutor_profile)), 200

@bp.route('/', methods=['POST'])
def create_tutor_profile():
    """ Create a new tutor profile
    ---
    post:
      summary: Create a new tutor profile
      tags:
        - Tutor Profiles
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TutorProfileRequest'
      responses:
        201:
          description: Tutor profile created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TutorProfileResponse'
        400:
          description: Invalid input
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    tutor_profile = tutor_profile_service.create_tutor_profile(
        name=data['name'],
        email=data['email'],
        phone=data['phone']
    )
    return jsonify(response_schema.dump(tutor_profile)), 201

@bp.route('/<int:tutor_profile_id>', methods=['PUT'])
def update_tutor_profile(tutor_profile_id):
    """ Update an existing tutor profile
    ---
    put:
      summary: Update an existing tutor profile
      tags:
        - Tutor Profiles
      parameters:
        - in: path
          name: tutor_profile_id
          required: true
          schema:
            type: integer
          description: The ID of the tutor profile to update
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TutorProfileRequest'
      responses:
        200:
          description: Tutor profile updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TutorProfileResponse'
        400:
          description: Invalid input
        404:
          description: Tutor profile not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    tutor_profile = tutor_profile_service.update_tutor_profile(
        tutor_profile_id=tutor_profile_id,
        name=data['name'],
        email=data['email'],
        phone=data['phone']
    )
    return jsonify(response_schema.dump(tutor_profile)), 200

@bp.route('/<int:tutor_profile_id>', methods=['PATCH'])
def patch_tutor_profile(tutor_profile_id):
    """ Patch an existing tutor profile
    ---
    patch:
      summary: Patch an existing tutor profile
      tags:
        - Tutor Profiles
      parameters:
        - in: path
          name: tutor_profile_id
          required: true
          schema:
            type: integer
          description: The ID of the tutor profile to patch
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TutorProfileRequest'
      responses:
        200:
          description: Tutor profile patched successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TutorProfileResponse'
        404:
          description: Tutor profile not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    tutor_profile = tutor_profile_service.update_tutor_profile(
        tutor_profile_id=tutor_profile_id,
        name=data.get('name', None),
        email=data.get('email', None),
        phone=data.get('phone', None)
    )
    return jsonify(response_schema.dump(tutor_profile)), 200

@bp.route('/<int:tutor_profile_id>', methods=['DELETE'])
def delete_tutor_profile(tutor_profile_id):
    """ Delete a tutor profile
    ---
    delete:
      summary: Delete a tutor profile
      tags:
        - Tutor Profiles
      parameters:
        - in: path
          name: tutor_profile_id
          required: true
          schema:
            type: integer
          description: The ID of the tutor profile to delete
      responses:
        204:
          description: Tutor profile deleted successfully
        404:
          description: Tutor profile not found
    """
    success = tutor_profile_service.delete_tutor_profile(tutor_profile_id)
    if not success:
        return jsonify({'message': 'Tutor profile not found'}), 404
    return '', 204