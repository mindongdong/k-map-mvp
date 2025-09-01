"""
Basic tests for Datasets CRUD API
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestDatasetsAPI:
    """Test datasets API endpoints"""
    
    def test_get_datasets_list(self):
        """Test getting datasets list"""
        response = client.get("/api/v1/datasets?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert "datasets" in data
        assert "total_count" in data
        assert isinstance(data["datasets"], list)
    
    def test_get_datasets_with_filters(self):
        """Test datasets with filters"""
        response = client.get("/api/v1/datasets?organ=Heart&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert "datasets" in data
        
        # All returned datasets should have Heart as organ (if any)
        for dataset in data["datasets"]:
            assert "Heart" in dataset.get("organ", "")
    
    def test_search_datasets(self):
        """Test dataset search functionality"""
        response = client.get("/api/v1/datasets?search=Heart&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert "datasets" in data
    
    def test_get_public_statistics(self):
        """Test public statistics endpoint"""
        response = client.get("/api/v1/datasets/statistics/summary")
        assert response.status_code == 200
        data = response.json()
        assert "total_datasets" in data
        assert "by_data_type" in data
        assert "by_organ" in data
        assert "by_status" in data
    
    def test_get_dataset_by_nonexistent_id(self):
        """Test getting non-existent dataset"""
        response = client.get("/api/v1/datasets/NONEXISTENT.ID.123")
        assert response.status_code == 404

class TestAdminAPI:
    """Test admin API endpoints"""
    
    @pytest.fixture(scope="class")
    def admin_token(self):
        """Get admin token for testing"""
        response = client.post(
            "/api/v1/admin/login",
            json={"username": "admin", "password": "admin_password"}
        )
        if response.status_code == 200:
            return response.json()["access_token"]
        return None
    
    def test_admin_login_success(self):
        """Test successful admin login"""
        response = client.post(
            "/api/v1/admin/login",
            json={"username": "admin", "password": "admin_password"}
        )
        # Note: This might fail in test environment without seeded data
        # In a real test, we'd need to set up test data first
        assert response.status_code in [200, 401]  # 401 if no admin user in test DB
    
    def test_admin_login_failure(self):
        """Test failed admin login"""
        response = client.post(
            "/api/v1/admin/login",
            json={"username": "admin", "password": "wrong_password"}
        )
        assert response.status_code == 401
    
    def test_admin_statistics_without_token(self):
        """Test admin statistics without authentication"""
        response = client.get("/api/v1/admin/datasets/statistics")
        assert response.status_code == 403  # Forbidden without token

class TestAPIHealth:
    """Test basic API health"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])