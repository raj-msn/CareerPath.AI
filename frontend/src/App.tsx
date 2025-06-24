import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import './App.css';
// import ChatInterface from './components/ChatInterface'; // No longer directly used here
import Navbar from './components/Navbar';
import LandingPage from './pages/LandingPage';
import ChatPage from './pages/ChatPage';
import RoadmapsPage from './pages/RoadmapsPage';
import Sidebar from './components/Sidebar';

// Main application content component
const AppContent = () => {
  const location = useLocation();
  const showSidebarAndNavbar = location.pathname !== '/';

  return (
    <div className={`app-layout ${showSidebarAndNavbar ? 'with-sidebar' : ''}`}>
      {/* Particle background should be here, covering the whole layout */}
      <div className="particles-container">
        <div className="particle p1"></div>
        <div className="particle p2"></div>
        <div className="particle p3"></div>
        <div className="particle p4"></div>
        <div className="particle p5"></div>
      </div>
      {showSidebarAndNavbar && <Sidebar />}
      <div className="main-content-area">
        {showSidebarAndNavbar && <Navbar />}
        <main>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/chat" element={<ChatPage />} />
            <Route path="/roadmaps" element={<RoadmapsPage />} />
            {/* Add other routes here, e.g., a 404 page */}
          </Routes>
        </main>
      </div>
    </div>
  );
};

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
