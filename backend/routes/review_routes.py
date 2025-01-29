from ext import Review, db,Namespace,Resource,reqparse
from models.review import Review

reviews_ns = Namespace('reviews', description='Reviews Operations')

def create_review_parser():
    parser = reqparse.RequestParser()

    parser.add_argument('tour_id', type=int, required=True, help='Tour is required')
    parser.add_argument('user_name', type=str, required=True, help='User Name required')
    parser.add_argument('rating', type=str, required=True, help='Please Rate')
    parser.add_argument('comment', type=str, required=True, help='Please add a comment')
    parser.add_argument('created_at', type=str, required=True, help='Date created')

    return parser

review_ns = create_review_parser()

def create_review_patch_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('tour_id', type=str, help='Tour id required')
    parser.add_argument('user_name', type=str, help='User name ')
    parser.add_argument('rating', type=int, help='Adding your rating')
    parser.add_argument('comment', type=str, help='Comment')
    parser.add_argument('created_at', type=str, help='Date created')

review_patch_parser = create_review_patch_parser()

def serialize_review(items):
    return {
        'tour_id': items.tour_id,
        'user_name': items.user_name,
        'rating': items.rating,
        'comment': items.comment,
        'created_at': items.created_at
    }

@reviews_ns.route("/v1/reviews")
class ReviewsCollectionResource(Resource):
    def get(self):
        reviews = Review.query.all()
        return {
            "reviews": [serialize_review(review) for review in reviews]
        }, 200
    @review_ns.expect(review_ns, validate = True)
    def post(self):
        args  = review_ns.parse_args()
        new_review = Review(
            tour_id = args["tour_id"],
            user_name = args["user_name"],
            rating = args["rating"],
            comment = args["comment"],
            created_at = args["created_at"],
        )
        db.session.add(new_review)
        try:
            db.session.commit()
            return{
                "message": "Review addeded successfully",
                "review":serialize_review(new_review)
            }, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to add review: {str(e)}"}, 500

    @review_ns.route("/v1/review/<int:id)")
    class ReviewResource(Resource):
        # it not a must to only get one review
        def get(self, id):
            review = Review.query.get(id)
            if review :
                return {"review": serialize_review(review)}, 200
            return {"status": "Review not found"}, 404

        def put(self, id):
            review = Review.query.get(id)
            if not review:
                return {"message": "Review not found"}, 404

            args = review_ns.parse_args()
            review.tour_id = args['tour_id']
            review.user_name = args['user_name']
            review.rating = args['rating']
            review.comment = args['comment']
            review.created_at = args['created_at']

            db.session.add(review)
            try:
                db.session.commit()
                return {
                    "message":"review added successfully",
                    "review": serialize_review(review)
                },200
            except Exception as e:
                db.session.rollback()
                return {"message":f"Failed to add review :{str(e)}"},500

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
                    "message": "Pricing updated successfully",
                    "pricing": serialize_review(review),
                }, 200
            except Exception as e:
                db.session.rollback()
                return {"message": f"Failed to update pricing: {str(e)}"}, 500

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


