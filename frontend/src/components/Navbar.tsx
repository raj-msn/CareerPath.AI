import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

const Navbar: React.FC = () => {
  const location = useLocation();

  // Don't show Navbar on the landing page
  if (location.pathname === '/') {
    return null;
  }

  return (
    <nav className="navbar">
      <Link to="/" className="nav-logo">
        CareerPath.AI
      </Link>
      <div className="nav-links">
        <Link to="/chat" className={location.pathname === '/chat' ? 'active' : ''}>
          Chat
        </Link>
        <Link to="/roadmaps" className={location.pathname === '/roadmaps' ? 'active' : ''}>
          Roadmaps
        </Link>
      </div>
    </nav>
  );
};

export default Navbar; 