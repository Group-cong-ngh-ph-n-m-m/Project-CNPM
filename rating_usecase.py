class RatingUseCase:
    def __init__(self, repository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, rating_id: int):
        return self.repository.get_by_id(rating_id)

    def create(self, data):
        return self.repository.create(data)

    def update(self, rating_id: int, data):
        return self.repository.update(rating_id, data)

    def delete(self, rating_id: int):
        return self.repository.delete(rating_id)
