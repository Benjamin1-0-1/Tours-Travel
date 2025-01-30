from flask_restx import Namespace, Resource, reqparse, fields
from models.review import Review
from routes.r_ext import db

# ✅ Define a Namespace correctly
review_ns = Namespace("reviews", description="Reviews Operations")

# ✅ Define Request Parsers
def create_review_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('tour_id', type=int, required=True, help='Tour ID is required')
    parser.add_argument('user_name', type=str, required=True, help='User Name required')
    parser.add_argument('rating', type=int, required=True, help='Please provide a rating')
    parser.add_argument('comment', type=str, required=True, help='Please add a comment')
    parser.add_argument('created_at', type=str, required=True, help='Date created')
    return parser

review_parser = create_review_parser()

def create_review_patch_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('tour_id', type=int, help='Tour ID')
    parser.add_argument('user_name', type=str, help='User Name')
    parser.add_argument('rating', type=int, help='Rating')
    parser.add_argument('comment', type=str, help='Comment')
    parser.add_argument('created_at', type=str, help='Date Created')
    return parser

review_patch_parser = create_review_patch_parser()

# ✅ Define a model for request validation
review_model = review_ns.model("Review", {
    "tour_id": fields.Integer(required=True, description="Tour ID"),
    "user_name": fields.String(required=True, description="User Name"),
    "rating": fields.Integer(required=True, description="Rating"),
    "comment": fields.String(required=True, description="Comment"),
    "created_at": fields.String(required=True, description="Date Created"),
})

# ✅ Serialize function
def serialize_review(items):
    return {
        'tour_id': items.tour_id,
        'user_name': items.user_name,
        'rating': items.rating,
        'comment': items.comment,
        'created_at': items.created_at
    }

# ✅ Collection Resource for Handling Multiple Reviews
@review_ns.route("/v1/reviews")
class ReviewsCollectionResource(Resource):
    def get(self):
        reviews = Review.query.all()
        return {
            "reviews": [serialize_review(review) for review in reviews]
        }, 200

    @review_ns.expect(review_model, validate=True)
    def post(self):
        args = review_parser.parse_args()
        new_review = Review(
            tour_id=args["tour_id"],
            user_name=args["user_name"],
            rating=args["rating"],
            comment=args["comment"],
            created_at=args["created_at"],
        )
        db.session.add(new_review)
        try:
            db.session.commit()
            return {
                "message": "Review added successfully",
                "review": serialize_review(new_review)
            }, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to add review: {str(e)}"}, 500

# ✅ Resource for Handling Single Review
@review_ns.route("/v1/review/<int:id>")
class ReviewResource(Resource):
    def get(self, id):
        review = Review.query.get(id)
        if review:
            return {"review": serialize_review(review)}, 200
        return {"message": "Review not found"}, 404

    @review_ns.expect(review_model, validate=True)
    def put(self, id):
        review = Review.query.get(id)
        if not review:
            return {"message": "Review not found"}, 404

        args = review_parser.parse_args()
        review.tour_id = args['tour_id']
        review.user_name = args['user_name']
        review.rating = args['rating']
        review.comment = args['comment']
        review.created_at = args['created_at']

        db.session.add(review)
        try:
            db.session.commit()
            return {
                "message": "Review updated successfully",
                "review": serialize_review(review)
            }, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to update review: {str(e)}"}, 500

    @review_ns.expect(review_patch_parser, validate=True)
    def patch(self, id):
        review = Review.query.get(id)
        if not review:
            return {"message": "Review not found"}, 404

        args = review_patch_parser.parse_args()
        for key, value in args.items():
            if value is not None:
                setattr(review, key, value)

        db.session.add(review)
        try:
            db.session.commit()
            return {
                "message": "Review updated successfully",
                "review": serialize_review(review),
            }, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to update review: {str(e)}"}, 500

    def delete(self, id):
        review = Review.query.get(id)
        if not review:
            return {"message": "Review not found"}, 404

        db.session.delete(review)
        try:
            db.session.commit()
            return {"message": "Review deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to delete review: {str(e)}"}, 500
