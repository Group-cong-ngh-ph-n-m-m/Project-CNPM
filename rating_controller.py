from flask import Blueprint, request, jsonify
from services.todo_service import RatingService
from infrastructure.repositories.rating_repositories import RatingRepository
from api.schemas.todo import RatingRequestSchema, RatingResponseSchema
from datetime import datetime
from infrastructure.databases.mssql import session

bp = Blueprint('rating', __name__, url_prefix='/ratings')

# Khởi tạo service và repository
rating_service = RatingService(RatingRepository(session))

request_schema = RatingRequestSchema()
response_schema = RatingResponseSchema()

@bp.route('/', methods=['GET'])
def list_ratings():
    """
    Get all ratings
    ---
    get:
      summary: Get all ratings
      tags:
        - Ratings
      parameters:
        - in: query
          name: rated_entity_type
          schema:
            type: string
          description: Filter ratings by entity type (e.g., 'product', 'service', 'user')
        - in: query
          name: rated_entity_id
          schema:
            type: integer
          description: Filter ratings by entity ID
        - in: query
          name: user_id
          schema:
            type: integer
          description: Filter ratings by user ID
        - in: query
          name: min_rating
          schema:
            type: integer
          description: Minimum rating value (1-5)
        - in: query
          name: max_rating
          schema:
            type: integer
          description: Maximum rating value (1-5)
      responses:
        200:
          description: List of ratings
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/RatingResponse'
    """
    rated_entity_type = request.args.get('rated_entity_type')
    rated_entity_id = request.args.get('rated_entity_id', type=int)
    user_id = request.args.get('user_id', type=int)
    min_rating = request.args.get('min_rating', type=int)
    max_rating = request.args.get('max_rating', type=int)
    
    ratings = rating_service.list_ratings(
        rated_entity_type=rated_entity_type,
        rated_entity_id=rated_entity_id,
        user_id=user_id,
        min_rating=min_rating,
        max_rating=max_rating
    )
    return jsonify(response_schema.dump(ratings, many=True)), 200

@bp.route('/<int:rating_id>', methods=['GET'])
def get_rating(rating_id):
    """ Get a rating by ID
    ---
    get:
      summary: Get a rating by ID
      tags:
        - Ratings
      parameters:
        - in: path
          name: rating_id
          required: true
          schema:
            type: integer
          description: The ID of the rating to retrieve
      responses:
        200:
          description: Rating found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RatingResponse'
        404:
          description: Rating not found
    """
    rating = rating_service.get_rating(rating_id)
    if not rating:
        return jsonify({'error': 'Rating not found'}), 404
    return jsonify(response_schema.dump(rating)), 200

@bp.route('/', methods=['POST'])
def create_rating():
    """ Create a new rating
    ---
    post:
      summary: Create a new rating
      tags:
        - Ratings
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RatingRequest'
      responses:
        201:
          description: Rating created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RatingResponse'
        400:
          description: Invalid input
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    rating = rating_service.create_rating(
        user_id=data['user_id'],
        rated_entity_type=data['rated_entity_type'],
        rated_entity_id=data['rated_entity_id'],
        rating_value=data['rating_value'],
        comment=data.get('comment'),
        is_approved=data.get('is_approved', True)
    )
    return jsonify(response_schema.dump(rating)), 201

@bp.route('/<int:rating_id>', methods=['PUT'])
def update_rating(rating_id):
    """ Update an existing rating
    ---
    put:
      summary: Update an existing rating
      tags:
        - Ratings
      parameters:
        - in: path
          name: rating_id
          required: true
          schema:
            type: integer
          description: The ID of the rating to update
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RatingRequest'
      responses:
        200:
          description: Rating updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RatingResponse'
        404:
          description: Rating not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    rating = rating_service.update_rating(
        rating_id=rating_id,
        rating_value=data.get('rating_value'),
        comment=data.get('comment'),
        is_approved=data.get('is_approved')
    )
    
    if not rating:
        return jsonify({'error': 'Rating not found'}), 404
        
    return jsonify(response_schema.dump(rating)), 200

@bp.route('/<int:rating_id>', methods=['PATCH'])
def patch_rating(rating_id):
    """ Patch an existing rating
    ---
    patch:
      summary: Patch an existing rating
      tags:
        - Ratings
      parameters:
        - in: path
          name: rating_id
          required: true
          schema:
            type: integer
          description: The ID of the rating to patch
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RatingRequest'
      responses:
        200:
          description: Rating patched successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RatingResponse'
        404:
          description: Rating not found
    """
    data = request.get_json()
    errors = request_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    
    rating = rating_service.patch_rating(
        rating_id=rating_id,
        rating_value=data.get('rating_value'),
        comment=data.get('comment'),
        is_approved=data.get('is_approved')
    )
    
    if not rating:
        return jsonify({'error': 'Rating not found'}), 404
        
    return jsonify(response_schema.dump(rating)), 200

@bp.route('/<int:rating_id>', methods=['DELETE'])
def delete_rating(rating_id):
    """ Delete a rating
    ---
    delete:
      summary: Delete a rating
      tags:
        - Ratings
      parameters:
        - in: path
          name: rating_id
          required: true
          schema:
            type: integer
          description: The ID of the rating to delete
      responses:
        204:
          description: Rating deleted successfully
        404:
          description: Rating not found
    """
    success = rating_service.delete_rating(rating_id)
    if not success:
        return jsonify({'error': 'Rating not found'}), 404
    return '', 204

@bp.route('/entity/<string:entity_type>/<int:entity_id>', methods=['GET'])
def get_entity_ratings(entity_type, entity_id):
    """ Get all ratings for a specific entity
    ---
    get:
      summary: Get all ratings for a specific entity
      tags:
        - Ratings
      parameters:
        - in: path
          name: entity_type
          required: true
          schema:
            type: string
          description: The type of entity (e.g., 'product', 'service', 'user')
        - in: path
          name: entity_id
          required: true
          schema:
            type: integer
          description: The ID of the entity
        - in: query
          name: min_rating
          schema:
            type: integer
          description: Minimum rating value (1-5)
        - in: query
          name: max_rating
          schema:
            type: integer
          description: Maximum rating value (1-5)
        - in: query
          name: only_approved
          schema:
            type: boolean
          description: Whether to only include approved ratings
      responses:
        200:
          description: List of entity ratings
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/RatingResponse'
    """
    min_rating = request.args.get('min_rating', type=int)
    max_rating = request.args.get('max_rating', type=int)
    only_approved = request.args.get('only_approved', type=lambda v: v.lower() == 'true' if v else True)
    
    ratings = rating_service.get_entity_ratings(
        entity_type=entity_type,
        entity_id=entity_id,
        min_rating=min_rating,
        max_rating=max_rating,
        only_approved=only_approved
    )
    return jsonify(response_schema.dump(ratings, many=True)), 200

@bp.route('/entity/<string:entity_type>/<int:entity_id>/stats', methods=['GET'])
def get_entity_rating_stats(entity_type, entity_id):
    """ Get rating statistics for a specific entity
    ---
    get:
      summary: Get rating statistics for a specific entity
      tags:
        - Ratings
      parameters:
        - in: path
          name: entity_type
          required: true
          schema:
            type: string
          description: The type of entity (e.g., 'product', 'service', 'user')
        - in: path
          name: entity_id
          required: true
          schema:
            type: integer
          description: The ID of the entity
        - in: query
          name: only_approved
          schema:
            type: boolean
          description: Whether to only include approved ratings
      responses:
        200:
          description: Rating statistics
          content:
            application/json:
              schema:
                type: object
                properties:
                  average_rating:
                    type: number
                    format: float
                  total_ratings:
                    type: integer
                  rating_distribution:
                    type: object
                    properties:
                      1:
                        type: integer
                      2:
                        type: integer
                      3:
                        type: integer
                      4:
                        type: integer
                      5:
                        type: integer
        404:
          description: Entity not found
    """
    only_approved = request.args.get('only_approved', type=lambda v: v.lower() == 'true' if v else True)
    
    stats = rating_service.get_entity_rating_stats(
        entity_type=entity_type,
        entity_id=entity_id,
        only_approved=only_approved
    )
    
    if not stats:
        return jsonify({'error': 'No ratings found for this entity'}), 404
        
    return jsonify(stats), 200

@bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_ratings(user_id):
    """ Get all ratings by a specific user
    ---
    get:
      summary: Get all ratings by a specific user
      tags:
        - Ratings
      parameters:
        - in: path
          name: user_id
          required: true
          schema:
            type: integer
          description: The ID of the user
        - in: query
          name: only_approved
          schema:
            type: boolean
          description: Whether to only include approved ratings
      responses:
        200:
          description: List of user ratings
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/RatingResponse'
    """
    only_approved = request.args.get('only_approved', type=lambda v: v.lower() == 'true' if v else True)
    
    ratings = rating_service.get_user_ratings(user_id, only_approved)
    return jsonify(response_schema.dump(ratings, many=True)), 200
