from flask import Blueprint, request, jsonify
from services.moderator_service import create_moderator, get_moderators

bp = Blueprint("moderators", __name__, url_prefix="/moderators")

@bp.route("/", methods=["GET"])
def list_moderators():
    moderators = get_moderators()
    return jsonify([{
        "id": m.id,
        "username": m.username,
        "email": m.email,
        "created_at": m.created_at
    } for m in moderators])

@bp.route("/", methods=["POST"])
def add_moderator():
    data = request.get_json()
    moderator = create_moderator(
        username=data["username"],
        email=data["email"]
    )
    return jsonify({
        "id": moderator.id,
        "username": moderator.username,
        "email": moderator.email,
        "created_at": moderator.created_at
    }), 201
