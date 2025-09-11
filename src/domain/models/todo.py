class Todo:
    def __init__(self, id: int, title: str, description: str, status: str, created_at, updated_at):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
class Subject:
    def __init__(self, id: int, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description

class TutorProfile:
    def __init__(self, id: int, name: str, email: str, phone: str):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone

class Message:
    def __init__(self, id: int, content: str, sender_id: int, receiver_id: int, created_at, updated_at):
        self.id = id
        self.content = content
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.created_at = created_at
        self.updated_at = updated_at

class Conversation:
    def __init__(self, id: int, sender_id: int, receiver_id: int, message: str, created_at, updated_at):
        self.id = id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message = message
        self.created_at = created_at
        self.updated_at = updated_at

class Review:
    def __init__(self, id: int, user_id: int, item_id: int, title: str, content: str, rating: float, created_at, updated_at):
        self.id = id
        self.user_id = user_id
        self.item_id = item_id
        self.title = title
        self.content = content
        self.rating = rating
        self.created_at = created_at
        self.updated_at = updated_at

class Rating:
    def __init__(self, id: int, user_id: int, item_id: int, score: float, comment: str, created_at, updated_at):
        self.id = id
        self.user_id = user_id
        self.item_id = item_id
        self.score = score
        self.comment = comment
        self.created_at = created_at
        self.updated_at = updated_at
