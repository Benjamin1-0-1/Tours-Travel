from routes.r_ext import jsonify, request, jsonify, app, db, limiter,generate_password_hash,Namespace, Resource, reqparse, jwt_required,get_jwt_identity
from models.user import User

user_profiles_ns = Namespace("User Profiles", description="User profiles related operations")

def create_user_profile_parser():
    parser = reqparse.RequestParser()

    parser.add_argument('user_name', type=str, required=True, help='User name is required')
    parser.add_argument('email', type=str, required=True, help='Email is required')
    parser.add_argument('password', type=str, required=True, help='Password is required')

    return parser

user_profile_parser = create_user_profile_parser()

def user_profile_patch_parser():
    parser = reqparse.RequestParser()

    parser.add_argument('user_name', type=str, help='Full name')
    parser.add_argument('email', type=str, help='Email')
    parser.add_argument('password', type=str, help='Password')

def serialize(items):
    return [item.serialize() for item in items]

@user_profiles_ns.route('/v1/user-profiles')
class UserProfileResource(Resource):
    @jwt_required()
    @user_profiles_ns.expect(user_profile_parser)
    def post():
        current_user_email = get_jwt_identity()
        if not current_user_email:
            return jsonify({"message": "Unauthorized access"}), 401

        data = user_profile_parser.parse_args()
        hashed_password = generate_password_hash(data['password'])

        new_user = User(
            email =  data['email'],
            user_name = data['user_name'],
            password = hashed_password
        )

        db.session.add(new_user)
        try:
            db.session.commit()
            return {"message": "New user created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": "Failed to create user", "details": str(e)}, 500

@user_profiles_ns.route("/v1/user-profiles/<int:id>")
class AdminProfileResource(Resource):
    @jwt_required()
    def get(self, id):
        current_user_email = get_jwt_identity()
        if not current_user_email:
            return {"error":"Unathorized access"}

        admin_user = User.query.filter_by(email=current_user_email).first()
        if not admin_user or admin_user.role != "admin":
            return {"error": "Forbidden :Admins only allowed"}, 403

        user = User.query.get(id)
        if not user:
            return {"error": "User not found"}, 404

        return user.to_dict(), 200

@user_profiles_ns.route("/v1/user-profile/self")
class UserProfileSelfResource(Resource):
    @jwt_required()
    def get (self):
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return {"error": "Unauthorized access"}, 401

        print("JWT Identity:", current_user_id)

        current_user = User.query.filter_by(id=current_user_id).first()

        print("User object:", current_user)
        if not current_user:
            return {"error": "User not found"}, 404

        return current_user.to_dict(), 200

    @jwt_required()
    @user_profiles_ns.expect(user_profile_parser)
    def patch(self):
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return {"error": "Unauthorized access"}, 401

        data = user_profile_parser.parse_args()
        current_user = User.query.filter_by(id=current_user_id).first()

        if not current_user:
            return {"error": "User not found"},404

        current_user.email = data["email"]
        current_user.user_name = data["user_name"]

        if data["password"]:
            current_user.password = generate_password_hash(data["password"])
        try:
            db.session.commit()
            return {"message": "Profile updated successfully"},201
        except Exception as e:
            db.session.rollback()
            return {"error": "Failed to update profile" , "details":str(e)},500

