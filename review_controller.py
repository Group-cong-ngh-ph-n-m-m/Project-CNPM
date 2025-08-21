from flask import Blueprint, request, jsonify
from services.review_service import (
    list_reviews,
    get_review,
    create_review,
    update_review,
    delete_review
)

bp = Blueprint("reviews", __name__, url_prefix="/reviews")


@bp.route("/", methods=["GET"])
def get_all_reviews():
    reviews = list_reviews()
    return jsonify([{
        "id": r.id,
        "content": r.content
    } for r in reviews]), 200


@bp.route("/<int:review_id>", methods=["GET"])
def get_review_by_id(review_id):
    review = get_review(review_id)
    if not review:
        return jsonify({"message": "Not found"}), 404
    return jsonify({
        "id": review.id,
        "content": review.content
    }), 200


@bp.route("/", methods=["POST"])
def add_review():
    data = request.get_json()
    review = create_review(content=data["content"])
    return jsonify({
        "id": review.id,
        "content": review.content
    }), 201


@bp.route("/<int:review_id>", methods=["PUT"])
def edit_review(review_id):
    data = request.get_json()
    review = update_review(review_id, content=data["content"])
    if not review:
        return jsonify({"message": "Not found"}), 404
    return jsonify({
        "id": review.id,
        "content": review.content
    }), 200


@bp.route("/<int:review_id>", methods=["DELETE"])
def remove_review(review_id):
    delete_review(review_id)
    return "", 204
