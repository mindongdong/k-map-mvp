"""Add UMAP materialized view

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2025-12-29 10:10:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create materialized view for fast UMAP queries
    op.execute("""
        CREATE MATERIALIZED VIEW IF NOT EXISTS umap_view AS
        SELECT
            c.id as cell_id,
            c.dataset_id,
            d.name as dataset_name,
            c.cell_barcode,
            c.umap_1,
            c.umap_2,
            c.cluster_id,
            c.cell_type,
            c.metadata,
            cs.cluster_color
        FROM cells c
        JOIN sc_datasets d ON c.dataset_id = d.id
        LEFT JOIN cluster_stats cs ON c.dataset_id = cs.dataset_id AND c.cluster_id = cs.cluster_id
    """)

    # Create indexes on materialized view
    op.execute("CREATE INDEX idx_umap_view_dataset ON umap_view(dataset_name)")
    op.execute("CREATE INDEX idx_umap_view_cluster ON umap_view(dataset_name, cluster_id)")
    op.execute("CREATE INDEX idx_umap_view_umap ON umap_view(dataset_name, umap_1, umap_2)")

    # Create unique index for concurrent refresh
    op.execute("CREATE UNIQUE INDEX idx_umap_view_cell_id ON umap_view(cell_id)")

    # Create function to refresh materialized view
    op.execute("""
        CREATE OR REPLACE FUNCTION refresh_umap_view()
        RETURNS void AS $$
        BEGIN
            REFRESH MATERIALIZED VIEW CONCURRENTLY umap_view;
        END;
        $$ LANGUAGE plpgsql
    """)

    # Create trigger function to update updated_at
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql
    """)

    # Create trigger on sc_datasets
    op.execute("""
        CREATE TRIGGER update_sc_datasets_updated_at
            BEFORE UPDATE ON sc_datasets
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column()
    """)


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS update_sc_datasets_updated_at ON sc_datasets")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column()")
    op.execute("DROP FUNCTION IF EXISTS refresh_umap_view()")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS umap_view")
