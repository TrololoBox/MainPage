import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session, sessionmaker

sys.path.append(str(Path(__file__).resolve().parents[2]))

from app import models
from app.db import Base, get_db
from app.main import app
from app.utils import create_access_token

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


def create_user(db: Session, email: str, role: models.UserRole) -> models.User:
    user = models.User(email=email, password_hash="hashed", role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def auth_headers(user: models.User) -> dict[str, str]:
    token = create_access_token(str(user.id))
    return {"Authorization": f"Bearer {token}"}


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


@pytest.fixture(autouse=True)
def stub_password_hash(monkeypatch):
    monkeypatch.setattr("app.utils.get_password_hash", lambda password: "hashed")
    monkeypatch.setattr("app.routes.admin.get_password_hash", lambda password: "hashed")


def test_admin_can_create_user(setup_db: Session):
    admin = create_user(setup_db, "admin@example.com", models.UserRole.admin)
    client = TestClient(app)

    response = client.post(
        "/admin/users",
        json={"email": "teacher@example.com", "password": "secret", "role": "teacher"},
        headers=auth_headers(admin),
    )

    assert response.status_code == 200
    assert response.json()["email"] == "teacher@example.com"


def test_teacher_cannot_create_user(setup_db: Session):
    teacher = create_user(setup_db, "teacher@example.com", models.UserRole.teacher)
    client = TestClient(app)

    response = client.post(
        "/admin/users",
        json={"email": "new@example.com", "password": "secret", "role": "parent"},
        headers=auth_headers(teacher),
    )

    assert response.status_code == 403


def test_teacher_can_create_excursion(setup_db: Session):
    teacher = create_user(setup_db, "creator@example.com", models.UserRole.teacher)
    client = TestClient(app)

    response = client.post(
        "/teacher/excursions",
        json={
            "student_class": "5A",
            "date": "2024-09-01",
            "location": "Museum",
            "price": 1000,
            "description": "History tour",
        },
        headers=auth_headers(teacher),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["created_by"] == teacher.id


def test_parent_cannot_create_excursion(setup_db: Session):
    parent = create_user(setup_db, "parent@example.com", models.UserRole.parent)
    client = TestClient(app)

    response = client.post(
        "/teacher/excursions",
        json={
            "student_class": "5A",
            "date": "2024-09-01",
            "location": "Park",
        },
        headers=auth_headers(parent),
    )

    assert response.status_code == 403


def test_parent_can_sign_and_teacher_cannot(setup_db: Session):
    teacher = create_user(setup_db, "teacher@example.com", models.UserRole.teacher)
    excursion = models.Excursion(
        student_class="5A", date="2024-10-01", location="Zoo", created_by=teacher.id
    )
    student = models.Student(name="Ivan", student_class="5A", parent_email="parent@mail.com")
    setup_db.add_all([excursion, student])
    setup_db.commit()
    setup_db.refresh(excursion)
    setup_db.refresh(student)

    parent = create_user(setup_db, "parent@example.com", models.UserRole.parent)
    client = TestClient(app)

    sign_payload = {
        "mode": "pdf",
        "metadata_json": {"signature_png_base64": ""},
        "pdf_path": None,
        "strokes": None,
    }

    parent_response = client.post(
        f"/parent/sign/{excursion.id}/{student.id}",
        json=sign_payload,
        headers=auth_headers(parent),
    )
    assert parent_response.status_code == 200

    teacher_response = client.post(
        f"/parent/sign/{excursion.id}/{student.id}",
        json=sign_payload,
        headers=auth_headers(teacher),
    )
    assert teacher_response.status_code == 403
