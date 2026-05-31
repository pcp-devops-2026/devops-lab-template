"""Tests for the Catalog service."""

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
    assert data["service"] == "catalog"


def test_list_courses(client):
    resp = client.get("/courses")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 3


def test_get_course_by_id(client):
    resp = client.get("/courses/CS101")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == "CS101"
    assert data["title"] == "Intro to Computer Science"
    assert data["department"] == "Computer Science"
    assert data["credits"] == 3


def test_get_course_not_found(client):
    resp = client.get("/courses/FAKE999")
    assert resp.status_code == 404
    data = resp.get_json()
    assert data["error"] == "NOT_FOUND"


def test_filter_courses_by_department(client):
    resp = client.get("/courses?department=Mathematics")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["id"] == "MATH201"


def test_filter_courses_by_department_no_match(client):
    resp = client.get("/courses?department=Physics")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data == []


def test_list_departments(client):
    resp = client.get("/departments")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert "Computer Science" in data
    assert "Mathematics" in data
    assert "English" in data
    assert len(data) == 3
