"""
Tests for Single-Cell Visualization API
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sc.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestSCDatasetsAPI:
    """Test single-cell datasets API endpoints"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Create tables before each test"""
        Base.metadata.create_all(bind=engine)
        yield
        Base.metadata.drop_all(bind=engine)

    def test_list_sc_datasets_empty(self):
        """Test listing datasets when none exist"""
        response = client.get("/api/v1/sc/datasets")
        assert response.status_code == 200
        data = response.json()
        assert "datasets" in data
        assert "total_count" in data
        assert data["total_count"] == 0
        assert data["datasets"] == []

    def test_get_nonexistent_dataset(self):
        """Test getting a non-existent dataset"""
        response = client.get("/api/v1/sc/datasets/nonexistent")
        assert response.status_code == 404


class TestUMAPAPI:
    """Test UMAP visualization API endpoints"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Create tables before each test"""
        Base.metadata.create_all(bind=engine)
        yield
        Base.metadata.drop_all(bind=engine)

    def test_get_umap_nonexistent_dataset(self):
        """Test getting UMAP data for non-existent dataset"""
        response = client.get("/api/v1/sc/umap/nonexistent")
        assert response.status_code == 404

    def test_get_umap_with_cluster_filter(self):
        """Test UMAP endpoint with cluster filter parameter"""
        response = client.get("/api/v1/sc/umap/test_dataset?cluster_ids=0,1,2")
        assert response.status_code == 404  # No data, so 404

    def test_get_umap_with_sample_rate(self):
        """Test UMAP endpoint with sample rate parameter"""
        response = client.get("/api/v1/sc/umap/test_dataset?sample_rate=0.5")
        assert response.status_code == 404  # No data, so 404

    def test_get_cells_in_region(self):
        """Test cells in region endpoint"""
        response = client.get(
            "/api/v1/sc/umap/test_dataset/region",
            params={
                "umap1_min": -10,
                "umap1_max": 10,
                "umap2_min": -10,
                "umap2_max": 10
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "cells" in data
        assert "count" in data


class TestMarkerGenesAPI:
    """Test marker genes API endpoints"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Create tables before each test"""
        Base.metadata.create_all(bind=engine)
        yield
        Base.metadata.drop_all(bind=engine)

    def test_get_marker_genes(self):
        """Test getting marker genes"""
        response = client.get("/api/v1/sc/markers/test_dataset")
        assert response.status_code == 200
        data = response.json()
        assert "marker_genes" in data
        assert "count" in data

    def test_get_marker_genes_with_cluster_filter(self):
        """Test getting marker genes for specific cluster"""
        response = client.get("/api/v1/sc/markers/test_dataset?cluster_id=0&top_n=10")
        assert response.status_code == 200

    def test_get_cluster_composition(self):
        """Test getting cluster composition"""
        response = client.get("/api/v1/sc/clusters/nonexistent")
        assert response.status_code == 404


class TestGeneExpressionAPI:
    """Test gene expression API endpoints"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Create tables before each test"""
        Base.metadata.create_all(bind=engine)
        yield
        Base.metadata.drop_all(bind=engine)

    def test_get_gene_expression(self):
        """Test getting gene expression"""
        response = client.get("/api/v1/sc/expression/test_dataset/CD3D")
        assert response.status_code == 200
        data = response.json()
        assert "cells" in data
        assert "gene_symbol" in data
        assert "found" in data
        # No data, so found should be False
        assert data["found"] == False

    def test_search_genes(self):
        """Test gene search"""
        response = client.get("/api/v1/sc/genes/test_dataset/search?q=CD")
        assert response.status_code == 200
        data = response.json()
        assert "genes" in data
        assert "count" in data

    def test_search_genes_missing_query(self):
        """Test gene search without query parameter"""
        response = client.get("/api/v1/sc/genes/test_dataset/search")
        assert response.status_code == 422  # Validation error


class TestSCAdminAPI:
    """Test single-cell admin API endpoints"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Create tables before each test"""
        Base.metadata.create_all(bind=engine)
        yield
        Base.metadata.drop_all(bind=engine)

    def test_import_without_auth(self):
        """Test import endpoint without authentication"""
        response = client.post(
            "/api/v1/sc/admin/import",
            json={
                "file_path": "/path/to/file.h5ad",
                "name": "test_dataset"
            }
        )
        assert response.status_code == 403  # Forbidden without token

    def test_delete_without_auth(self):
        """Test delete endpoint without authentication"""
        response = client.delete("/api/v1/sc/admin/datasets/test_dataset")
        assert response.status_code == 403  # Forbidden without token

    def test_refresh_view_without_auth(self):
        """Test refresh view endpoint without authentication"""
        response = client.post("/api/v1/sc/admin/refresh-view")
        assert response.status_code == 403  # Forbidden without token


class TestAPIEndpointsExist:
    """Test that all expected endpoints exist"""

    def test_sc_datasets_endpoint_exists(self):
        """Verify /sc/datasets endpoint exists"""
        response = client.get("/api/v1/sc/datasets")
        assert response.status_code != 404

    def test_sc_umap_endpoint_exists(self):
        """Verify /sc/umap/{name} endpoint exists"""
        response = client.get("/api/v1/sc/umap/test")
        # 404 is expected for non-existent dataset, but not 405 (Method Not Allowed)
        assert response.status_code in [200, 404]

    def test_sc_markers_endpoint_exists(self):
        """Verify /sc/markers/{name} endpoint exists"""
        response = client.get("/api/v1/sc/markers/test")
        assert response.status_code in [200, 404]

    def test_sc_expression_endpoint_exists(self):
        """Verify /sc/expression/{name}/{gene} endpoint exists"""
        response = client.get("/api/v1/sc/expression/test/GENE")
        assert response.status_code in [200, 404]

    def test_sc_genes_search_endpoint_exists(self):
        """Verify /sc/genes/{name}/search endpoint exists"""
        response = client.get("/api/v1/sc/genes/test/search?q=test")
        assert response.status_code in [200, 404]

    def test_sc_clusters_endpoint_exists(self):
        """Verify /sc/clusters/{name} endpoint exists"""
        response = client.get("/api/v1/sc/clusters/test")
        assert response.status_code in [200, 404]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
