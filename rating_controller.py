from flask import Blueprint, request, jsonify
from services.rating_service import (
    list_ratings,
    get_rating,
    create_rating,
    update_rating,
    delete_rating
)

bp = Blueprint("ratings", __name__, url_prefix="/ratings")


@bp.route("/", methods=["GET"])
def get_all_ratings():
    ratings = list_ratings()
    return jsonify([{
        "id": r.id,
        "score": r.score,
        "comment": r.comment
    } for r in ratings]), 200


@bp.route("/<int:rating_id>", methods=["GET"])
def get_rating_by_id(rating_id):
    rating = get_rating(rating_id)
    if not rating:
        return jsonify({"message": "Not found"}), 404
    return jsonify({
        "id": rating.id,
        "score": rating.score,
        "comment": rating.comment
    }), 200


@bp.route("/", methods=["POST"])
def add_rating():
    data = request.get_json()
    rating = create_rating(
        score=data["score"],
        comment=data.get("comment")
    )
    return jsonify({
        "id": rating.id,
        "score": rating.score,
        "comment": rating.comment
    }), 201


@bp.route("/<int:rating_id>", methods=["PUT"])
def edit_rating(rating_id):
    data = request.get_json()
    rating = update_rating(
        rating_id,
        score=data["score"],
        comment=data.get("comment")
    )
    if not rating:
        return jsonify({"message": "Not found"}), 404
    return jsonify({
        "id": rating.id,
        "score": rating.score,
        "comment": rating.comment
    }), 200


@bp.route("/<int:rating_id>", methods=["DELETE"])
def remove_rating(rating_id):
    delete_rating(rating_id)
    return "", 204
