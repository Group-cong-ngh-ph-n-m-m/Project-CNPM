from flask import Blueprint, request, jsonify
from usecase.admin_usecase import AdminUseCase
from infrastructure.repositories.admin_repository import AdminRepository

bp = Blueprint("admin", __name__, url_prefix="/admins")
uc = AdminUseCase(AdminRepository())

@bp.route("/", methods=["GET"])
def list_admins():
    return jsonify(uc.get_all()), 200

@bp.route("/", methods=["POST"])
def create_admin():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    data = request.get_json()
    return jsonify(uc.create(data)), 201
