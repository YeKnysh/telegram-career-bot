import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


def make_mock_task(task_id=1):
    return {
        "id": task_id,
        "title": "Test Task",
        "description": "Test description",
        "status": "pending",
        "assigned_to": "@testuser",
        "created_at": "2026-01-01T10:00:00",
    }


@patch("app.main.get_db_connection")
def test_root(mock_db):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@patch("app.main.get_db_connection")
def test_get_tasks(mock_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [make_mock_task()]

    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@patch("app.main.get_db_connection")
def test_create_task(mock_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.lastrowid = 1
    mock_cursor.fetchone.return_value = make_mock_task()

    payload = {"title": "New Task", "status": "pending"}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201


@patch("app.main.get_db_connection")
def test_get_task_not_found(mock_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    response = client.get("/tasks/999")
    assert response.status_code == 404


@patch("app.main.get_db_connection")
def test_delete_task(mock_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1

    response = client.delete("/tasks/1")
    assert response.status_code == 204
