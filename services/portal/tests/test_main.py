"""Tests for the Portal service."""

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
    assert data["service"] == "portal"


def test_get_dashboard(client):
    resp = client.get("/dashboard/u001")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["student_id"] == "u001"
    assert data["name"] == "Alice Student"
    assert isinstance(data["enrolled_courses"], list)
    assert len(data["enrolled_courses"]) == 2
    assert data["enrolled_courses"][0]["course_id"] == "CS101"
    assert data["enrolled_courses"][1]["course_id"] == "MATH201"
    assert data["notifications_count"] == 2
    assert data["current_gpa"] == 3.65


def test_get_dashboard_reflects_student_id(client):
    resp = client.get("/dashboard/u042")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["student_id"] == "u042"


def test_get_transcript(client):
    resp = client.get("/transcript/u001")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["student_id"] == "u001"
    assert data["name"] == "Alice Student"
    assert isinstance(data["courses"], list)
    assert len(data["courses"]) == 2
    assert data["courses"][0]["course_id"] == "CS101"
    assert data["courses"][0]["grade"] == "A"
    assert data["courses"][0]["credits"] == 3
    assert data["courses"][1]["course_id"] == "MATH201"
    assert data["courses"][1]["grade"] == "B+"
    assert data["cumulative_gpa"] == 3.65
    assert data["total_credits"] == 7


def test_get_transcript_reflects_student_id(client):
    resp = client.get("/transcript/u099")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["student_id"] == "u099"
