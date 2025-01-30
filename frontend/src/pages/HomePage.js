import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchTours } from "../store/slices/toursSlice";
import { Link } from 'react-router-dom';

function HomePage() {
  const dispatch = useDispatch();
  const { tours, status, error } = useSelector((state) => state.tours);

  useEffect(() => {
    if (status === 'idle') {
      dispatch(fetchTours());
    }
  }, [status, dispatch]);

  if (status === 'loading') return <div>Loading...</div>;
  if (status === 'failed') return <div>Error: {error}</div>;

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Available Tours</h2>
      <ul>
        {tours.map((tour) => (
          <li key={tour.id}>
            <Link to={`/tours/${tour.id}`}>{tour.name}</Link> - ${tour.price}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default HomePage;
