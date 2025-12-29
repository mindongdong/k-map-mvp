import React, { useState } from 'react';
import { getGeneExpression } from '../api/KmapApi';

const GeneSearch = ({ datasetName, onExpressionDataChange }) => {
  const [gene, setGene] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!datasetName || !gene) {
      setError('Please select a dataset and enter a gene symbol.');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const response = await getGeneExpression(datasetName, gene);
      onExpressionDataChange(response.data);
    } catch (err) {
      setError(`Gene '${gene}' not found or error fetching data.`);
      console.error(err);
      onExpressionDataChange(null); // Clear previous expression data on error
    } finally {
      setLoading(false);
    }
  };
  
  const handleClear = () => {
    setGene('');
    setError(null);
    onExpressionDataChange(null);
    // To reset the plot to cluster view, we need to trigger a re-fetch of the original UMAP data.
    // The easiest way is to have App.js manage this state.
    // For now, we just clear the expression. A better implementation would involve a state reset in App.
  }

  return (
    <div className="mb-3">
        <h5>Gene Expression</h5>
        <form onSubmit={handleSearch} className="d-flex">
            <input
            type="text"
            className="form-control me-2"
            value={gene}
            onChange={(e) => setGene(e.target.value.toUpperCase())}
            placeholder="e.g., CD3D"
            disabled={!datasetName}
            />
            <button type="submit" className="btn btn-success me-2" disabled={loading || !datasetName}>
            {loading ? 'Searching...' : 'Search'}
            </button>
            <button type="button" className="btn btn-secondary" onClick={handleClear} disabled={!datasetName}>
                Clear
            </button>
        </form>
        {error && <div className="alert alert-danger mt-2">{error}</div>}
    </div>
  );
};

export default GeneSearch;
