# backend/models/tour.py
from models.ext import db, datetime, timezone

class Tours(db.Model):
    __tablename__ = 'tours'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    main_image = db.Column(db.String(255))  # main cover image
    images = db.Column(db.Text)  # comma-separated or JSON
    video_url = db.Column(db.String(255))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,  # corrected key from "nmae"
            "location": self.location,
            "price": self.price,
            "description": self.description,
            "main_image": self.main_image,
            "images": self.images,
            "video_url": self.video_url
        }
