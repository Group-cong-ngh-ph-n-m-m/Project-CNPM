class User:
    def __init__(self, id: int, username: str, email: str, created_at, updated_at):
        self.id = id
        self.username = username
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at