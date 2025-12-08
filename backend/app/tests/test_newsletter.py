import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session, sessionmaker

sys.path.append(str(Path(__file__).resolve().parents[2]))

from app import models  # noqa: E402
from app.db import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield db
    app.dependency_overrides.clear()
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_subscribe_newsletter_success(setup_db: Session):
    client = TestClient(app)
    response = client.post("/newsletter", json={"email": "user@example.com", "name": "Мария"})

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "user@example.com"
    assert body["name"] == "Мария"
    assert "id" in body


def test_subscribe_newsletter_duplicate_email_returns_conflict(setup_db: Session):
    client = TestClient(app)
    first = client.post("/newsletter", json={"email": "user@example.com", "name": "Мария"})
    assert first.status_code == 201

    second = client.post("/newsletter", json={"email": "user@example.com"})

    assert second.status_code == 409
    assert second.json() == {
        "code": "conflict",
        "message": "Subscription already exists",
        "details": None,
    }


def test_subscribe_newsletter_invalid_email(setup_db: Session):
    client = TestClient(app)
    response = client.post("/newsletter", json={"email": "invalid", "name": "M"})

    assert response.status_code == 422
    body = response.json()
    assert body["code"] == "validation_error"
    assert body["message"] == "Validation error"
    assert isinstance(body.get("details"), list)
