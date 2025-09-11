from typing import List, Optional, Dict, Any
from domain.video import Video
from infrastructure.repositories.video_repository import VideoRepository

class VideoUseCase:
    def __init__(self, repository: VideoRepository):
        self.repository = repository
    def get_all(self) -> List[Video]:
        return self.repository.get_all()
    def get_by_id(self, video_id: int) -> Optional[Video]:
        return self.repository.get_by_id(video_id)
    def create(self, data: Dict[str, Any]) -> Video:
        if "title" not in data or not data["title"]:
            raise ValueError("Title is required")
        if "url" not in data or not data["url"]:
            raise ValueError("URL is required")
        if "service_id" not in data or not data["service_id"]:
            raise ValueError("Service ID is required")
        return self.repository.create(data)
    def update(self, video_id: int, data: Dict[str, Any]) -> Optional[Video]:
        return self.repository.update(video_id, data)
    def delete(self, video_id: int) -> bool:
        return self.repository.delete(video_id)
