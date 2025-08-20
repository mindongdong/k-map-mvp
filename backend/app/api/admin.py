from fastapi import APIRouter, HTTPException, Body
from typing import List
from datetime import datetime, date

from app.schemas.dataset import DatasetCreate, DatasetUpdate, DatasetResponse
from app.models.mockup import MOCK_DATASETS

router = APIRouter()

@router.post("/login")
async def admin_login(username: str = Body(...), password: str = Body(...)):
    """관리자 로그인"""
    # 실제 인증 로직은 여기에 구현되어야 합니다.
    if username == "admin" and password == "admin_password":
        return {"message": "Admin login successful", "token": "fake-jwt-token"}
    raise HTTPException(status_code=401, detail="Incorrect username or password")

@router.post("/datasets", response_model=DatasetResponse, status_code=201)
async def create_dataset(dataset: DatasetCreate):
    """데이터셋 생성 (업로드)"""
    new_dataset = dataset.dict()
    new_dataset["dataset_id"] = max(d["dataset_id"] for d in MOCK_DATASETS) + 1
    new_dataset["created_at"] = datetime.now()
    new_dataset["updated_at"] = datetime.now()
    MOCK_DATASETS.append(new_dataset)
    return new_dataset

@router.put("/datasets/{public_dataset_id}", response_model=DatasetResponse)
async def update_dataset(public_dataset_id: str, dataset_update: DatasetUpdate):
    """데이터셋 수정"""
    for i, dataset in enumerate(MOCK_DATASETS):
        if dataset["public_dataset_id"] == public_dataset_id:
            update_data = dataset_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                dataset[key] = value
            dataset["updated_at"] = datetime.now()
            MOCK_DATASETS[i] = dataset
            return dataset
    raise HTTPException(status_code=404, detail="Dataset not found")

@router.delete("/datasets/{public_dataset_id}", status_code=204)
async def delete_dataset(public_dataset_id: str):
    """데이터셋 삭제"""
    global MOCK_DATASETS
    original_len = len(MOCK_DATASETS)
    MOCK_DATASETS = [d for d in MOCK_DATASETS if d["public_dataset_id"] != public_dataset_id]
    if len(MOCK_DATASETS) == original_len:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return
