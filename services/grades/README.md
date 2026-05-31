# Grades Service

The Grades service manages student grades and GPA calculation for CampusHub.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| GET | /grades/{studentId} | Get all grades for a student (returns empty list if none) |
| GET | /grades/{studentId}/gpa | Calculate GPA for a student |
| POST | /grades | Create a new grade record |

## Running locally

```bash
pip install -r requirements.txt
python src/main.py
```

The service starts on port **5003** by default (override with `PORT` env var).

## Running tests

```bash
cd services/grades
pip install -r requirements.txt
pytest
```

## Docker

```bash
docker build -t campushub-grades .
docker run -p 5003:5003 campushub-grades
```

## Mock data

The service includes three hardcoded grade records for development:

| ID | Student ID | Course ID | Grade | Semester |
|----|-----------|-----------|-------|----------|
| g001 | u001 | CS101 | A | Fall 2026 |
| g002 | u001 | MATH201 | B+ | Fall 2026 |
| g003 | u003 | ENG102 | B | Fall 2026 |

## Grade point mapping

| Grade | Points |
|-------|--------|
| A | 4.0 |
| A- | 3.7 |
| B+ | 3.3 |
| B | 3.0 |
| B- | 2.7 |
| C+ | 2.3 |
| C | 2.0 |
| F | 0.0 |
