from ext import reqparse, Namespace, Resource , db
from models.booking import BookingPlacement

bookingPlacement_ns = Namespace("bookings", description="Booking operations")

# POST AND PUT METHOD used to create new records
def create_booking_parser():
    parser = reqparse.RequestParser()

    parser.add_argument(
        "userId", type=int, required=True, help="User ID is required")
    parser.add_argument(
        "price", type=float, required=True, help="Price is required")
    parser.add_argument(
        "adults", type=int, required=True, help="Number of adults is required")
    parser.add_argument(
        "children", type=int, required=True, help="Number of children is required")
    parser.add_argument(
        "startDate", type=str, required=True, help="Start date is required")
    parser.add_argument(
        "endDate", type=str, required=True, help="End date is required")
    parser.add_argument(
        "fullName", type=str, required=True, help="Full name is required")
    parser.add_argument(
        "email", type=str, required=True, help="Email is required")

    return parser

# PATCH METHOD used to do modifications
def bookingPlacement_patch_parser():
    parser = reqparse.RequestParser()
    parser.add_argument("userId", type=int)
    parser.add_argument("price", type=float)
    parser.add_argument("adults", type=int,)
    parser.add_argument("children", type=int,)
    parser.add_argument("startDate", type=str)
    parser.add_argument("endDate", type=str)
    parser.add_argument("fullName", type=str)
    parser.add_argument("email", type=str)

    return parser

bookingPlacement_parser = create_booking_parser()
bookingPlacement_patch_parser = bookingPlacement_patch_parser()

def serialize_bookingPlacement(booking):
    return {
        "id": booking.id,
        "userId": booking.userId,
        "price": booking.price,
        "adults": booking.adults,
        "children": booking.children,
        "startDate": booking.start_date,
        "endDate": booking.end_date,
        "fullName": booking.full_name,
        "email": booking.email
        }


@bookingPlacement_ns.route("/v1/bookings")
class BookingPlacementCollectionResource(Resource):
    #get all bookings
    def get(self):
        bookings = BookingPlacement.query.all()
        return {
            "bookingsPlacement":
            [serialize_bookingPlacement(booking) for booking in bookings]
        }, 200

    @bookingPlacement_ns.expect(bookingPlacement_parser, validate=True)
    def post(self):
        args = bookingPlacement_parser.parse_args()
        new_booking = BookingPlacement(
            user_id=args["userId"],
            price=args["price"],
            adults=args["adults"],
            children=args["children"],
            start_date=args["startDate"],
            end_date=args["endDate"],
            full_name=args["fullName"],
            email=args["email"]
        )
        db.session.add(new_booking)
        try:
            db.session.commit()
            return {
                "message": "Booking created successfully",
                "bookingPlacement":serialize_bookingPlacement(new_booking)
            } ,201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to create booking: {e}"} , 400#could be 500


@bookingPlacement_ns.route("/v1/bookings/<int:id>")
class BookingPlacementResource(Resource):
    def get(self, id):
        booking = BookingPlacement.query.get(id)
        if booking:
            return {"bookingPlacement": serialize_bookingPlacement(booking)}, 200
        return {"message": "Booking Placement not found"}, 404

    @bookingPlacement_ns.expect(bookingPlacement_parser, validate=True)
    def put(self, id):
        booking = BookingPlacement.query.get(id)
        if not booking:
            return {"message": "Booking Placement not found"}, 404
        args = bookingPlacement_parser.parse_args()
        booking.useId = args["userId"]
        booking.price = args["price"]
        booking.adults = args["adults"]
        booking.children = args["children"]
        booking.start_date = args["startDate"]
        booking.end_date = args["endDate"]
        booking.full_name = args["fullName"]
        booking.email = args["email"]

        db.session.add(booking)
        try:
            db.session.commit()
            return {"message": "Booking updated successfully",
                    "bookingPlacement": serialize_bookingPlacement(booking)}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to update booking: {e}"} , 500

    @bookingPlacement_ns.expect(bookingPlacement_patch_parser, validate=True)
    def patch(self, id):
        booking = BookingPlacement.query.get(id)
        if not booking:
            return {"message": "Booking Placement not found"}, 404
        args = bookingPlacement_patch_parser.parse_args()
        if args['userId'] is not None:#i think it should be user but to b checked
            booking.userId = args["userId"]
        if args['price'] is not None:
            booking.price = args["price"]
        if args['adults'] is not None:
            booking.adults = args["adults"]
        if args['children'] is not None:
            booking.children = args["children"]
        if args['startDate'] is not None:
            booking.start_date = args["startDate"]
        if args['endDate'] is not None:
            booking.end_date = args["endDate"]
        if args['fullName'] is not None:
            booking.full_name = args["fullName"]
        if args['email'] is not None:
            booking.email = args["email"]

        db.session.add(booking)
        try:
            db.session.commit()
            return {"message": "Booking updated successfully",
                    "bookingPlacement": serialize_bookingPlacement(booking)}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to update booking: {e}"} , 500

    def delete(self, id):
        booking = BookingPlacement.query.get(id)
        if not booking:
            return {"message": "Booking Placement not found"}, 404
        db.session.delete(booking)
        try:
            db.session.commit()
            return {"message": "Booking deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to delete booking: {e}"} , 500
