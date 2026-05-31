"""CampusHub Portal Service - Student-facing aggregator portal."""

import os
from pathlib import Path

from flask import Flask, jsonify, send_file
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

# --- Downstream service URLs ---
AUTH_URL = os.environ.get("AUTH_URL", "http://localhost:5000")
CATALOG_URL = os.environ.get("CATALOG_URL", "http://localhost:5001")
ENROLLMENT_URL = os.environ.get("ENROLLMENT_URL", "http://localhost:5002")
GRADES_URL = os.environ.get("GRADES_URL", "http://localhost:5003")


# --- Routes ---


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "portal"})


@app.route("/dashboard/<student_id>", methods=["GET"])
def get_dashboard(student_id):
    return jsonify({
        "student_id": student_id,
        "name": "Alice Student",
        "enrolled_courses": [
            {"course_id": "CS101", "title": "Intro to Computer Science"},
            {"course_id": "MATH201", "title": "Linear Algebra"},
        ],
        "notifications_count": 2,
        "current_gpa": 3.65,
    })


@app.route("/transcript/<student_id>", methods=["GET"])
def get_transcript(student_id):
    return jsonify({
        "student_id": student_id,
        "name": "Alice Student",
        "courses": [
            {
                "course_id": "CS101",
                "title": "Intro to Computer Science",
                "grade": "A",
                "credits": 3,
                "semester": "Fall 2026",
            },
            {
                "course_id": "MATH201",
                "title": "Linear Algebra",
                "grade": "B+",
                "credits": 4,
                "semester": "Fall 2026",
            },
        ],
        "cumulative_gpa": 3.65,
        "total_credits": 7,
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
