"""CampusHub Grades Service - Student grade management and GPA calculation."""

import os
import uuid
from pathlib import Path

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)

SPEC_PATH = Path(__file__).resolve().parent.parent / "openapi.yaml"
app.register_blueprint(
    get_swaggerui_blueprint("/apidocs", "/apispec.yaml"),
    url_prefix="/apidocs",
)


@app.route("/apispec.yaml")
def apispec():
    return send_file(SPEC_PATH, mimetype="text/yaml")

# --- Grade point mapping ---
GRADE_POINTS = {
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "F": 0.0,
}

# --- Mock data ---
GRADES = [
    {
        "id": "g001",
        "student_id": "u001",
        "course_id": "CS101",
        "grade": "A",
        "semester": "Fall 2026",
    },
    {
        "id": "g002",
        "student_id": "u001",
        "course_id": "MATH201",
        "grade": "B+",
        "semester": "Fall 2026",
    },
    {
        "id": "g003",
        "student_id": "u003",
        "course_id": "ENG102",
        "grade": "B",
        "semester": "Fall 2026",
    },
]


# --- Routes ---


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "grades"})


@app.route("/grades/<student_id>", methods=["GET"])
def get_grades(student_id):
    student_grades = [g for g in GRADES if g["student_id"] == student_id]
    return jsonify(student_grades)


@app.route("/grades/<student_id>/gpa", methods=["GET"])
def get_gpa(student_id):
    student_grades = [g for g in GRADES if g["student_id"] == student_id]
    if not student_grades:
        return jsonify(
            {
                "error": "NOT_FOUND",
                "message": f"No grades found for student {student_id}",
                "status": 404,
            }
        ), 404

    points = [GRADE_POINTS[g["grade"]] for g in student_grades]
    gpa = sum(points) / len(points)
    return jsonify(
        {
            "student_id": student_id,
            "gpa": round(gpa, 2),
            "courses_counted": len(student_grades),
        }
    )


@app.route("/grades", methods=["POST"])
def create_grade():
    data = request.get_json()
    required_fields = ["student_id", "course_id", "grade", "semester"]

    if not data or any(field not in data for field in required_fields):
        return jsonify(
            {
                "error": "BAD_REQUEST",
                "message": "Missing required fields: student_id, course_id, grade, semester",
                "status": 400,
            }
        ), 400

    if data["grade"] not in GRADE_POINTS:
        return jsonify(
            {
                "error": "BAD_REQUEST",
                "message": f"Invalid grade '{data['grade']}'. Must be one of: {', '.join(GRADE_POINTS.keys())}",
                "status": 400,
            }
        ), 400

    new_grade = {
        "id": f"g{uuid.uuid4().hex[:6]}",
        "student_id": data["student_id"],
        "course_id": data["course_id"],
        "grade": data["grade"],
        "semester": data["semester"],
    }
    GRADES.append(new_grade)
    return jsonify(new_grade), 201


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5003))
    app.run(host="0.0.0.0", port=port, debug=True)
