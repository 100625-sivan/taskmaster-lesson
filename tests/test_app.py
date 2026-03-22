"""
Tests for the TaskMaster API.
"""

import json


class TestHealthEndpoint:
    """The /health endpoint is used by Docker HEALTHCHECK and CD workflows."""

    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_healthy_status(self, client):
        data = json.loads(response.data) if (response := client.get("/health")) else {}
        assert data["status"] == "healthy"

    def test_health_includes_version(self, client):
        data = json.loads(client.get("/health").data)
        assert "version" in data


class TestHomeEndpoint:
    """The / endpoint serves the Kanban board UI."""

    def test_home_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_home_returns_html(self, client):
        response = client.get("/")
        assert b"TaskMaster" in response.data


class TestGreetingEndpoint:
    """The /greeting endpoint - added to test CI/CD pipeline."""

    def test_greeting_returns_200(self, client):
        response = client.get("/greeting")
        assert response.status_code == 200

    def test_greeting_has_message(self, client):
        data = json.loads(client.get("/greeting").data)
        assert "message" in data


class TestTasksAPI:
    """CRUD operations on /api/tasks."""

    def test_list_tasks_returns_200(self, client):
        response = client.get("/api/tasks")
        assert response.status_code == 200

    def test_list_tasks_returns_array(self, client):
        data = json.loads(client.get("/api/tasks").data)
        assert isinstance(data["tasks"], list)
        assert data["count"] == len(data["tasks"])

    def test_list_tasks_has_preloaded_data(self, client):
        data = json.loads(client.get("/api/tasks").data)
        assert data["count"] >= 3  # We start with 3 tasks

    def test_create_task(self, client):
        response = client.post(
            "/api/tasks",
            data=json.dumps({"title": "New test task"}),
            content_type="application/json",
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["title"] == "New test task"
        assert data["done"] is False

    def test_create_task_missing_title(self, client):
        response = client.post(
            "/api/tasks",
            data=json.dumps({"description": "no title here"}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_create_task_empty_body(self, client):
        response = client.post("/api/tasks", content_type="application/json")
        assert response.status_code == 400

    def test_get_task_by_id(self, client):
        response = client.get("/api/tasks/1")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["id"] == 1

    def test_get_task_not_found(self, client):
        response = client.get("/api/tasks/9999")
        assert response.status_code == 404

    def test_delete_task(self, client):
        response = client.delete("/api/tasks/1")
        assert response.status_code == 200
        # Verify it's gone
        response = client.get("/api/tasks/1")
        assert response.status_code == 404

    def test_delete_task_not_found(self, client):
        response = client.delete("/api/tasks/9999")
        assert response.status_code == 404
