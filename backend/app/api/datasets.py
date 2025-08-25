
from fastapi import APIRouter, HTTPException
from app.schemas.dataset import DatasetListSchema, DatasetSchema
from datetime import date
from fastapi.responses import FileResponse
import os

router = APIRouter(tags=["Datasets"])

mock_db = [
    DatasetSchema(
        dataset_id=1,
        public_dataset_id="HBM123.ABCD.456",
        uploader_id=1,
        group_name="K-map Consortium",
        data_type="scRNA-seq",
        organ="Lung",
        status="Published",
        publication_date=date(2024, 8, 22),
        description="A sample dataset for lung tissue.",
        citation="K-map et al. (2024)",
        created_at=date(2024, 8, 22),
        updated_at=date(2024, 8, 22),
    ),
    DatasetSchema(
        dataset_id=2,
        public_dataset_id="HBM456.EFGH.789",
        uploader_id=1,
        group_name="K-map Consortium",
        data_type="WGS",
        organ="Blood",
        status="Published",
        publication_date=date(2024, 8, 23),
        description="A sample dataset for blood.",
        citation="K-map et al. (2024)",
        created_at=date(2024, 8, 23),
        updated_at=date(2024, 8, 23),
    )
]

@router.get("", response_model=DatasetListSchema)
def get_datasets():
    """
    임시 데이터셋 목록을 반환합니다.
    """
    return DatasetListSchema(datasets=mock_db)

@router.get("/{dataset_id}", response_model=DatasetSchema)
def get_dataset_by_id(dataset_id: int):
    """
    ID로 특정 데이터셋의 정보를 조회합니다.
    """
    for dataset in mock_db:
        if dataset.dataset_id == dataset_id:
            return dataset
    raise HTTPException(status_code=404, detail="Dataset not found")

@router.get("/{dataset_id}/download/{file_name}")
def download_dataset_file(dataset_id: int, file_name: str):
    """
    특정 데이터셋의 파일을 다운로드합니다. (임시 구현)
    """
    # 임시 파일 생성 및 다운로드 로직 (실제 파일 대신 메시지 반환)
    # file_path = f"temp_{file_name}"
    # with open(file_path, "w") as f:
    #     f.write(f"This is a dummy file for dataset {dataset_id}: {file_name}")
    # return FileResponse(path=file_path, filename=file_name, media_type='application/octet-stream')
    return {"message": f"Request to download {file_name} for dataset {dataset_id} received.", "status": "mocked"}
