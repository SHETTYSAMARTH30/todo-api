from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_todo():
    response = client.post("/todos", json={"title": "Buy milk", "done": False})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["done"] is False
    assert "id" in data


def test_list_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_todo():
    create = client.post("/todos", json={"title": "Read book", "done": False})
    todo_id = create.json()["id"]

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Read book"


def test_update_todo():
    create = client.post("/todos", json={"title": "Walk dog", "done": False})
    todo_id = create.json()["id"]

    response = client.put(f"/todos/{todo_id}", json={"title": "Walk dog", "done": True})
    assert response.status_code == 200
    assert response.json()["done"] is True


def test_delete_todo():
    create = client.post("/todos", json={"title": "Clean house", "done": False})
    todo_id = create.json()["id"]

    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 204

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404


def test_get_nonexistent_todo():
    response = client.get("/todos/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"
