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

export interface ApiError {
  detail: string;
}