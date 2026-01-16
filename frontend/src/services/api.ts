import axios, { AxiosError } from "axios";
import {
  Dataset,
  DatasetDetail,
  PaginatedResponse,
  UMAPData,
  HeatmapData,
  VisualizationResponse,
} from "../types/api";

const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:8000/api/v1";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// 에러 인터셉터
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/admin";
    }
    return Promise.reject(error);
  }
);

export const datasetService = {
  async getDatasets(
    page: number = 1,
    pageSize: number = 20
  ): Promise<PaginatedResponse<Dataset>> {
    const response = await api.get("/datasets", {
      params: { page, page_size: pageSize },
    });
    return response.data;
  },

  async getDatasetById(id: string): Promise<DatasetDetail> {
    const response = await api.get(`/datasets/${id}`);
    return response.data;
  },

  async downloadFile(datasetId: string, fileName: string): Promise<Blob> {
    const response = await api.get(
      `/datasets/${datasetId}/download/${fileName}`,
      { responseType: "blob" }
    );
    return response.data;
  },
};

export const visualizationService = {
  async getUMAPData(datasetId: string): Promise<VisualizationResponse<UMAPData>> {
    const response = await api.get("/visualizations/umap", {
      params: { dataset_id: datasetId },
    });
    return response.data;
  },

  async getHeatmapData(
    genes: string[],
    tissues: string[]
  ): Promise<VisualizationResponse<HeatmapData>> {
    const response = await api.post("/visualizations/heatmap", {
      genes,
      tissues,
    });
    return response.data;
  },
};

export const adminService = {
  async login(username: string, password: string): Promise<{ token: string }> {
    const response = await api.post("/admin/login", { username, password });
    const token = response.data.token;
    localStorage.setItem("token", token);
    api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    return response.data;
  },

  async createDataset(data: FormData): Promise<Dataset> {
    const response = await api.post("/admin/datasets", data, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response.data;
  },

  async updateDataset(id: string, data: Partial<Dataset>): Promise<Dataset> {
    const response = await api.put(`/admin/datasets/${id}`, data);
    return response.data;
  },

  async deleteDataset(id: string): Promise<void> {
    await api.delete(`/admin/datasets/${id}`);
  },
};

export default api;
