import pytest
from fastapi.testclient import TestClient


def test_create_department(client: TestClient, authenticated_client: TestClient):
    """Test create department"""
    response = authenticated_client.post(
        "/api/v1/departments",
        json={
            "name": "Engineering",
            "description": "Engineering department"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["name"] == "Engineering"
    assert data["description"] == "Engineering department"


def test_create_duplicate_department(client: TestClient, authenticated_client: TestClient):
    """Test create department with duplicate name"""
    # First create the department
    authenticated_client.post(
        "/api/v1/departments",
        json={
            "name": "Duplicate Dept",
            "description": "First department"
        }
    )
    
    # Try to create same department again
    response = authenticated_client.post(
        "/api/v1/departments",
        json={
            "name": "Duplicate Dept",
            "description": "Second department"
        }
    )
    assert response.status_code == 400


def test_get_departments(client: TestClient, authenticated_client: TestClient):
    """Test get all departments"""
    # Create some departments
    for i in range(3):
        authenticated_client.post(
            "/api/v1/departments",
            json={
                "name": f"Department {i}",
                "description": f"Description for department {i}"
            }
        )
    
    response = authenticated_client.get("/api/v1/departments")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3


def test_get_department(client: TestClient, authenticated_client: TestClient):
    """Test get department by ID"""
    # First create a department
    create_response = authenticated_client.post(
        "/api/v1/departments",
        json={
            "name": "Test Department",
            "description": "Department to retrieve"
        }
    )
    department_id = create_response.json()["id"]
    
    # Retrieve the department
    response = authenticated_client.get(f"/api/v1/departments/{department_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == department_id
    assert data["name"] == "Test Department"


def test_get_nonexistent_department(client: TestClient, authenticated_client: TestClient):
    """Test get department with invalid ID"""
    response = authenticated_client.get("/api/v1/departments/999")
    assert response.status_code == 404


def test_update_department(client: TestClient, authenticated_client: TestClient):
    """Test update department"""
    # First create a department
    create_response = authenticated_client.post(
        "/api/v1/departments",
        json={
            "name": "Original Department",
            "description": "Original description"
        }
    )
    department_id = create_response.json()["id"]
    
    # Update the department
    response = authenticated_client.put(
        f"/api/v1/departments/{department_id}",
        json={
            "name": "Updated Department",
            "description": "Updated description"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Department"
    assert data["description"] == "Updated description"


def test_update_nonexistent_department(client: TestClient, authenticated_client: TestClient):
    """Test update department with invalid ID"""
    response = authenticated_client.put(
        "/api/v1/departments/999",
        json={
            "name": "Invalid Department",
            "description": "This department doesn't exist"
        }
    )
    assert response.status_code == 404


def test_delete_department(client: TestClient, authenticated_client: TestClient):
    """Test delete department"""
    # First create a department
    create_response = authenticated_client.post(
        "/api/v1/departments",
        json={
            "name": "Department to Delete",
            "description": "This department will be deleted"
        }
    )
    department_id = create_response.json()["id"]
    
    # Delete the department
    response = authenticated_client.delete(f"/api/v1/departments/{department_id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = authenticated_client.get(f"/api/v1/departments/{department_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_department(client: TestClient, authenticated_client: TestClient):
    """Test delete department with invalid ID"""
    response = authenticated_client.delete("/api/v1/departments/999")
    assert response.status_code == 404
