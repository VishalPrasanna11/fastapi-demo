import pytest
from fastapi.testclient import TestClient
from app.main import app, users_db, next_user_id


@pytest.fixture(autouse=True)
def reset_db():
    """Reset the database before each test"""
    users_db.clear()
    import app.main
    app.main.next_user_id = 1
    yield
    users_db.clear()


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
