import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.services.auth import ensure_default_roles

SQLALCHEMY_DATABASE_URL = "sqlite+pysqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    ensure_default_roles(session)
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_register_creates_user_and_tokens(client):
    response = client.post(
        "/auth/register",
        json={"email": "teacher@example.com", "password": "secret123", "role": "teacher"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["email"] == "teacher@example.com"
    assert data["user"]["role"] == "teacher"
    assert data["access_token"]
    assert data["refresh_token"]


def test_register_duplicate_email_returns_400(client):
    payload = {"email": "dup@example.com", "password": "secret123", "role": "teacher"}
    assert client.post("/auth/register", json=payload).status_code == 201
    duplicate = client.post("/auth/register", json=payload)
    assert duplicate.status_code == 400
    assert duplicate.json() == {
        "code": "bad_request",
        "message": "User with this email already exists",
        "details": None,
    }


def test_login_success_and_invalid_password(client):
    register_payload = {"email": "login@example.com", "password": "secret123", "role": "teacher"}
    client.post("/auth/register", json=register_payload)

    login_response = client.post(
        "/auth/login", json={"email": register_payload["email"], "password": "secret123"}
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

    bad_password = client.post(
        "/auth/login", json={"email": register_payload["email"], "password": "wrong"}
    )
    assert bad_password.status_code == 401
    assert bad_password.json() == {
        "code": "unauthorized",
        "message": "Incorrect email or password",
        "details": None,
    }


def test_refresh_rotates_token_and_rejects_revoked(client):
    register_payload = {"email": "refresh@example.com", "password": "secret123", "role": "teacher"}
    register_response = client.post("/auth/register", json=register_payload)
    refresh_token = register_response.json()["refresh_token"]

    first_refresh = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert first_refresh.status_code == 200
    new_refresh = first_refresh.json()["refresh_token"]
    assert new_refresh != refresh_token

    second_refresh = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert second_refresh.status_code == 401
    assert second_refresh.json() == {
        "code": "unauthorized",
        "message": "Invalid refresh token",
        "details": None,
    }

    rotated_refresh = client.post("/auth/refresh", json={"refresh_token": new_refresh})
    assert rotated_refresh.status_code == 200


def test_logout_revokes_refresh_token(client):
    payload = {"email": "logout@example.com", "password": "secret123", "role": "teacher"}
    register_response = client.post("/auth/register", json=payload)
    refresh_token = register_response.json()["refresh_token"]

    logout_response = client.post("/auth/logout", json={"refresh_token": refresh_token})
    assert logout_response.status_code == 200
    assert logout_response.json()["detail"] == "Logged out"

    refresh_after_logout = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_after_logout.status_code == 401
    assert refresh_after_logout.json() == {
        "code": "unauthorized",
        "message": "Invalid refresh token",
        "details": None,
    }
