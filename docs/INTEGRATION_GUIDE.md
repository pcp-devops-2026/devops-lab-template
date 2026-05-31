# Integration Guide

How CampusHub services work together and how to build inter-service communication.

## Service Dependencies

```
Portal ──► Auth        (validate user session)
Portal ──► Catalog     (fetch course details)
Portal ──► Enrollment  (fetch student enrollments)
Portal ──► Grades      (fetch grades and GPA)

Enrollment ──► Catalog (verify course exists)
Enrollment ──► Auth    (verify student exists)
Enrollment ──► Notifications (notify on enrollment)

Grades ──► Auth        (verify student exists)
Grades ──► Enrollment  (verify student is enrolled)
```

## Authentication Flow

1. Client sends `POST /login` to Auth with username/password
2. Auth returns a JWT token
3. Client includes the token in subsequent requests: `Authorization: Bearer <token>`
4. Receiving service validates the token against Auth's `POST /validate` endpoint (or validates locally using the shared public key)

### Example: Authenticated request

```bash
# Step 1: Login
TOKEN=$(curl -s -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "password123"}' | jq -r '.token')

# Step 2: Use the token (future implementation)
curl -H "Authorization: Bearer $TOKEN" http://localhost:5001/courses
```

In the reference skeleton, authentication middleware is not yet wired into the other services. Students add this as a course exercise.

## Adding Inter-Service Communication

The reference skeletons use mock data. To add real inter-service calls:

### 1. Use the `requests` library

```python
import requests
import os

AUTH_URL = os.environ.get("AUTH_URL", "http://localhost:5000")

def validate_token(token):
    resp = requests.post(f"{AUTH_URL}/validate", json={"token": token})
    if resp.status_code != 200:
        return None
    return resp.json()
```

### 2. Add error handling

```python
from requests.exceptions import ConnectionError, Timeout

def get_course(course_id):
    try:
        resp = requests.get(f"{CATALOG_URL}/courses/{course_id}", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except (ConnectionError, Timeout):
        return {"error": "SERVICE_UNAVAILABLE", "message": "Catalog service unreachable", "status": 503}
```

### 3. Use Docker Compose networking

When running via `docker compose`, services communicate using their service names as hostnames:

```python
# In docker-compose, catalog is reachable at http://catalog:5001
CATALOG_URL = os.environ.get("CATALOG_URL", "http://catalog:5001")
```

## Testing Integrations

### Unit tests (mock external calls)

```python
from unittest.mock import patch

def test_dashboard_with_mock_catalog(client):
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = [{"id": "CS101", "title": "Intro to CS"}]
        mock_get.return_value.status_code = 200
        resp = client.get("/dashboard/u001")
        assert resp.status_code == 200
```

### Integration tests (with Docker Compose)

```bash
# Start all services
docker compose up -d

# Wait for health checks
for port in 5000 5001 5002 5003 5004 8000; do
  curl --retry 5 --retry-delay 2 http://localhost:$port/health
done

# Run integration tests
pytest tests/integration/ -v

# Tear down
docker compose down
```

## Common Patterns

### Health check aggregation (Portal)

The Portal service can aggregate health from all upstream services:

```python
@app.route("/health/all")
def health_all():
    services = {"auth": AUTH_URL, "catalog": CATALOG_URL}
    results = {}
    for name, url in services.items():
        try:
            r = requests.get(f"{url}/health", timeout=2)
            results[name] = r.json()
        except Exception:
            results[name] = {"status": "unreachable"}
    return jsonify(results)
```

### Retry with backoff

```python
import time

def call_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
    return None
```
