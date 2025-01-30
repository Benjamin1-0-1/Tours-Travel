// frontend/src/pages/HomePage.js
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchTours } from '../store/slices/toursSlice';
import ToursList from '../components/ToursList';

function HomePage() {
  const dispatch = useDispatch();
  const { tours, status, error } = useSelector((state) => state.tours);

  useEffect(() => {
    if (status === 'idle') {
      dispatch(fetchTours());
    }
  }, [status, dispatch]);

  if (status === 'loading') return <div>Loading tours...</div>;
  if (status === 'failed') return <div>Error: {error}</div>;

  return (
    <div>
      <h2 style={{ textAlign: 'center', marginTop: '1rem' }}>Explore Our Tours</h2>
      <ToursList tours={tours} />
    </div>
  );
}

export default HomePage;
