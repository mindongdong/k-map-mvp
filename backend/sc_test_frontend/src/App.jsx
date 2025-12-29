import React, { useState } from 'react';
import DatasetSelector from './components/DatasetSelector';
import UMAPPlot from './components/UMAPPlot';
import GeneSearch from './components/GeneSearch';
import ClusterInfo from './components/ClusterInfo';
import FileManager from './components/FileManager';
import DatasetManager from './components/DatasetManager';

function App() {
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [expressionData, setExpressionData] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleDatasetSelect = (datasetName) => {
    setSelectedDataset(datasetName);
    setExpressionData(null); // Reset expression data when dataset changes
  };

  const handleExpressionChange = (data) => {
    if (data) {
      setExpressionData(data);
    } else {
      setExpressionData(null);
      setSelectedDataset(prev => prev);
    }
  };

  const handleActionComplete = () => {
    setRefreshKey(k => k + 1);
  };

  return (
    <div className="container-fluid mt-3">
      <header className="mb-4">
        <h1>KMAP Visualization</h1>
        <p className="lead">Interactive single-cell data exploration</p>
      </header>

      <div className="row">
        <div className="col-md-4">
          <div className="card mb-3">
            <div className="card-body">
              <FileManager onImportSuccess={handleActionComplete} />
            </div>
          </div>
          <div className="card">
            <div className="card-body">
              <DatasetSelector refreshKey={refreshKey} onDatasetSelect={handleDatasetSelect} />
              <hr />
              <GeneSearch
                datasetName={selectedDataset}
                onExpressionDataChange={handleExpressionChange}
              />
            </div>
          </div>
          <div className="card mt-3">
              <div className="card-body">
                <ClusterInfo datasetName={selectedDataset} />
              </div>
          </div>
          <div className="card mt-3">
            <div className="card-body">
              <DatasetManager refreshKey={refreshKey} onActionComplete={handleActionComplete} />
            </div>
          </div>
        </div>
        
        <div className="col-md-8">
            <div className="card">
                <div className="card-body">
                    <UMAPPlot 
                        key={selectedDataset} // Re-mount when dataset changes
                        datasetName={selectedDataset} 
                        expressionData={expressionData} 
                    />
                </div>
            </div>
        </div>
      </div>
    </div>
  );
}

export default App;
