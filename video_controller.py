from flask import Blueprint, request, jsonify
from usecase.video_usecase import VideoUseCase
from infrastructure.repositories.video_repository import VideoRepository

bp = Blueprint("video", __name__, url_prefix="/videos")
uc = VideoUseCase(VideoRepository())

@bp.route("/", methods=["GET"])
def list_videos():
    return jsonify(uc.get_all()), 200

@bp.route("/", methods=["POST"])
def create_video():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    data = request.get_json()
    return jsonify(uc.create(data)), 201
