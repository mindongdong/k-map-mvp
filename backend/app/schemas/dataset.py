

from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import List, Optional

class DatasetSchema(BaseModel):
    dataset_id: int
    public_dataset_id: str
    uploader_id: int
    group_name: Optional[str] = None
    data_type: Optional[str] = None
    organ: Optional[str] = None
    status: Optional[str] = None
    publication_date: Optional[date] = None
    description: Optional[str] = None
    citation: Optional[str] = None
    file_storage_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DatasetListSchema(BaseModel):
    datasets: List[DatasetSchema]
    total_count: Optional[int] = None
    skip: Optional[int] = None
    limit: Optional[int] = None

class DatasetCreate(BaseModel):
    public_dataset_id: str = Field(..., description="공개 데이터셋 ID (예: HBM123.ABCD.456)")
    group_name: Optional[str] = None
    data_type: Optional[str] = None
    organ: Optional[str] = None
    description: Optional[str] = None
    citation: Optional[str] = None
    file_storage_path: Optional[str] = None
    publication_date: Optional[date] = None

class DatasetUpdate(BaseModel):
    group_name: Optional[str] = None
    data_type: Optional[str] = None
    organ: Optional[str] = None
    status: Optional[str] = None
    publication_date: Optional[date] = None
    description: Optional[str] = None
    citation: Optional[str] = None
