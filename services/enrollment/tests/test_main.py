"""Tests for the Enrollment service."""

import pytest

from src.main import app, ENROLLMENTS


@pytest.fixture(autouse=True)
def reset_enrollments():
    """Reset ENROLLMENTS to initial state before each test."""
    original = [
        {
            "id": "e001",
            "student_id": "u001",
            "course_id": "CS101",
            "semester": "Fall 2026",
            "status": "active",
        },
        {
            "id": "e002",
            "student_id": "u001",
            "course_id": "MATH201",
            "semester": "Fall 2026",
            "status": "active",
        },
        {
            "id": "e003",
            "student_id": "u003",
            "course_id": "ENG102",
            "semester": "Fall 2026",
            "status": "dropped",
        },
    ]
    ENROLLMENTS.clear()
    ENROLLMENTS.extend(original)
    yield
    ENROLLMENTS.clear()
    ENROLLMENTS.extend(original)


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
    assert data["service"] == "enrollment"


def test_list_enrollments(client):
    resp = client.get("/enrollments")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 3


def test_filter_enrollments_by_student_id(client):
    resp = client.get("/enrollments?student_id=u001")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 2
    assert all(e["student_id"] == "u001" for e in data)


def test_create_enrollment(client):
    payload = {"student_id": "u002", "course_id": "PHYS301", "semester": "Fall 2026"}
    resp = client.post("/enrollments", json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["student_id"] == "u002"
    assert data["course_id"] == "PHYS301"
    assert data["semester"] == "Fall 2026"
    assert data["status"] == "active"
    assert "id" in data


def test_create_enrollment_missing_fields(client):
    resp = client.post("/enrollments", json={"student_id": "u002"})
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["error"] == "BAD_REQUEST"


def test_delete_enrollment(client):
    resp = client.delete("/enrollments/e001")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "deleted" in data["message"]

    # Verify it's gone
    list_resp = client.get("/enrollments")
    ids = [e["id"] for e in list_resp.get_json()]
    assert "e001" not in ids


def test_delete_enrollment_not_found(client):
    resp = client.delete("/enrollments/e999")
    assert resp.status_code == 404
    data = resp.get_json()
    assert data["error"] == "NOT_FOUND"
