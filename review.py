class Review:
    def __init__(
        self,
        id: int = None,
        user_id: int = None,
        tutor_id: int = None,
        rating: int = 0,
        comment: str = ""
    ):
        self.id = id
        self.user_id = user_id
        self.tutor_id = tutor_id
        self.rating = rating
        self.comment = comment

    def __repr__(self):
        return (
            f"<Review id={self.id}, user_id={self.user_id}, "
            f"tutor_id={self.tutor_id}, rating={self.rating}, comment={self.comment}>"
        )
