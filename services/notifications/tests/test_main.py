"""Tests for the Notifications service."""

import pytest

from src.main import app, NOTIFICATIONS


@pytest.fixture(autouse=True)
def reset_notifications():
    """Reset notifications list and counter to initial state before each test."""
    import src.main as main_module

    original = [
        {
            "id": "n001",
            "user_id": "u001",
            "message": "Welcome to CampusHub!",
            "type": "info",
            "read": False,
            "timestamp": "2026-09-01T09:00:00Z",
        },
        {
            "id": "n002",
            "user_id": "u001",
            "message": "You have been enrolled in CS101",
            "type": "enrollment",
            "read": False,
            "timestamp": "2026-09-01T10:00:00Z",
        },
        {
            "id": "n003",
            "user_id": "u002",
            "message": "New student enrolled in your course",
            "type": "enrollment",
            "read": True,
            "timestamp": "2026-09-01T10:05:00Z",
        },
    ]
    main_module.NOTIFICATIONS.clear()
    main_module.NOTIFICATIONS.extend(original)
    main_module._notification_counter = 4
    yield


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
    assert data["service"] == "notifications"


def test_get_notifications_for_user(client):
    resp = client.get("/notifications/u001")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 2
    assert all(n["user_id"] == "u001" for n in data)


def test_get_notifications_empty(client):
    resp = client.get("/notifications/u999")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data == []


def test_create_notification(client):
    payload = {
        "user_id": "u001",
        "message": "Your grade has been posted",
        "type": "grade",
    }
    resp = client.post("/notify", json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["user_id"] == "u001"
    assert data["message"] == "Your grade has been posted"
    assert data["type"] == "grade"
    assert data["read"] is False
    assert "id" in data
    assert "timestamp" in data


def test_create_notification_default_type(client):
    payload = {"user_id": "u003", "message": "Hello from admin"}
    resp = client.post("/notify", json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["type"] == "info"


def test_create_notification_missing_fields(client):
    resp = client.post("/notify", json={"user_id": "u001"})
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["error"] == "BAD_REQUEST"


def test_filter_unread_only(client):
    resp = client.get("/notifications/u001?unread_only=true")
    assert resp.status_code == 200
    data = resp.get_json()
    assert all(not n["read"] for n in data)
    # u001 has 2 unread notifications in mock data
    assert len(data) == 2


def test_filter_unread_only_excludes_read(client):
    # u002 has 1 notification that is read
    resp = client.get("/notifications/u002?unread_only=true")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data == []
