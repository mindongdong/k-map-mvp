export interface Dataset {
  id: string;
  group: string;
  dataType: string;
  organ: string;
  status: string;
  publicationDate: string;
  description?: string;
  citation?: string;
}

export interface DatasetDetail extends Dataset {
  files: DatasetFile[];
  metadata: Record<string, string>;
  createdAt: string;
  updatedAt: string;
}

export interface DatasetFile {
  name: string;
  size: number;
  format: string;
  downloadUrl: string;
}

export interface UMAPData {
  x: number[];
  y: number[];
  cellTypes: string[];
  colors: string[];
}

export interface HeatmapData {
  genes: string[];
  tissues: string[];
  values: number[][];
}

export interface VisualizationResponse<T> {
  data: T;
  metadata: {
    generatedAt: string;
    datasetId: string;
  };
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
}

export interface ApiError {
  detail: string;
}
