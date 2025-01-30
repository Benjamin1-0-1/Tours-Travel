import React from 'react';
import { useParams } from 'react-router-dom';

function TourDetailPage() {
  const { id } = useParams();
  // In real usage, you might fetch the single tour detail from an API or use your Redux state
  return (
    <div style={{ padding: '2rem' }}>
      <h2>Tour Detail - ID: {id}</h2>
      {/* Display details about the selected tour */}
    </div>
  );
}

export default TourDetailPage;
