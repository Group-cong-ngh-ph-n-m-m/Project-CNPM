from flask import Blueprint, request, jsonify
from services.todo_service import MessageService
from infrastructure.repositories.message_repositories import MessageRepository
from api.schemas.todo import MessageRequestSchema, MessageResponseSchema
from datetime import datetime
from infrastructure.databases.mssql import session

bp = Blueprint('message', __name__, url_prefix='/messages')

# Khởi tạo service và repository (dùng memory, chưa kết nối DB thật)
message_service = MessageService(MessageRepository(session))

request_schema = MessageRequestSchema()
response_schema = MessageResponseSchema()

@bp.route('/', methods=['GET'])
def list_messages():
    """
    Get all messages
    ---
    get:
      summary: Get all messages
      tags:
        - Messages
      responses:
        200:
          description: List of messages
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/MessageResponse'
    """
    messages = message_service.list_messages()
    return jsonify(response_schema.dump(messages, many=True)), 200

@bp.route('/<int:message_id>', methods=['GET'])
def get_message(message_id):
    """ Get a message by ID
    ---
    get:
      summary: Get a message by ID
      tags:
        - Messages
      parameters:
        - in: path
          name: message_id
          required: true
          schema:
            type: integer
          description: The ID of the message to retrieve
      responses:
        200:
          description: Message found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MessageResponse'
        404:
          description: Message not found
    """
    message = message_service.get_message(message_id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    return jsonify(response_schema.dump(message)), 200

@bp.route('/', methods=['POST'])
def create_message():
    """ Create a new message
    ---
    post:
      summary: Create a new message
      tags:
        - Messages
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MessageRequest'
      responses:
        201:
          description: Message created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MessageResponse'
        400:
          description: Invalid input
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    message = message_service.create_message(
        content=data['content'],
        sender_id=data['sender_id'],
        receiver_id=data['receiver_id']
    )
    return jsonify(response_schema.dump(message)), 201

@bp.route('/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    """ Update an existing message
    ---
    put:
      summary: Update an existing message
      tags:
        - Messages
      parameters:
        - in: path
          name: message_id
          required: true
          schema:
            type: integer
          description: The ID of the message to update
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MessageRequest'
      responses:
        200:
          description: Message updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MessageResponse'
        404:
          description: Message not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    message = message_service.update_message(
        message_id=message_id,
        content=data.get('content', ''),
        sender_id=data.get('sender_id'),
        receiver_id=data.get('receiver_id')
    )
    return jsonify(response_schema.dump(message)), 200

@bp.route('/<int:message_id>', methods=['PATCH'])
def patch_message(message_id):
    """ Patch an existing message
    ---
    patch:
      summary: Patch an existing message
      tags:
        - Messages
      parameters:
        - in: path
          name: message_id
          required: true
          schema:
            type: integer
          description: The ID of the message to patch
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MessageRequest'
      responses:
        200:
          description: Message patched successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MessageResponse'
        404:
          description: Message not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    message = message_service.patch_message(
        message_id=message_id,
        content=data.get('content', None),
        sender_id=data.get('sender_id', None),
        receiver_id=data.get('receiver_id', None)
    )
    return jsonify(response_schema.dump(message)), 200

@bp.route('/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    """ Delete a message
    ---
    delete:
      summary: Delete a message
      tags:
        - Messages
      parameters:
        - in: path
          name: message_id
          required: true
          schema:
            type: integer
          description: The ID of the message to delete
      responses:
        204:
          description: Message deleted successfully
        404:
          description: Message not found
    """
    message_service.delete_message(message_id)
    return '', 204