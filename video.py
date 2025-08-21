class Video:
    def __init__(self, id: int = None, title: str = "", url: str = "", description: str = ""):
        self.id = id
        self.title = title
        self.url = url
        self.description = description

    def __repr__(self):
        return f"<Video id={self.id}, title={self.title}>"
