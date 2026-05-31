"""CampusHub Notifications Service - Sending and retrieving notifications."""

import os
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, request, send_file
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

SPEC_PATH = Path(__file__).resolve().parent.parent / "openapi.yaml"
app.register_blueprint(
    get_swaggerui_blueprint("/apidocs", "/apispec.yaml"),
    url_prefix="/apidocs",
)


@app.route("/apispec.yaml")
def apispec():
    return send_file(SPEC_PATH, mimetype="text/yaml")

# --- Mock data ---
NOTIFICATIONS = [
    {
        "id": "n001",
        "user_id": "u001",
        "message": "Welcome to CampusHub!",
        "type": "info",
        "read": False,
        "timestamp": "2026-09-01T09:00:00Z",
    },
    {
        "id": "n002",
        "user_id": "u001",
        "message": "You have been enrolled in CS101",
        "type": "enrollment",
        "read": False,
        "timestamp": "2026-09-01T10:00:00Z",
    },
    {
        "id": "n003",
        "user_id": "u002",
        "message": "New student enrolled in your course",
        "type": "enrollment",
        "read": True,
        "timestamp": "2026-09-01T10:05:00Z",
    },
]

_notification_counter = 4


# --- Routes ---


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "notifications"})


@app.route("/notify", methods=["POST"])
def notify():
    global _notification_counter

    data = request.get_json()
    if not data or "user_id" not in data or "message" not in data:
        return jsonify(
            {
                "error": "BAD_REQUEST",
                "message": "Missing required fields: user_id and message",
                "status": 400,
            }
        ), 400

    notification_id = f"n{_notification_counter:03d}"
    _notification_counter += 1

    notification = {
        "id": notification_id,
        "user_id": data["user_id"],
        "message": data["message"],
        "type": data.get("type", "info"),
        "read": False,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    NOTIFICATIONS.append(notification)
    return jsonify(notification), 201


@app.route("/notifications/<user_id>", methods=["GET"])
def get_notifications(user_id):
    unread_only = request.args.get("unread_only", "false").lower() == "true"

    results = [n for n in NOTIFICATIONS if n["user_id"] == user_id]

    if unread_only:
        results = [n for n in results if not n["read"]]

    return jsonify(results)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5004))
    app.run(host="0.0.0.0", port=port, debug=True)
