import pytest
from fastapi.testclient import TestClient
from src.main import api, todos  # import the list too

client = TestClient(api)


@pytest.fixture(autouse=True)
def reset_todos():
    """Clear the todos list before each test to avoid shared state."""
    todos.clear()
    yield
    todos.clear()


# Test home endpoint
def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Hello World"}


# Test POST
def test_create_todo():
    response = client.post("/todo", json={
        "id": 1,
        "name": "Study",
        "des": "Prepare for exams"
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Study"


# Test GET all (now seeds its own data first)
def test_get_todos():
    client.post("/todo", json={"id": 1, "name": "Study", "des": "Prepare for exams"})

    response = client.get("/todo")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


# Test PUT (seeds its own data first)
def test_update_todo():
    client.post("/todo", json={"id": 1, "name": "Study", "des": "Prepare for exams"})

    response = client.put("/todo/1", json={
        "id": 1,
        "name": "Study Updated",
        "des": "Prepare for math exams"
    })
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Study Updated"


# Test DELETE (seeds its own data first)
def test_delete_todo():
    client.post("/todo", json={
        "id": 1,
        "name": "Study Updated",
        "des": "Prepare for math exams"
    })

    response = client.delete("/todo/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Study Updated",
        "des": "Prepare for math exams"
    }