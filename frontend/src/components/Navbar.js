import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

function Navbar() {
  const { authToken, logout } = useContext(AuthContext);

  return (
    <div className="navbar">
      <div>
        <Link to="/">Tours & Travel</Link>
        <Link to="/faq" style={{ marginLeft: '20px', color: '#fff' }}>FAQ</Link>
      </div>
      <div>
        {authToken ? (
          <button onClick={logout} style={{ marginLeft: '10px' }}>
            Logout
          </button>
        ) : (
          <>
            <Link to="/login" style={{ marginLeft: '10px', color: '#fff' }}>
              Login
            </Link>
            <Link to="/register" style={{ marginLeft: '10px', color: '#fff' }}>
              Register
            </Link>
          </>
        )}
      </div>
    </div>
  );
}

export default Navbar;
