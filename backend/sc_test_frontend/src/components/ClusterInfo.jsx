import React, { useState, useEffect } from 'react';
import { getMarkerGenes } from '../api/KmapApi';

const ClusterInfo = ({ datasetName }) => {
  const [markerGenes, setMarkerGenes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!datasetName) return;

    const fetchMarkerGenes = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await getMarkerGenes(datasetName, null, 5); // Get top 5 marker genes for all clusters
        
        // Group genes by cluster
        const genesByCluster = response.data.marker_genes.reduce((acc, gene) => {
            const cluster = gene.cluster_id;
            if (!acc[cluster]) {
                acc[cluster] = [];
            }
            acc[cluster].push(gene);
            return acc;
        }, {});

        setMarkerGenes(genesByCluster);

      } catch (err) {
        setError('Failed to fetch marker genes.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchMarkerGenes();
  }, [datasetName]);

  if (!datasetName) {
      return null;
  }

  if (loading) {
    return <p>Loading cluster info...</p>;
  }

  if (error) {
    return <div className="alert alert-danger">{error}</div>;
  }

  return (
    <div className="mt-4">
      <h5>Top 5 Marker Genes per Cluster</h5>
      <div className="accordion" id="cluster-accordion">
        {Object.entries(markerGenes).map(([clusterId, genes]) => (
          <div className="accordion-item" key={clusterId}>
            <h2 className="accordion-header" id={`heading-${clusterId}`}>
              <button 
                className="accordion-button collapsed" 
                type="button" 
                data-bs-toggle="collapse" 
                data-bs-target={`#collapse-${clusterId}`}
              >
                Cluster {clusterId}
              </button>
            </h2>
            <div id={`collapse-${clusterId}`} className="accordion-collapse collapse" data-bs-parent="#cluster-accordion">
              <div className="accordion-body">
                <ul className="list-group">
                  {genes.map((gene) => (
                    <li key={gene.gene_symbol} className="list-group-item d-flex justify-content-between align-items-center">
                      {gene.gene_symbol}
                      <span className="badge bg-primary rounded-pill">
                        log2fc: {gene.log2_fold_change != null ? gene.log2_fold_change.toFixed(2) : 'N/A'}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ClusterInfo;
