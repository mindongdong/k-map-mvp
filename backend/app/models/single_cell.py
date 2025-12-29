from sqlalchemy import (
    Column, Integer, BigInteger, String, Float, Boolean, TIMESTAMP, ForeignKey, Text
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class SCDataset(Base):
    """Single-cell dataset metadata."""
    __tablename__ = "sc_datasets"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    original_filename = Column(String(255), nullable=False)
    n_cells = Column(Integer, nullable=False)
    n_genes = Column(Integer, nullable=False)
    processing_status = Column(String(50), server_default='pending')
    imported_cells = Column(Integer, server_default='0')
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    cells = relationship("Cell", back_populates="dataset", cascade="all, delete-orphan")
    genes = relationship("Gene", back_populates="dataset", cascade="all, delete-orphan")
    marker_genes = relationship("MarkerGene", back_populates="dataset", cascade="all, delete-orphan")
    cluster_stats = relationship("ClusterStats", back_populates="dataset", cascade="all, delete-orphan")

    def __repr__(self):
        return f"SCDataset(id={self.id}, name={self.name}, n_cells={self.n_cells})"


class Cell(Base):
    """Cell metadata with UMAP coordinates."""
    __tablename__ = "cells"

    id = Column(BigInteger, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("sc_datasets.id", ondelete="CASCADE"), nullable=False)
    cell_barcode = Column(String(255), nullable=False)
    umap_1 = Column(Float, nullable=False)
    umap_2 = Column(Float, nullable=False)
    cluster_id = Column(String(50))
    cell_type = Column(String(100))
    cell_metadata = Column("metadata", JSONB)

    # Relationships
    dataset = relationship("SCDataset", back_populates="cells")
    expressions = relationship("GeneExpression", back_populates="cell", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Cell(id={self.id}, barcode={self.cell_barcode}, cluster={self.cluster_id})"


class Gene(Base):
    """Gene information."""
    __tablename__ = "genes"

    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("sc_datasets.id", ondelete="CASCADE"), nullable=False)
    gene_symbol = Column(String(100), nullable=False, index=True)
    gene_id = Column(String(100))
    highly_variable = Column(Boolean, server_default='false')
    mean_expression = Column(Float)
    dispersion = Column(Float)

    # Relationships
    dataset = relationship("SCDataset", back_populates="genes")
    expressions = relationship("GeneExpression", back_populates="gene", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Gene(id={self.id}, symbol={self.gene_symbol})"


class MarkerGene(Base):
    """Cluster-specific marker genes."""
    __tablename__ = "marker_genes"

    id = Column(BigInteger, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("sc_datasets.id", ondelete="CASCADE"), nullable=False)
    cluster_id = Column(String(50), nullable=False)
    gene_symbol = Column(String(100), nullable=False)
    gene_id = Column(String(100))
    log2_fold_change = Column(Float)
    pvalue = Column(Float)
    pvalue_adj = Column(Float)
    rank = Column(Integer)

    # Relationships
    dataset = relationship("SCDataset", back_populates="marker_genes")

    def __repr__(self):
        return f"MarkerGene(cluster={self.cluster_id}, gene={self.gene_symbol}, rank={self.rank})"


class ClusterStats(Base):
    """Cluster statistics for quick summary views."""
    __tablename__ = "cluster_stats"

    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("sc_datasets.id", ondelete="CASCADE"), nullable=False)
    cluster_id = Column(String(50), nullable=False)
    cell_count = Column(Integer, nullable=False)
    mean_umap_1 = Column(Float)
    mean_umap_2 = Column(Float)
    cluster_color = Column(String(7))  # Hex color code

    # Relationships
    dataset = relationship("SCDataset", back_populates="cluster_stats")

    def __repr__(self):
        return f"ClusterStats(cluster={self.cluster_id}, count={self.cell_count})"


class GeneExpression(Base):
    """Sparse storage for gene expression values."""
    __tablename__ = "gene_expression"

    id = Column(BigInteger, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("sc_datasets.id", ondelete="CASCADE"), nullable=False)
    cell_id = Column(BigInteger, ForeignKey("cells.id", ondelete="CASCADE"), nullable=False)
    gene_id = Column(Integer, ForeignKey("genes.id", ondelete="CASCADE"), nullable=False)
    expression_value = Column(Float, nullable=False)

    # Relationships
    cell = relationship("Cell", back_populates="expressions")
    gene = relationship("Gene", back_populates="expressions")

    def __repr__(self):
        return f"GeneExpression(cell={self.cell_id}, gene={self.gene_id}, value={self.expression_value})"
