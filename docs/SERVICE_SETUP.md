# Service Setup Guide

How to set up and run any CampusHub service locally.

## Prerequisites

Run the toolchain check to verify your environment:

```bash
chmod +x setup.sh
./setup.sh
```

You need:

- Python 3.11+
- pip
- Docker (optional, for containerized runs)
- Git

## Running a Service

### Option 1: Direct Python

```bash
cd services/<service-name>
pip install -r requirements.txt
python src/main.py
```

The service starts on its default port. Override with the `PORT` environment variable:

```bash
PORT=9000 python src/main.py
```

### Option 2: Docker

Build and run a single service:

```bash
cd services/<service-name>
docker build -t campushub-<service-name> .
docker run -p <port>:<port> campushub-<service-name>
```

### Option 3: Docker Compose (all services)

From the project root:

```bash
docker compose up
```

This starts all 6 services on their default ports. See `docker-compose.yml` for details.

## Running Tests

Each service has a `tests/` directory with pytest tests:

```bash
cd services/<service-name>
pip install -r requirements.txt
PYTHONPATH=. pytest tests/ -v
```

Run tests for all services:

```bash
for svc in auth catalog enrollment grades notifications portal; do
  echo "=== Testing $svc ==="
  (cd services/$svc && PYTHONPATH=. pytest tests/ -v)
done
```

## Default Ports

| Service | Port |
|---------|------|
| Auth | 5000 |
| Catalog | 5001 |
| Enrollment | 5002 |
| Grades | 5003 |
| Notifications | 5004 |
| Portal | 8000 |

## Environment Variables

### All services

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Port to listen on | Service-specific |

### Portal service (additional)

| Variable | Description | Default |
|----------|-------------|---------|
| `AUTH_URL` | Auth service base URL | `http://localhost:5000` |
| `CATALOG_URL` | Catalog service base URL | `http://localhost:5001` |
| `ENROLLMENT_URL` | Enrollment service base URL | `http://localhost:5002` |
| `GRADES_URL` | Grades service base URL | `http://localhost:5003` |

## Project Structure (per service)

```
services/<service-name>/
├── openapi.yaml       # API specification
├── requirements.txt   # Python dependencies
├── Dockerfile         # Multi-stage container build
├── README.md          # Service-specific docs
├── src/
│   └── main.py        # Flask application
└── tests/
    └── test_main.py   # pytest tests
```
