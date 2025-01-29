from ext import db, datetime, timezone
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime,
        default=datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)

    @validates('email')
    def validate_email(self, key, email):
            if "@" not in email:
                raise ValueError("Invalid email address")
            return email

    @validates("password")
    def validate_password(self, key, password):
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return generate_password_hash(password)

    def __init__(self, **kwargs):
            super().__init__(**kwargs)

    @classmethod
    def create_user(cls, **kwargs):
        kwargs["password"] = generate_password_hash(kwargs["password"])
        return cls(**kwargs)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "user_name": self.user_name,
            "created_at": self.created_at,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
        }

    def __repr__(self):
        return f"<User {self.id} : ({self.email}) {self.user_name}>"
