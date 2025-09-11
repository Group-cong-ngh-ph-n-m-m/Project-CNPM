from infrastructure.databases import db

class VideoModel(db.Model):
    __tablename__ = "videos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    def __repr__(self):
        return f"<VideoModel id={self.id}, title={self.title}, service_id={self.service_id}>"

