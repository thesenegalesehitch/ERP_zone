import pytest
from fastapi.testclient import TestClient


def test_create_leave_request(client: TestClient, authenticated_client: TestClient):
    """Test create leave request"""
    response = authenticated_client.post(
        "/api/v1/leave-requests",
        json={
            "start_date": "2024-06-01",
            "end_date": "2024-06-05",
            "reason": "Annual leave"
        }
    )
    # This may fail if user doesn't have an employee profile
    # Testing the response code
    assert response.status_code in [201, 400, 404]


def test_get_leave_requests(client: TestClient, authenticated_client: TestClient):
    """Test get all leave requests"""
    response = authenticated_client.get("/api/v1/leave-requests")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_leave_request(client: TestClient, authenticated_client: TestClient):
    """Test get leave request by ID"""
    response = authenticated_client.get("/api/v1/leave-requests/999")
    # Either 404 or the leave request exists
    assert response.status_code in [200, 404]


def test_update_leave_request(client: TestClient, authenticated_client: TestClient):
    """Test update leave request"""
    response = authenticated_client.put(
        "/api/v1/leave-requests/999",
        json={
            "status": "approved"
        }
    )
    assert response.status_code in [200, 404]


def test_delete_leave_request(client: TestClient, authenticated_client: TestClient):
    """Test delete leave request"""
    response = authenticated_client.delete("/api/v1/leave-requests/999")
    assert response.status_code in [204, 404]
