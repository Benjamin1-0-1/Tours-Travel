import React, { useEffect, useState } from 'react';
import { getAllTours } from '../services/api';
import TourCard from '../components/TourCard';

function HomePage() {
  const [tours, setTours] = useState([]);

  useEffect(() => {
    getAllTours()
      .then((res) => setTours(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div>
      <h1 style={{ textAlign: 'center' }}>Available Tours</h1>
      <div className="tour-list">
        {tours.map((tour) => (
          <TourCard key={tour.id} tour={tour} />
        ))}
      </div>
    </div>
  );
}

export default HomePage;
