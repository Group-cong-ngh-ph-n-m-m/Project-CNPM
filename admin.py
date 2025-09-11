class Admin:
    def __init__(self, id: int = None, username: str = "", email: str = "", password: str = None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
    def __repr__(self):
        return f"<Admin id={self.id}, username={self.username}, email={self.email}>"

