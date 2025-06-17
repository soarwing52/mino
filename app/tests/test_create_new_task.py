import pytest
from fastapi.testclient import TestClient

from app.main import app  # 你的FastAPI app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_create_new_task(client):
    # 準備上傳的文件
    files = {
        "file": ("test.txt", b"Hello, world!", "text/plain"),
    }
    data = {
        "title": "Test Task",
        "description": "This is a test task.",
    }

    response = client.post("/api/v1/tasks/", files=files, data=data)
    assert response.status_code == 200

    response_json = response.json()
    assert "id" in response_json
    assert response_json["title"] == "Test Task"
    assert response_json["description"] == "This is a test task."
    assert "file_key" in response_json
