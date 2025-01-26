import React from 'react';
import { Link } from 'react-router-dom';

function TourCard({ tour }) {
  return (
    <div className="tour-card">
      <img src={tour.imageUrl} alt={tour.name} className="tour-image" />
      <h3>{tour.name}</h3>
      <p>{tour.location}</p>
      <p>${tour.price}</p>
      <Link to={`/tours/${tour.id}`}>View Details</Link>
    </div>
  );
}

export default TourCard;
