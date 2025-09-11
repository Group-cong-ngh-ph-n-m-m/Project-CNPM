class Video:
    def __init__(
        self,
        id: int = None,
        title: str = "",
        url: str = "",
        description: str = "",
        service_id: int = None
    ):
        self.id = id
        self.title = title
        self.url = url
        self.description = description
        self.service_id = service_id  # liên kết với Service
    def __repr__(self):
        return f"<Video id={self.id}, title={self.title}, service_id={self.service_id}>"
