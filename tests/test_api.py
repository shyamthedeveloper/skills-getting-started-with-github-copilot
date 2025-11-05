import pytest
from fastapi.testclient import TestClient
from urllib.parse import quote
from src.app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Basic sanity: known activity present
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "pytest-test-user@example.com"
    enc = quote(activity, safe="")

    # Ensure email not present before test (cleanup attempt)
    client.delete(f"/activities/{enc}/participants?email={email}")

    # Sign up
    r = client.post(f"/activities/{enc}/signup?email={email}")
    assert r.status_code == 200
    assert "Signed up" in r.json().get("message", "")

    # Verify participant was added
    r = client.get("/activities")
    participants = r.json()[activity]["participants"]
    assert email in participants

    # Unregister
    r = client.delete(f"/activities/{enc}/participants?email={email}")
    assert r.status_code == 200
    assert "Unregistered" in r.json().get("message", "")

    # Verify removal
    r = client.get("/activities")
    participants = r.json()[activity]["participants"]
    assert email not in participants
