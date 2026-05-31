# Portal Service

The Portal service is the student-facing aggregator for CampusHub. It combines data from the Auth, Catalog, Enrollment, and Grades services into unified views for students. Since downstream services may not always be running, it returns mock aggregated data suitable for development and testing.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| GET | /dashboard/{studentId} | Aggregated student dashboard (courses, GPA, notifications) |
| GET | /transcript/{studentId} | Full student transcript with grades and credits |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| PORT | 8000 | Port the service listens on |
| AUTH_URL | http://localhost:5000 | URL of the Auth service |
| CATALOG_URL | http://localhost:5001 | URL of the Catalog service |
| ENROLLMENT_URL | http://localhost:5002 | URL of the Enrollment service |
| GRADES_URL | http://localhost:5003 | URL of the Grades service |

## Running locally

```bash
pip install -r requirements.txt
python src/main.py
```

The service starts on port **8000** by default (override with `PORT` env var).

## Running tests

```bash
cd services/portal
pip install -r requirements.txt
pytest
```

## Docker

```bash
docker build -t campushub-portal .
docker run -p 8000:8000 campushub-portal
```

To point at real downstream services:

```bash
docker run -p 8000:8000 \
  -e AUTH_URL=http://auth:5000 \
  -e CATALOG_URL=http://catalog:5001 \
  -e ENROLLMENT_URL=http://enrollment:5002 \
  -e GRADES_URL=http://grades:5003 \
  campushub-portal
```
