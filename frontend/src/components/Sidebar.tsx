import React, { useState } from 'react';
import './Sidebar.css';

const Sidebar: React.FC = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);

  const toggleSidebar = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <aside className={`sidebar ${isCollapsed ? 'sidebar-collapsed' : ''}`}>
      <div className="sidebar-header">
        {!isCollapsed && <h3>Chats</h3>}
        <button onClick={toggleSidebar} className="sidebar-toggle-btn">
          {isCollapsed ? '»' : '«'}
        </button>
        {/* Add a "New Chat" button here later */}
      </div>
      {!isCollapsed && (
        <div className="sidebar-content">
          {/* Placeholder for chat history items */}
          <p>Previous chats will appear here.</p>
        </div>
      )}
    </aside>
  );
};

export default Sidebar; 