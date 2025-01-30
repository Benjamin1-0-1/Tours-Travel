# backend/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from models.user import User
from models.ext import db

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Body JSON example: {
      "user_name": "Alice",
      "email": "alice@example.com",
      "password": "secret123"
    }
    """
    data = request.get_json()
    user_name = data.get("user_name")
    email = data.get("email")
    password = data.get("password")

    if not all([user_name, email, password]):
        return jsonify({"message": "Missing fields"}), 400

    # Check if user exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Email already registered"}), 409

    # Create new user
    new_user = User(user_name=user_name, email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Body JSON example: {
      "email": "alice@example.com",
      "password": "secret123"
    }
    """
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"message": "Missing fields"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

    if not user.check_password(password):
        return jsonify({"message": "Invalid email or password"}), 401

    # Create JWT
    access_token = create_access_token(identity=user.id)
    return jsonify({
        "message": "Login successful",
        "token": access_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "user_name": user.user_name
        }
    }), 200
