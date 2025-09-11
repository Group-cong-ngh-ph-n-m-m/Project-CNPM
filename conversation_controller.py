from flask import Blueprint, request, jsonify
from services.todo_service import ConversationService
from infrastructure.repositories.conversation_respositories import ConversationRepository
from api.schemas.todo import ConversationRequestSchema, ConversationResponseSchema
from datetime import datetime
from infrastructure.databases.mssql import session

bp = Blueprint('conversation', __name__, url_prefix='/conversations')

# Khởi tạo service và repository
conversation_service = ConversationService(ConversationRepository(session))

request_schema = ConversationRequestSchema()
response_schema = ConversationResponseSchema()

@bp.route('/', methods=['GET'])
def list_conversations():
    """
    Get all conversations
    ---
    get:
      summary: Get all conversations
      tags:
        - Conversations
      parameters:
        - in: query
          name: user_id
          schema:
            type: integer
          description: Filter conversations by user ID
        - in: query
          name: is_active
          schema:
            type: boolean
          description: Filter conversations by active status
      responses:
        200:
          description: List of conversations
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ConversationResponse'
    """
    user_id = request.args.get('user_id', type=int)
    is_active = request.args.get('is_active', type=lambda v: v.lower() == 'true' if v else None)
    
    conversations = conversation_service.list_conversations(user_id, is_active)
    return jsonify(response_schema.dump(conversations, many=True)), 200

@bp.route('/<int:conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """ Get a conversation by ID
    ---
    get:
      summary: Get a conversation by ID
      tags:
        - Conversations
      parameters:
        - in: path
          name: conversation_id
          required: true
          schema:
            type: integer
          description: The ID of the conversation to retrieve
      responses:
        200:
          description: Conversation found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ConversationResponse'
        404:
          description: Conversation not found
    """
    conversation = conversation_service.get_conversation(conversation_id)
    if not conversation:
        return jsonify({'error': 'Conversation not found'}), 404
    return jsonify(response_schema.dump(conversation)), 200

@bp.route('/', methods=['POST'])
def create_conversation():
    """ Create a new conversation
    ---
    post:
      summary: Create a new conversation
      tags:
        - Conversations
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ConversationRequest'
      responses:
        201:
          description: Conversation created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ConversationResponse'
        400:
          description: Invalid input
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    conversation = conversation_service.create_conversation(
        title=data.get('title'),
        created_by=data['created_by'],
        is_group=data.get('is_group', False),
        is_active=data.get('is_active', True)
    )
    return jsonify(response_schema.dump(conversation)), 201

@bp.route('/<int:conversation_id>', methods=['PUT'])
def update_conversation(conversation_id):
    """ Update an existing conversation
    ---
    put:
      summary: Update an existing conversation
      tags:
        - Conversations
      parameters:
        - in: path
          name: conversation_id
          required: true
          schema:
            type: integer
          description: The ID of the conversation to update
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ConversationRequest'
      responses:
        200:
          description: Conversation updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ConversationResponse'
        404:
          description: Conversation not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    conversation = conversation_service.update_conversation(
        conversation_id=conversation_id,
        title=data.get('title'),
        is_group=data.get('is_group'),
        is_active=data.get('is_active')
    )
    
    if not conversation:
        return jsonify({'error': 'Conversation not found'}), 404
        
    return jsonify(response_schema.dump(conversation)), 200

@bp.route('/<int:conversation_id>', methods=['PATCH'])
def patch_conversation(conversation_id):
    """ Patch an existing conversation
    ---
    patch:
      summary: Patch an existing conversation
      tags:
        - Conversations
      parameters:
        - in: path
          name: conversation_id
          required: true
          schema:
            type: integer
          description: The ID of the conversation to patch
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ConversationRequest'
      responses:
        200:
          description: Conversation patched successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ConversationResponse'
        404:
          description: Conversation not found
    """
    data = request.get_json()
    errors = request_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    
    conversation = conversation_service.patch_conversation(
        conversation_id=conversation_id,
        title=data.get('title'),
        is_group=data.get('is_group'),
        is_active=data.get('is_active')
    )
    
    if not conversation:
        return jsonify({'error': 'Conversation not found'}), 404
        
    return jsonify(response_schema.dump(conversation)), 200

@bp.route('/<int:conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    """ Delete a conversation
    ---
    delete:
      summary: Delete a conversation
      tags:
        - Conversations
      parameters:
        - in: path
          name: conversation_id
          required: true
          schema:
            type: integer
          description: The ID of the conversation to delete
      responses:
        204:
          description: Conversation deleted successfully
        404:
          description: Conversation not found
    """
    success = conversation_service.delete_conversation(conversation_id)
    if not success:
        return jsonify({'error': 'Conversation not found'}), 404
    return '', 204

@bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_conversations(user_id):
    """ Get all conversations for a specific user
    ---
    get:
      summary: Get all conversations for a specific user
      tags:
        - Conversations
      parameters:
        - in: path
          name: user_id
          required: true
          schema:
            type: integer
          description: The ID of the user
        - in: query
          name: is_active
          schema:
            type: boolean
          description: Filter conversations by active status
      responses:
        200:
          description: List of user conversations
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ConversationResponse'
    """
    is_active = request.args.get('is_active', type=lambda v: v.lower() == 'true' if v else None)
    conversations = conversation_service.get_user_conversations(user_id, is_active)
    return jsonify(response_schema.dump(conversations, many=True)), 200

@bp.route('/<int:conversation_id>/participants', methods=['POST'])
def add_participant(conversation_id):
    """ Add a participant to a conversation
    ---
    post:
      summary: Add a participant to a conversation
      tags:
        - Conversations
      parameters:
        - in: path
          name: conversation_id
          required: true
          schema:
            type: integer
          description: The ID of the conversation
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                user_id:
                  type: integer
                  description: The ID of the user to add
              required:
                - user_id
      responses:
        200:
          description: Participant added successfully
        404:
          description: Conversation not found
        400:
          description: Invalid input
    """
    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({'error': 'User ID is required'}), 400
    
    success = conversation_service.add_participant(conversation_id, data['user_id'])
    if not success:
        return jsonify({'error': 'Conversation not found or user already added'}), 404
        
    return jsonify({'message': 'Participant added successfully'}), 200

@bp.route('/<int:conversation_id>/participants/<int:user_id>', methods=['DELETE'])
def remove_participant(conversation_id, user_id):
    """ Remove a participant from a conversation
    ---
    delete:
      summary: Remove a participant from a conversation
      tags:
        - Conversations
      parameters:
        - in: path
          name: conversation_id
          required: true
          schema:
            type: integer
          description: The ID of the conversation
        - in: path
          name: user_id
          required: true
          schema:
            type: integer
          description: The ID of the user to remove
      responses:
        200:
          description: Participant removed successfully
        404:
          description: Conversation or participant not found
    """
    success = conversation_service.remove_participant(conversation_id, user_id)
    if not success:
        return jsonify({'error': 'Conversation or participant not found'}), 404
        
    return jsonify({'message': 'Participant removed successfully'}), 200
