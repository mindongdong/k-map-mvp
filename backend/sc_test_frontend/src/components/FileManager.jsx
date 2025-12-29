import React, { useState, useEffect, useRef } from 'react';
import { scanFiles, importFile, getDatasetSummary } from '../api/KmapApi';

const FileManager = ({ onImportSuccess }) => {
  const [files, setFiles] = useState([]);
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState(null);
  const [datasetNames, setDatasetNames] = useState({});
  const [importStatus, setImportStatus] = useState({});

  const pollingRef = useRef(null);

  const handleScanFiles = async () => {
    try {
      setScanning(true);
      setError(null);
      const response = await scanFiles();
      const fileObjects = response.data.files.map(filename => ({
        filename,
        path: `/data/h5ad/${filename}`,
      }));
      setFiles(fileObjects);

      const initialNames = {};
      fileObjects.forEach(file => {
        const basename = file.filename.replace('.h5ad', '').replace('processed_', '');
        initialNames[file.path] = basename;
      });
      setDatasetNames(initialNames);
    } catch (err) {
      setError('Failed to scan files: ' + (err.response?.data?.detail || err.message));
    } finally {
      setScanning(false);
    }
  };

  const pollStatus = async () => {
    let activePollers = 0;
    
    // Use a functional update to get the latest state inside the interval
    setImportStatus(currentStatus => {
      const newStatus = { ...currentStatus };
      
      Object.keys(newStatus).forEach(async (name) => {
        const status = newStatus[name]?.dataset_info?.processing_status || newStatus[name]?.processing_status;

        if (status === 'importing' || status === 'starting') {
          activePollers++;
          try {
            const res = await getDatasetSummary(name);
            if (res.data) {
              setImportStatus(prev => ({ ...prev, [name]: res.data }));
              if (res.data.dataset_info.processing_status === 'completed' && onImportSuccess) {
                onImportSuccess();
              }
            }
          } catch (err) {
            if (err.response && err.response.status === 404) {
              console.log(`Polling for ${name}, but not found yet. Continuing.`);
            } else {
              console.error(`Error polling status for ${name}:`, err);
              setImportStatus(prev => ({ ...prev, [name]: { ...prev[name], processing_status: 'failed' } }));
            }
          }
        }
      });
      
      if (activePollers === 0 && pollingRef.current) {
        clearInterval(pollingRef.current);
        pollingRef.current = null;
      }
      return newStatus;
    });
  };

  const handleImport = async (file) => {
    const datasetName = datasetNames[file.path];
    if (!datasetName) return;

    try {
      setImportStatus(prev => ({ ...prev, [datasetName]: { processing_status: 'starting' } }));
      setError(null);
      
      await importFile(file.path, datasetName, true); // Overwrite by default
      
      setImportStatus(prev => ({ ...prev, [datasetName]: { processing_status: 'importing' } }));

      if (!pollingRef.current) {
        pollingRef.current = setInterval(pollStatus, 2500); // Poll every 2.5 seconds
      }
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message;
      setError(`Failed to start import for ${file.filename}: ${errorMsg}`);
      setImportStatus(prev => ({ ...prev, [datasetName]: { processing_status: 'failed' } }));
    }
  };

  useEffect(() => {
    return () => { if (pollingRef.current) clearInterval(pollingRef.current); };
  }, []);

  const renderStatus = (filePath, datasetName) => {
    const statusObj = importStatus[datasetName];
    const status = statusObj?.dataset_info?.processing_status || statusObj?.processing_status;
    const file = files.find(f => f.path === filePath);

    switch (status) {
      case 'starting':
        return <button className="btn btn-sm btn-info" disabled>Starting...</button>;
      case 'importing':
        const info = statusObj.dataset_info;
        const progress = info && info.n_cells > 0 ? `(${info.imported_cells} / ${info.n_cells})` : '';
        return <button className="btn btn-sm btn-info" disabled>{`Importing... ${progress}`}</button>;
      case 'completed':
        return <button className="btn btn-sm btn-success" disabled>Completed</button>;
      case 'failed':
        return <button className="btn btn-sm btn-danger" onClick={() => handleImport(file)}>Failed. Retry?</button>;
      default:
        return <button className="btn btn-sm btn-primary" onClick={() => handleImport(file)} disabled={!datasetName}>Import</button>;
    }
  };

  return (
    <div>
      <h5>File Manager</h5>
      <p className="text-muted">Scan and import .h5ad files from the server.</p>
      <button className="btn btn-primary mb-3" onClick={handleScanFiles} disabled={scanning}>{scanning ? 'Scanning...' : 'Scan Files'}</button>
      {error && <div className="alert alert-danger mt-2">{error}</div>}
      {files.length > 0 && (
        <div className="list-group mt-2">
          {files.map((file) => {
            const datasetName = datasetNames[file.path] || '';
            const isImporting = importStatus[datasetName] && (importStatus[datasetName].processing_status === 'importing' || importStatus[datasetName].processing_status === 'starting');
            return (
            <div key={file.path} className="list-group-item">
              <div className="d-flex w-100 justify-content-between align-items-center">
                <div className="flex-grow-1 me-3"><h6 className="mb-1">{file.filename}</h6></div>
                <div className="d-flex align-items-center">
                  <input
                    type="text"
                    className="form-control form-control-sm me-2"
                    style={{ width: '200px' }}
                    placeholder="Dataset name"
                    value={datasetName}
                    onChange={(e) => setDatasetNames(prev => ({...prev, [file.path]: e.target.value}))}
                    disabled={isImporting}
                  />
                  {renderStatus(file.path, datasetName)}
                </div>
              </div>
            </div>
          )})}
        </div>
      )}
    </div>
  );
};

export default FileManager;
