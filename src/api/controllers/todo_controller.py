from flask import Blueprint, request, jsonify
from services.todo_service import TodoService
from infrastructure.repositories.todo_repository import TodoRepository
from api.schemas.todo import TodoRequestSchema, TodoResponseSchema
from datetime import datetime
from infrastructure.databases.mssql import session

bp = Blueprint('todo', __name__, url_prefix='/todos')

# Khởi tạo service và repository (dùng memory, chưa kết nối DB thật)
todo_service = TodoService(TodoRepository(session))

request_schema = TodoRequestSchema()
response_schema = TodoResponseSchema()

@bp.route('/', methods=['GET'])
def list_todos():
    """
    Get all todos
    ---
    get:
      summary: Get all todos
      tags:
        - Todos
      responses:
        200:
          description: List of todos
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/TodoResponse'
    """
    todos = todo_service.list_todos()
    return jsonify(response_schema.dump(todos, many=True)), 200

@bp.route('/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """ Get a todo by ID
    ---
    get:
      summary: Get a todo by ID
      tags:
        - Todos
      parameters:
        - in: path
          name: todo_id
          required: true
          schema:
            type: integer
          description: The ID of the todo to retrieve
      responses:
        200:
          description: Todo found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TodoResponse'
        404:
          description: Todo not found
    """
    todo = todo_service.get_todo(todo_id)
    if not todo:
        return jsonify({'message': 'Todo not found'}), 404
    return jsonify(response_schema.dump(todo)), 200

@bp.route('/', methods=['POST'])
def create_todo():
    """
    Create a new todo
    ---
    post:
        summary: Create a new todo
        tags:
          - Todos
        requestBody:
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TodoRequest'
        responses:
          201:
            description: Todo created successfully
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/TodoResponse'
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    now = datetime.utcnow()
    todo = todo_service.create_todo(
        title=data['title'],
        description=data['description'],
        status=data['status'],
        created_at=now,
        updated_at=now
    )
    return jsonify(response_schema.dump(todo)), 201

@bp.route('/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """ Update an existing todo
    ---
    put:
      summary: Update an existing todo
      tags:
        - Todos
      parameters:
        - in: path
          name: todo_id
          required: true
          schema:
            type: integer
          description: The ID of the todo to update
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TodoRequest'
      responses:
        200:
          description: Todo updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TodoResponse'
        400:
          description: Invalid input
        404:
          description: Todo not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    todo = todo_service.update_todo(
        todo_id=todo_id,
        title=data['title'],
        description=data['description'],
        status=data['status'],
        created_at=datetime.utcnow(),  # Có thể lấy từ DB nếu cần
        updated_at=datetime.utcnow()
    )
    return jsonify(response_schema.dump(todo)), 200

@bp.route('/<int:todo_id>', methods=['PATCH'])
def patch_todo(todo_id):
    """ Patch an existing todo
    ---
    patch:
      summary: Patch an existing todo
      tags:
        - Todos
      parameters:
        - in: path
          name: todo_id
          required: true
          schema:
            type: integer
          description: The ID of the todo to patch
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TodoRequest'
      responses:
        200:
          description: Todo patched successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TodoResponse'
        400:
          description: Invalid input
        404:
          description: Todo not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    todo = todo_service.patch_todo(
        todo_id=todo_id,
        title=data.get('title'),
        description=data.get('description'),
        status=data.get('status'),
        updated_at=datetime.utcnow()
    )
    return jsonify(response_schema.dump(todo)), 200

@bp.route('/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """ Delete a todo
    ---
    delete:
      summary: Delete a todo
      tags:
        - Todos
      parameters:
        - in: path
          name: todo_id
          required: true
          schema:
            type: integer
          description: The ID of the todo to delete
      responses:
        204:
          description: Todo deleted successfully
        404:
          description: Todo not found
    """
    todo = todo_service.get_todo(todo_id)
    if not todo:
        return jsonify({'message': 'Todo not found'}), 404
    todo_service.delete_todo(todo_id)
    return '', 204 