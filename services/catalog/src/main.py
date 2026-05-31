"""CampusHub Catalog Service - Course catalog and department management."""

import os
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
COURSES = {
    "CS101": {
        "id": "CS101",
        "title": "Intro to Computer Science",
        "department": "Computer Science",
        "credits": 3,
        "instructor_id": "u002",
    },
    "MATH201": {
        "id": "MATH201",
        "title": "Linear Algebra",
        "department": "Mathematics",
        "credits": 4,
        "instructor_id": "u002",
    },
    "ENG102": {
        "id": "ENG102",
        "title": "Technical Writing",
        "department": "English",
        "credits": 3,
        "instructor_id": "u002",
    },
}


# --- Routes ---


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "catalog"})


@app.route("/courses", methods=["GET"])
def list_courses():
    department = request.args.get("department")
    courses = list(COURSES.values())
    if department:
        courses = [c for c in courses if c["department"] == department]
    return jsonify(courses)


@app.route("/courses/<course_id>", methods=["GET"])
def get_course(course_id):
    course = COURSES.get(course_id)
    if not course:
        return jsonify(
            {"error": "NOT_FOUND", "message": f"Course {course_id} not found", "status": 404}
        ), 404
    return jsonify(course)


@app.route("/departments", methods=["GET"])
def list_departments():
    departments = sorted({c["department"] for c in COURSES.values()})
    return jsonify(departments)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
