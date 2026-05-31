"""Tests for the Grades service."""

import pytest

from src.main import app, GRADES


@pytest.fixture(autouse=True)
def reset_grades():
    """Reset GRADES list to initial state before each test."""
    original = [
        {
            "id": "g001",
            "student_id": "u001",
            "course_id": "CS101",
            "grade": "A",
            "semester": "Fall 2026",
        },
        {
            "id": "g002",
            "student_id": "u001",
            "course_id": "MATH201",
            "grade": "B+",
            "semester": "Fall 2026",
        },
        {
            "id": "g003",
            "student_id": "u003",
            "course_id": "ENG102",
            "grade": "B",
            "semester": "Fall 2026",
        },
    ]
    GRADES.clear()
    GRADES.extend(original)
    yield
    GRADES.clear()
    GRADES.extend(original)


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
    assert data["service"] == "grades"


def test_get_grades_for_student(client):
    resp = client.get("/grades/u001")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 2
    student_ids = {g["student_id"] for g in data}
    assert student_ids == {"u001"}


def test_get_grades_empty(client):
    resp = client.get("/grades/u999")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data == []


def test_get_gpa(client):
    resp = client.get("/grades/u001/gpa")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["student_id"] == "u001"
    # A = 4.0, B+ = 3.3 -> average = 3.65
    assert data["gpa"] == 3.65
    assert data["courses_counted"] == 2


def test_get_gpa_not_found(client):
    resp = client.get("/grades/u999/gpa")
    assert resp.status_code == 404
    data = resp.get_json()
    assert data["error"] == "NOT_FOUND"


def test_post_grade(client):
    resp = client.post(
        "/grades",
        json={
            "student_id": "u002",
            "course_id": "PHY301",
            "grade": "A-",
            "semester": "Spring 2027",
        },
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["student_id"] == "u002"
    assert data["course_id"] == "PHY301"
    assert data["grade"] == "A-"
    assert data["semester"] == "Spring 2027"
    assert "id" in data

    # Verify it was persisted
    list_resp = client.get("/grades/u002")
    assert any(g["course_id"] == "PHY301" for g in list_resp.get_json())


def test_post_grade_invalid_grade(client):
    resp = client.post(
        "/grades",
        json={
            "student_id": "u002",
            "course_id": "PHY301",
            "grade": "Z",
            "semester": "Spring 2027",
        },
    )
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["error"] == "BAD_REQUEST"


def test_post_grade_missing_fields(client):
    resp = client.post(
        "/grades",
        json={"student_id": "u002", "course_id": "PHY301"},
    )
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["error"] == "BAD_REQUEST"
