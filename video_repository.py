from typing import List, Optional
from domain.video import Video                   
from infrastructure.models.video import VideoModel   
from infrastructure.databases import db

class VideoRepository:
    def get_all(self) -> List[Video]:
        videos = VideoModel.query.all()
        return [
            Video(
                id=v.id,
                title=v.title,
                url=v.url,
                description=v.description,
                service_id=v.service_id
            )
            for v in videos
        ]
    def get_by_id(self, video_id: int) -> Optional[Video]:
        v = VideoModel.query.get(video_id)
        if not v:
            return None
        return Video(
            id=v.id,
            title=v.title,
            url=v.url,
            description=v.description,
            service_id=v.service_id
        )
    def create(self, data: dict) -> Video:
        video_model = VideoModel(**data)
        db.session.add(video_model)
        db.session.commit()
        return Video(
            id=video_model.id,
            title=video_model.title,
            url=video_model.url,
            description=video_model.description,
            service_id=video_model.service_id
        )
    def update(self, video_id: int, data: dict) -> Optional[Video]:
        video_model = VideoModel.query.get(video_id)
        if not video_model:
            return None
        for key, value in data.items():
            setattr(video_model, key, value)
        db.session.commit()
        return Video(
            id=video_model.id,
            title=video_model.title,
            url=video_model.url,
            description=video_model.description,
            service_id=video_model.service_id
        )
    def delete(self, video_id: int) -> bool:
        video_model = VideoModel.query.get(video_id)
        if not video_model:
            return False
        db.session.delete(video_model)
        db.session.commit()
        return True
