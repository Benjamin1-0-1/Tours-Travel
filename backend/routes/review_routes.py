from ext import Review, Tour, db, jsonify, request, app, limiter

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
