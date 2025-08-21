class Admin:
    def __init__(self, id: int = None, username: str = "", email: str = ""):
        self.id = id
        self.username = username
        self.email = email

    def __repr__(self):
        return f"<Admin id={self.id}, username={self.username}>"
