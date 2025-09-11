from flask import Blueprint, request, jsonify
from usecase.video_usecase import VideoUseCase
from infrastructure.repositories.video_repository import VideoRepository

bp = Blueprint("video", __name__, url_prefix="/videos")
uc = VideoUseCase(VideoRepository())

@bp.route("/", methods=["GET"])
def list_videos():
    videos = uc.get_all()
    return jsonify([v.to_dict() for v in videos]), 200

@bp.route("/", methods=["POST"])
def create_video():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    data = request.get_json()
    video = uc.create(data)
    return jsonify(video.to_dict()), 201

