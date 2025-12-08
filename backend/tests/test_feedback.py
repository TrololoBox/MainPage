from fastapi.testclient import TestClient

from app import models
from app.db import SessionLocal
from app.main import app


def setup_function():
    with SessionLocal() as db:
        db.query(models.Feedback).delete()
        db.commit()


def test_submit_feedback_creates_record_and_returns_payload():
    client = TestClient(app)
    payload = {
        "name": "Мария",
        "email": "maria@example.com",
        "message": "Хочу понять, как автоматизировать экспорт отчётов в PDF.",
    }

    response = client.post("/feedback", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert payload["message"] in data["message"]
    assert "created_at" in data

    with SessionLocal() as db:
        saved = db.get(models.Feedback, data["id"])
        assert saved is not None
        assert saved.message == payload["message"]


def test_submit_feedback_validates_message_length():
    client = TestClient(app)
    payload = {"name": "Иван", "email": "ivan@example.com", "message": "Коротко"}

    response = client.post("/feedback", json=payload)

    assert response.status_code == 422
    error = response.json()
    assert error["code"] == "validation_error"
    assert error["message"] == "Validation error"
    assert error["details"][0]["loc"][-1] == "message"
