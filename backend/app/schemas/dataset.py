from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class DatasetBase(BaseModel):
    public_dataset_id: str
    group_name: str
    data_type: str
    organ: str
    status: str
    publication_date: Optional[date] = None
    description: Optional[str] = None
    citation: Optional[str] = None
    file_storage_path: str

class DatasetCreate(DatasetBase):
    uploader_id: int

class DatasetUpdate(BaseModel):
    group_name: Optional[str] = None
    data_type: Optional[str] = None
    organ: Optional[str] = None
    status: Optional[str] = None
    publication_date: Optional[date] = None
    description: Optional[str] = None
    citation: Optional[str] = None

class DatasetResponse(DatasetBase):
    dataset_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
