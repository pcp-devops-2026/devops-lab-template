# CampusHub Architecture

## Overview

CampusHub is a microservices-based university management platform used as the capstone project for the IBM DevOps & Software Engineering course. Each service is independently deployable, follows REST conventions, and communicates over HTTP.

## System Diagram

```
                    ┌──────────────┐
                    │    Portal    │
                    │   (8000)     │
                    └──────┬───────┘
                           │ aggregates
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────▼─────┐   ┌─────▼──────┐   ┌─────▼─────┐
    │  Catalog   │   │ Enrollment │   │  Grades   │
    │  (5001)    │   │  (5002)    │   │  (5003)   │
    └────────────┘   └────────────┘   └───────────┘
                           │
                    ┌──────▼───────┐
                    │Notifications │
                    │  (5004)      │
                    └──────────────┘

    ┌──────────────┐
    │    Auth      │  ◄── all services validate tokens against Auth
    │   (5000)     │
    └──────────────┘
```

## Services

| Service | Port | Responsibility | Owner |
|---------|------|---------------|-------|
| Auth | 5000 | Authentication, JWT tokens, user profiles | Instructor |
| Catalog | 5001 | Course listings and departments | Student team |
| Enrollment | 5002 | Student course registrations | Student team |
| Grades | 5003 | Grade records and GPA calculation | Student team |
| Notifications | 5004 | User notifications | Student team |
| Portal | 8000 | Student-facing dashboard, aggregates other services | Student team |

## Communication Patterns

- **Synchronous HTTP/REST**: All inter-service communication uses REST APIs over HTTP
- **Authentication**: Auth service issues JWT tokens; other services validate tokens using the shared public key in `shared/jwt-public-key.pem`
- **Error format**: All services return errors in the standard format defined in `shared/error-response-schema.json`

## Data Strategy

In the reference implementation, each service uses **in-memory mock data** (2-3 hardcoded records). Students extend this by adding databases as the course progresses:

- **Week 10-12**: Add persistent storage (PostgreSQL, MongoDB, etc.)
- **Week 13-15**: Add inter-service communication
- **Week 16-18**: Add resilience patterns (retries, circuit breakers)

## Key Principles

1. **Independent deployability** - Each service has its own Dockerfile and can be built/deployed independently
2. **API-first design** - Each service has an OpenAPI spec (`openapi.yaml`) that defines its contract
3. **Health checks** - Every service exposes `GET /health` for container orchestration
4. **Configuration via environment** - Ports and service URLs are configurable via environment variables
5. **No shared databases** - Each service owns its data (even if mock for now)

## Directory Structure

```
devops-lab-reference-project/
├── services/
│   ├── auth/           # Authentication (instructor-maintained)
│   ├── catalog/        # Course catalog
│   ├── enrollment/     # Course enrollment
│   ├── grades/         # Grades and GPA
│   ├── notifications/  # User notifications
│   └── portal/         # Student dashboard (aggregator)
├── shared/             # Shared schemas and keys
├── docs/               # Project documentation
├── docker-compose.yml  # Local orchestration
└── setup.sh            # Toolchain verification
```
