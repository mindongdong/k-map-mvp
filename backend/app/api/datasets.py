
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.dataset import DatasetListSchema, DatasetSchema
from app.core.dependencies import get_db, get_current_user_optional
from app.services.dataset_service import DatasetService
from app.models.user import User
from fastapi.responses import FileResponse
import os

router = APIRouter(tags=["Datasets"])

# Mock data removed - now using real database

@router.get("", response_model=DatasetListSchema)
def get_datasets(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    group_name: Optional[str] = Query(None, description="Filter by research group name"),
    data_type: Optional[str] = Query(None, description="Filter by data type"),
    organ: Optional[str] = Query(None, description="Filter by organ"),
    status: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search in description, citation, and group name"),
    sort_by: str = Query("publication_date", description="Field to sort by"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order: asc or desc"),
    db: Session = Depends(get_db)
):
    """
    데이터셋 목록을 반환합니다. (필터링, 검색, 정렬, 페이지네이션 지원)
    """
    datasets = DatasetService.get_datasets(
        db=db,
        skip=skip,
        limit=limit,
        group_name=group_name,
        data_type=data_type,
        organ=organ,
        status=status,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    total_count = DatasetService.get_datasets_count(
        db=db,
        group_name=group_name,
        data_type=data_type,
        organ=organ,
        status=status,
        search=search
    )
    
    return DatasetListSchema(
        datasets=datasets,
        total_count=total_count,
        skip=skip,
        limit=limit
    )

@router.get("/{public_dataset_id}", response_model=DatasetSchema)
def get_dataset_by_public_id(
    public_dataset_id: str,
    db: Session = Depends(get_db)
):
    """
    Public ID로 특정 데이터셋의 정보를 조회합니다.
    """
    dataset = DatasetService.get_dataset_by_public_id(db=db, public_dataset_id=public_dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset

@router.get("/internal/{dataset_id}", response_model=DatasetSchema)
def get_dataset_by_internal_id(
    dataset_id: int,
    db: Session = Depends(get_db)
):
    """
    내부 ID로 특정 데이터셋의 정보를 조회합니다.
    """
    dataset = DatasetService.get_dataset_by_id(db=db, dataset_id=dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset

@router.get("/{public_dataset_id}/download/{file_name}")
def download_dataset_file(
    public_dataset_id: str,
    file_name: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    특정 데이터셋의 파일을 다운로드합니다.
    """
    # 데이터셋 존재 확인
    dataset = DatasetService.get_dataset_by_public_id(db=db, public_dataset_id=public_dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # 파일 경로 구성
    file_path = os.path.join(dataset.file_storage_path, file_name)
    
    # 파일 존재 확인 (현재는 mock)
    if not os.path.exists(file_path):
        # Mock response for development
        return {
            "message": f"Request to download {file_name} for dataset {public_dataset_id} received.", 
            "status": "mocked",
            "file_path": file_path,
            "user_authenticated": current_user is not None
        }
    
    # 실제 파일 서빙 (프로덕션에서 활성화)
    # return FileResponse(
    #     path=file_path, 
    #     filename=file_name, 
    #     media_type='application/octet-stream'
    # )

@router.get("/statistics/summary")
def get_public_statistics(db: Session = Depends(get_db)):
    """
    공개 데이터셋 통계를 반환합니다.
    """
    stats = DatasetService.get_dataset_statistics(db=db)
    # 민감하지 않은 정보만 공개
    return {
        "total_datasets": stats["total_datasets"],
        "by_data_type": stats["by_data_type"],
        "by_organ": stats["by_organ"],
        "by_status": stats["by_status"]
    }
