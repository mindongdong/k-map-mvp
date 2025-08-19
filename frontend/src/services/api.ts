import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const datasetService = {
  async getDatasets(): Promise<any> {
    const response = await api.get('/datasets');
    return response.data;
  },
};

export default api;