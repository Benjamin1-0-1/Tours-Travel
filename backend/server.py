# backend/server.py
import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import stripe
import paypalrestsdk
import requests
import base64
from datetime import datetime

from config import Config
from models import db, bcrypt, User, Tour, Booking, Review

def create_app():
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

    # Rate Limiter
    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        default_limits=[app.config['RATELIMIT_DEFAULT']]
    )

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

    ########################################
    # AUTH ROUTES
    ########################################
    @app.route('/api/auth/register', methods=['POST'])
    @limiter.limit("5 per minute")
    def register():
        data = request.json
        email = data.get("email")
        password = data.get("password")
        full_name = data.get("fullName", "")

        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400

        existing = User.query.filter_by(email=email).first()
        if existing:
            return jsonify({"message": "Email already registered"}), 400

        user = User(email=email, full_name=full_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "Registration successful"}), 201

    @app.route('/api/auth/login', methods=['POST'])
    @limiter.limit("10 per minute")
    def login():
        data = request.json
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify({"message": "Invalid email or password"}), 401

        access_token = create_access_token(identity=user.id)
        return jsonify({"token": access_token, "message": "Login successful"}), 200

    ########################################
    # TOURS
    ########################################
    @app.route('/api/tours', methods=['GET'])
    def get_tours():
        tours = Tour.query.all()
        result = []
        for t in tours:
            result.append({
                "id": t.id,
                "name": t.name,
                "location": t.location,
                "price": t.price,
                "description": t.description,
                "imageUrl": t.main_image,
                "images": parse_images(t.images),
                "videoUrl": t.video_url
            })
        return jsonify(result)

    @app.route('/api/tours/<int:tour_id>', methods=['GET'])
    def get_tour_detail(tour_id):
        tour = Tour.query.get_or_404(tour_id)
        return jsonify({
            "id": tour.id,
            "name": tour.name,
            "location": tour.location,
            "price": tour.price,
            "description": tour.description,
            "imageUrl": tour.main_image,
            "images": parse_images(tour.images),
            "videoUrl": tour.video_url
        })

    def parse_images(images_field):
        if not images_field:
            return []
        return [url.strip() for url in images_field.split(',')]

    ########################################
    # REVIEWS
    ########################################
    @app.route('/api/tours/<int:tour_id>/reviews', methods=['GET'])
    def get_reviews(tour_id):
        reviews = Review.query.filter_by(tour_id=tour_id).order_by(Review.created_at.desc()).all()
        data = []
        for r in reviews:
            data.append({
                "id": r.id,
                "username": r.user_name,
                "rating": r.rating,
                "comment": r.comment,
                "date": r.created_at.strftime("%Y-%m-%d")
            })
        return jsonify(data)

    @app.route('/api/tours/<int:tour_id>/reviews', methods=['POST'])
    @limiter.limit("10 per minute")
    def post_review(tour_id):
        tour = Tour.query.get_or_404(tour_id)
        data = request.json
        username = data.get("username", "Anonymous")
        rating = data.get("rating")
        comment = data.get("comment")

        if rating is None or comment is None:
            return jsonify({"message": "Missing rating or comment"}), 400

        review = Review(
            tour_id=tour.id,
            user_name=username,
            rating=int(rating),
            comment=comment
        )
        db.session.add(review)
        db.session.commit()

        return jsonify({
            "id": review.id,
            "username": review.user_name,
            "rating": review.rating,
            "comment": review.comment,
            "date": review.created_at.strftime("%Y-%m-%d")
        }), 201

    ########################################
    # BOOKING & PAYMENTS
    ########################################
    @app.route('/api/bookings', methods=['POST'])
    @jwt_required()
    def create_booking():
        current_user_id = get_jwt_identity()
        data = request.json
        tour_id = data.get("tourId")
        full_name = data.get("fullName")
        email = data.get("email")
        payment_method = data.get("paymentMethod")
        payment_token = data.get("paymentToken")

        if not (tour_id and full_name and email and payment_method):
            return jsonify({"message": "Missing required fields"}), 400

        tour = Tour.query.get_or_404(tour_id)
        success, error_msg = process_payment(
            tour.price, payment_method, payment_token, tour.name
        )
        if not success:
            return jsonify({"message": f"Payment failed: {error_msg}"}), 402

        # Create booking record
        booking = Booking(
            user_id=current_user_id,
            tour_id=tour_id,
            payment_method=payment_method,
            status="confirmed"
        )
        db.session.add(booking)
        db.session.commit()

        # Send email notification
        try:
            send_booking_emails(mail, email, full_name, tour.name, booking.id, tour.price)
        except Exception as e:
            app.logger.error(f"Error sending booking email: {e}")

        return jsonify({
            "message": f"Tour (ID: {tour_id}) booked successfully for {full_name} ({email}).",
            "bookingId": booking.id
        }), 201

    ########################################
    # PAYMENT PROCESSING
    ########################################
    def process_payment(amount, method, token_or_phone, description):
        if method == "stripe":
            return process_stripe(amount, token_or_phone, description)
        elif method == "paypal":
            return process_paypal(amount, description)
        elif method == "mpesa":
            return process_mpesa(amount, token_or_phone)
        else:
            return (False, "Unsupported payment method")

    def process_stripe(amount, source_token, desc):
        try:
            amount_cents = int(float(amount) * 100)
            stripe.Charge.create(
                amount=amount_cents,
                currency="usd",
                source=source_token,
                description=f"Payment for {desc}"
            )
            return (True, "")
        except Exception as e:
            return (False, str(e))

    def process_paypal(amount, desc):
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "http://localhost:3000/payment/success",
                "cancel_url": "http://localhost:3000/payment/cancel"
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": desc,
                        "sku": "tour",
                        "price": str(amount),
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {"total": str(amount), "currency": "USD"},
                "description": f"Payment for {desc}"
            }]
        })

        if payment.create():
            # This is partial. In real flow, you'd redirect user to PayPal approval
            return (True, "")
        else:
            return (False, str(payment.error))

    def process_mpesa(amount, phone_number):
        token = generate_mpesa_access_token()
        if not token:
            return (False, "Failed to get M-Pesa access token")

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        data_to_encode = app.config['MPESA_SHORTCODE'] + app.config['MPESA_PASSKEY'] + timestamp
        encoded_pass = base64.b64encode(data_to_encode.encode()).decode()

        env = app.config['MPESA_ENVIRONMENT']
        base_url = "https://sandbox.safaricom.co.ke" if env == "sandbox" else "https://api.safaricom.co.ke"
        stk_url = f"{base_url}/mpesa/stkpush/v1/processrequest"

        payload = {
            "BusinessShortCode": app.config['MPESA_SHORTCODE'],
            "Password": encoded_pass,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": str(amount),
            "PartyA": phone_number,
            "PartyB": app.config['MPESA_SHORTCODE'],
            "PhoneNumber": phone_number,
            "CallBackURL": "https://yourdomain.com/api/mpesa/callback",
            "AccountReference": "TourBooking",
            "TransactionDesc": "Payment for Tour"
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        r = requests.post(stk_url, json=payload, headers=headers)
        if r.status_code == 200:
            resp_json = r.json()
            if resp_json.get("ResponseCode") == "0":
                return (True, "")
            else:
                return (False, resp_json.get("CustomerMessage", "STK push failed"))
        else:
            return (False, f"HTTP error: {r.status_code}, {r.text}")

    def generate_mpesa_access_token():
        env = app.config['MPESA_ENVIRONMENT']
        base_url = "https://sandbox.safaricom.co.ke" if env == "sandbox" else "https://api.safaricom.co.ke"
        url = f"{base_url}/oauth/v1/generate?grant_type=client_credentials"

        resp = requests.get(url, auth=(app.config['MPESA_CONSUMER_KEY'], app.config['MPESA_CONSUMER_SECRET']))
        if resp.status_code == 200:
            return resp.json()['access_token']
        return None

    ########################################
    # EMAIL SENDING
    ########################################
    def send_booking_emails(mail, user_email, user_name, tour_name, booking_id, amount):
        subject_user = f"Booking Confirmation - {tour_name}"
        body_user = (
            f"Hello {user_name},\n\n"
            f"Thank you for booking the {tour_name} tour.\n"
            f"Your booking ID is {booking_id}. The amount charged is ${amount}.\n\n"
            f"We look forward to having you on the tour!\n\n"
            f"Best regards,\nTours & Travel"
        )
        msg_user = Message(subject_user, recipients=[user_email])
        msg_user.body = body_user
        mail.send(msg_user)

        # Company
        COMPANY_EMAIL = "company@example.com"
        subject_company = f"New Booking: {tour_name} (ID: {booking_id})"
        body_company = (
            f"A new booking has been made.\n\n"
            f"Booking ID: {booking_id}\n"
            f"Customer Name: {user_name}\n"
            f"Customer Email: {user_email}\n"
            f"Tour: {tour_name}\n"
            f"Amount: ${amount}\n\n"
            f"Please proceed with any required follow-up."
        )
        msg_company = Message(subject_company, recipients=[COMPANY_EMAIL])
        msg_company.body = body_company
        mail.send(msg_company)

    return app
