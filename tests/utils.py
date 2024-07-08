from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest
from db import Base
from main import app
from models import Todos

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "sungat", "id": 1, "user_role": "admin", "user_id": 1}


client = TestClient(app)


@pytest.fixture()
def test_todo():
    todo = Todos(
        title="sun sun sun",
        description="way way way",
        priority=5,
        complete=False,
        owner_id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

