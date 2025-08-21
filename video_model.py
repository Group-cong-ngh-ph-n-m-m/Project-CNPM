from infrastructure.databases import db

class VideoEntity(db.Model):
    __tablename__ = "videos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255), nullable=False)

    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
