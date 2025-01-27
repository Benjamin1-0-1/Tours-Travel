from ext import jsonify, request, jsonify, app, db, limiter,create_access_token,jwt_required, User, get_jwt_identity
from flask_restx import Namespace, Resource,reqparse
from werkzeug.security import generate_password_hash

user_profiles_ns = Namespace('user_profiles', description='User profile operations')

user_profile_parser = reqparse.RequestParser()

user_profile_parser.add_argument('fullName', type=str, required=True, help='Full name is required')
user_profile_parser.add_argument('email', type=str, required=True, help='Email is required')
user_profile_parser.add_argument('password', type=str, required=True, help='Password is required')

@user_profiles_ns.route('/v1/user-profile')
@limiter.limit("5 per minute")
class UserProfileResource(Resource):
    @jwt_required()
    @user_profiles_ns.expect(user_profile_parser)
    def register():
        current_user_email = get_jwt_identity()
        if not current_user_email:
            return jsonify({"message": "Unauthorized"}), 401

        data = user_profile_parser.parse_args()
        required_fields = ['email', 'password','fullName']
        for field in required_fields:
            if field not in data:
                return {"error": f"Missing required field: {field}"}, 400

        email = data.get("email")
        password = data['password']
        hashed_password = generate_password_hash(password)
        full_name = data.get("fullName", "")

        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return jsonify({"message": "Email already registered"}), 400

        user_details = {
            "email": data['email'],
            "password": hashed_password,
            "fullName": data['full_name']
            # "registeredAt": str(datetime.datetime.now())
        }
        # check above for inputing user details
        new_user = User(**user_details)
        new_user.set_password(password)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"error": "Failed to create profile", "details": str(e)}, 500

        return jsonify({"message": "Profile created successfully"}), 201


@user_profiles_ns.route('/v1/user-profile/<int:id>')
@limiter.limit("10 per minute")
class UserProfileResource(Resource):
    @jwt_required()
    def get(id):
        current_user_email = get_jwt_identity()
        if not current_user_email:
            return jsonify({"message": "Unauthorized"}), 401

        user = User.query.filter_by(id=id).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400

        user_data = {
            "id": user.id,
            "email": user.email,
            "fullName": user.full_name,
            "registeredAt": user.registered_at
        }
        return jsonify(user_data), 200
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")



    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid email or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"token": access_token, "message": "Login successful"}), 200
