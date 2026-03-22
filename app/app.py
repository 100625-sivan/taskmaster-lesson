"""
TaskMaster API - A simple task management service.

This is a minimal Flask API used for teaching CI/CD concepts.
It manages a list of tasks (in-memory) and exposes REST endpoints.
"""

import os
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Configuration from environment (set by Docker / CI / Terraform)
# ---------------------------------------------------------------------------
APP_VERSION = os.environ.get("APP_VERSION", "0.0.1-local")
BUILD_SHA = os.environ.get("BUILD_SHA", "unknown")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")

# ---------------------------------------------------------------------------
# In-memory task store (resets on restart - that's fine for teaching)
# ---------------------------------------------------------------------------
_tasks = [
    {"id": 1, "title": "Learn GitHub Actions", "done": False},
    {"id": 2, "title": "Write a Dockerfile", "done": True},
    {"id": 3, "title": "Deploy to EC2", "done": False},
]
_next_id = 4


# ===========================================================================
#  Routes
# ===========================================================================

@app.route("/")
def home():
    """Main UI - Kanban board."""
    return render_template("index.html",
        version=APP_VERSION, environment=ENVIRONMENT,
        build_sha=BUILD_SHA, tasks=_tasks)


@app.route("/health")
def health():
    """Health check endpoint - used by Docker HEALTHCHECK and CD workflows."""
    return jsonify({
        "status": "healthy",
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
    })


@app.route("/api/tasks", methods=["GET"])
def list_tasks():
    """Return all tasks."""
    return jsonify({"tasks": _tasks, "count": len(_tasks)})


@app.route("/api/tasks", methods=["POST"])
def create_task():
    """Create a new task. Expects JSON: {"title": "..."}"""
    global _next_id
    data = request.get_json(silent=True)

    if not data or "title" not in data:
        return jsonify({"error": "Missing 'title' field"}), 400

    task = {
        "id": _next_id,
        "title": data["title"],
        "done": False,
    }
    _next_id += 1
    _tasks.append(task)
    return jsonify(task), 201


@app.route("/greeting")
def greeting():
    """A friendly greeting - added to test the CI/CD pipeline."""
    return jsonify({"message": "Hello from TaskMaster!", "version": APP_VERSION})


@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """Get a single task by ID."""
    task = next((t for t in _tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": f"Task {task_id} not found"}), 404
    return jsonify(task)


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task by ID."""
    task = next((t for t in _tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": f"Task {task_id} not found"}), 404
    _tasks.remove(task)
    return jsonify({"message": f"Task {task_id} deleted"})


# ===========================================================================
#  Entry point (for local development without gunicorn)
# ===========================================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
