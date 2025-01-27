from ext import jsonify, request, jsonify, app, db, Tour

@app.route('/api/tours', methods=['GET'])
def get_tours():
    tours = Tour.query.all()
    result = []
    for t in tours:
        result.append({
            "id": t.id,
            "name": t.name,
            "location": t.location,
            "price": t.price,
            "description": t.description,
            "imageUrl": t.main_image,
            "images": parse_images(t.images),
            "videoUrl": t.video_url
        })
    return jsonify(result)

@app.route('/api/tours/<int:tour_id>', methods=['GET'])
def get_tour_detail(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    return jsonify({
        "id": tour.id,
        "name": tour.name,
        "location": tour.location,
        "price": tour.price,
        "description": tour.description,
        "imageUrl": tour.main_image,
        "images": parse_images(tour.images),
        "videoUrl": tour.video_url
    })

def parse_images(images_field):
    if not images_field:
        return []
    return [url.strip() for url in images_field.split(',')]
