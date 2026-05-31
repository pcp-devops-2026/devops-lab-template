# Enrollment Service

The Enrollment service manages course enrollments for CampusHub students. It supports listing, creating, and deleting enrollments.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| GET | /enrollments | List all enrollments (supports `?student_id=` filter) |
| POST | /enrollments | Create a new enrollment |
| DELETE | /enrollments/{id} | Delete an enrollment by ID |

## Running locally

```bash
pip install -r requirements.txt
python src/main.py
```

The service starts on port **5002** by default (override with `PORT` env var).

## Running tests

```bash
cd services/enrollment
pip install -r requirements.txt
pytest
```

## Docker

```bash
docker build -t campushub-enrollment .
docker run -p 5002:5002 campushub-enrollment
```

## Mock data

The service includes three hardcoded enrollments for development:

| ID | Student ID | Course ID | Semester | Status |
|----|-----------|-----------|----------|--------|
| e001 | u001 | CS101 | Fall 2026 | active |
| e002 | u001 | MATH201 | Fall 2026 | active |
| e003 | u003 | ENG102 | Fall 2026 | dropped |
