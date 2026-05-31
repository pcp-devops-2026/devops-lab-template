# CampusHub Reference Project

A microservices-based university management platform used as the capstone project for the **IBM DevOps & Software Engineering Professional Certificate** cohort.

This repository is the **reference implementation** — a forkable starting point containing 6 service skeletons, OpenAPI specs, Docker configs, and documentation. Students fork this repo, pick a service, and build it out across a 20-week course.

## Services

| Service | Port | Description |
|---------|------|-------------|
| [Auth](services/auth/) | 5000 | Authentication, JWT tokens, user profiles (instructor-maintained) |
| [Catalog](services/catalog/) | 5001 | Course listings and departments |
| [Enrollment](services/enrollment/) | 5002 | Student course registrations |
| [Grades](services/grades/) | 5003 | Grade records and GPA calculation |
| [Notifications](services/notifications/) | 5004 | User notifications |
| [Portal](services/portal/) | 8000 | Student dashboard, aggregates other services |

Each service includes a Flask skeleton with mock data, a `GET /health` endpoint, pytest tests, an OpenAPI spec, and a multi-stage Dockerfile.

## Getting Started

### 1. Fork this repository

Click **Fork** at the top of this page.

### 2. Rename your fork

Follow the naming convention:

```
campushub-<service>-<your-github-id>
```

Example: `campushub-catalog-alice123`

### 3. Clone and verify

```bash
git clone https://github.com/<you>/campushub-<service>-<you>.git
cd campushub-<service>-<you>
chmod +x setup.sh
./setup.sh
```

### 4. Run your service

```bash
cd services/<service-name>
pip install -r requirements.txt
python src/main.py
```

### 5. Run tests

```bash
cd services/<service-name>
PYTHONPATH=. pytest tests/ -v
```

### 6. Run all services with Docker Compose

```bash
docker compose up
```

## Repo Structure

```
├── services/
│   ├── auth/              # Authentication service
│   ├── catalog/           # Course catalog service
│   ├── enrollment/        # Enrollment service
│   ├── grades/            # Grades service
│   ├── notifications/     # Notifications service
│   └── portal/            # Student portal (aggregator)
├── shared/                # Shared schemas and keys
│   ├── error-response-schema.json
│   ├── jwt-public-key.pem
│   └── README.md
├── docs/
│   ├── ARCHITECTURE.md    # System design and service map
│   ├── FORK_WORKFLOW.md   # Fork, rename, and contribute
│   ├── SERVICE_SETUP.md   # Running and testing services
│   └── INTEGRATION_GUIDE.md  # Inter-service communication
├── docker-compose.yml     # Run all services locally
├── setup.sh               # Toolchain verification
├── .editorconfig          # Consistent formatting
└── LICENSE                # MIT
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md) — system diagram, service responsibilities, design principles
- [Fork Workflow](docs/FORK_WORKFLOW.md) — how to fork, rename, and sync with upstream
- [Service Setup](docs/SERVICE_SETUP.md) — running, testing, and configuring services
- [Integration Guide](docs/INTEGRATION_GUIDE.md) — inter-service communication patterns

## Course Timeline

| Weeks | Focus |
|-------|-------|
| 1-6 | DevOps fundamentals, Git, Linux |
| 7-9 | Agile, CI/CD concepts |
| 10-12 | Containers, Docker, service skeletons |
| 13-15 | Kubernetes, deployment |
| 16-18 | Monitoring, testing, resilience |
| 19-20 | Capstone — full platform integration |

## Naming Convention

All forks follow this pattern:

```
campushub-<service>-<github-id>
```

This keeps the cohort's repos discoverable and consistently organized.

## Conventional Commits

Use prefixes: `feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`, `ci:`.

Example: `feat: add /courses endpoint with pagination`

## Language Note

The reference implementation uses **Python/Flask**, but students may reimplement their service in any language as long as the API contract (OpenAPI spec) is maintained.

## License

[MIT](LICENSE)
