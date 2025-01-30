# backend/models/user.py
from models.ext import db, datetime, timezone
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    # Add role for admin checks
    role = db.Column(db.String(50), default="user")

    @validates('email')
    def validate_email(self, key, email):
        if "@" not in email:
            raise ValueError("Invalid email address")
        return email

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "user_name": self.user_name,
            "created_at": self.created_at,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "role": self.role
        }

    def __repr__(self):
        return f"<User {self.id}: {self.email} ({self.user_name})>"
