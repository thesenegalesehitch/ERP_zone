import pytest
from fastapi.testclient import TestClient


def test_register(client: TestClient):
    """Test user registration"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword123",
            "role_id": 1
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "email" in data
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_register_duplicate_email(client: TestClient):
    """Test registration with existing email"""
    # First registration
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "password123",
            "role_id": 1
        }
    )
    
    # Second registration with same email
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "password456",
            "role_id": 1
        }
    )
    assert response.status_code == 400


def test_register_invalid_role(client: TestClient):
    """Test registration with invalid role"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "invalidrole@example.com",
            "password": "password123",
            "role_id": 999  # Non-existent role
        }
    )
    assert response.status_code == 404


def test_login(client: TestClient):
    """Test user login"""
    # First register the user
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@example.com",
            "password": "loginpassword123",
            "role_id": 1
        }
    )
    
    # Then try to login
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "login@example.com",
            "password": "loginpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


def test_login_incorrect_email(client: TestClient):
    """Test login with incorrect email"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401


def test_login_incorrect_password(client: TestClient):
    """Test login with incorrect password"""
    # First register the user
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "wrongpass@example.com",
            "password": "correctpassword",
            "role_id": 1
        }
    )
    
    # Try to login with wrong password
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "wrongpass@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
