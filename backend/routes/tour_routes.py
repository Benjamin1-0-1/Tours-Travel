from routes.r_ext import jsonify, request, jsonify, app, db, Namespace, Resource, Resource,reqparse
from models.tour import Tours


tours_ns = Namespace("tours", description="Tours Operations Resource")

def create_tours_parser():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="Name of Tour")
    parser.add_argument(
        "location", type=str, required=True, help="Location of Tour")
    parser.add_argument(
        "price", type=int, required=True, help="Price")
    parser.add_argument(
        "description", type=str, required=True, help="Description of Tour")
    parser.add_argument(
        "main_image", type=str, required=True, help="Main cover Image")
    parser.add_argument(
        "images", type=str, required=True, help="Other Images")
    parser.add_argument(
        "video_url", type=str, required=True, help="Video of the Tour")

    return parser


def tours_patch_parser():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, help="Name of Tour")
    parser.add_argument(
        "location", type=str, help="Location of Tour")
    parser.add_argument(
        "price", type=int, help="Price")
    parser.add_argument(
        "description", type=str,  help="Description of Tour")
    parser.add_argument(
        "main_image", type=str, help="Main cover Image")
    parser.add_argument(
        "images", type=str, help="Other Images")
    parser.add_argument(
        "video_url", type=str, help="Video of the Tour")

    return parser

tours_parser = create_tours_parser()
tours_patch_parser = tours_patch_parser()

def serialize_tours(tours):
    return [tour.serialize() for tour in tours]

@tours_ns.route("/v1/tours")
class ToursResource(Resource):
    @tours_ns.expect(tours_parser)
    def post(self):
        args = tours_parser.parse_args()
        new_tour= Tours(**args)
        db.session.add(new_tour)
        db.session.commit()
        return {
            "message": "Tour created successfully",
            "new_extra_tour": new_tour.serialize(),
        }, 201

    def get(self):
        tours = Tours.query.all()
        return {"tours": serialize_tours(tours)}, 200

@tours_ns.route("/v1/tours/<int:id>")
class ToursItemResource(Resource):
    @tours_ns.expect(tours_patch_parser)
    def get(self, id):
        tour = Tours.query.get(id)
        if not tour:
            return {"message": "Tour not found"}, 404
        return {"tour": tour.serialize()}, 200

    def put(self, id):
        args = tours_patch_parser.parse_args()
        tour = Tours.query.get(id)
        if not tour:
            return {"message": "Tour not found"}, 404
        for key, value in args.items():
            if value:
                setattr(tour, key, value)
        db.session.commit()
        return {
            "message": "Tour updated successfully",
            "updated_tour": tour.serialize(),
        }, 200

    def patch(self, id):
        args = tours_patch_parser.parse_args()
        tour= Tours.query.get(id)
        if not tour:
            return {"message": "Tour not found"}, 404
        for key, value in args.items():
            if value:
                setattr(tour, key, value)
        db.session.commit()
        return {
            "message": "Tour updated successfully",
            "updated_tour": tour.serialize(),
        }, 200

    def delete(self, id):
        tour = Tours.query.get(id)
        if not tour:
            return {"message": "Tour not found"}, 404
        db.session.delete(tour)
        db.session.commit()
        return {"message": "Tour deleted successfully"}, 200

