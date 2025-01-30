from routes.booking_routes import bookingPlacement_ns
from routes.tour_routes import tours_ns
from routes.user_routes import user_profiles_ns
from routes.review_routes import review_ns

all_namespaces =[
    (bookingPlacement_ns, "/bookingPlacement"),
    (tours_ns, "/tours"),
    (user_profiles_ns, "/user_profiles"),
    (review_ns, "/review"),
]
