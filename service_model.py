from infrastructure.databases import db

class ServiceModel(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    videos = db.relationship(
        "VideoModel",               
        backref="service",
        lazy=True,
        cascade="all, delete-orphan"
    )
    def __repr__(self):
        return f"<ServiceModel id={self.id}, name={self.name}, price={self.price}>"
