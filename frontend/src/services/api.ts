// API 서비스 및 HTTP 클라이언트 설정
//
// 이 파일에서 구현할 내용:
// 1. Axios 인스턴스 설정 (baseURL, timeout, headers)
// 2. Request/Response 인터셉터 (인증 토큰, 에러 처리)
// 3. Dataset API 서비스 (목록, 상세, 다운로드)
// 4. Visualization API 서비스 (UMAP, 히트맵, 박스플롯)
// 5. Admin API 서비스 (로그인, CRUD 작업)
// 6. 에러 처리 및 타입 안전성
//
// 예시 구조:
// import axios from 'axios';
// import { Dataset } from '../types/api';
//
// const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';
//
// const api = axios.create({
//   baseURL: API_BASE_URL,
//   timeout: 10000,
//   headers: {
//     'Content-Type': 'application/json',
//   },
// });
//
// // Request interceptor
// api.interceptors.request.use(
//   (config) => {
//     const token = localStorage.getItem('admin_token');
//     if (token) {
//       config.headers.Authorization = `Bearer ${token}`;
//     }
//     return config;
//   },
//   (error) => {
//     return Promise.reject(error);
//   }
// );
//
// // Response interceptor
// api.interceptors.response.use(
//   (response) => response,
//   (error) => {
//     if (error.response?.status === 401) {
//       localStorage.removeItem('admin_token');
//       window.location.href = '/admin';
//     }
//     return Promise.reject(error);
//   }
// );
//
// // Dataset API
// export const datasetService = {
//   async getDatasets(filters?: any): Promise<Dataset[]> {
//     // 데이터셋 목록 조회 로직
//   },
//
//   async getDataset(datasetId: string): Promise<Dataset> {
//     // 데이터셋 상세 조회 로직
//   },
//
//   async downloadFile(datasetId: string, fileName: string): Promise<any> {
//     // 파일 다운로드 로직
//   },
// };
//
// // Visualization API
// export const visualizationService = {
//   async getUmapVisualization(): Promise<any> {
//     // UMAP 시각화 데이터 조회 로직
//   },
//
//   async getHeatmapVisualization(): Promise<any> {
//     // 히트맵 시각화 데이터 조회 로직
//   },
//
//   async getBoxplotVisualization(): Promise<any> {
//     // 박스플롯 시각화 데이터 조회 로직
//   },
// };
//
// // Admin API
// export const adminService = {
//   async login(username: string, password: string): Promise<any> {
//     // 관리자 로그인 로직
//   },
//
//   async createDataset(dataset: any): Promise<Dataset> {
//     // 데이터셋 생성 로직
//   },
//
//   async updateDataset(datasetId: string, dataset: any): Promise<Dataset> {
//     // 데이터셋 수정 로직
//   },
//
//   async deleteDataset(datasetId: string): Promise<void> {
//     // 데이터셋 삭제 로직
//   },
//
//   async uploadFile(datasetId: string, file: File): Promise<any> {
//     // 파일 업로드 로직
//   },
// };
//
// export default api;

// TODO: 위 구조를 참고하여 API 서비스를 구현하세요