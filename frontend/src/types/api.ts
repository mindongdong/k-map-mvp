// API 타입 정의
//
// 이 파일에서 정의할 타입들:
// 1. Dataset 관련 타입 (Dataset, DatasetCreate, DatasetUpdate, DatasetResponse)
// 2. API 요청/응답 타입 (DatasetFilters, LoginRequest, LoginResponse)
// 3. 에러 타입 (ApiError)
// 4. 시각화 관련 타입
//
// 예시 구조:
// export interface Dataset {
//   id: number;
//   dataset_id: string;
//   group: string;
//   data_type: string;
//   organ: string;
//   status: string;
//   description?: string;
//   citation?: string;
//   publication_date: string;
//   created_at: string;
//   updated_at?: string;
//   technical_metadata: Record<string, any>;
// }
//
// export interface DatasetCreate {
//   dataset_id: string;
//   group: string;
//   data_type: string;
//   organ: string;
//   status?: string;
//   description?: string;
//   citation?: string;
//   publication_date: string;
//   technical_metadata?: Record<string, any>;
// }
//
// export interface DatasetUpdate {
//   dataset_id?: string;
//   group?: string;
//   data_type?: string;
//   organ?: string;
//   status?: string;
//   description?: string;
//   citation?: string;
//   publication_date?: string;
//   technical_metadata?: Record<string, any>;
// }
//
// export interface DatasetFilters {
//   group?: string;
//   data_type?: string;
//   organ?: string;
//   search?: string;
//   skip?: number;
//   limit?: number;
// }
//
// export interface LoginRequest {
//   username: string;
//   password: string;
// }
//
// export interface LoginResponse {
//   access_token: string;
//   token_type: string;
// }
//
// export interface ApiError {
//   detail: string;
// }

// TODO: 위 구조를 참고하여 API 타입을 정의하세요