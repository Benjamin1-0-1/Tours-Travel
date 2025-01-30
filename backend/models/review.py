# backend/models/review.py
from models.ext import db, datetime, timezone

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable=False)
    user_name = db.Column(db.String(120), default='Anonymous')
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def serialize_review(self):
        return {
            "id": self.id,
            "tour_id": self.tour_id,
            "user_name": self.user_name,
            "rating": self.rating,
            "comment": self.comment,
            "created_at": self.created_at
        }
