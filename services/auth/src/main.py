"""CampusHub Auth Service - Authentication and user management."""

import os

from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Mock data ---
USERS = {
    "u001": {
        "id": "u001",
        "username": "alice",
        "email": "alice@campus.edu",
        "role": "student",
        "password": "password123",
    },
    "u002": {
        "id": "u002",
        "username": "bob",
        "email": "bob@campus.edu",
        "role": "instructor",
        "password": "securepass",
    },
    "u003": {
        "id": "u003",
        "username": "charlie",
        "email": "charlie@campus.edu",
        "role": "admin",
        "password": "adminpass",
    },
}

USERNAMES = {u["username"]: u for u in USERS.values()}

# Mock token counter (in real service, use JWT)
_token_counter = 0


def _make_token(user_id):
    global _token_counter
    _token_counter += 1
    return f"mock-jwt-{user_id}-{_token_counter}"


# In-memory token store (mock — real service would use JWT validation)
TOKENS = {}


# --- Routes ---


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "auth"})


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify(
            {"error": "BAD_REQUEST", "message": "Missing username or password", "status": 400}
        ), 400

    user = USERNAMES.get(data["username"])
    if not user or user["password"] != data["password"]:
        return jsonify(
            {"error": "UNAUTHORIZED", "message": "Invalid credentials", "status": 401}
        ), 401

    token = _make_token(user["id"])
    TOKENS[token] = user["id"]
    return jsonify({"token": token, "user_id": user["id"]})


@app.route("/validate", methods=["POST"])
def validate():
    data = request.get_json()
    if not data or "token" not in data:
        return jsonify(
            {"error": "BAD_REQUEST", "message": "Missing token", "status": 400}
        ), 400

    token = data["token"]
    user_id = TOKENS.get(token)
    if not user_id:
        return jsonify(
            {"error": "UNAUTHORIZED", "message": "Invalid or expired token", "status": 401}
        ), 401

    return jsonify({"valid": True, "user_id": user_id})


@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = USERS.get(user_id)
    if not user:
        return jsonify(
            {"error": "NOT_FOUND", "message": f"User {user_id} not found", "status": 404}
        ), 404

    # Don't expose password
    return jsonify({k: v for k, v in user.items() if k != "password"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
