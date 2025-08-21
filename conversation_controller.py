from flask import Blueprint, request, jsonify
from services.conversation_service import (
    list_conversations,
    get_conversation,
    create_conversation,
    update_conversation,
    delete_conversation
)

bp = Blueprint("conversations", __name__, url_prefix="/conversations")


@bp.route("/", methods=["GET"])
def get_all_conversations():
    conversations = list_conversations()
    return jsonify([{
        "id": c.id,
        "topic": c.topic
    } for c in conversations]), 200


@bp.route("/<int:conversation_id>", methods=["GET"])
def get_conversation_by_id(conversation_id):
    conversation = get_conversation(conversation_id)
    if not conversation:
        return jsonify({"message": "Not found"}), 404
    return jsonify({
        "id": conversation.id,
        "topic": conversation.topic
    }), 200


@bp.route("/", methods=["POST"])
def add_conversation():
    data = request.get_json()
    conversation = create_conversation(topic=data["topic"])
    return jsonify({
        "id": conversation.id,
        "topic": conversation.topic
    }), 201


@bp.route("/<int:conversation_id>", methods=["PUT"])
def edit_conversation(conversation_id):
    data = request.get_json()
    conversation = update_conversation(conversation_id, topic=data["topic"])
    if not conversation:
        return jsonify({"message": "Not found"}), 404
    return jsonify({
        "id": conversation.id,
        "topic": conversation.topic
    }), 200


@bp.route("/<int:conversation_id>", methods=["DELETE"])
def remove_conversation(conversation_id):
    delete_conversation(conversation_id)
    return "", 204
