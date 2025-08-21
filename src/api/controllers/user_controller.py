from flask import Blueprint, request, jsonify
from services.user_service import UserService
from infrastructure.repositories.user_repository import UserRepository
from api.schemas.user import UserRequestSchema, UserResponseSchema
from datetime import datetime
from infrastructure.databases.mssql import session

bp = Blueprint('user', __name__, url_prefix='/users')

# Khởi tạo service và repository (dùng memory, chưa kết nối DB thật)
user_service = UserService(UserRepository(session))

request_schema = UserRequestSchema()
response_schema = UserResponseSchema()

@bp.route('/', methods=['GET'])
def list_users():
    """
    Get all users
    ---
    get:
      summary: Get all users
      tags:
        - Users
      responses:
        200:
          description: List of users
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/UserResponse'
    """
    users = user_service.list_users()
    return jsonify(response_schema.dump(users, many=True)), 200

@bp.route('/<int:todo_id>', methods=['GET'])
def get_user(user_id):
    """ Get a user by ID
    ---
    get:
      summary: Get a user by ID
      tags:
        - Users
      parameters:
        - in: path
          name: user_id
          required: true
          schema:
            type: integer
          description: The ID of the user to retrieve
      responses:
        200:
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        404:
          description: User not found
    """
    user = user_service.get_user(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(response_schema.dump(user)), 200

@bp.route('/', methods=['POST'])
def create_user():
    """ Create a new user
    ---
    post:
      summary: Create a new user
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserRequest'
      responses:
        201:
          description: User created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        400:
          description: Invalid input
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    user = user_service.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        role=data['role'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    return jsonify(response_schema.dump(user)), 201

@bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """ Update an existing user
    ---
    put:
      summary: Update an existing user
      tags:
        - Users
      parameters:
        - in: path
          name: user_id
          required: true
          schema:
            type: integer
          description: The ID of the user to update
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserRequest'
      responses:
        200:
          description: User updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        404:
          description: User not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    user = user_service.update_user(
        user_id=user_id,
        username=data['username'],
        email=data['email'],
        password=data['password'],
        role=data['role'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    return jsonify(response_schema.dump(user)), 200

@bp.route('/<int:user_id>', methods=['PATCH'])
def partial_update_user(user_id):
    """ Partially update an existing user
    ---
    patch:
      summary: Partially update an existing user
      tags:
        - Users
      parameters:
        - in: path
          name: user_id
          required: true
          schema:
            type: integer
          description: The ID of the user to update
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserRequest'
      responses:
        200:
          description: User partially updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        404:
          description: User not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    user = user_service.update_user(
        user_id=user_id,
        username=data.get('username', None),
        email=data.get('email', None),
        password=data.get('password', None),
        role=data.get('role', None),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    return jsonify(response_schema.dump(user)), 200

@bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ Delete a user
    ---
    delete:
      summary: Delete a user
      tags:
        - Users
      parameters:
        - in: path
          name: user_id
          required: true
          schema:
            type: integer
          description: The ID of the user to delete
      responses:
        204:
          description: User deleted successfully
        404:
          description: User not found
    """
    try:
        user_service.delete_user(user_id)
        return '', 204
    except ValueError as e:
        return jsonify({'message': str(e)}), 404 