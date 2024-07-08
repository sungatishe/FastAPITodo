from starlette import status
from routers.auth import get_current_user
from routers.todos import get_db
from tests.utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_auth(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    print(response.json())
    assert response.json() == [
        {"complete": False, "title": "sun sun sun", "description": "way way way", "priority": 5, "id": test_todo.id,
         "owner_id": test_todo.owner_id}
    ]


def test_read_one_todo(test_todo):
    response = client.get(f"/todos/{test_todo.id}")
    print(response)
    assert response.status_code == status.HTTP_200_OK


def test_create_todo(test_todo):
    request_data = {
        'title': 'New todo',
        'description': 'todotodotodotodotodo',
        'priority': 5,
        'complete': False
    }

    response = client.post('/todo/', json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.complete == request_data.get("complete")


def test_update_todo(test_todo):
    request_data = {
        'title': 'NEW New todo',
        'description': 'NEW todotodotodotodotodo',
        'priority': 4,
        'complete': True
    }

    response = client.put("/todo/1", json=request_data)
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == 'NEW New todo'


def test_not_found_updated_todo(test_todo):
    request_data = {
        'title': 'NEW New todo',
        'description': 'NEW todotodotodotodotodo',
        'priority': 4,
        'complete': True
    }

    response = client.put("/todo/999", json=request_data)
    assert response.status_code == 404


def test_delete_todo(test_todo):
    response = client.delete('/todo/delete/1')
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None
