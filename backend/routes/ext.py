from backend.models.ext import db, bcrypt
from flask_restx import Resource, Namespace, reqparse

import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash

import stripe
import paypalrestsdk
import requests
import base64
from datetime import datetime
from config import Config



app = Flask(__name__)
app.config.from_object(Config)

# Initialize DB, Migrate, Bcrypt
db.init_app(app)
Migrate(app, db)
bcrypt.init_app(app)

# CORS, Mail, Logging
CORS(app)
mail = Mail(app)
logging.basicConfig(level=logging.INFO)

# JWT
jwt = JWTManager(app)
# Optionally set token expiration
# from datetime import timedelta
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)

# Payment config
stripe.api_key = app.config['STRIPE_SECRET_KEY']
paypalrestsdk.configure({
    "mode": "sandbox",  # or 'live'
    "client_id": app.config['PAYPAL_CLIENT_ID'],
    "client_secret": app.config['PAYPAL_CLIENT_SECRET']
})

# Rate limiting
limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        default_limits=[app.config['RATELIMIT_DEFAULT']]
    )
