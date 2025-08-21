from datetime import datetime
from infrastructure.db import SessionLocal
from domain.conversation import Conversation

db = SessionLocal()

def create_conversation(user_id: int, tutor_id: int, topic: str):
    new_conversation = Conversation(
        user_id=user_id,
        tutor_id=tutor_id,
        topic=topic,
        created_at=datetime.now()
    )
    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)
    return new_conversation

def get_conversations():
    return db.query(Conversation).all()

def get_conversation(conversation_id: int):
    return db.query(Conversation).filter_by(id=conversation_id).first()

def update_conversation(conversation_id: int, topic: str):
    conversation = db.query(Conversation).filter_by(id=conversation_id).first()
    if not conversation:
        return None
    conversation.topic = topic
    db.commit()
    db.refresh(conversation)
    return conversation

def delete_conversation(conversation_id: int):
    conversation = db.query(Conversation).filter_by(id=conversation_id).first()
    if not conversation:
        return False
    db.delete(conversation)
    db.commit()
    return True
