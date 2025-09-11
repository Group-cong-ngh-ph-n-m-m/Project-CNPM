from flask import Blueprint, request, jsonify
from services.todo_service import ReviewService
from infrastructure.repositories.review_repositories import ReviewRepository
from api.schemas.todo import ReviewRequestSchema, ReviewResponseSchema
from datetime import datetime
from infrastructure.databases.mssql import session

bp = Blueprint('review', __name__, url_prefix='/reviews')

# Khởi tạo service và repository
review_service = ReviewService(ReviewRepository(session))

request_schema = ReviewRequestSchema()
response_schema = ReviewResponseSchema()

@bp.route('/', methods=['GET'])
def list_reviews():
    """
    Get all reviews
    ---
    get:
      summary: Get all reviews
      tags:
        - Reviews
      parameters:
        - in: query
          name: reviewed_entity_type
          schema:
            type: string
          description: Filter reviews by entity type (e.g., 'product', 'service', 'restaurant')
        - in: query
          name: reviewed_entity_id
          schema:
            type: integer
          description: Filter reviews by entity ID
        - in: query
          name: user_id
          schema:
            type: integer
          description: Filter reviews by user ID
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
          name: is_approved
          schema:
            type: boolean
          description: Filter by approval status
        - in: query
          name: has_photos
          schema:
            type: boolean
          description: Filter reviews that have photos
      responses:
        200:
          description: List of reviews
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ReviewResponse'
    """
    reviewed_entity_type = request.args.get('reviewed_entity_type')
    reviewed_entity_id = request.args.get('reviewed_entity_id', type=int)
    user_id = request.args.get('user_id', type=int)
    min_rating = request.args.get('min_rating', type=int)
    max_rating = request.args.get('max_rating', type=int)
    is_approved = request.args.get('is_approved', type=lambda v: v.lower() == 'true' if v else None)
    has_photos = request.args.get('has_photos', type=lambda v: v.lower() == 'true' if v else None)
    
    reviews = review_service.list_reviews(
        reviewed_entity_type=reviewed_entity_type,
        reviewed_entity_id=reviewed_entity_id,
        user_id=user_id,
        min_rating=min_rating,
        max_rating=max_rating,
        is_approved=is_approved,
        has_photos=has_photos
    )
    return jsonify(response_schema.dump(reviews, many=True)), 200

@bp.route('/<int:review_id>', methods=['GET'])
def get_review(review_id):
    """ Get a review by ID
    ---
    get:
      summary: Get a review by ID
      tags:
        - Reviews
      parameters:
        - in: path
          name: review_id
          required: true
          schema:
            type: integer
          description: The ID of the review to retrieve
      responses:
        200:
          description: Review found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ReviewResponse'
        404:
          description: Review not found
    """
    review = review_service.get_review(review_id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    return jsonify(response_schema.dump(review)), 200

@bp.route('/', methods=['POST'])
def create_review():
    """ Create a new review
    ---
    post:
      summary: Create a new review
      tags:
        - Reviews
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ReviewRequest'
      responses:
        201:
          description: Review created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ReviewResponse'
        400:
          description: Invalid input
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    review = review_service.create_review(
        user_id=data['user_id'],
        reviewed_entity_type=data['reviewed_entity_type'],
        reviewed_entity_id=data['reviewed_entity_id'],
        rating=data['rating'],
        title=data.get('title'),
        content=data['content'],
        is_approved=data.get('is_approved', False),
        photos=data.get('photos', [])
    )
    return jsonify(response_schema.dump(review)), 201

@bp.route('/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    """ Update an existing review
    ---
    put:
      summary: Update an existing review
      tags:
        - Reviews
      parameters:
        - in: path
          name: review_id
          required: true
          schema:
            type: integer
          description: The ID of the review to update
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ReviewRequest'
      responses:
        200:
          description: Review updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ReviewResponse'
        404:
          description: Review not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    review = review_service.update_review(
        review_id=review_id,
        rating=data.get('rating'),
        title=data.get('title'),
        content=data.get('content'),
        is_approved=data.get('is_approved'),
        photos=data.get('photos')
    )
    
    if not review:
        return jsonify({'error': 'Review not found'}), 404
        
    return jsonify(response_schema.dump(review)), 200

@bp.route('/<int:review_id>', methods=['PATCH'])
def patch_review(review_id):
    """ Patch an existing review
    ---
    patch:
      summary: Patch an existing review
      tags:
        - Reviews
      parameters:
        - in: path
          name: review_id
          required: true
          schema:
            type: integer
          description: The ID of the review to patch
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ReviewRequest'
      responses:
        200:
          description: Review patched successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ReviewResponse'
        404:
          description: Review not found
    """
    data = request.get_json()
    errors = request_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    
    review = review_service.patch_review(
        review_id=review_id,
        rating=data.get('rating'),
        title=data.get('title'),
        content=data.get('content'),
        is_approved=data.get('is_approved'),
        photos=data.get('photos')
    )
    
    if not review:
        return jsonify({'error': 'Review not found'}), 404
        
    return jsonify(response_schema.dump(review)), 200

@bp.route('/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ Delete a review
    ---
    delete:
      summary: Delete a review
      tags:
        - Reviews
      parameters:
        - in: path
          name: review_id
          required: true
          schema:
            type: integer
          description: The ID of the review to delete
      responses:
        204:
          description: Review deleted successfully
        404:
          description: Review not found
    """
    success = review_service.delete_review(review_id)
    if not success:
        return jsonify({'error': 'Review not found'}), 404
    return '', 204

@bp.route('/entity/<string:entity_type>/<int:entity_id>', methods=['GET'])
def get_entity_reviews(entity_type, entity_id):
    """ Get all reviews for a specific entity
    ---
    get:
      summary: Get all reviews for a specific entity
      tags:
        - Reviews
      parameters:
        - in: path
          name: entity_type
          required: true
          schema:
            type: string
          description: The type of entity (e.g., 'product', 'service', 'restaurant')
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
          description: Whether to only include approved reviews
        - in: query
          name: sort_by
          schema:
            type: string
            enum: [newest, oldest, highest_rating, lowest_rating, most_helpful]
          description: Sort order for reviews
      responses:
        200:
          description: List of entity reviews
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ReviewResponse'
    """
    min_rating = request.args.get('min_rating', type=int)
    max_rating = request.args.get('max_rating', type=int)
    only_approved = request.args.get('only_approved', type=lambda v: v.lower() == 'true' if v else True)
    sort_by = request.args.get('sort_by', 'newest')
    
    reviews = review_service.get_entity_reviews(
        entity_type=entity_type,
        entity_id=entity_id,
        min_rating=min_rating,
        max_rating=max_rating,
        only_approved=only_approved,
        sort_by=sort_by
    )
    return jsonify(response_schema.dump(reviews, many=True)), 200

@bp.route('/entity/<string:entity_type>/<int:entity_id>/stats', methods=['GET'])
def get_entity_review_stats(entity_type, entity_id):
    """ Get review statistics for a specific entity
    ---
    get:
      summary: Get review statistics for a specific entity
      tags:
        - Reviews
      parameters:
        - in: path
          name: entity_type
          required: true
          schema:
            type: string
          description: The type of entity (e.g., 'product', 'service', 'restaurant')
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
          description: Whether to only include approved reviews
      responses:
        200:
          description: Review statistics
          content:
            application/json:
              schema:
                type: object
                properties:
                  average_rating:
                    type: number
                    format: float
                  total_reviews:
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
                  with_photos_count:
                    type: integer
        404:
          description: Entity not found
    """
    only_approved = request.args.get('only_approved', type=lambda v: v.lower() == 'true' if v else True)
    
    stats = review_service.get_entity_review_stats(
        entity_type=entity_type,
        entity_id=entity_id,
        only_approved=only_approved
    )
    
    if not stats:
        return jsonify({'error': 'No reviews found for this entity'}), 404
        
    return jsonify(stats), 200

@bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_reviews(user_id):
    """ Get all reviews by a specific user
    ---
    get:
      summary: Get all reviews by a specific user
      tags:
        - Reviews
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
          description: Whether to only include approved reviews
      responses:
        200:
          description: List of user reviews
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ReviewResponse'
    """
    only_approved = request.args.get('only_approved', type=lambda v: v.lower() == 'true' if v else True)
    
    reviews = review_service.get_user_reviews(user_id, only_approved)
    return jsonify(response_schema.dump(reviews, many=True)), 200

@bp.route('/<int:review_id>/helpful', methods=['POST'])
def mark_review_helpful(review_id):
    """ Mark a review as helpful
    ---
    post:
      summary: Mark a review as helpful
      tags:
        - Reviews
      parameters:
        - in: path
          name: review_id
          required: true
          schema:
            type: integer
          description: The ID of the review
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                user_id:
                  type: integer
                  description: The ID of the user marking as helpful
                is_helpful:
                  type: boolean
                  description: Whether the review is helpful
              required:
                - user_id
                - is_helpful
      responses:
        200:
          description: Helpful status updated successfully
        404:
          description: Review not found
    """
    data = request.get_json()
    if not data or 'user_id' not in data or 'is_helpful' not in data:
        return jsonify({'error': 'User ID and is_helpful are required'}), 400
    
    success = review_service.mark_helpful(
        review_id=review_id,
        user_id=data['user_id'],
        is_helpful=data['is_helpful']
    )
    
    if not success:
        return jsonify({'error': 'Review not found'}), 404
        
    return jsonify({'message': 'Helpful status updated successfully'}), 200

@bp.route('/<int:review_id>/approve', methods=['PATCH'])
def approve_review(review_id):
    """ Approve a review
    ---
    patch:
      summary: Approve a review
      tags:
        - Reviews
      parameters:
        - in: path
          name: review_id
          required: true
          schema:
            type: integer
          description: The ID of the review to approve
      responses:
        200:
          description: Review approved successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ReviewResponse'
        404:
          description: Review not found
    """
    review = review_service.approve_review(review_id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404
        
    return jsonify(response_schema.dump(review)), 200
