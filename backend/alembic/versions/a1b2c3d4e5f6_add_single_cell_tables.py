"""Add single cell visualization tables

Revision ID: a1b2c3d4e5f6
Revises: 7f07c02e05a9
Create Date: 2025-12-29 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '7f07c02e05a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # sc_datasets table
    op.create_table('sc_datasets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('original_filename', sa.String(length=255), nullable=False),
        sa.Column('n_cells', sa.Integer(), nullable=False),
        sa.Column('n_genes', sa.Integer(), nullable=False),
        sa.Column('processing_status', sa.String(length=50), server_default='pending', nullable=True),
        sa.Column('imported_cells', sa.Integer(), server_default='0', nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index('idx_sc_datasets_name', 'sc_datasets', ['name'])
    op.create_index('idx_sc_datasets_status', 'sc_datasets', ['processing_status'])

    # cells table
    op.create_table('cells',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('dataset_id', sa.Integer(), nullable=False),
        sa.Column('cell_barcode', sa.String(length=255), nullable=False),
        sa.Column('umap_1', sa.Float(), nullable=False),
        sa.Column('umap_2', sa.Float(), nullable=False),
        sa.Column('cluster_id', sa.String(length=50), nullable=True),
        sa.Column('cell_type', sa.String(length=100), nullable=True),
        sa.Column('metadata', JSONB(), nullable=True),
        sa.ForeignKeyConstraint(['dataset_id'], ['sc_datasets.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('dataset_id', 'cell_barcode', name='uq_cells_dataset_barcode')
    )
    op.create_index('idx_cells_dataset', 'cells', ['dataset_id'])
    op.create_index('idx_cells_cluster', 'cells', ['dataset_id', 'cluster_id'])
    op.create_index('idx_cells_umap', 'cells', ['dataset_id', 'umap_1', 'umap_2'])

    # genes table
    op.create_table('genes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dataset_id', sa.Integer(), nullable=False),
        sa.Column('gene_symbol', sa.String(length=100), nullable=False),
        sa.Column('gene_id', sa.String(length=100), nullable=True),
        sa.Column('highly_variable', sa.Boolean(), server_default='false', nullable=True),
        sa.Column('mean_expression', sa.Float(), nullable=True),
        sa.Column('dispersion', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['dataset_id'], ['sc_datasets.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('dataset_id', 'gene_symbol', name='uq_genes_dataset_symbol')
    )
    op.create_index('idx_genes_dataset', 'genes', ['dataset_id'])
    op.create_index('idx_genes_symbol', 'genes', ['gene_symbol'])
    op.create_index('idx_genes_variable', 'genes', ['dataset_id', 'highly_variable'])

    # marker_genes table
    op.create_table('marker_genes',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('dataset_id', sa.Integer(), nullable=False),
        sa.Column('cluster_id', sa.String(length=50), nullable=False),
        sa.Column('gene_symbol', sa.String(length=100), nullable=False),
        sa.Column('gene_id', sa.String(length=100), nullable=True),
        sa.Column('log2_fold_change', sa.Float(), nullable=True),
        sa.Column('pvalue', sa.Float(), nullable=True),
        sa.Column('pvalue_adj', sa.Float(), nullable=True),
        sa.Column('rank', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['dataset_id'], ['sc_datasets.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('dataset_id', 'cluster_id', 'gene_symbol', name='uq_marker_genes_dataset_cluster_symbol')
    )
    op.create_index('idx_marker_genes_dataset_cluster', 'marker_genes', ['dataset_id', 'cluster_id'])
    op.create_index('idx_marker_genes_rank', 'marker_genes', ['dataset_id', 'cluster_id', 'rank'])
    op.create_index('idx_marker_genes_symbol', 'marker_genes', ['gene_symbol'])

    # cluster_stats table
    op.create_table('cluster_stats',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dataset_id', sa.Integer(), nullable=False),
        sa.Column('cluster_id', sa.String(length=50), nullable=False),
        sa.Column('cell_count', sa.Integer(), nullable=False),
        sa.Column('mean_umap_1', sa.Float(), nullable=True),
        sa.Column('mean_umap_2', sa.Float(), nullable=True),
        sa.Column('cluster_color', sa.String(length=7), nullable=True),
        sa.ForeignKeyConstraint(['dataset_id'], ['sc_datasets.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('dataset_id', 'cluster_id', name='uq_cluster_stats_dataset_cluster')
    )
    op.create_index('idx_cluster_stats_dataset', 'cluster_stats', ['dataset_id'])

    # gene_expression table (sparse storage)
    op.create_table('gene_expression',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('dataset_id', sa.Integer(), nullable=False),
        sa.Column('cell_id', sa.BigInteger(), nullable=False),
        sa.Column('gene_id', sa.Integer(), nullable=False),
        sa.Column('expression_value', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['dataset_id'], ['sc_datasets.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['cell_id'], ['cells.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['gene_id'], ['genes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('cell_id', 'gene_id', name='uq_gene_expression_cell_gene')
    )
    op.create_index('idx_expression_dataset', 'gene_expression', ['dataset_id'])
    op.create_index('idx_expression_cell', 'gene_expression', ['cell_id'])
    op.create_index('idx_expression_gene', 'gene_expression', ['gene_id'])
    op.create_index('idx_expression_dataset_gene', 'gene_expression', ['dataset_id', 'gene_id'])


def downgrade() -> None:
    op.drop_table('gene_expression')
    op.drop_table('cluster_stats')
    op.drop_table('marker_genes')
    op.drop_table('genes')
    op.drop_table('cells')
    op.drop_table('sc_datasets')
