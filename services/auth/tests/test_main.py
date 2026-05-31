"""Tests for the Auth service."""

import pytest

from src.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "healthy"
    assert data["service"] == "auth"


def test_login_success(client):
    resp = client.post("/login", json={"username": "alice", "password": "password123"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "token" in data
    assert data["user_id"] == "u001"


def test_login_invalid_credentials(client):
    resp = client.post("/login", json={"username": "alice", "password": "wrong"})
    assert resp.status_code == 401
    data = resp.get_json()
    assert data["error"] == "UNAUTHORIZED"


def test_login_missing_fields(client):
    resp = client.post("/login", json={"username": "alice"})
    assert resp.status_code == 400


def test_validate_token(client):
    login_resp = client.post("/login", json={"username": "alice", "password": "password123"})
    token = login_resp.get_json()["token"]

    resp = client.post("/validate", json={"token": token})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["valid"] is True
    assert data["user_id"] == "u001"


def test_validate_invalid_token(client):
    resp = client.post("/validate", json={"token": "fake-token"})
    assert resp.status_code == 401


def test_get_user(client):
    resp = client.get("/users/u001")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["username"] == "alice"
    assert "password" not in data


def test_get_user_not_found(client):
    resp = client.get("/users/u999")
    assert resp.status_code == 404
    data = resp.get_json()
    assert data["error"] == "NOT_FOUND"
