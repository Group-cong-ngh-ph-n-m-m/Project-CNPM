from infrastructure.databases import db
from infrastructure.models.video_model import VideoEntity

class VideoRepository:
    def get_all(self):
        return VideoEntity.query.all()

    def get_by_id(self, video_id):
        return VideoEntity.query.get(video_id)

    def create(self, data):
        video = VideoEntity(**data)
        db.session.add(video)
        db.session.commit()
        return video

    def update(self, video_id, data):
        video = VideoEntity.query.get(video_id)
        if not video:
            return None
        for key, value in data.items():
            setattr(video, key, value)
        db.session.commit()
        return video

    def delete(self, video_id):
        video = VideoEntity.query.get(video_id)
        if not video:
            return False
        db.session.delete(video)
        db.session.commit()
        return True
