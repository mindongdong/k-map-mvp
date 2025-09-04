import React from 'react';
import Plot from 'react-plotly.js';
import { generateTissueData, generateCellTypeData, generateUMAPData } from '../data/sampleData';

const PlotlyVisualization = ({ selectedOptions, searchTerm }) => {
  
  // Plot 1: Sort by Tissue (Boxplot + Pie + Scatter)
  const renderSortByTissuePlot = () => {
    const data = generateTissueData(searchTerm || 'PECAM1');
    
    // Boxplot traces
    const boxTraces = data.expressionData.map((item, index) => ({
      x: new Array(item.values.length).fill(index),
      y: item.values,
      type: 'box',
      boxpoints: 'outliers',
      jitter: 0.3,
      pointpos: -1.8,
      marker: {
        size: 2,
        color: 'skyblue',
        opacity: 0.7
      },
      line: {
        color: 'skyblue',
        width: 1
      },
      showlegend: false,
      xaxis: 'x',
      yaxis: 'y'
    }));

    // Cell fraction pie traces
    const pieTraces = data.cellFractionData.map((item, index) => {
      if (item.fraction <= 0) return null;
      
      return {
        type: 'pie',
        values: [item.fraction, 1 - item.fraction],
        labels: ['Expressing', 'Non-expressing'],
        domain: {
          x: [index / data.groups.length, (index + 1) / data.groups.length],
          y: [0.12, 0.19]
        },
        marker: {
          colors: ['dodgerblue', 'lightgray'],
          line: { width: 0.5, color: 'white' }
        },
        textinfo: 'none',
        showlegend: false,
        hole: 0.5
      };
    }).filter(Boolean);

    // Total cell count scatter
    const scatterTrace = {
      x: data.totalCellData.map((_, index) => index),
      y: data.totalCellData.map(() => 0),
      mode: 'markers',
      type: 'scatter',
      marker: {
        size: data.totalCellData.map(item => 
          Math.max(8, (item.count / Math.max(...data.totalCellData.map(d => d.count))) * 25)
        ),
        color: '#1f3b87',
        opacity: 0.6,
        line: {
          color: 'white',
          width: 0.5
        }
      },
      showlegend: false,
      name: 'Total cells',
      xaxis: 'x',
      yaxis: 'y2'
    };

    // annotations
    const annotations = [];
    let tissueStart = 0;
    for (let i = 1; i <= data.expressionData.length; i++) {
      const prev = data.expressionData[i - 1];
      const curr = data.expressionData[i];
      const boundary = i === data.expressionData.length || (curr && curr.tissue !== prev.tissue);
      if (boundary) {
        const tissueEnd = i - 1;
        const center = (tissueStart + tissueEnd) / 2;
        annotations.push({
          x: center,
          y: 1.02,
          xref: 'x',
          yref: 'paper',
          showarrow: false,
          text: prev.tissue,
          xanchor: 'center',
          yanchor: 'bottom',
          font: { size: 12, color: '#404040' }
        });
        tissueStart = i;
      }
    }

    const layout = {
      title: {
        text: `${data.geneName} expression distribution`,
        font: { size: 16, color: '#404040' }
      },
      xaxis: {
        title: '',
        tickmode: 'array',
        tickvals: data.groups.map((_, index) => index),
        ticktext: data.groups,
        tickangle: -90,
        tickfont: { size: 9 },
        showgrid: false,
        zeroline: false
      },
      yaxis: {
        title: 'Expression',
        titlefont: { size: 12 },
        showgrid: true,
        gridcolor: '#f0f0f0',
        zeroline: false,
        domain: [0.25, 1.0]
      },
      yaxis2: {
        title: '',
        showgrid: false,
        zeroline: false,
        showticklabels: false,
        domain: [0.0, 0.1]
      },
      height: 600,
      margin: { l: 60, r: 50, t: 80, b: 140 },
      showlegend: false,
      plot_bgcolor: 'white',
      paper_bgcolor: 'white',
      annotations: annotations
    };

    return (
      <Plot
        data={[...boxTraces, ...pieTraces, scatterTrace]}
        layout={layout}
        config={{
          displayModeBar: true,
          displaylogo: false,
          modeBarButtonsToAdd: ['drawline', 'drawopenpath', 'eraseshape', 'autoscale2d', 'resetScale2d'],
          modeBarButtonsToRemove: ['toggleSpikelines'],
          toImageButtonOptions: {
            format: 'png',
            filename: `${data.geneName}_tissue_expression`,
            height: 600,
            width: 1200,
            scale: 2
          }
        }}
        style={{ width: '100%', height: '100%' }}
        useResizeHandler={true}
      />
    );
  };

  // Plot 2: Sort by Cell Type (Boxplot + Pie + Scatter)
  const renderSortByCellTypePlot = () => {
    const data = generateCellTypeData(searchTerm || 'PECAM1');
    
    // Boxplot traces
    const boxTraces = data.expressionData.map((item, index) => ({
      x: new Array(item.values.length).fill(index),
      y: item.values,
      type: 'box',
      boxpoints: 'outliers',
      jitter: 0.3,
      pointpos: -1.8,
      marker: {
        size: 2,
        color: 'skyblue',
        opacity: 0.7
      },
      line: {
        color: 'skyblue',
        width: 1
      },
      showlegend: false,
      xaxis: 'x',
      yaxis: 'y'
    }));

    // Cell fraction pie traces
    const pieTraces = data.cellFractionData.map((item, index) => {
      if (item.fraction <= 0) return null;
      
      return {
        type: 'pie',
        values: [item.fraction, 1 - item.fraction],
        labels: ['Expressing', 'Non-expressing'],
        domain: {
          x: [index / data.groups.length, (index + 1) / data.groups.length],
          y: [0.12, 0.19]
        },
        marker: {
          colors: ['dodgerblue', 'lightgray'],
          line: { width: 0.5, color: 'white' }
        },
        textinfo: 'none',
        showlegend: false,
        hole: 0.5
      };
    }).filter(Boolean);

    // Total cell count scatter
    const scatterTrace = {
      x: data.totalCellData.map((_, index) => index),
      y: data.totalCellData.map(() => 0),
      mode: 'markers',
      type: 'scatter',
      marker: {
        size: data.totalCellData.map(item => 
          Math.max(8, (item.count / Math.max(...data.totalCellData.map(d => d.count))) * 25)
        ),
        color: '#1f3b87',
        opacity: 0.6,
        line: {
          color: 'white',
          width: 0.5
        }
      },
      showlegend: false,
      name: 'Total cells',
      xaxis: 'x',
      yaxis: 'y2'
    };

    // annotations
    const annotations = [];
    let cellTypeStart = 0;
    for (let i = 1; i <= data.expressionData.length; i++) {
      const prev = data.expressionData[i - 1];
      const curr = data.expressionData[i];
      const boundary = i === data.expressionData.length || (curr && curr.celltype !== prev.celltype);
      if (boundary) {
        const end = i - 1;
        const center = (cellTypeStart + end) / 2;
        annotations.push({
          x: center,
          y: 1.02,
          xref: 'x',
          yref: 'paper',
          showarrow: false,
          text: prev.celltype,
          xanchor: 'center',
          yanchor: 'bottom',
          font: { size: 12, color: '#404040' }
        });
        cellTypeStart = i;
      }
    }

    const layout = {
      title: {
        text: `${data.geneName} expression distribution`,
        font: { size: 16, color: '#404040' }
      },
      xaxis: {
        title: '',
        tickmode: 'array',
        tickvals: data.groups.map((_, index) => index),
        ticktext: data.groups,
        tickangle: -90,
        tickfont: { size: 9 },
        showgrid: false,
        zeroline: false
      },
      yaxis: {
        title: 'Expression',
        titlefont: { size: 12 },
        showgrid: true,
        gridcolor: '#f0f0f0',
        zeroline: false,
        domain: [0.25, 1.0]
      },
      yaxis2: {
        title: '',
        showgrid: false,
        zeroline: false,
        showticklabels: false,
        domain: [0.0, 0.1]
      },
      height: 600,
      margin: { l: 60, r: 50, t: 80, b: 140 },
      showlegend: false,
      plot_bgcolor: 'white',
      paper_bgcolor: 'white',
      annotations: annotations
    };

    return (
      <Plot
        data={[...boxTraces, ...pieTraces, scatterTrace]}
        layout={layout}
        config={{
          displayModeBar: true,
          displaylogo: false,
          modeBarButtonsToAdd: ['drawline', 'drawopenpath', 'eraseshape', 'autoscale2d', 'resetScale2d'],
          modeBarButtonsToRemove: ['toggleSpikelines'],
          toImageButtonOptions: {
            format: 'png',
            filename: `${data.geneName}_celltype_expression`,
            height: 600,
            width: 1200,
            scale: 2
          }
        }}
        style={{ width: '100%', height: '100%' }}
        useResizeHandler={true}
      />
    );
  };

  // Plot 3: UMAP Clustering (Scatter plot)
  const renderUMAPPlot = () => {
    const umapData = generateUMAPData();
    const cellTypes = [...new Set(umapData.map(d => d.celltype))];
    const colors = [
      '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
      '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ];

    const traces = cellTypes.map((cellType, index) => {
      const subset = umapData.filter(d => d.celltype === cellType);
      return {
        x: subset.map(d => d.UMAP1),
        y: subset.map(d => d.UMAP2),
        mode: 'markers',
        type: 'scatter',
        name: cellType,
        marker: {
          size: 5,
          color: colors[index % colors.length],
          opacity: 0.8,
          line: { width: 0 }
        }
      };
    });

    const layout = {
      title: {
        text: 'UMAP: Broad cell type',
        font: { size: 16, color: '#404040' }
      },
      xaxis: {
        title: 'UMAP1',
        showticklabels: false,
        showgrid: false,
        zeroline: false
      },
      yaxis: {
        title: 'UMAP2',
        showticklabels: false,
        showgrid: false,
        zeroline: false
      },
      height: 600,
      margin: { l: 60, r: 50, t: 80, b: 50 },
      plot_bgcolor: 'white',
      paper_bgcolor: 'white',
      legend: {
        x: 1.02,
        y: 1,
        font: { size: 10 }
      }
    };

    return (
      <Plot
        data={traces}
        layout={layout}
        config={{
          displayModeBar: true,
          displaylogo: false,
          modeBarButtonsToAdd: ['drawline', 'drawopenpath', 'eraseshape', 'autoscale2d', 'resetScale2d'],
          toImageButtonOptions: {
            format: 'png',
            filename: 'umap_celltype_clustering',
            height: 700,
            width: 1000,
            scale: 2
          }
        }}
        style={{ width: '100%', height: '100%' }}
        useResizeHandler={true}
      />
    );
  };

  // Plot 4: UMAP Feature (Gene expression)
  const renderUMAPFeaturePlot = () => {
    const umapData = generateUMAPData();
    const gene = searchTerm || 'CST3';

    const trace = {
      x: umapData.map(d => d.UMAP1),
      y: umapData.map(d => d.UMAP2),
      mode: 'markers',
      type: 'scatter',
      marker: {
        size: 8,
        color: umapData.map(d => d[gene] || Math.random() * 5),
        colorscale: 'Viridis',
        opacity: 0.8,
        colorbar: {
          title: `${gene} expression`,
          titleside: 'right',
          titlefont: { size: 12 }
        }
      },
      showlegend: false
    };

    const layout = {
      title: {
        text: `UMAP: ${gene}`,
        font: { size: 16, color: '#404040' }
      },
      xaxis: {
        title: 'UMAP1',
        showticklabels: false,
        showgrid: false,
        zeroline: false
      },
      yaxis: {
        title: 'UMAP2',
        showticklabels: false,
        showgrid: false,
        zeroline: false
      },
      height: 600,
      margin: { l: 60, r: 80, t: 80, b: 50 },
      plot_bgcolor: 'white',
      paper_bgcolor: 'white'
    };

    return (
      <Plot
        data={[trace]}
        layout={layout}
        config={{
          displayModeBar: true,
          displaylogo: false,
          modeBarButtonsToAdd: ['drawline', 'drawopenpath', 'eraseshape', 'autoscale2d', 'resetScale2d'],
          toImageButtonOptions: {
            format: 'png',
            filename: `umap_${gene}_expression`,
            height: 700,
            width: 1000,
            scale: 2
          }
        }}
        style={{ width: '100%', height: '100%' }}
        useResizeHandler={true}
      />
    );
  };

  if (selectedOptions.tissue) {
    return renderSortByTissuePlot();
  } else if (selectedOptions.cellType) {
    return renderSortByCellTypePlot();
  } else if (selectedOptions.umap1) {
    return renderUMAPPlot();
  } else if (selectedOptions.umapFeature) {
    return renderUMAPFeaturePlot();
  } else {
    return (
      <div style={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center', 
        height: '100%',
        color: '#9a9a9a',
        fontSize: '18px',
        fontFamily: 'Pretendard, sans-serif'
      }}>
        Select a visualization option from the sidebar
      </div>
    );
  }
};

export default PlotlyVisualization;
