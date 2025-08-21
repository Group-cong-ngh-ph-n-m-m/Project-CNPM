from datetime import datetime

class Conversation:
    def __init__(self, id: int = None, topic: str = "", created_at: datetime = None):
        self.id = id
        self.topic = topic
        self.created_at = created_at or datetime.utcnow()

    def __repr__(self):
        return f"<Conversation id={self.id}, topic={self.topic}, created_at={self.created_at}>"
