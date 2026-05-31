# Auth Service

The Auth service handles authentication and user management for CampusHub. It is maintained by the instructor and provides JWT tokens that all other services depend on.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| POST | /login | Authenticate user, return JWT |
| POST | /validate | Validate a JWT token |
| GET | /users/{id} | Get user profile |

## Running locally

```bash
pip install -r requirements.txt
python src/main.py
```

The service starts on port **5000** by default (override with `PORT` env var).

## Running tests

```bash
cd services/auth
pip install -r requirements.txt
pytest
```

## Docker

```bash
docker build -t campushub-auth .
docker run -p 5000:5000 campushub-auth
```

## Mock data

The service includes three hardcoded users for development:

| ID | Username | Role |
|----|----------|------|
| u001 | alice | student |
| u002 | bob | instructor |
| u003 | charlie | admin |
