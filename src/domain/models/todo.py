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
