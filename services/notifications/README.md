# Notifications Service

The Notifications service handles sending and retrieving notifications for CampusHub users.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| POST | /notify | Create and send a notification |
| GET | /notifications/{userId} | Get notifications for a user |

The `GET /notifications/{userId}` endpoint supports an optional `?unread_only=true` query parameter to filter for unread notifications only.

## Running locally

```bash
pip install -r requirements.txt
python src/main.py
```

The service starts on port **5004** by default (override with `PORT` env var).

## Running tests

```bash
cd services/notifications
pip install -r requirements.txt
pytest
```

## Docker

```bash
docker build -t campushub-notifications .
docker run -p 5004:5004 campushub-notifications
```

## Mock data

The service includes three hardcoded notifications for development:

| ID | User | Message | Type | Read |
|----|------|---------|------|------|
| n001 | u001 | Welcome to CampusHub! | info | false |
| n002 | u001 | You have been enrolled in CS101 | enrollment | false |
| n003 | u002 | New student enrolled in your course | enrollment | true |
