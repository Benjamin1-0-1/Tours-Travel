// frontend/src/components/ToursList.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import './ToursList.css';

function ToursList({ tours }) {
  return (
    <div className="tours-container">
      {tours.map((tour) => (
        <div key={tour.id} className="tour-card">
          <img
            src={tour.main_image || 'https://via.placeholder.com/300x200'}
            alt={tour.name}
            className="tour-image"
          />
          <div className="tour-info">
            <h3>{tour.name}</h3>
            <p className="tour-location">{tour.location}</p>
            <p className="tour-price">${tour.price}</p>
            <p className="tour-description">
              {tour.description?.substring(0, 60)}...
            </p>
            <Link to={`/tours/${tour.id}`} className="view-btn">View More</Link>
          </div>
        </div>
      ))}
    </div>
  );
}

export default ToursList;
