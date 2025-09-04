import React, { useState } from 'react';
import Sidebar from '../components/Layout/Sidebar';
import Navigation from '../components/Visualization/Navigation';
function VisualizationPage() {
  const [selectedOptions, setSelectedOptions] = useState({
    multiGene: true,
    tissue: true,
    cellType: false,
    umap: false,
    umap1: false,
    umapFeature: false
  });
  const [searchTerm, setSearchTerm] = useState('');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

    return (
    <div style={{ height: '100vh', display: 'flex' }}>
      <Sidebar
        selectedOptions={selectedOptions}
        setSelectedOptions={setSelectedOptions}
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
        sidebarCollapsed={sidebarCollapsed}
        setSidebarCollapsed={setSidebarCollapsed}
      />
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', backgroundColor: '#ffffff' }}>
        <Navigation selectedOptions={selectedOptions} />
      </div>
    </div>
  );
}

export default VisualizationPage;
