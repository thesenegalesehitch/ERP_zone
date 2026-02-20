import pytest
from fastapi.testclient import TestClient


def test_create_employee(client: TestClient, authenticated_client: TestClient):
    """Test create employee"""
    # First create a user to associate with employee
    user_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "employee@example.com",
            "password": "password123",
            "role_id": 1
        }
    )
    user_id = user_response.json()["id"]
    
    # Create employee
    response = authenticated_client.post(
        "/api/v1/employees",
        json={
            "user_id": user_id,
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "hire_date": "2020-01-01",
            "position": "Software Engineer",
            "salary": 50000,
            "department_id": 1
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"


def test_create_employee_with_existing_user(client: TestClient, authenticated_client: TestClient):
    """Test create employee with existing user ID"""
    # First create a user and employee
    user_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "password123",
            "role_id": 1
        }
    )
    user_id = user_response.json()["id"]
    
    authenticated_client.post(
        "/api/v1/employees",
        json={
            "user_id": user_id,
            "first_name": "Jane",
            "last_name": "Smith",
            "date_of_birth": "1995-05-05",
            "hire_date": "2021-02-01",
            "position": "HR Manager",
            "salary": 60000,
            "department_id": 1
        }
    )
    
    # Try to create another employee with same user ID
    response = authenticated_client.post(
        "/api/v1/employees",
        json={
            "user_id": user_id,
            "first_name": "Jane",
            "last_name": "Smith",
            "date_of_birth": "1995-05-05",
            "hire_date": "2021-02-01",
            "position": "HR Manager",
            "salary": 60000,
            "department_id": 1
        }
    )
    assert response.status_code == 400


def test_get_employees(client: TestClient, authenticated_client: TestClient):
    """Test get all employees"""
    # Create test data
    for i in range(3):
        user_response = client.post(
            "/api/v1/auth/register",
            json={
                "email": f"emp{i}@example.com",
                "password": "password123",
                "role_id": 1
            }
        )
        user_id = user_response.json()["id"]
        
        authenticated_client.post(
            "/api/v1/employees",
            json={
                "user_id": user_id,
                "first_name": f"First{i}",
                "last_name": f"Last{i}",
                "date_of_birth": "1990-01-01",
                "hire_date": "2020-01-01",
                "position": "Test Position",
                "salary": 50000,
                "department_id": 1
            }
        )
    
    # Get employees
    response = authenticated_client.get("/api/v1/employees")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3


def test_get_employee(client: TestClient, authenticated_client: TestClient):
    """Test get employee by ID"""
    # Create test employee
    user_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "single@example.com",
            "password": "password123",
            "role_id": 1
        }
    )
    user_id = user_response.json()["id"]
    
    create_response = authenticated_client.post(
        "/api/v1/employees",
        json={
            "user_id": user_id,
            "first_name": "Single",
            "last_name": "Employee",
            "date_of_birth": "1990-01-01",
            "hire_date": "2020-01-01",
            "position": "Test Position",
            "salary": 50000,
            "department_id": 1
        }
    )
    employee_id = create_response.json()["id"]
    
    # Get employee
    response = authenticated_client.get(f"/api/v1/employees/{employee_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == employee_id
    assert data["first_name"] == "Single"


def test_get_nonexistent_employee(client: TestClient, authenticated_client: TestClient):
    """Test get employee with invalid ID"""
    response = authenticated_client.get("/api/v1/employees/999")
    assert response.status_code == 404


def test_update_employee(client: TestClient, authenticated_client: TestClient):
    """Test update employee"""
    # Create test employee
    user_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "update@example.com",
            "password": "password123",
            "role_id": 1
        }
    )
    user_id = user_response.json()["id"]
    
    create_response = authenticated_client.post(
        "/api/v1/employees",
        json={
            "user_id": user_id,
            "first_name": "Original",
            "last_name": "Employee",
            "date_of_birth": "1990-01-01",
            "hire_date": "2020-01-01",
            "position": "Test Position",
            "salary": 50000,
            "department_id": 1
        }
    )
    employee_id = create_response.json()["id"]
    
    # Update employee
    response = authenticated_client.put(
        f"/api/v1/employees/{employee_id}",
        json={
            "first_name": "Updated",
            "salary": 60000
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Updated"
    assert data["salary"] == 60000


def test_update_nonexistent_employee(client: TestClient, authenticated_client: TestClient):
    """Test update employee with invalid ID"""
    response = authenticated_client.put(
        "/api/v1/employees/999",
        json={
            "first_name": "Invalid",
            "salary": 100000
        }
    )
    assert response.status_code == 404


def test_delete_employee(client: TestClient, authenticated_client: TestClient):
    """Test delete employee"""
    # Create test employee
    user_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "delete@example.com",
            "password": "password123",
            "role_id": 1
        }
    )
    user_id = user_response.json()["id"]
    
    create_response = authenticated_client.post(
        "/api/v1/employees",
        json={
            "user_id": user_id,
            "first_name": "Delete",
            "last_name": "Employee",
            "date_of_birth": "1990-01-01",
            "hire_date": "2020-01-01",
            "position": "Test Position",
            "salary": 50000,
            "department_id": 1
        }
    )
    employee_id = create_response.json()["id"]
    
    # Delete employee
    response = authenticated_client.delete(f"/api/v1/employees/{employee_id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = authenticated_client.get(f"/api/v1/employees/{employee_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_employee(client: TestClient, authenticated_client: TestClient):
    """Test delete employee with invalid ID"""
    response = authenticated_client.delete("/api/v1/employees/999")
    assert response.status_code == 404
