"""
Single-cell visualization API endpoints.
Provides UMAP coordinates, marker genes, gene expression, and cluster data.
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, List
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.services.visualization_service import VisualizationService
from app.schemas.single_cell import (
    SCDatasetListSchema, SCDatasetSchema, SCDatasetSummary,
    UMAPResponse, CellsInRegionResponse, CellData, ClusterInfo,
    MarkerGenesResponse, MarkerGeneSchema, ClusterGenesResponse,
    GeneExpressionResponse, GeneExpressionCell, ExpressionStatistics,
    GeneSearchResponse, GeneSearchResult
)

router = APIRouter(tags=["Single Cell Visualization"])


@router.get("/datasets", response_model=SCDatasetListSchema)
def list_sc_datasets(db: Session = Depends(get_db)):
    """List all available single-cell datasets."""
    datasets = VisualizationService.list_datasets(db)
    return SCDatasetListSchema(
        datasets=[SCDatasetSchema(**ds) for ds in datasets],
        total_count=len(datasets)
    )


@router.get("/datasets/{dataset_name}", response_model=SCDatasetSummary)
def get_sc_dataset(dataset_name: str, db: Session = Depends(get_db)):
    """Get detailed information about a single-cell dataset."""
    summary = VisualizationService.get_dataset_summary(db, dataset_name)
    if not summary:
        raise HTTPException(status_code=404, detail=f"Dataset '{dataset_name}' not found")

    return SCDatasetSummary(
        dataset_info=SCDatasetSchema(**summary["dataset_info"]),
        n_clusters=len(summary["clusters"]),
        gene_statistics=summary["gene_statistics"]
    )


@router.get("/umap/{dataset_name}", response_model=UMAPResponse)
def get_umap_data(
    dataset_name: str,
    cluster_ids: Optional[str] = Query(None, description="Comma-separated cluster IDs to filter"),
    sample_rate: Optional[float] = Query(None, ge=0.0, le=1.0, description="Sampling rate for large datasets"),
    db: Session = Depends(get_db)
):
    """
    Get UMAP coordinates and metadata for visualization.

    - **dataset_name**: Name of the dataset
    - **cluster_ids**: Optional comma-separated list of cluster IDs to filter
    - **sample_rate**: Optional sampling rate (0.0-1.0) for large datasets
    """
    # Parse cluster_ids
    cluster_list = None
    if cluster_ids:
        cluster_list = [c.strip() for c in cluster_ids.split(",")]

    result = VisualizationService.get_umap_data(
        db=db,
        dataset_name=dataset_name,
        cluster_ids=cluster_list,
        sample_rate=sample_rate
    )

    if not result["cells"] and not result["clusters"]:
        raise HTTPException(status_code=404, detail=f"Dataset '{dataset_name}' not found or has no data")

    return UMAPResponse(
        cells=[CellData(**c) for c in result["cells"]],
        clusters=[ClusterInfo(**c) for c in result["clusters"]],
        total_cells=result["total_cells"],
        query_duration_ms=result.get("query_duration_ms")
    )


@router.get("/umap/{dataset_name}/region", response_model=CellsInRegionResponse)
def get_cells_in_region(
    dataset_name: str,
    umap1_min: float = Query(..., description="Minimum UMAP1 coordinate"),
    umap1_max: float = Query(..., description="Maximum UMAP1 coordinate"),
    umap2_min: float = Query(..., description="Minimum UMAP2 coordinate"),
    umap2_max: float = Query(..., description="Maximum UMAP2 coordinate"),
    db: Session = Depends(get_db)
):
    """
    Get cells within a specific UMAP region (for selection/zooming).

    - **umap1_min/max**: UMAP dimension 1 bounds
    - **umap2_min/max**: UMAP dimension 2 bounds
    """
    cells = VisualizationService.get_cells_in_region(
        db=db,
        dataset_name=dataset_name,
        umap1_min=umap1_min,
        umap1_max=umap1_max,
        umap2_min=umap2_min,
        umap2_max=umap2_max
    )

    return CellsInRegionResponse(
        cells=[CellData(**c) for c in cells],
        count=len(cells)
    )


@router.get("/markers/{dataset_name}", response_model=MarkerGenesResponse)
def get_marker_genes(
    dataset_name: str,
    cluster_id: Optional[str] = Query(None, description="Specific cluster ID"),
    top_n: int = Query(25, ge=1, le=200, description="Number of top genes per cluster"),
    db: Session = Depends(get_db)
):
    """
    Get marker genes for clusters.

    - **cluster_id**: Optional specific cluster ID (returns all clusters if not specified)
    - **top_n**: Number of top genes per cluster (default: 25)
    """
    markers = VisualizationService.get_marker_genes(
        db=db,
        dataset_name=dataset_name,
        cluster_id=cluster_id,
        top_n=top_n
    )

    return MarkerGenesResponse(
        marker_genes=[MarkerGeneSchema(**m) for m in markers],
        count=len(markers)
    )


@router.get("/clusters/{dataset_name}", response_model=List[ClusterInfo])
def get_cluster_composition(
    dataset_name: str,
    db: Session = Depends(get_db)
):
    """Get cluster composition statistics for a dataset."""
    clusters = VisualizationService.get_cluster_composition(db, dataset_name)

    if not clusters:
        raise HTTPException(status_code=404, detail=f"Dataset '{dataset_name}' not found or has no clusters")

    return [ClusterInfo(**c) for c in clusters]


@router.get("/clusters/{dataset_name}/{cluster_id}/genes", response_model=ClusterGenesResponse)
def get_genes_by_cluster(
    dataset_name: str,
    cluster_id: str,
    min_log2fc: float = Query(0.5, description="Minimum log2 fold change"),
    max_pvalue: float = Query(0.05, description="Maximum adjusted p-value"),
    db: Session = Depends(get_db)
):
    """
    Get significant marker genes for a specific cluster with filters.

    - **min_log2fc**: Minimum log2 fold change (default: 0.5)
    - **max_pvalue**: Maximum adjusted p-value (default: 0.05)
    """
    genes = VisualizationService.get_genes_by_cluster(
        db=db,
        dataset_name=dataset_name,
        cluster_id=cluster_id,
        min_log2fc=min_log2fc,
        max_pvalue=max_pvalue
    )

    return ClusterGenesResponse(
        cluster_id=cluster_id,
        genes=[MarkerGeneSchema(cluster_id=cluster_id, **g) for g in genes],
        count=len(genes)
    )


@router.get("/expression/{dataset_name}/{gene_symbol}", response_model=GeneExpressionResponse)
def get_gene_expression(
    dataset_name: str,
    gene_symbol: str,
    db: Session = Depends(get_db)
):
    """
    Get gene expression values overlaid on UMAP coordinates.

    - **gene_symbol**: Gene symbol to visualize
    """
    result = VisualizationService.get_gene_expression_on_umap(
        db=db,
        dataset_name=dataset_name,
        gene_symbol=gene_symbol
    )

    if not result["found"]:
        return GeneExpressionResponse(
            cells=[],
            gene_symbol=gene_symbol,
            statistics=None,
            found=False
        )

    return GeneExpressionResponse(
        cells=[GeneExpressionCell(**c) for c in result["cells"]],
        gene_symbol=result["gene_symbol"],
        statistics=ExpressionStatistics(**result["statistics"]) if result.get("statistics") else None,
        found=result["found"]
    )


@router.get("/genes/{dataset_name}/search", response_model=GeneSearchResponse)
def search_genes(
    dataset_name: str,
    q: str = Query(..., min_length=1, description="Search term"),
    limit: int = Query(50, ge=1, le=200, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Search for genes by symbol (case-insensitive).

    - **q**: Search string
    - **limit**: Maximum number of results (default: 50)
    """
    genes = VisualizationService.search_genes(
        db=db,
        dataset_name=dataset_name,
        search_term=q,
        limit=limit
    )

    return GeneSearchResponse(
        genes=[GeneSearchResult(**g) for g in genes],
        count=len(genes)
    )
