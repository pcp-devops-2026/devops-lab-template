"""CampusHub Enrollment Service - Course enrollment management."""

import os
import uuid

from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Mock data ---
ENROLLMENTS = [
    {
        "id": "e001",
        "student_id": "u001",
        "course_id": "CS101",
        "semester": "Fall 2026",
        "status": "active",
    },
    {
        "id": "e002",
        "student_id": "u001",
        "course_id": "MATH201",
        "semester": "Fall 2026",
        "status": "active",
    },
    {
        "id": "e003",
        "student_id": "u003",
        "course_id": "ENG102",
        "semester": "Fall 2026",
        "status": "dropped",
    },
]


# --- Routes ---


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "enrollment"})


@app.route("/enrollments", methods=["GET"])
def list_enrollments():
    student_id = request.args.get("student_id")
    if student_id:
        result = [e for e in ENROLLMENTS if e["student_id"] == student_id]
    else:
        result = ENROLLMENTS
    return jsonify(result)


@app.route("/enrollments", methods=["POST"])
def create_enrollment():
    data = request.get_json()
    if not data or not all(k in data for k in ("student_id", "course_id", "semester")):
        return jsonify(
            {
                "error": "BAD_REQUEST",
                "message": "Missing required fields: student_id, course_id, semester",
                "status": 400,
            }
        ), 400

    enrollment = {
        "id": f"e{uuid.uuid4().hex[:6]}",
        "student_id": data["student_id"],
        "course_id": data["course_id"],
        "semester": data["semester"],
        "status": data.get("status", "active"),
    }
    ENROLLMENTS.append(enrollment)
    return jsonify(enrollment), 201


@app.route("/enrollments/<enrollment_id>", methods=["DELETE"])
def delete_enrollment(enrollment_id):
    for i, enrollment in enumerate(ENROLLMENTS):
        if enrollment["id"] == enrollment_id:
            ENROLLMENTS.pop(i)
            return jsonify({"message": f"Enrollment {enrollment_id} deleted"})

    return jsonify(
        {
            "error": "NOT_FOUND",
            "message": f"Enrollment {enrollment_id} not found",
            "status": 404,
        }
    ), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host="0.0.0.0", port=port, debug=True)
