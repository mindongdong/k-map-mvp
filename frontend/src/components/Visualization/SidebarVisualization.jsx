import React from 'react';
import './SidebarVisualization.css';

const SidebarVisualization = ({ selectedOptions, setSelectedOptions, searchTerm, setSearchTerm }) => {

  const handleOptionClick = (option) => {
    if (option === 'multiGene' || option === 'umap') {
      setSelectedOptions(prev => ({
        ...prev,
        [option]: !prev[option]
      }));
    } else {
      setSelectedOptions(prev => {
        const newState = {
          multiGene: prev.multiGene,
          umap: prev.umap,
          tissue: false,
          cellType: false,
          umap1: false,
          umapFeature: false
        };
        newState[option] = !prev[option];
        return newState;
      });
    }
  };

  return (
    <div className="sidebar-visualization">
      <div className="search-section">
        <input
          type="text"
          placeholder="Search Gene..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
        <img src="/Search.svg" alt="Search" className="Search" />
      </div>

      <div className="section">
        <div className="section-title" onClick={() => handleOptionClick('multiGene')}>
          <div className="title-icon title-icon--stack">
            <img src="/logo-bg-gray.svg" alt="bg" className="logo-bg-gray" />
            <img src="/bar-chart.svg" alt="fg" className="bar-chart" />
          </div>
          <span className="title-text">Multi-Gene Single Cell</span>
        </div>
        
        <div className="sub-options">
          <div className="option-item" onClick={() => handleOptionClick('tissue')}>
            <div className={`option-indicator ${selectedOptions.tissue ? 'active' : ''}`}></div>
            <span className="option-text">Sort by Tissue</span>
          </div>
          
          <div className="option-item" onClick={() => handleOptionClick('cellType')}>
            <div className={`option-indicator ${selectedOptions.cellType ? 'active' : ''}`}></div>
            <span className="option-text">Sort by Cell Type</span>
          </div>
        </div>
      </div>

      <div className="section">
        <div className="section-title" onClick={() => handleOptionClick('umap')}>
          <div className="title-icon title-icon--stack">
            <img src="/logo-bg-gray.svg" alt="bg" className="logo-bg-gray" />
            <img src="/scatter-plot.svg" alt="fg" className="scatter-plot" />
          </div>
          <span className="title-text">UMAP</span>
        </div>
        
        <div className="sub-options">
          <div className="option-item" onClick={() => handleOptionClick('umap1')}>
            <div className={`option-indicator ${selectedOptions.umap1 ? 'active' : ''}`}></div>
            <span className="option-text">UMAP</span>
          </div>
          
          <div className="option-item" onClick={() => handleOptionClick('umapFeature')}>
            <div className={`option-indicator ${selectedOptions.umapFeature ? 'active' : ''}`}></div>
            <span className="option-text">UMAP Feature</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SidebarVisualization;
