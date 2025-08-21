from flask import Blueprint, request, jsonify
from services.user_service import AdminService
from infrastructure.repositories.admin_repositories import AdminRepository
from api.schemas.user import AdminRequestSchema, AdminResponseSchema
from datetime import datetime
from infrastructure.databases.mssql import session

bp = Blueprint('admin', __name__, url_prefix='/admins')

# Khởi tạo service và repository (dùng memory, chưa kết nối DB thật)
admin_service = AdminService(AdminRepository(session))

request_schema = AdminRequestSchema()
response_schema = AdminResponseSchema()

@bp.route('/', methods=['GET'])
def list_admins():
    """
    Get all admins
    ---
    get:
      summary: Get all admins
      tags:
        - Admins
      responses:
        200:
          description: List of admins
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/AdminResponse'
    """
    admins = admin_service.list_admins()
    return jsonify(response_schema.dump(admins, many=True)), 200

@bp.route('/<int:admin_id>', methods=['GET'])
def get_admin(admin_id):
    """ Get an admin by ID
    ---
    get:
      summary: Get an admin by ID
      tags:
        - Admins
      parameters:
        - in: path
          name: admin_id
          required: true
          schema:
            type: integer
          description: The ID of the admin to retrieve
      responses:
        200:
          description: Admin found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminResponse'
        404:
          description: Admin not found
    """
    admin = admin_service.get_admin(admin_id)
    if not admin:
        return jsonify({'error': 'Admin not found'}), 404
    return jsonify(response_schema.dump(admin)), 200

@bp.route('/', methods=['POST'])
def create_admin():
    """ Create a new admin
    ---
    post:
      summary: Create a new admin
      tags:
        - Admins
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AdminRequest'
      responses:
        201:
          description: Admin created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminResponse'
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    admin = admin_service.create_admin(
        user_id=data.get('user_id'),
        username=data.get('username'),
        email=data.get('email')
    )
    return jsonify(response_schema.dump(admin)), 201

@bp.route('/<int:admin_id>', methods=['PUT'])
def update_admin(admin_id):
    """ Update an existing admin
    ---
    put:
      summary: Update an existing admin
      tags:
        - Admins
      parameters:
        - in: path
          name: admin_id
          required: true
          schema:
            type: integer
          description: The ID of the admin to update
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AdminRequest'
      responses:
        200:
          description: Admin updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminResponse'
        404:
          description: Admin not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    admin = admin_service.update_admin(
        admin_id=admin_id,
        user_id=data.get('user_id'),
        username=data.get('username'),
        email=data.get('email')
    )
    return jsonify(response_schema.dump(admin)), 200

@bp.route('/<int:admin_id>', methods=['PATCH'])
def patch_admin(admin_id):
    """ Patch an existing admin
    ---
    patch:
      summary: Patch an existing admin
      tags:
        - Admins
      parameters:
        - in: path
          name: admin_id
          required: true
          schema:
            type: integer
          description: The ID of the admin to patch
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AdminRequest'
      responses:
        200:
          description: Admin patched successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminResponse'
        404:
          description: Admin not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    admin = admin_service.patch_admin(
        admin_id=admin_id,
        user_id=data.get('user_id'),
        username=data.get('username'),
        email=data.get('email')
    )
    return jsonify(response_schema.dump(admin)), 200

@bp.route('/<int:admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    """ Delete an admin by ID
    ---
    delete:
      summary: Delete an admin by ID
      tags:
        - Admins
      parameters:
        - in: path
          name: admin_id
          required: true
          schema:
            type: integer
          description: The ID of the admin to delete
      responses:
        204:
          description: Admin deleted successfully
        404:
          description: Admin not found
    """
    if not admin_service.delete_admin(admin_id):
        return jsonify({'error': 'Admin not found'}), 404
    return '', 204