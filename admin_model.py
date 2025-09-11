from infrastructure.databases import db

class AdminModel(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<AdminModel id={self.id}, username={self.username}, email={self.email}>"
