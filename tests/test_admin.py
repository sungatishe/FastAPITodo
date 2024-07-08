from tests.utils import *
from routers.admin import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all_auth(test_todo):
    response = client.get("/admin/todo")
    print(f"SSSSsa{response.json()}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'description': 'way way way',
                                'title': 'sun sun sun',
                                'priority': 5,
                                'owner_id': 1,
                                'id': 1,
                                'complete': False}]


def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == 200

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None
