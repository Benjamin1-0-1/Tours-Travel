import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  return (
    <div className="navbar">
      <Link to="/" className="logo">Tours & Travel</Link>
      <div className="nav-links">
        <Link to="/">Home</Link>
      </div>
    </div>
  );
}

export default Navbar;
