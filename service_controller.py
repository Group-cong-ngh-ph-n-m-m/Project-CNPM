from flask import Blueprint, request, jsonify
from usecase.service_usecase import ServiceUseCase
from infrastructure.repositories.service_repository import ServiceRepository

bp = Blueprint("service", __name__, url_prefix="/services")
uc = ServiceUseCase(ServiceRepository())

@bp.route("/", methods=["GET"])
def list_services():
    return jsonify(uc.get_all()), 200

@bp.route("/", methods=["POST"])
def create_service():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    data = request.get_json()
    return jsonify(uc.create(data)), 201

