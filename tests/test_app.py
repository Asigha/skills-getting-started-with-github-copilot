import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball" in data

def test_signup_and_remove_participant():
    # Sign up a new participant
    email = "testuser@mergington.edu"
    activity = "Basketball"
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert f"Signed up {email}" in signup_resp.json()["message"]

    # Duplicate signup should fail
    dup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert dup_resp.status_code == 400
    assert "already signed up" in dup_resp.json()["detail"]

    # Remove participant
    del_resp = client.delete(f"/activities/{activity}/participants/{email}")
    assert del_resp.status_code == 200
    assert f"Removed {email}" in del_resp.json()["message"]

    # Remove again should fail
    del_resp2 = client.delete(f"/activities/{activity}/participants/{email}")
    assert del_resp2.status_code == 404
    assert "Participant not found" in del_resp2.json()["detail"]

def test_get_activity():
    resp = client.get("/activities/Basketball")
    assert resp.status_code == 200
    data = resp.json()
    assert data["description"].startswith("Team sport focusing")

    not_found = client.get("/activities/Nonexistent")
    assert not_found.status_code == 404
    assert "Activity not found" in not_found.json()["detail"]
