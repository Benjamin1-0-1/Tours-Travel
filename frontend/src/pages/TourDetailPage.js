import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { useSelector } from 'react-redux';

function TourDetailPage() {
  const { id } = useParams();
  const [tour, setTour] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [reviews, setReviews] = useState([]);
  const [newRating, setNewRating] = useState(5);
  const [newComment, setNewComment] = useState('');
  const [reviewMessage, setReviewMessage] = useState('');

  const { token } = useSelector((state) => state.auth);

  const TOUR_DETAIL_URL = `http://localhost:5500/apis/tours/v1/tours/${id}`;
  const REVIEWS_URL = `http://localhost:5500/apis/review/v1/reviews`; // same route for GET & POST

  // 1. Load the Tour
  useEffect(() => {
    axios.get(TOUR_DETAIL_URL)
      .then(res => {
        setTour(res.data.tour);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to fetch tour details");
        setLoading(false);
      });
  }, [TOUR_DETAIL_URL]);

  // 2. Load All Reviews, Filter for This Tour
  useEffect(() => {
    axios.get(REVIEWS_URL)
      .then(res => {
        // { reviews: [...] }
        const all = res.data.reviews;
        const filtered = all.filter(r => r.tour_id === parseInt(id));
        setReviews(filtered);
      })
      .catch(err => {
        console.error("Failed to fetch reviews:", err);
      });
  }, [REVIEWS_URL, id]);

  if (loading) return <div>Loading tour...</div>;
  if (error) return <div>{error}</div>;
  if (!tour) return <div>No tour data found</div>;

  // 3. POST a new review
  const handleReviewSubmit = async (e) => {
    e.preventDefault();
    if (!token) {
      setReviewMessage("You must be logged in to submit a review!");
      return;
    }
    try {
      // The backend requires user_name & created_at
      const response = await axios.post(REVIEWS_URL, {
        tour_id: parseInt(id),
        user_name: "Ben",  // or from your user state
        rating: parseInt(newRating),
        comment: newComment,
        created_at: new Date().toISOString()
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setReviewMessage("Review submitted!");
      // Add new review to local state
      setReviews(prev => [response.data.review, ...prev]);
      setNewRating(5);
      setNewComment('');
    } catch (err) {
      console.error(err);
      setReviewMessage("Failed to submit review");
    }
  };

  return (
    <div style={{ padding: '1rem' }}>
      <h2>{tour.name}</h2>
      <p><strong>Location:</strong> {tour.location}</p>
      <p><strong>Price:</strong> ${tour.price}</p>
      <p><strong>Description:</strong> {tour.description}</p>

      <hr />
      <h3>Reviews</h3>
      {reviews.length === 0 ? (
        <p>No reviews yet. Be the first to review!</p>
      ) : (
        reviews.map(r => (
          <div key={r.id} style={{ borderBottom: '1px solid #ccc', marginBottom: '1rem' }}>
            <p><strong>Rating:</strong> {r.rating} / 5</p>
            <p>{r.comment}</p>
            <p style={{ fontSize: '0.8rem', color: '#666' }}>
              (Review ID: {r.id}, Tour ID: {r.tour_id}, By: {r.user_name})
            </p>
          </div>
        ))
      )}

      <div style={{ marginTop: '2rem' }}>
        <h4>Add a Review</h4>
        <form onSubmit={handleReviewSubmit} style={{ maxWidth: '300px' }}>
          <label>Rating (1-5):</label>
          <input
            type="number"
            min="1"
            max="5"
            value={newRating}
            onChange={(e) => setNewRating(e.target.value)}
            required
          />
          <label>Comment:</label>
          <textarea
            rows="3"
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            required
          />
          <button type="submit" style={{ marginTop: '0.5rem' }}>Submit Review</button>
        </form>
        {reviewMessage && <p style={{ color: 'green', marginTop: '0.5rem' }}>{reviewMessage}</p>}
      </div>
    </div>
  );
}

export default TourDetailPage;
