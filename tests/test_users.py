import pytest
from fastapi.testclient import TestClient
from app.main import app, users_db


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


def test_get_users_empty(client):
    """Test getting users when database is empty"""
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []


def test_create_user(client):
    """Test creating a new user"""
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert data["age"] == user_data["age"]


def test_create_user_without_age(client):
    """Test creating a user without age (optional field)"""
    user_data = {
        "name": "Jane Doe",
        "email": "jane@example.com"
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert data["age"] is None


def test_get_users(client):
    """Test getting all users"""
    # Create two users
    client.post("/users", json={"name": "User 1", "email": "user1@example.com", "age": 25})
    client.post("/users", json={"name": "User 2", "email": "user2@example.com", "age": 35})
    
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "User 1"
    assert data[1]["name"] == "User 2"


def test_get_user_by_id(client):
    """Test getting a user by ID"""
    # Create a user
    create_response = client.post("/users", json={"name": "John Doe", "email": "john@example.com", "age": 30})
    user_id = create_response.json()["id"]
    
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == "John Doe"


def test_get_user_not_found(client):
    """Test getting a non-existent user"""
    response = client.get("/users/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_user(client):
    """Test updating an existing user"""
    # Create a user
    create_response = client.post("/users", json={"name": "John Doe", "email": "john@example.com", "age": 30})
    user_id = create_response.json()["id"]
    
    # Update the user
    updated_data = {
        "name": "John Smith",
        "email": "johnsmith@example.com",
        "age": 31
    }
    response = client.put(f"/users/{user_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == updated_data["name"]
    assert data["email"] == updated_data["email"]
    assert data["age"] == updated_data["age"]


def test_update_user_not_found(client):
    """Test updating a non-existent user"""
    response = client.put("/users/999", json={"name": "Test", "email": "test@example.com"})
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_delete_user(client):
    """Test deleting a user"""
    # Create a user
    create_response = client.post("/users", json={"name": "John Doe", "email": "john@example.com", "age": 30})
    user_id = create_response.json()["id"]
    
    # Delete the user
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    
    # Verify user is deleted
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404


def test_delete_user_not_found(client):
    """Test deleting a non-existent user"""
    response = client.delete("/users/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_create_user_invalid_data(client):
    """Test creating a user with invalid data"""
    # Missing required field
    response = client.post("/users", json={"name": "John Doe"})
    assert response.status_code == 422
    
    # Empty name
    response = client.post("/users", json={"name": "", "email": "test@example.com"})
    assert response.status_code == 422
    
    # Invalid age (negative)
    response = client.post("/users", json={"name": "John", "email": "john@example.com", "age": -5})
    assert response.status_code == 422
