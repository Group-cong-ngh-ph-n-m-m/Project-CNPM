from infrastructure.databases import db

class ServiceEntity(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    videos = db.relationship("VideoEntity", backref="service", lazy=True, cascade="all, delete-orphan")

