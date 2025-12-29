from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict, Any


# ============ Dataset Schemas ============

class SCDatasetBase(BaseModel):
    name: str = Field(..., description="Dataset name for queries")
    original_filename: str = Field(..., description="Original h5ad filename")
    n_cells: int = Field(..., ge=0)
    n_genes: int = Field(..., ge=0)


class SCDatasetCreate(SCDatasetBase):
    pass


class SCDatasetSchema(SCDatasetBase):
    id: int
    processing_status: Optional[str] = 'pending'
    imported_cells: Optional[int] = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SCDatasetListSchema(BaseModel):
    datasets: List[SCDatasetSchema]
    total_count: int


class SCDatasetSummary(BaseModel):
    dataset_info: SCDatasetSchema
    n_clusters: int
    gene_statistics: Dict[str, Any]


# ============ Cell Schemas ============

class CellData(BaseModel):
    cell_id: int
    cell_barcode: str
    umap_1: float
    umap_2: float
    cluster_id: Optional[str] = None
    cell_type: Optional[str] = None
    cluster_color: Optional[str] = None


class ClusterInfo(BaseModel):
    cluster_id: str
    cell_count: int
    mean_umap_1: Optional[float] = None
    mean_umap_2: Optional[float] = None
    cluster_color: Optional[str] = None
    percentage: Optional[float] = None


class UMAPResponse(BaseModel):
    cells: List[CellData]
    clusters: List[ClusterInfo]
    total_cells: int
    query_duration_ms: Optional[int] = None


class CellsInRegionResponse(BaseModel):
    cells: List[CellData]
    count: int


# ============ Gene Schemas ============

class GeneSearchResult(BaseModel):
    gene_symbol: str
    highly_variable: Optional[bool] = False
    mean_expression: Optional[float] = None
    dispersion: Optional[float] = None


class GeneSearchResponse(BaseModel):
    genes: List[GeneSearchResult]
    count: int


# ============ Marker Gene Schemas ============

class MarkerGeneSchema(BaseModel):
    cluster_id: str
    gene_symbol: str
    log2_fold_change: Optional[float] = None
    pvalue: Optional[float] = None
    pvalue_adj: Optional[float] = None
    rank: int

    class Config:
        from_attributes = True


class MarkerGenesResponse(BaseModel):
    marker_genes: List[MarkerGeneSchema]
    count: int


class ClusterGenesResponse(BaseModel):
    cluster_id: str
    genes: List[MarkerGeneSchema]
    count: int


# ============ Expression Schemas ============

class GeneExpressionCell(BaseModel):
    cell_id: int
    cell_barcode: str
    umap_1: float
    umap_2: float
    cluster_id: Optional[str] = None
    expression: float


class ExpressionStatistics(BaseModel):
    min: float
    max: float
    mean: float
    median: float
    pct_expressing: float


class GeneExpressionResponse(BaseModel):
    cells: List[GeneExpressionCell]
    gene_symbol: str
    statistics: Optional[ExpressionStatistics] = None
    found: bool


# ============ Import Schemas ============

class ImportRequest(BaseModel):
    file_path: str = Field(..., description="Path to h5ad file")
    name: str = Field(..., description="Dataset name")
    import_expression: bool = Field(default=False, description="Whether to import expression data")
    n_top_genes: int = Field(default=100, ge=1, le=5000, description="Number of top genes to import")


class ImportResponse(BaseModel):
    success: bool
    message: str
    dataset_name: Optional[str] = None
    n_cells: Optional[int] = None
    n_genes: Optional[int] = None


class RefreshViewResponse(BaseModel):
    success: bool
    message: str
