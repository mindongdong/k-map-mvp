from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.schemas.dataset import DatasetCreate, DatasetUpdate, DatasetSchema
from app.core.dependencies import get_db, get_admin_user
from app.core.security import verify_password, create_access_token
from app.services.dataset_service import DatasetService
from app.models.user import User

router = APIRouter()

from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def admin_login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """관리자 로그인"""
    # 데이터베이스에서 사용자 검증
    user = db.query(User).filter(User.username == login_data.username).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401, 
            detail="Incorrect username or password"
        )
    
    if user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    
    # JWT 토큰 생성
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.user_id,
        "username": user.username,
        "role": user.role
    }

@router.post("/datasets", response_model=DatasetSchema, status_code=201)
async def create_dataset(
    dataset: DatasetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """데이터셋 생성 (업로드)"""
    return DatasetService.create_dataset(db=db, dataset=dataset, uploader_id=current_user.user_id)

@router.put("/datasets/{public_dataset_id}", response_model=DatasetSchema)
async def update_dataset(
    public_dataset_id: str,
    dataset_update: DatasetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """데이터셋 수정"""
    updated_dataset = DatasetService.update_dataset(db=db, public_dataset_id=public_dataset_id, dataset_update=dataset_update)
    if not updated_dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return updated_dataset

@router.delete("/datasets/{public_dataset_id}", status_code=204)
async def delete_dataset(
    public_dataset_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """데이터셋 삭제"""
    success = DatasetService.delete_dataset(db=db, public_dataset_id=public_dataset_id)
    if not success:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return

@router.get("/datasets/statistics")
async def get_dataset_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """데이터셋 통계 조회 (관리자 전용)"""
    return DatasetService.get_dataset_statistics(db=db)
