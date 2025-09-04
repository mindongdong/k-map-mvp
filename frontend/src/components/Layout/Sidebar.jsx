import React from 'react';
import './Sidebar.css';
import SidebarVisualization from '../Visualization/SidebarVisualization';

const Sidebar = ({ selectedOptions, setSelectedOptions, searchTerm, setSearchTerm, sidebarCollapsed, setSidebarCollapsed }) => {

  return (
    <>
      <div className={`sidebar ${sidebarCollapsed ? 'collapsed' : ''}`}>
        <div className="logo-section">
          <img src="/logo-black.svg" alt="K-MAP Logo" className="logo-black" />
          <h1 className="logo-text">K-MAP</h1>
          <img src="/arrow-forward-ios.svg" alt="Arrow" className="arrow-forward-ios" />
          <h1 className="page-title">Visualization</h1>
        </div>
        
        <SidebarVisualization
          selectedOptions={selectedOptions}
          setSelectedOptions={setSelectedOptions}
          searchTerm={searchTerm}
          setSearchTerm={setSearchTerm}
        />

        <div className="button-menu">
          <button className="profile-button" title="My Menu">
            <img src="/nest-wake-on.svg" alt="My Menu" className="nest-wake-on" />
          </button>
          <div className="action-buttons">
            <button 
              className="action-button" 
              title="Close Sidebar"
              onClick={() => setSidebarCollapsed(true)}
            >
              <img src="/left-panel-close.svg" alt="Close" className="left-panel-close" />
            </button>
            <button className="action-button" title="Scroll to Top">
              <img src="/vertical-align-top.svg" alt="Scroll Top" className="vertical-align-top" />
            </button>
            <button className="action-button" title="Scroll to Bottom">
              <img src="/vertical-align-bottom.svg" alt="Scroll Down" className="vertical-align-bottom" />
            </button>
          </div>
        </div>
      </div>
      
      {sidebarCollapsed && (
        <button
          className="sidebar-toggle"
          onClick={() => setSidebarCollapsed(false)}
          title="Open Sidebar"
        >
          <img 
            src="/left-panel-open.svg" 
            alt="Open Sidebar" 
            className="left-panel-open"
          />
        </button>
      )}
    </>
  );
};

export default Sidebar;
