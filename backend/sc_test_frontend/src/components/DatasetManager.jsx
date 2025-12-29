import React, { useState, useEffect } from 'react';
import { listDatasets, deleteDataset } from '../api/KmapApi';

const DatasetManager = ({ onActionComplete, refreshKey }) => {
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchDatasets = async () => {
    try {
      setLoading(true);
      const response = await listDatasets();
      setDatasets(response.data.datasets || []);
      setError(null);
    } catch (err) {
      setError('Failed to fetch datasets.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDatasets();
  }, [refreshKey]); // Refresh when the key changes

  const handleDelete = async (datasetName) => {
    if (!window.confirm(`Are you sure you want to delete the dataset "${datasetName}"? This action cannot be undone.`)) {
      return;
    }

    try {
      await deleteDataset(datasetName);
      // Refresh the list
      fetchDatasets();
      // Notify parent if needed
      if (onActionComplete) {
        onActionComplete();
      }
    } catch (err) {
      alert(`Failed to delete dataset: ${err.response?.data?.detail || err.message}`);
      console.error(err);
    }
  };

  if (loading) {
    return <p>Loading datasets...</p>;
  }

  if (error) {
    return <div className="alert alert-danger">{error}</div>;
  }

  return (
    <div>
      <h5>Manage Datasets</h5>
      {datasets.length === 0 ? (
        <p>No datasets found.</p>
      ) : (
        <ul className="list-group">
          {datasets.map((dataset) => (
            <li key={dataset.id} className="list-group-item d-flex justify-content-between align-items-center">
              <div>
                <strong>{dataset.name}</strong>
                <br />
                <small className="text-muted">
                  {dataset.n_cells} cells, {dataset.n_genes} genes - Status: {dataset.processing_status}
                </small>
              </div>
              <button
                className="btn btn-sm btn-outline-danger"
                onClick={() => handleDelete(dataset.name)}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default DatasetManager;
