# backend/seed.py
import datetime
from models.ext import db
from models.user import User
from models.tour import Tours
from models.booking import BookingPlacement
from models.review import Review
from flask import Flask
from flask_migrate import Migrate
from config import Config

def seed_data(app):
    with app.app_context():
        # Create sample users
        user1 = User(user_name="Alice", email="alice@example.com")
        user1.set_password("secret123")
        user1.role = "admin"

        user2 = User(user_name="Bob", email="bob@example.com")
        user2.set_password("test456")

        db.session.add_all([user1, user2])
        db.session.commit()

        # Create sample tours
        tour1 = Tours(
            name="New York City Tour",
            location="New York, USA",
            price=120.0,
            description="Experience NYC",
            main_image="https://example.com/nyc.jpg",
            images="https://example.com/nyc1.jpg,https://example.com/nyc2.jpg",
            video_url="https://youtube.com/embed/NYC123"
        )
        tour2 = Tours(
            name="Paris Highlights",
            location="Paris, France",
            price=200.0,
            description="Romantic city of lights",
            main_image="https://example.com/paris.jpg",
            images="",
            video_url="https://youtube.com/embed/PARIS456"
        )
        db.session.add_all([tour1, tour2])
        db.session.commit()

        # Create sample booking
        booking = BookingPlacement(
            user_id=user1.id,
            tour_id=tour1.id,
            price=tour1.price,
            adults=2,
            children=0,
            start_date=datetime.datetime(2024,5,1),
            end_date=datetime.datetime(2024,5,5),
            full_name="Alice Wonderland",
            email="alice@example.com",
            payment_method="stripe",
            status="confirmed"
        )
        db.session.add(booking)
        db.session.commit()

        # Create a sample review
        review = Review(
            tour_id=tour1.id,
            user_name="Alice",
            rating=5,
            comment="Amazing experience!"
        )
        db.session.add(review)
        db.session.commit()

        print("Seeding completed successfully!")

if __name__ == "__main__":
    from flask import Flask
    from config import Config
    from models.ext import db
    from flask_migrate import Migrate

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    seed_data(app)
