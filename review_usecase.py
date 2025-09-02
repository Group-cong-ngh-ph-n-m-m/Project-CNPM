class ReviewUseCase:
    def __init__(self, repository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, review_id: int):
        return self.repository.get_by_id(review_id)

    def create(self, data):
        return self.repository.create(data)

    def update(self, review_id: int, data):
        return self.repository.update(review_id, data)

    def delete(self, review_id: int):
        return self.repository.delete(review_id)
