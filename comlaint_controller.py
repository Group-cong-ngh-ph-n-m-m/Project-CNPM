from flask import Blueprint, request, jsonify
from services.complain_service import create_complain, get_complains

bp = Blueprint("complains", __name__, url_prefix="/complains")

@bp.route("/", methods=["GET"])
def list_complains():
    complains = get_complains()
    return jsonify([{
        "id": c.id,
        "title": c.title,
        "description": c.description,
        "status": c.status,
        "created_at": c.created_at,
        "user_id": c.user_id
    } for c in complains])

@bp.route("/", methods=["POST"])
def add_complain():
    data = request.get_json()
    complain = create_complain(
        title=data["title"],
        description=data["description"],
        user_id=data.get("user_id")
    )
    return jsonify({
        "id": complain.id,
        "title": complain.title,
        "description": complain.description,
        "status": complain.status,
        "created_at": complain.created_at,
        "user_id": complain.user_id
    }), 201
