import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Use a unique email for testing
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Ensure user is not already signed up (ignore result)
    client.post(f"/activities/{activity}/unregister?email={email}")

    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    print('Signup response:', response.status_code, response.text)
    assert response.status_code == 200, f"Signup failed: {response.text}"
    assert f"Signed up {email}" in response.json()["message"]

    # Unregister
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    print('Unregister response:', response.status_code, response.text)
    assert response.status_code == 200, f"Unregister failed: {response.text}"
    assert f"Removed {email}" in response.json()["message"]

    # Unregister again should fail
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    print('Unregister again response:', response.status_code, response.text)
    assert response.status_code == 400
    assert "Student not registered" in response.json()["detail"]
