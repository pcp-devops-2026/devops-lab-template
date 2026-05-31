# Catalog Service

The Catalog service manages course listings and department information for the CampusHub platform.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| GET | /courses | List all courses (optional `?department=` filter) |
| GET | /courses/{id} | Get a course by ID |
| GET | /departments | List all unique department names |

## Running locally

```bash
pip install -r requirements.txt
python src/main.py
```

The service starts on port **5001** by default (override with `PORT` env var).

## Running tests

```bash
cd services/catalog
pip install -r requirements.txt
pytest
```

## Docker

```bash
docker build -t campushub-catalog .
docker run -p 5001:5001 campushub-catalog
```

## Mock data

The service includes three hardcoded courses for development:

| ID | Title | Department | Credits |
|----|-------|------------|---------|
| CS101 | Intro to Computer Science | Computer Science | 3 |
| MATH201 | Linear Algebra | Mathematics | 4 |
| ENG102 | Technical Writing | English | 3 |
