import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import TourDetailPage from './pages/TourDetailPage';
import Navbar from './components/Navbar';

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/tours/:id" element={<TourDetailPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
