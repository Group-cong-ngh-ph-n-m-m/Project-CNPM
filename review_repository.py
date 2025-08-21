from infrastructure.databases import db
from infrastructure.models.review_model import Review


class ReviewRepository:
    def get_all(self):
        return Review.query.all()

    def get_by_id(self, review_id):
        return Review.query.get(review_id)

    def create(self, data):
        review = Review(**data)
        db.session.add(review)
        db.session.commit()
        return review

    def update(self, review_id, data):
        review = Review.query.get(review_id)
        if not review:
            return None
        for key, value in data.items():
            setattr(review, key, value)
        db.session.commit()
        return review

    def delete(self, review_id):
        review = Review.query.get(review_id)
        if not review:
            return False
        db.session.delete(review)
        db.session.commit()
        return True
