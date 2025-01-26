import React, { useEffect, useState, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getTourDetail, getReviews, postReview, bookTour } from '../services/api';
import { AuthContext } from '../context/AuthContext';

function TourDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { authToken } = useContext(AuthContext);

  const [tour, setTour] = useState(null);

  // Booking states
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [paymentMethod, setPaymentMethod] = useState('stripe');
  const [paymentToken, setPaymentToken] = useState('');
  const [bookingMessage, setBookingMessage] = useState('');

  // Reviews
  const [reviews, setReviews] = useState([]);
  const [username, setUsername] = useState('');
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState('');
  const [reviewMessage, setReviewMessage] = useState('');

  useEffect(() => {
    getTourDetail(id)
      .then((res) => setTour(res.data))
      .catch((err) => console.error("Tour detail error:", err));

    getReviews(id)
      .then((res) => setReviews(res.data))
      .catch((err) => console.error("Reviews error:", err));
  }, [id]);

  // Booking
  const handleBooking = async (e) => {
    e.preventDefault();
    if (!authToken) {
      setBookingMessage("You must be logged in to book a tour!");
      navigate('/login');
      return;
    }

    try {
      const res = await bookTour({
        tourId: parseInt(id),
        fullName,
        email,
        paymentMethod,
        paymentToken
      }, authToken);
      setBookingMessage(res.data.message);
      // reset
      setFullName('');
      setEmail('');
      setPaymentMethod('stripe');
      setPaymentToken('');
    } catch (error) {
      if (error.response && error.response.data && error.response.data.message) {
        setBookingMessage(error.response.data.message);
      } else {
        setBookingMessage("Booking failed. Please try again.");
      }
    }
  };

  // Reviews
  const handleReviewSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await postReview(id, {
        username: username || 'Anonymous',
        rating,
        comment
      });
      setReviews(prev => [res.data, ...prev]);
      setReviewMessage("Review submitted successfully!");
      // reset
      setUsername('');
      setRating(5);
      setComment('');
    } catch (err) {
      setReviewMessage("Failed to submit review");
    }
  };

  if (!tour) return <div>Loading...</div>;

  return (
    <div className="tour-detail">
      <h2>{tour.name}</h2>
      <img
        src={tour.imageUrl}
        alt={tour.name}
        style={{ maxWidth: '400px', display: 'block', marginBottom: '1rem' }}
      />
      <p><strong>Location:</strong> {tour.location}</p>
      <p><strong>Price:</strong> ${tour.price}</p>
      <p>{tour.description}</p>

      {/* Gallery */}
      {tour.images && tour.images.length > 0 && (
        <div className="gallery">
          {tour.images.map((img, idx) => (
            <img key={idx} src={img} alt={`${tour.name}-${idx}`} />
          ))}
        </div>
      )}

      {/* Video */}
      {tour.videoUrl && (
        <div className="video-container">
          <iframe
            title="Tour Video"
            src={tour.videoUrl}
            allowFullScreen
          />
        </div>
      )}

      {/* WhatsApp Chat */}
      <div style={{ marginTop: '1rem' }}>
        <a
          href="https://wa.me/254700123456?text=Hello%2C%20I%20am%20interested%20in%20the%20tour"
          target="_blank"
          rel="noopener noreferrer"
          className="btn-whatsapp"
        >
          Chat on WhatsApp
        </a>
        <p className="whatsapp-note">Click to chat directly with us on WhatsApp!</p>
      </div>

      {/* Booking Form */}
      <div className="booking-form">
        <h3>Book this tour</h3>
        <form onSubmit={handleBooking}>
          <label>Full Name:</label>
          <input
            type="text"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            required
          />

          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label>Payment Method:</label>
          <select
            value={paymentMethod}
            onChange={(e) => setPaymentMethod(e.target.value)}
          >
            <option value="stripe">Credit Card (Stripe)</option>
            <option value="paypal">PayPal</option>
            <option value="mpesa">M-Pesa</option>
          </select>

          {paymentMethod === 'stripe' && (
            <>
              <label>Fake Card Token:</label>
              <input
                type="text"
                placeholder="tok_visa"
                value={paymentToken}
                onChange={(e) => setPaymentToken(e.target.value)}
              />
            </>
          )}

          {paymentMethod === 'mpesa' && (
            <>
              <label>Phone Number (254XXXXXXXXX):</label>
              <input
                type="text"
                placeholder="2547XXXXXXX"
                value={paymentToken}
                onChange={(e) => setPaymentToken(e.target.value)}
              />
            </>
          )}

          <button type="submit">Book & Pay</button>
        </form>
        {bookingMessage && (
          <p className="booking-message">{bookingMessage}</p>
        )}
      </div>

      {/* Reviews */}
      <div className="reviews">
        <h3>Reviews</h3>
        {reviews.length === 0 ? (
          <p>No reviews yet. Be the first to review!</p>
        ) : (
          <ul className="review-list">
            {reviews.map((r) => (
              <li key={r.id}>
                <p><strong>{r.username}</strong> <em>({r.rating}/5)</em></p>
                <p>{r.comment}</p>
                <p style={{ fontSize: '0.8rem', color: '#666' }}>
                  {r.date}
                </p>
              </li>
            ))}
          </ul>
        )}

        <h4>Add a Review</h4>
        <form className="add-review-form" onSubmit={handleReviewSubmit}>
          <label>Name (optional):</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <label>Rating (1-5):</label>
          <input
            type="number"
            min="1"
            max="5"
            value={rating}
            onChange={(e) => setRating(e.target.value)}
            required
          />

          <label>Comment:</label>
          <textarea
            rows="3"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            required
          />

          <button type="submit">Submit Review</button>
        </form>
        {reviewMessage && (
          <p className="review-message">{reviewMessage}</p>
        )}
      </div>
    </div>
  );
}

export default TourDetailPage;
