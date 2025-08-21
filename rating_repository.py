from infrastructure.databases import db
from infrastructure.models.rating_model import Rating


class RatingRepository:
    def get_all(self):
        return Rating.query.all()

    def get_by_id(self, rating_id):
        return Rating.query.get(rating_id)

    def create(self, data):
        rating = Rating(**data)
        db.session.add(rating)
        db.session.commit()
        return rating

    def update(self, rating_id, data):
        rating = Rating.query.get(rating_id)
        if not rating:
            return None
        for key, value in data.items():
            setattr(rating, key, value)
        db.session.commit()
        return rating

    def delete(self, rating_id):
        rating = Rating.query.get(rating_id)
        if not rating:
            return False
        db.session.delete(rating)
        db.session.commit()
        return True
