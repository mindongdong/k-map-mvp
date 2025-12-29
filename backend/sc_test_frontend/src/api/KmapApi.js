import axios from 'axios';

// k-map-mvp API endpoint
const API_URL = 'http://localhost:8000/api/v1/sc';
const ADMIN_URL = 'http://localhost:8000/api/v1/sc/admin';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

const adminClient = axios.create({
  baseURL: ADMIN_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const listDatasets = () => {
  return apiClient.get('/datasets');
};

export const getDatasetSummary = (datasetName) => {
  return apiClient.get(`/datasets/${datasetName}`);
};

export const getUmapData = (datasetName, clusterIds = null, sampleRate = null) => {
  const params = {};
  if (clusterIds) {
    params.cluster_ids = clusterIds.join(',');
  }
  if (sampleRate) {
    params.sample_rate = sampleRate;
  }
  return apiClient.get(`/umap/${datasetName}`, { params });
};

export const getMarkerGenes = (datasetName, clusterId = null, topN = 25) => {
    const params = { top_n: topN };
    if (clusterId) {
        params.cluster_id = clusterId;
    }
    return apiClient.get(`/markers/${datasetName}`, { params });
};

export const getGeneExpression = (datasetName, geneSymbol) => {
  return apiClient.get(`/expression/${datasetName}/${geneSymbol}`);
};

export const searchGenes = (datasetName, query, limit = 50) => {
    const params = { q: query, limit: limit };
    return apiClient.get(`/genes/${datasetName}/search`, { params });
};

export const deleteDataset = (datasetName) => {
  return adminClient.delete(`/datasets/${datasetName}`);
};

// File management APIs (admin endpoints)
export const scanFiles = (directory = '/data/h5ad') => {
    return adminClient.get('/files/scan', { params: { directory } });
};

export const importFile = (filePath, datasetName, overwrite = false, importExpression = false) => {
    const endpoint = overwrite ? '/import/overwrite' : '/import';
    return adminClient.post(endpoint, {
        file_path: filePath,
        name: datasetName,
        import_expression: importExpression
    });
};
