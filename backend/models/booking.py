from ext import db, datetime, timezone
class BookingPlacement(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)

    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable=False)

    price = db.Column(db.Float, nullable=False)
    adults = db.Column(db.Integer, nullable=False)
    children = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    full_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))


    def serialize_bookingPlacement(self):
        return {
            'id': self.id,
            'payment_method': self.payment_method,
            'status': self.status,
            'created_at': self.created_at,
            'user_id': self.user_id,
            'tour_id': self.tour_id
        }
