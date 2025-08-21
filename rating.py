class Rating:
    def __init__(self, id: int = None, score: int = 0, comment: str = ""):
        self.id = id
        self.score = score
        self.comment = comment

    def __repr__(self):
        return f"<Rating id={self.id}, score={self.score}, comment={self.comment}>"
