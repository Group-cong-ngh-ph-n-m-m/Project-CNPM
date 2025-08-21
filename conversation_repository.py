from infrastructure.databases import db
from infrastructure.models.conversation_model import Conversation


class ConversationRepository:
    def get_all(self):
        return Conversation.query.all()

    def get_by_id(self, conversation_id):
        return Conversation.query.get(conversation_id)

    def create(self, data):
        conversation = Conversation(**data)
        db.session.add(conversation)
        db.session.commit()
        return conversation

    def update(self, conversation_id, data):
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            return None
        for key, value in data.items():
            setattr(conversation, key, value)
        db.session.commit()
        return conversation

    def delete(self, conversation_id):
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            return False
        db.session.delete(conversation)
        db.session.commit()
        return True
