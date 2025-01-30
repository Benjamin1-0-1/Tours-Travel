// frontend/src/pages/TourDetailPage.js
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import './TourDetailPage.css';

function TourDetailPage() {
  const { id } = useParams();
  const [tour, setTour] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchTour() {
      try {
        const res = await axios.get(`http://localhost:5000/apis/tours/v1/tours/${id}`);
        // Adjust if your route is different
        setTour(res.data.tour);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch tour details');
        setLoading(false);
      }
    }
    fetchTour();
  }, [id]);

  if (loading) return <div>Loading tour...</div>;
  if (error) return <div>{error}</div>;
  if (!tour) return <div>Tour not found</div>;

  return (
    <div className="tour-detail-page">
      <div className="tour-detail-content">
        <img
          src={tour.main_image || 'https://via.placeholder.com/600x400'}
          alt={tour.name}
          className="tour-detail-image"
        />
        <div className="tour-detail-info">
          <h2>{tour.name}</h2>
          <p><strong>Location:</strong> {tour.location}</p>
          <p><strong>Price:</strong> ${tour.price}</p>
          <p><strong>Description:</strong> {tour.description}</p>
          {tour.images && <p><strong>Gallery images:</strong> {tour.images}</p>}
          {/* You can parse the comma-separated images for a small gallery */}
        </div>
      </div>
    </div>
  );
}

export default TourDetailPage;
