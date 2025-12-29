import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import { getUmapData } from '../api/KmapApi';

const UMAPPlot = ({ datasetName, expressionData }) => {
  const [plotData, setPlotData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [loadTime, setLoadTime] = useState(null);
  const [networkTime, setNetworkTime] = useState(null);
  const [totalTime, setTotalTime] = useState(null);

  useEffect(() => {
    if (!datasetName) return;

    const fetchUmapData = async () => {
      try {
        setLoading(true);
        setError(null);
        setLoadTime(null);
        setNetworkTime(null);
        setTotalTime(null);

        const startTime = performance.now();
        const response = await getUmapData(datasetName, null, null); // Fetch all data points
        const endTime = performance.now();
        const data = response.data;

        const totalMs = Math.round(endTime - startTime);
        const queryMs = data.query_duration_ms || 0;
        const networkMs = totalMs - queryMs;
        
        // Manually convert cluster_id strings to numbers for categorical coloring
        const uniqueClusters = [...new Set(data.cells.map(c => c.cluster_id))];
        const clusterColorMap = new Map(uniqueClusters.map((cluster, index) => [cluster, index]));
        const numericalColorData = data.cells.map(c => clusterColorMap.get(c.cluster_id));

        const trace = {
          x: data.cells.map(c => c.umap_1),
          y: data.cells.map(c => c.umap_2),
          mode: 'markers',
          type: 'scattergl', // Use WebGL for better performance
          marker: {
            color: numericalColorData,
            colorscale: 'Viridis',
            size: 5,
            showscale: false,
          },
          // Pass detailed data for the hover template
          customdata: data.cells.map(c => ({
            barcode: c.cell_barcode,
            cluster: c.cluster_id,
            celltype: c.cell_type || 'N/A'
          })),
          // Use a rich hovertemplate instead of simple text
          hovertemplate:
            '<b>Cell: %{customdata.barcode}</b><br>' +
            'Cluster: %{customdata.cluster}<br>' +
            'Cell Type: %{customdata.celltype}<br>' +
            'UMAP-1: %{x:.3f}<br>' +
            'UMAP-2: %{y:.3f}' +
            '<extra></extra>', // Hides the trace name
          hoverinfo: 'none'
        };
        
        setPlotData([trace]);
        setLoadTime(queryMs);
        setNetworkTime(networkMs);
        setTotalTime(totalMs);

      } catch (err) {
        setError('Failed to fetch UMAP data.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchUmapData();
  }, [datasetName]);

  useEffect(() => {
    if (expressionData && plotData) {
      const newTrace = { ...plotData[0] };
      newTrace.marker = {
        ...newTrace.marker,
        color: expressionData.values,
        colorscale: 'Plasma',
        colorbar: { title: 'Expression' }
      };
      newTrace.text = expressionData.values.map(v => `Expression: ${v.toFixed(3)}`);
      setPlotData([newTrace]);
    }
  }, [expressionData]);


  if (loading) {
    return <p>Loading UMAP plot...</p>;
  }

  if (error) {
    return <div className="alert alert-danger">{error}</div>;
  }

  if (!plotData) {
    return <p>Select a dataset to view the UMAP plot.</p>;
  }

  return (
    <>
      {totalTime != null && (
        <p className="text-muted text-center" style={{ fontSize: '0.9em' }}>
          DB Query: {loadTime} ms | Network: {networkTime} ms | Total: {totalTime} ms
        </p>
      )}
      <Plot
        data={plotData}
        layout={{
          title: `UMAP of ${datasetName}`,
          xaxis: { title: 'UMAP 1' },
          yaxis: { title: 'UMAP 2' },
          autosize: true
        }}
        useResizeHandler={true}
        style={{ width: '100%', height: '600px' }}
      />
    </>
  );
};

export default UMAPPlot;
