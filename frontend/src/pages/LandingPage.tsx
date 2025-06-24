import React from 'react';
import { Link } from 'react-router-dom';
import './LandingPage.css'; // We'll create this for styling

const LandingPage: React.FC = () => {
  return (
    <div className="landing-container">
      <div className="landing-content">
        <h1>CareerPath.AI</h1>
        <p className="welcome-text">Discover Your Future.</p>
        {/* <p>Navigate your career journey with personalized AI guidance.</p> */}
        <Link to="/chat" className="cta-button">
          Start Your Journey
        </Link>
      </div>
    </div>
  );
};

export default LandingPage; 