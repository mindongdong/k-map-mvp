"""
H5AD Import Service for single-cell datasets.
Imports h5ad files into PostgreSQL database for fast visualization.
"""

import os
import json
import numpy as np
from typing import Dict, Any, Optional
from tqdm import tqdm
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.single_cell import SCDataset, Cell, Gene, MarkerGene, ClusterStats, GeneExpression


class H5ADImportService:
    """Service class for importing h5ad files into the database."""

    @staticmethod
    def dataset_exists(db: Session, dataset_name: str) -> bool:
        """Check if a dataset with the given name already exists."""
        return db.query(SCDataset).filter(SCDataset.name == dataset_name).first() is not None

    @staticmethod
    def delete_dataset(db: Session, dataset_name: str) -> bool:
        """Delete a dataset and all its related data."""
        dataset = db.query(SCDataset).filter(SCDataset.name == dataset_name).first()
        if not dataset:
            return False
        db.delete(dataset)
        db.commit()
        return True

    @staticmethod
    def import_dataset(
        db: Session,
        h5ad_path: str,
        dataset_name: str,
        overwrite: bool = False,
        import_expression: bool = False,
        n_top_genes: int = 100
    ) -> Dict[str, Any]:
        """
        Import a processed h5ad file into PostgreSQL.

        Args:
            db: Database session
            h5ad_path: Path to the processed .h5ad file
            dataset_name: Name to identify this dataset in the database
            overwrite: If True, delete existing dataset before importing
            import_expression: If True, import expression data for highly variable genes
            n_top_genes: Number of top marker genes to import per cluster

        Returns:
            Dictionary with import result
        """
        import scanpy as sc

        if not os.path.exists(h5ad_path):
            return {"success": False, "message": f"File not found: {h5ad_path}"}

        # Check if dataset exists
        if H5ADImportService.dataset_exists(db, dataset_name):
            if overwrite:
                H5ADImportService.delete_dataset(db, dataset_name)
            else:
                return {"success": False, "message": f"Dataset '{dataset_name}' already exists. Use overwrite=True to replace."}

        try:
            # Load h5ad file
            adata = sc.read_h5ad(h5ad_path)

            # Validate required fields
            validation = H5ADImportService._validate_adata(adata)
            if not validation["valid"]:
                return {"success": False, "message": validation["message"]}

            # Import dataset metadata
            dataset = H5ADImportService._import_dataset_metadata(db, adata, dataset_name, h5ad_path)

            # Import genes
            H5ADImportService._import_genes(db, adata, dataset.id, import_expression)

            # Import cells
            H5ADImportService._import_cells(db, adata, dataset.id)

            # Import cluster stats
            H5ADImportService._import_cluster_stats(db, adata, dataset.id)

            # Import marker genes
            if 'rank_genes_groups' in adata.uns:
                H5ADImportService._import_marker_genes(db, adata, dataset.id, n_top_genes)

            # Import gene expression if requested
            if import_expression:
                H5ADImportService._import_gene_expression(db, adata, dataset.id)

            # Update dataset status
            dataset.processing_status = 'completed'
            db.commit()

            # Refresh materialized view
            H5ADImportService.refresh_materialized_view(db)

            return {
                "success": True,
                "message": f"Successfully imported dataset '{dataset_name}'",
                "dataset_name": dataset_name,
                "n_cells": adata.n_obs,
                "n_genes": adata.n_vars
            }

        except Exception as e:
            db.rollback()
            return {"success": False, "message": f"Error importing dataset: {str(e)}"}

    @staticmethod
    def _validate_adata(adata) -> Dict[str, Any]:
        """Validate that AnnData has required fields for visualization."""
        required_obsm = ['X_umap']
        missing = []

        for field in required_obsm:
            if field not in adata.obsm:
                missing.append(f"obsm['{field}']")

        # Check for any cluster column
        has_clusters = any(col in adata.obs.columns for col in ['leiden', 'louvain', 'cluster'])
        if not has_clusters:
            missing.append("obs clustering column (leiden/louvain/cluster)")

        if missing:
            return {"valid": False, "message": f"Missing required fields: {', '.join(missing)}"}

        return {"valid": True, "message": "Validation passed"}

    @staticmethod
    def _import_dataset_metadata(db: Session, adata, dataset_name: str, original_filename: str) -> SCDataset:
        """Import dataset metadata and return dataset object."""
        dataset = SCDataset(
            name=dataset_name,
            original_filename=os.path.basename(original_filename),
            n_cells=adata.n_obs,
            n_genes=adata.n_vars,
            processing_status='importing'
        )
        db.add(dataset)
        db.flush()  # Get the ID without committing
        return dataset

    @staticmethod
    def _import_genes(db: Session, adata, dataset_id: int, import_expression: bool):
        """Import gene information."""
        genes_to_add = []

        for idx, gene_name in enumerate(adata.var_names):
            highly_variable = False
            mean_expr = None
            dispersion = None

            if 'highly_variable' in adata.var.columns:
                highly_variable = bool(adata.var.iloc[idx]['highly_variable'])

            if 'means' in adata.var.columns:
                mean_expr = float(adata.var.iloc[idx]['means'])

            if 'dispersions' in adata.var.columns:
                dispersion = float(adata.var.iloc[idx]['dispersions'])

            # Only import highly variable genes if import_expression is True
            if import_expression and not highly_variable:
                continue

            genes_to_add.append(Gene(
                dataset_id=dataset_id,
                gene_symbol=gene_name,
                gene_id=gene_name,
                highly_variable=highly_variable,
                mean_expression=mean_expr,
                dispersion=dispersion
            ))

        db.bulk_save_objects(genes_to_add)
        db.flush()

    @staticmethod
    def _import_cells(db: Session, adata, dataset_id: int):
        """Import cell metadata and UMAP coordinates in batches."""
        cluster_col = next((col for col in ['leiden', 'louvain', 'cluster'] if col in adata.obs.columns), None)

        cells_to_add = []
        batch_size = 2000
        imported_count = 0

        for idx, cell_barcode in enumerate(tqdm(adata.obs_names, desc="Processing cells")):
            umap_coords = adata.obsm['X_umap'][idx]
            cluster_id = str(adata.obs.iloc[idx][cluster_col]) if cluster_col else None
            cell_type = str(adata.obs.iloc[idx]['cell_type']) if 'cell_type' in adata.obs.columns else None

            metadata = {}
            for col in adata.obs.columns:
                if col not in [cluster_col, 'cell_type']:
                    val = adata.obs.iloc[idx][col]
                    if isinstance(val, (np.integer, np.floating)):
                        val = float(val)
                        if not np.isfinite(val):
                            val = None
                    elif isinstance(val, np.bool_):
                        val = bool(val)
                    else:
                        val = str(val)
                    metadata[col] = val

            cells_to_add.append(Cell(
                dataset_id=dataset_id,
                cell_barcode=cell_barcode,
                umap_1=float(umap_coords[0]),
                umap_2=float(umap_coords[1]),
                cluster_id=cluster_id,
                cell_type=cell_type,
                metadata=metadata if metadata else None
            ))

            if len(cells_to_add) >= batch_size:
                db.bulk_save_objects(cells_to_add)
                db.flush()
                imported_count += len(cells_to_add)

                # Update import progress
                db.execute(
                    text("UPDATE sc_datasets SET imported_cells = :count WHERE id = :id"),
                    {"count": imported_count, "id": dataset_id}
                )
                db.flush()
                cells_to_add = []

        # Save remaining cells
        if cells_to_add:
            db.bulk_save_objects(cells_to_add)
            db.flush()
            imported_count += len(cells_to_add)
            db.execute(
                text("UPDATE sc_datasets SET imported_cells = :count WHERE id = :id"),
                {"count": imported_count, "id": dataset_id}
            )
            db.flush()

    @staticmethod
    def _import_cluster_stats(db: Session, adata, dataset_id: int):
        """Calculate and import cluster statistics."""
        cluster_col = None
        for col in ['leiden', 'louvain', 'cluster']:
            if col in adata.obs.columns:
                cluster_col = col
                break

        if not cluster_col:
            return

        clusters = adata.obs[cluster_col].unique()
        stats_to_add = []

        for cluster_id in clusters:
            mask = adata.obs[cluster_col] == cluster_id
            cell_count = mask.sum()

            umap_coords = adata.obsm['X_umap'][mask]
            mean_umap_1 = float(np.mean(umap_coords[:, 0]))
            mean_umap_2 = float(np.mean(umap_coords[:, 1]))

            # Get cluster color if available
            color = None
            color_key = f'{cluster_col}_colors'
            if color_key in adata.uns:
                cluster_list = list(clusters)
                cluster_idx = cluster_list.index(cluster_id)
                if cluster_idx < len(adata.uns[color_key]):
                    color = adata.uns[color_key][cluster_idx]

            stats_to_add.append(ClusterStats(
                dataset_id=dataset_id,
                cluster_id=str(cluster_id),
                cell_count=int(cell_count),
                mean_umap_1=mean_umap_1,
                mean_umap_2=mean_umap_2,
                cluster_color=color
            ))

        db.bulk_save_objects(stats_to_add)
        db.flush()

    @staticmethod
    def _import_marker_genes(db: Session, adata, dataset_id: int, n_top_genes: int):
        """Import marker genes for each cluster."""
        rank_genes = adata.uns['rank_genes_groups']
        clusters = rank_genes['names'].dtype.names

        markers_to_add = []
        for cluster in clusters:
            for rank in range(min(n_top_genes, len(rank_genes['names'][cluster]))):
                gene_symbol = rank_genes['names'][cluster][rank]

                logfc = float(rank_genes['logfoldchanges'][cluster][rank]) if 'logfoldchanges' in rank_genes else None
                pval = float(rank_genes['pvals'][cluster][rank]) if 'pvals' in rank_genes else None
                pval_adj = float(rank_genes['pvals_adj'][cluster][rank]) if 'pvals_adj' in rank_genes else None

                markers_to_add.append(MarkerGene(
                    dataset_id=dataset_id,
                    cluster_id=str(cluster),
                    gene_symbol=str(gene_symbol),
                    gene_id=str(gene_symbol),
                    log2_fold_change=logfc,
                    pvalue=pval,
                    pvalue_adj=pval_adj,
                    rank=rank + 1
                ))

        db.bulk_save_objects(markers_to_add)
        db.flush()

    @staticmethod
    def _import_gene_expression(db: Session, adata, dataset_id: int):
        """Import gene expression data for highly variable genes."""
        from scipy.sparse import csr_matrix

        # Get highly variable genes
        if 'highly_variable' not in adata.var.columns:
            return

        hvg_mask = adata.var['highly_variable'].values
        hvg_indices = np.where(hvg_mask)[0]

        if len(hvg_indices) == 0:
            return

        # Get gene IDs from database
        genes = db.query(Gene.id, Gene.gene_symbol).filter(
            Gene.dataset_id == dataset_id,
            Gene.highly_variable == True
        ).all()
        gene_map = {g.gene_symbol: g.id for g in genes}

        # Get cell IDs from database
        cells = db.query(Cell.id, Cell.cell_barcode).filter(Cell.dataset_id == dataset_id).all()
        cell_map = {c.cell_barcode: c.id for c in cells}

        # Extract expression matrix
        if adata.raw is not None:
            X = adata.raw.X[:, hvg_indices]
        else:
            X = adata.X[:, hvg_indices]

        # Convert to sparse if not already
        if not hasattr(X, 'tocoo'):
            X = csr_matrix(X)

        X_coo = X.tocoo()

        expressions_to_add = []
        batch_size = 10000

        for i, j, v in tqdm(zip(X_coo.row, X_coo.col, X_coo.data), total=len(X_coo.data), desc="Processing expression"):
            if v > 0:
                cell_barcode = adata.obs_names[i]
                gene_symbol = adata.var_names[hvg_indices[j]]

                if cell_barcode in cell_map and gene_symbol in gene_map:
                    expressions_to_add.append(GeneExpression(
                        dataset_id=dataset_id,
                        cell_id=cell_map[cell_barcode],
                        gene_id=gene_map[gene_symbol],
                        expression_value=float(v)
                    ))

                if len(expressions_to_add) >= batch_size:
                    db.bulk_save_objects(expressions_to_add)
                    db.flush()
                    expressions_to_add = []

        if expressions_to_add:
            db.bulk_save_objects(expressions_to_add)
            db.flush()

    @staticmethod
    def refresh_materialized_view(db: Session) -> bool:
        """Refresh the UMAP materialized view."""
        try:
            db.execute(text("REFRESH MATERIALIZED VIEW umap_view"))
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False
