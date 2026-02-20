import pytest
from fastapi.testclient import TestClient


def test_create_role(client: TestClient, authenticated_client: TestClient):
    """Test create role"""
    response = authenticated_client.post(
        "/api/v1/roles",
        json={
            "name": "Test Role",
            "description": "Test role description"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["name"] == "Test Role"
    assert data["description"] == "Test role description"


def test_create_duplicate_role(client: TestClient, authenticated_client: TestClient):
    """Test create role with duplicate name"""
    # First create the role
    authenticated_client.post(
        "/api/v1/roles",
        json={
            "name": "Duplicate Role",
            "description": "First role"
        }
    )
    
    # Try to create same role again
    response = authenticated_client.post(
        "/api/v1/roles",
        json={
            "name": "Duplicate Role",
            "description": "Second role"
        }
    )
    assert response.status_code == 400


def test_get_roles(client: TestClient, authenticated_client: TestClient):
    """Test get all roles"""
    # Create some roles
    for i in range(3):
        authenticated_client.post(
            "/api/v1/roles",
            json={
                f"name": f"Role {i}",
                "description": f"Description for role {i}"
            }
        )
    
    response = authenticated_client.get("/api/v1/roles")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3


def test_get_role(client: TestClient, authenticated_client: TestClient):
    """Test get role by ID"""
    # First create a role
    create_response = authenticated_client.post(
        "/api/v1/roles",
        json={
            "name": "Single Role",
            "description": "Role to retrieve"
        }
    )
    role_id = create_response.json()["id"]
    
    # Retrieve the role
    response = authenticated_client.get(f"/api/v1/roles/{role_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == role_id
    assert data["name"] == "Single Role"


def test_get_nonexistent_role(client: TestClient, authenticated_client: TestClient):
    """Test get role with invalid ID"""
    response = authenticated_client.get("/api/v1/roles/999")
    assert response.status_code == 404


def test_update_role(client: TestClient, authenticated_client: TestClient):
    """Test update role"""
    # First create a role
    create_response = authenticated_client.post(
        "/api/v1/roles",
        json={
            "name": "Original Role",
            "description": "Original description"
        }
    )
    role_id = create_response.json()["id"]
    
    # Update the role
    response = authenticated_client.put(
        f"/api/v1/roles/{role_id}",
        json={
            "name": "Updated Role",
            "description": "Updated description"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Role"
    assert data["description"] == "Updated description"


def test_update_nonexistent_role(client: TestClient, authenticated_client: TestClient):
    """Test update role with invalid ID"""
    response = authenticated_client.put(
        "/api/v1/roles/999",
        json={
            "name": "Invalid Role",
            "description": "This role doesn't exist"
        }
    )
    assert response.status_code == 404


def test_delete_role(client: TestClient, authenticated_client: TestClient):
    """Test delete role"""
    # First create a role
    create_response = authenticated_client.post(
        "/api/v1/roles",
        json={
            "name": "Role to Delete",
            "description": "This role will be deleted"
        }
    )
    role_id = create_response.json()["id"]
    
    # Delete the role
    response = authenticated_client.delete(f"/api/v1/roles/{role_id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = authenticated_client.get(f"/api/v1/roles/{role_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_role(client: TestClient, authenticated_client: TestClient):
    """Test delete role with invalid ID"""
    response = authenticated_client.delete("/api/v1/roles/999")
    assert response.status_code == 404
