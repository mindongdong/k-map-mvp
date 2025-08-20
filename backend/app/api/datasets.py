from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import List
import os

from app.schemas.dataset import DatasetResponse
from app.models.mockup import MOCK_DATASETS

router = APIRouter()

@router.get("/", response_model=List[DatasetResponse])
async def get_datasets():
    """데이터셋 목록 조회"""
    return MOCK_DATASETS

@router.get("/{public_dataset_id}", response_model=DatasetResponse)
async def get_dataset(public_dataset_id: str):
    """특정 데이터셋 상세 정보 조회"""
    for dataset in MOCK_DATASETS:
        if dataset["public_dataset_id"] == public_dataset_id:
            return dataset
    raise HTTPException(status_code=404, detail="Dataset not found")

@router.get("/{public_dataset_id}/download/{file_name}")
async def download_file(public_dataset_id: str, file_name: str):
    """데이터셋 파일 다운로드"""
    dataset_found = None
    for dataset in MOCK_DATASETS:
        if dataset["public_dataset_id"] == public_dataset_id:
            dataset_found = dataset
            break
    
    if not dataset_found:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # 실제 파일 경로 확인 (보안상 실제 경로 노출은 주의해야 함)
    # 여기서는 목업 데이터의 경로를 사용합니다.
    file_path = dataset_found["file_storage_path"]
    
    if os.path.basename(file_path) != file_name:
        raise HTTPException(status_code=404, detail="File not found in dataset")

    # 실제 파일 시스템에 파일이 존재한다고 가정하고 FileResponse를 반환합니다.
    # 지금은 목업이므로, 실제 파일이 없으면 에러가 발생합니다.
    # return FileResponse(path=file_path, filename=file_name)
    
    # 임시 목업 응답
    return {"message": f"Attempting to download {file_name} from {public_dataset_id}", "file_path": file_path}