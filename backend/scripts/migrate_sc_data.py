#!/usr/bin/env python3
"""
Data migration script for single-cell visualization data.
Migrates data from optimization_v2 PostgreSQL to k-map-mvp PostgreSQL.

Usage:
    python scripts/migrate_sc_data.py

Environment variables (source DB - optimization_v2):
    SOURCE_DB_HOST: Source database host (default: localhost)
    SOURCE_DB_PORT: Source database port (default: 5432)
    SOURCE_DB_NAME: Source database name (default: kmap_visualization)
    SOURCE_DB_USER: Source database user (default: kmap)
    SOURCE_DB_PASSWORD: Source database password (from optimization_v2/.env)
"""

import os
import sys
from typing import List, Dict, Any

import psycopg2
from psycopg2.extras import RealDictCursor, execute_batch
from tqdm import tqdm

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import settings


class DataMigrator:
    """Migrates single-cell data between PostgreSQL databases."""

    def __init__(self):
        # Source DB (optimization_v2)
        self.source_config = {
            'host': os.getenv('SOURCE_DB_HOST', 'localhost'),
            'port': int(os.getenv('SOURCE_DB_PORT', '5432')),
            'database': os.getenv('SOURCE_DB_NAME', 'kmap_visualization'),
            'user': os.getenv('SOURCE_DB_USER', 'kmap'),
            'password': os.getenv('SOURCE_DB_PASSWORD', ''),
        }

        # Target DB (k-map-mvp) - from settings
        self.target_config = {
            'host': settings.POSTGRES_SERVER,
            'port': settings.POSTGRES_PORT,
            'database': settings.POSTGRES_DB,
            'user': settings.POSTGRES_USER,
            'password': settings.POSTGRES_PASSWORD,
        }

        self.source_conn = None
        self.target_conn = None

    def connect(self):
        """Establish connections to both databases."""
        print("Connecting to source database (optimization_v2)...")
        self.source_conn = psycopg2.connect(**self.source_config)
        print(f"  Connected to {self.source_config['database']}")

        print("Connecting to target database (k-map-mvp)...")
        self.target_conn = psycopg2.connect(**self.target_config)
        print(f"  Connected to {self.target_config['database']}")

    def disconnect(self):
        """Close database connections."""
        if self.source_conn:
            self.source_conn.close()
        if self.target_conn:
            self.target_conn.close()
        print("Connections closed.")

    def migrate_datasets(self) -> Dict[int, int]:
        """
        Migrate datasets table.
        Returns mapping of old_id -> new_id.
        """
        print("\nMigrating datasets...")

        # Source table: datasets -> Target table: sc_datasets
        with self.source_conn.cursor(cursor_factory=RealDictCursor) as src_cur:
            src_cur.execute("""
                SELECT id, name, original_filename, n_cells, n_genes,
                       processing_status, imported_cells, created_at, updated_at
                FROM datasets
                ORDER BY id
            """)
            datasets = src_cur.fetchall()

        if not datasets:
            print("  No datasets found in source database.")
            return {}

        id_mapping = {}
        with self.target_conn.cursor() as tgt_cur:
            for ds in tqdm(datasets, desc="  Datasets"):
                tgt_cur.execute("""
                    INSERT INTO sc_datasets (name, original_filename, n_cells, n_genes,
                                            processing_status, imported_cells, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (name) DO UPDATE SET
                        n_cells = EXCLUDED.n_cells,
                        n_genes = EXCLUDED.n_genes,
                        processing_status = EXCLUDED.processing_status,
                        updated_at = EXCLUDED.updated_at
                    RETURNING id
                """, (
                    ds['name'], ds['original_filename'], ds['n_cells'], ds['n_genes'],
                    ds['processing_status'], ds['imported_cells'], ds['created_at'], ds['updated_at']
                ))
                new_id = tgt_cur.fetchone()[0]
                id_mapping[ds['id']] = new_id

        self.target_conn.commit()
        print(f"  Migrated {len(datasets)} datasets.")
        return id_mapping

    def migrate_cells(self, dataset_id_mapping: Dict[int, int]) -> Dict[int, int]:
        """
        Migrate cells table.
        Returns mapping of old_cell_id -> new_cell_id.
        """
        print("\nMigrating cells...")

        cell_id_mapping = {}

        for old_ds_id, new_ds_id in dataset_id_mapping.items():
            with self.source_conn.cursor(cursor_factory=RealDictCursor) as src_cur:
                src_cur.execute("""
                    SELECT id, cell_barcode, umap_1, umap_2, cluster_id, cell_type, metadata
                    FROM cells WHERE dataset_id = %s ORDER BY id
                """, (old_ds_id,))
                cells = src_cur.fetchall()

            if not cells:
                continue

            with self.target_conn.cursor() as tgt_cur:
                for cell in tqdm(cells, desc=f"  Cells (dataset {new_ds_id})", leave=False):
                    tgt_cur.execute("""
                        INSERT INTO cells (dataset_id, cell_barcode, umap_1, umap_2,
                                          cluster_id, cell_type, metadata)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (dataset_id, cell_barcode) DO UPDATE SET
                            umap_1 = EXCLUDED.umap_1,
                            umap_2 = EXCLUDED.umap_2
                        RETURNING id
                    """, (
                        new_ds_id, cell['cell_barcode'], cell['umap_1'], cell['umap_2'],
                        cell['cluster_id'], cell['cell_type'],
                        psycopg2.extras.Json(cell['metadata']) if cell['metadata'] else None
                    ))
                    new_cell_id = tgt_cur.fetchone()[0]
                    cell_id_mapping[cell['id']] = new_cell_id

            self.target_conn.commit()
            print(f"  Dataset {new_ds_id}: {len(cells)} cells migrated.")

        return cell_id_mapping

    def migrate_genes(self, dataset_id_mapping: Dict[int, int]) -> Dict[int, int]:
        """
        Migrate genes table.
        Returns mapping of old_gene_id -> new_gene_id.
        """
        print("\nMigrating genes...")

        gene_id_mapping = {}

        for old_ds_id, new_ds_id in dataset_id_mapping.items():
            with self.source_conn.cursor(cursor_factory=RealDictCursor) as src_cur:
                src_cur.execute("""
                    SELECT id, gene_symbol, gene_id, highly_variable, mean_expression, dispersion
                    FROM genes WHERE dataset_id = %s ORDER BY id
                """, (old_ds_id,))
                genes = src_cur.fetchall()

            if not genes:
                continue

            with self.target_conn.cursor() as tgt_cur:
                for gene in tqdm(genes, desc=f"  Genes (dataset {new_ds_id})", leave=False):
                    tgt_cur.execute("""
                        INSERT INTO genes (dataset_id, gene_symbol, gene_id,
                                          highly_variable, mean_expression, dispersion)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (dataset_id, gene_symbol) DO UPDATE SET
                            highly_variable = EXCLUDED.highly_variable
                        RETURNING id
                    """, (
                        new_ds_id, gene['gene_symbol'], gene['gene_id'],
                        gene['highly_variable'], gene['mean_expression'], gene['dispersion']
                    ))
                    new_gene_id = tgt_cur.fetchone()[0]
                    gene_id_mapping[gene['id']] = new_gene_id

            self.target_conn.commit()
            print(f"  Dataset {new_ds_id}: {len(genes)} genes migrated.")

        return gene_id_mapping

    def migrate_marker_genes(self, dataset_id_mapping: Dict[int, int]):
        """Migrate marker_genes table."""
        print("\nMigrating marker genes...")

        for old_ds_id, new_ds_id in dataset_id_mapping.items():
            with self.source_conn.cursor(cursor_factory=RealDictCursor) as src_cur:
                src_cur.execute("""
                    SELECT cluster_id, gene_symbol, gene_id, log2_fold_change,
                           pvalue, pvalue_adj, rank
                    FROM marker_genes WHERE dataset_id = %s
                """, (old_ds_id,))
                markers = src_cur.fetchall()

            if not markers:
                continue

            data = [
                (new_ds_id, m['cluster_id'], m['gene_symbol'], m['gene_id'],
                 m['log2_fold_change'], m['pvalue'], m['pvalue_adj'], m['rank'])
                for m in markers
            ]

            with self.target_conn.cursor() as tgt_cur:
                execute_batch(tgt_cur, """
                    INSERT INTO marker_genes (dataset_id, cluster_id, gene_symbol, gene_id,
                                             log2_fold_change, pvalue, pvalue_adj, rank)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (dataset_id, cluster_id, gene_symbol) DO NOTHING
                """, data, page_size=1000)

            self.target_conn.commit()
            print(f"  Dataset {new_ds_id}: {len(markers)} marker genes migrated.")

    def migrate_cluster_stats(self, dataset_id_mapping: Dict[int, int]):
        """Migrate cluster_stats table."""
        print("\nMigrating cluster stats...")

        for old_ds_id, new_ds_id in dataset_id_mapping.items():
            with self.source_conn.cursor(cursor_factory=RealDictCursor) as src_cur:
                src_cur.execute("""
                    SELECT cluster_id, cell_count, mean_umap_1, mean_umap_2, cluster_color
                    FROM cluster_stats WHERE dataset_id = %s
                """, (old_ds_id,))
                stats = src_cur.fetchall()

            if not stats:
                continue

            with self.target_conn.cursor() as tgt_cur:
                for stat in stats:
                    tgt_cur.execute("""
                        INSERT INTO cluster_stats (dataset_id, cluster_id, cell_count,
                                                  mean_umap_1, mean_umap_2, cluster_color)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (dataset_id, cluster_id) DO UPDATE SET
                            cell_count = EXCLUDED.cell_count,
                            cluster_color = EXCLUDED.cluster_color
                    """, (
                        new_ds_id, stat['cluster_id'], stat['cell_count'],
                        stat['mean_umap_1'], stat['mean_umap_2'], stat['cluster_color']
                    ))

            self.target_conn.commit()
            print(f"  Dataset {new_ds_id}: {len(stats)} cluster stats migrated.")

    def migrate_gene_expression(self, dataset_id_mapping: Dict[int, int],
                                cell_id_mapping: Dict[int, int],
                                gene_id_mapping: Dict[int, int]):
        """Migrate gene_expression table (sparse, may be large)."""
        print("\nMigrating gene expression data...")

        for old_ds_id, new_ds_id in dataset_id_mapping.items():
            with self.source_conn.cursor(cursor_factory=RealDictCursor) as src_cur:
                src_cur.execute("""
                    SELECT cell_id, gene_id, expression_value
                    FROM gene_expression WHERE dataset_id = %s
                """, (old_ds_id,))
                expressions = src_cur.fetchall()

            if not expressions:
                print(f"  Dataset {new_ds_id}: No expression data.")
                continue

            data = []
            for expr in expressions:
                new_cell_id = cell_id_mapping.get(expr['cell_id'])
                new_gene_id = gene_id_mapping.get(expr['gene_id'])
                if new_cell_id and new_gene_id:
                    data.append((new_ds_id, new_cell_id, new_gene_id, expr['expression_value']))

            if data:
                with self.target_conn.cursor() as tgt_cur:
                    execute_batch(tgt_cur, """
                        INSERT INTO gene_expression (dataset_id, cell_id, gene_id, expression_value)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (cell_id, gene_id) DO NOTHING
                    """, data, page_size=5000)

                self.target_conn.commit()
                print(f"  Dataset {new_ds_id}: {len(data)} expression values migrated.")

    def refresh_materialized_view(self):
        """Refresh the UMAP materialized view."""
        print("\nRefreshing materialized view...")
        with self.target_conn.cursor() as tgt_cur:
            tgt_cur.execute("REFRESH MATERIALIZED VIEW umap_view")
        self.target_conn.commit()
        print("  Materialized view refreshed.")

    def run(self):
        """Run the full migration."""
        try:
            self.connect()

            # Migrate in order (respecting foreign key dependencies)
            dataset_mapping = self.migrate_datasets()

            if not dataset_mapping:
                print("\nNo data to migrate.")
                return

            cell_mapping = self.migrate_cells(dataset_mapping)
            gene_mapping = self.migrate_genes(dataset_mapping)
            self.migrate_marker_genes(dataset_mapping)
            self.migrate_cluster_stats(dataset_mapping)
            self.migrate_gene_expression(dataset_mapping, cell_mapping, gene_mapping)

            self.refresh_materialized_view()

            print("\nMigration completed successfully!")

        except Exception as e:
            print(f"\nError during migration: {e}")
            if self.target_conn:
                self.target_conn.rollback()
            raise
        finally:
            self.disconnect()


def main():
    """Main entry point."""
    print("=" * 60)
    print("Single-Cell Data Migration Tool")
    print("Source: optimization_v2 PostgreSQL")
    print("Target: k-map-mvp PostgreSQL")
    print("=" * 60)

    # Check for required environment variable
    if not os.getenv('SOURCE_DB_PASSWORD'):
        print("\nWarning: SOURCE_DB_PASSWORD not set.")
        print("Set it with: export SOURCE_DB_PASSWORD=your_password")

    migrator = DataMigrator()
    migrator.run()


if __name__ == "__main__":
    main()
