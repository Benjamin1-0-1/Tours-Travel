# routes/tours.py
from routes.r_ext import db, Namespace, Resource, reqparse, jsonify, request
from models.tour import Tours

tours_ns = Namespace("tours", description="Tours Operations Resource")

def create_tours_parser():
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True, help="Name of Tour")
    parser.add_argument("location", type=str, required=True, help="Location of Tour")
    parser.add_argument("price", type=int, required=True, help="Price")
    parser.add_argument("description", type=str, required=True, help="Description of Tour")
    parser.add_argument("main_image", type=str, required=True, help="Main cover Image")
    parser.add_argument("images", type=str, required=True, help="Other Images")
    parser.add_argument("video_url", type=str, required=True, help="Video of the Tour")
    return parser

def tours_patch_parser():
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, help="Name of Tour")
    parser.add_argument("location", type=str, help="Location of Tour")
    parser.add_argument("price", type=int, help="Price")
    parser.add_argument("description", type=str, help="Description of Tour")
    parser.add_argument("main_image", type=str, help="Main cover Image")
    parser.add_argument("images", type=str, help="Other Images")
    parser.add_argument("video_url", type=str, help="Video of the Tour")
    return parser

tours_parser = create_tours_parser()
tours_patch_parser = tours_patch_parser()

def serialize_tours(tours_list):
    return [t.serialize() for t in tours_list]

@tours_ns.route("/v1/tours")
class ToursResource(Resource):
    # CREATE Tour
    @tours_ns.expect(tours_parser)
    def post(self):
        args = tours_parser.parse_args()
        new_tour = Tours(**args)
        db.session.add(new_tour)
        db.session.commit()
        return {
            "message": "Tour created successfully",
            "new_extra_tour": new_tour.serialize()
        }, 201

    # GET all tours
    def get(self):
        tours = Tours.query.all()
        return {"tours": serialize_tours(tours)}, 200

@tours_ns.route("/v1/tours/<int:id>")
class ToursItemResource(Resource):
    # GET single tour
    def get(self, id):
        tour = Tours.query.get(id)
        if not tour:
            return {"message": "Tour not found"}, 404
        return {"tour": tour.serialize()}, 200

    # PUT update entire tour
    @tours_ns.expect(tours_patch_parser)
    def put(self, id):
        tour = Tours.query.get(id)
        if not tour:
            return {"message": "Tour not found"}, 404
        args = tours_patch_parser.parse_args()
        for key, value in args.items():
            if value is not None:
                setattr(tour, key, value)
        db.session.commit()
        return {
            "message": "Tour updated successfully",
            "updated_tour": tour.serialize()
        }, 200

    # PATCH partial update
    @tours_ns.expect(tours_patch_parser)
    def patch(self, id):
        tour = Tours.query.get(id)
        if not tour:
            return {"message": "Tour not found"}, 404
        args = tours_patch_parser.parse_args()
        for key, value in args.items():
            if value is not None:
                setattr(tour, key, value)
        db.session.commit()
        return {
            "message": "Tour updated successfully",
            "updated_tour": tour.serialize()
        }, 200

    # DELETE
    def delete(self, id):
        tour = Tours.query.get(id)
        if not tour:
            return {"message": "Tour not found"}, 404
        db.session.delete(tour)
        db.session.commit()
        return {"message": "Tour deleted successfully"}, 200
