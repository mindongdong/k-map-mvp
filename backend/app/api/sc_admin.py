"""
Single-cell admin API endpoints.
Provides dataset import, deletion, and maintenance operations.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_admin_user
from app.models.user import User
from app.services.import_service import H5ADImportService
from app.services.visualization_service import VisualizationService
from app.schemas.single_cell import ImportRequest, ImportResponse, RefreshViewResponse

router = APIRouter(tags=["Single Cell Admin"])


@router.post("/import", response_model=ImportResponse)
def import_h5ad_dataset(
    request: ImportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """
    Import an h5ad file into the database.

    Requires admin authentication.

    - **file_path**: Path to the h5ad file on the server
    - **name**: Name to identify this dataset
    - **import_expression**: Whether to import expression data for highly variable genes
    - **n_top_genes**: Number of top marker genes to import per cluster
    """
    result = H5ADImportService.import_dataset(
        db=db,
        h5ad_path=request.file_path,
        dataset_name=request.name,
        overwrite=False,
        import_expression=request.import_expression,
        n_top_genes=request.n_top_genes
    )

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    return ImportResponse(**result)


@router.post("/import/overwrite", response_model=ImportResponse)
def import_h5ad_dataset_overwrite(
    request: ImportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """
    Import an h5ad file, overwriting existing dataset if present.

    Requires admin authentication.
    """
    result = H5ADImportService.import_dataset(
        db=db,
        h5ad_path=request.file_path,
        dataset_name=request.name,
        overwrite=True,
        import_expression=request.import_expression,
        n_top_genes=request.n_top_genes
    )

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    return ImportResponse(**result)


@router.delete("/datasets/{dataset_name}", status_code=204)
def delete_sc_dataset(
    dataset_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """
    Delete a single-cell dataset and all its related data.

    Requires admin authentication.
    """
    success = H5ADImportService.delete_dataset(db, dataset_name)

    if not success:
        raise HTTPException(status_code=404, detail=f"Dataset '{dataset_name}' not found")

    # Refresh materialized view after deletion
    H5ADImportService.refresh_materialized_view(db)

    return None


@router.post("/refresh-view", response_model=RefreshViewResponse)
def refresh_materialized_view(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """
    Refresh the UMAP materialized view.

    Call this after importing multiple datasets or if data seems stale.
    Requires admin authentication.
    """
    success = VisualizationService.refresh_materialized_view(db)

    if not success:
        raise HTTPException(status_code=500, detail="Failed to refresh materialized view")

    return RefreshViewResponse(
        success=True,
        message="Materialized view refreshed successfully"
    )


@router.get("/datasets/{dataset_name}/status")
def get_import_status(
    dataset_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """
    Get the import status of a dataset.

    Useful for monitoring long-running imports.
    Requires admin authentication.
    """
    info = VisualizationService.get_dataset_info(db, dataset_name)

    if not info:
        raise HTTPException(status_code=404, detail=f"Dataset '{dataset_name}' not found")

    return {
        "dataset_name": dataset_name,
        "processing_status": info["processing_status"],
        "imported_cells": info["imported_cells"],
        "total_cells": info["n_cells"],
        "progress_percent": round(info["imported_cells"] / info["n_cells"] * 100, 2) if info["n_cells"] > 0 else 0
    }
