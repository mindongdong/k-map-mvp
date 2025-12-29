import React, { useState, useEffect, useImperativeHandle, forwardRef } from 'react';
import { listDatasets } from '../api/KmapApi';

const DatasetSelector = forwardRef((props, ref) => {
  const { onDatasetSelect, refreshKey } = props;
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
      setError('Failed to fetch datasets. Is the API server running?');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDatasets();
  }, [refreshKey]);

  if (loading) {
    return <p>Loading datasets...</p>;
  }

  if (error) {
    return <div className="alert alert-danger">{error}</div>;
  }

  return (
    <div className="mb-3">
      <label htmlFor="dataset-select" className="form-label"><h3>Select a Dataset</h3></label>
      <select 
        id="dataset-select"
        className="form-select" 
        onChange={(e) => onDatasetSelect(e.target.value)}
        defaultValue=""
      >
        <option value="" disabled>Choose a dataset</option>
        {datasets.map((dataset) => (
          <option key={dataset.id} value={dataset.name}>
            {dataset.name} ({dataset.n_cells} cells)
          </option>
        ))}
      </select>
    </div>
  );
});

export default DatasetSelector;
