from ext import jsonify, request, jsonify, app, db, mail, jwt_required, get_jwt_identity, stripe,paypalrestsdk, requests, base64, datetime, Message
from flask_restx import Resource,Namespace,reqparse
from models import Tour, Booking


''' check this later'''
# auth_ns = Namespace('auth', description='Authentication operations')
# login_parser = reqparse.RequestParser()




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

