"""
Single-cell visualization service layer.
High-performance queries for UMAP and other visualization data.
"""

from typing import List, Dict, Any, Optional
import time
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.single_cell import SCDataset, MarkerGene, ClusterStats, Gene


class VisualizationService:
    """Service class for single-cell visualization queries."""

    @staticmethod
    def list_datasets(db: Session) -> List[Dict[str, Any]]:
        """List all available single-cell datasets."""
        datasets = db.query(SCDataset).order_by(SCDataset.created_at.desc()).all()
        return [
            {
                "id": ds.id,
                "name": ds.name,
                "original_filename": ds.original_filename,
                "n_cells": ds.n_cells,
                "n_genes": ds.n_genes,
                "processing_status": ds.processing_status,
                "imported_cells": ds.imported_cells,
                "created_at": ds.created_at,
                "updated_at": ds.updated_at
            }
            for ds in datasets
        ]

    @staticmethod
    def get_dataset_info(db: Session, dataset_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a dataset."""
        query = text("""
            SELECT
                d.id,
                d.name,
                d.original_filename,
                d.n_cells,
                d.n_genes,
                d.processing_status,
                d.imported_cells,
                d.created_at,
                COUNT(DISTINCT cs.cluster_id) as n_clusters
            FROM sc_datasets d
            LEFT JOIN cluster_stats cs ON d.id = cs.dataset_id
            WHERE d.name = :dataset_name
            GROUP BY d.id
        """)
        result = db.execute(query, {"dataset_name": dataset_name}).fetchone()
        if not result:
            return None
        return dict(result._mapping)

    @staticmethod
    def get_umap_data(
        db: Session,
        dataset_name: str,
        cluster_ids: Optional[List[str]] = None,
        sample_rate: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Get UMAP coordinates and metadata for visualization.

        Args:
            db: Database session
            dataset_name: Name of the dataset
            cluster_ids: Optional list of cluster IDs to filter
            sample_rate: Optional sampling rate (0.0-1.0) for large datasets

        Returns:
            Dictionary with cell data and cluster information
        """
        start_time = time.time()

        # Build query with optional filters
        base_query = """
            SELECT
                cell_id,
                cell_barcode,
                umap_1,
                umap_2,
                cluster_id,
                cell_type,
                cluster_color
            FROM umap_view
            WHERE dataset_name = :dataset_name
        """

        params: Dict[str, Any] = {"dataset_name": dataset_name}

        if cluster_ids:
            base_query += " AND cluster_id = ANY(:cluster_ids)"
            params["cluster_ids"] = cluster_ids

        if sample_rate and 0 < sample_rate < 1:
            base_query += " AND random() < :sample_rate"
            params["sample_rate"] = sample_rate

        base_query += " ORDER BY cell_id"

        cells = db.execute(text(base_query), params).fetchall()
        cells_data = [dict(row._mapping) for row in cells]

        # Get cluster statistics
        cluster_query = """
            SELECT
                cs.cluster_id,
                cs.cell_count,
                cs.mean_umap_1,
                cs.mean_umap_2,
                cs.cluster_color
            FROM cluster_stats cs
            JOIN sc_datasets d ON cs.dataset_id = d.id
            WHERE d.name = :dataset_name
        """

        cluster_params: Dict[str, Any] = {"dataset_name": dataset_name}

        if cluster_ids:
            cluster_query += " AND cs.cluster_id = ANY(:cluster_ids)"
            cluster_params["cluster_ids"] = cluster_ids

        clusters = db.execute(text(cluster_query), cluster_params).fetchall()
        clusters_data = [dict(row._mapping) for row in clusters]

        duration_ms = int((time.time() - start_time) * 1000)

        return {
            "cells": cells_data,
            "clusters": clusters_data,
            "total_cells": len(cells_data),
            "query_duration_ms": duration_ms
        }

    @staticmethod
    def get_marker_genes(
        db: Session,
        dataset_name: str,
        cluster_id: Optional[str] = None,
        top_n: int = 25
    ) -> List[Dict[str, Any]]:
        """
        Get marker genes for clusters.

        Args:
            db: Database session
            dataset_name: Name of the dataset
            cluster_id: Specific cluster ID (None for all clusters)
            top_n: Number of top genes per cluster

        Returns:
            List of marker gene records
        """
        query = """
            SELECT
                mg.cluster_id,
                mg.gene_symbol,
                mg.log2_fold_change,
                mg.pvalue,
                mg.pvalue_adj,
                mg.rank
            FROM marker_genes mg
            JOIN sc_datasets d ON mg.dataset_id = d.id
            WHERE d.name = :dataset_name
        """

        params: Dict[str, Any] = {"dataset_name": dataset_name, "top_n": top_n}

        if cluster_id:
            query += " AND mg.cluster_id = :cluster_id"
            params["cluster_id"] = cluster_id

        query += " AND mg.rank <= :top_n ORDER BY mg.cluster_id, mg.rank"

        result = db.execute(text(query), params).fetchall()
        return [dict(row._mapping) for row in result]

    @staticmethod
    def get_gene_expression_on_umap(
        db: Session,
        dataset_name: str,
        gene_symbol: str
    ) -> Dict[str, Any]:
        """
        Get gene expression values overlaid on UMAP coordinates.

        Args:
            db: Database session
            dataset_name: Name of the dataset
            gene_symbol: Gene symbol to visualize

        Returns:
            Dictionary with UMAP coordinates and expression values
        """
        query = text("""
            SELECT
                c.id as cell_id,
                c.cell_barcode,
                c.umap_1,
                c.umap_2,
                c.cluster_id,
                COALESCE(ge.expression_value, 0) as expression
            FROM cells c
            JOIN sc_datasets d ON c.dataset_id = d.id
            LEFT JOIN genes g ON g.dataset_id = d.id AND g.gene_symbol = :gene_symbol
            LEFT JOIN gene_expression ge ON ge.cell_id = c.id AND ge.gene_id = g.id
            WHERE d.name = :dataset_name
            ORDER BY c.id
        """)

        cells = db.execute(query, {"gene_symbol": gene_symbol, "dataset_name": dataset_name}).fetchall()

        if not cells:
            return {"cells": [], "gene_symbol": gene_symbol, "found": False}

        cells_data = [dict(row._mapping) for row in cells]

        # Calculate expression statistics
        expressions = [c["expression"] for c in cells_data]
        non_zero = [e for e in expressions if e > 0]

        stats = {
            "min": float(np.min(expressions)),
            "max": float(np.max(expressions)),
            "mean": float(np.mean(expressions)),
            "median": float(np.median(expressions)),
            "pct_expressing": len(non_zero) / len(expressions) * 100 if expressions else 0
        }

        return {
            "cells": cells_data,
            "gene_symbol": gene_symbol,
            "statistics": stats,
            "found": True
        }

    @staticmethod
    def get_cluster_composition(db: Session, dataset_name: str) -> List[Dict[str, Any]]:
        """
        Get cluster composition statistics.

        Args:
            db: Database session
            dataset_name: Name of the dataset

        Returns:
            List of cluster statistics
        """
        query = text("""
            SELECT
                cs.cluster_id,
                cs.cell_count,
                cs.mean_umap_1,
                cs.mean_umap_2,
                cs.cluster_color,
                ROUND(cs.cell_count * 100.0 / d.n_cells, 2) as percentage
            FROM cluster_stats cs
            JOIN sc_datasets d ON cs.dataset_id = d.id
            WHERE d.name = :dataset_name
            ORDER BY cs.cluster_id
        """)

        result = db.execute(query, {"dataset_name": dataset_name}).fetchall()
        return [dict(row._mapping) for row in result]

    @staticmethod
    def get_genes_by_cluster(
        db: Session,
        dataset_name: str,
        cluster_id: str,
        min_log2fc: float = 0.5,
        max_pvalue: float = 0.05
    ) -> List[Dict[str, Any]]:
        """
        Get significant marker genes for a specific cluster with filters.

        Args:
            db: Database session
            dataset_name: Name of the dataset
            cluster_id: Cluster ID
            min_log2fc: Minimum log2 fold change
            max_pvalue: Maximum adjusted p-value

        Returns:
            List of filtered marker genes
        """
        query = text("""
            SELECT
                mg.gene_symbol,
                mg.log2_fold_change,
                mg.pvalue,
                mg.pvalue_adj,
                mg.rank,
                g.mean_expression
            FROM marker_genes mg
            JOIN sc_datasets d ON mg.dataset_id = d.id
            LEFT JOIN genes g ON g.dataset_id = d.id AND g.gene_symbol = mg.gene_symbol
            WHERE d.name = :dataset_name
                AND mg.cluster_id = :cluster_id
                AND mg.log2_fold_change >= :min_log2fc
                AND mg.pvalue_adj <= :max_pvalue
            ORDER BY mg.log2_fold_change DESC
        """)

        result = db.execute(query, {
            "dataset_name": dataset_name,
            "cluster_id": cluster_id,
            "min_log2fc": min_log2fc,
            "max_pvalue": max_pvalue
        }).fetchall()

        return [dict(row._mapping) for row in result]

    @staticmethod
    def search_genes(
        db: Session,
        dataset_name: str,
        search_term: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Search for genes by symbol.

        Args:
            db: Database session
            dataset_name: Name of the dataset
            search_term: Search string (case-insensitive)
            limit: Maximum number of results

        Returns:
            List of matching genes
        """
        query = text("""
            SELECT
                g.gene_symbol,
                g.highly_variable,
                g.mean_expression,
                g.dispersion
            FROM genes g
            JOIN sc_datasets d ON g.dataset_id = d.id
            WHERE d.name = :dataset_name
                AND g.gene_symbol ILIKE :search_pattern
            ORDER BY g.mean_expression DESC NULLS LAST
            LIMIT :limit
        """)

        result = db.execute(query, {
            "dataset_name": dataset_name,
            "search_pattern": f"%{search_term}%",
            "limit": limit
        }).fetchall()

        return [dict(row._mapping) for row in result]

    @staticmethod
    def get_cells_in_region(
        db: Session,
        dataset_name: str,
        umap1_min: float,
        umap1_max: float,
        umap2_min: float,
        umap2_max: float
    ) -> List[Dict[str, Any]]:
        """
        Get cells within a specific UMAP region (for selection/zooming).

        Args:
            db: Database session
            dataset_name: Name of the dataset
            umap1_min, umap1_max: UMAP dimension 1 bounds
            umap2_min, umap2_max: UMAP dimension 2 bounds

        Returns:
            List of cells in the region
        """
        query = text("""
            SELECT
                cell_id,
                cell_barcode,
                umap_1,
                umap_2,
                cluster_id,
                cell_type
            FROM umap_view
            WHERE dataset_name = :dataset_name
                AND umap_1 BETWEEN :umap1_min AND :umap1_max
                AND umap_2 BETWEEN :umap2_min AND :umap2_max
            ORDER BY cell_id
        """)

        result = db.execute(query, {
            "dataset_name": dataset_name,
            "umap1_min": umap1_min,
            "umap1_max": umap1_max,
            "umap2_min": umap2_min,
            "umap2_max": umap2_max
        }).fetchall()

        return [dict(row._mapping) for row in result]

    @staticmethod
    def get_dataset_summary(db: Session, dataset_name: str) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive summary of a dataset.

        Args:
            db: Database session
            dataset_name: Name of the dataset

        Returns:
            Dictionary with dataset summary statistics
        """
        info = VisualizationService.get_dataset_info(db, dataset_name)
        if not info:
            return None

        clusters = VisualizationService.get_cluster_composition(db, dataset_name)

        # Get gene statistics
        gene_query = text("""
            SELECT
                COUNT(*) as total_genes,
                COUNT(*) FILTER (WHERE highly_variable = TRUE) as hvg_count
            FROM genes
            WHERE dataset_id = (SELECT id FROM sc_datasets WHERE name = :dataset_name)
        """)
        gene_stats = db.execute(gene_query, {"dataset_name": dataset_name}).fetchone()

        return {
            "dataset_info": info,
            "clusters": clusters,
            "gene_statistics": dict(gene_stats._mapping) if gene_stats else {}
        }

    @staticmethod
    def refresh_materialized_view(db: Session) -> bool:
        """Refresh the UMAP materialized view."""
        try:
            db.execute(text("SELECT refresh_umap_view()"))
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False
