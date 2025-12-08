from __future__ import annotations

from datetime import datetime, timedelta
from typing import Iterable

from sqlalchemy.orm import Session

from app import models
from app.core.config import get_settings
from app.db import Base, SessionLocal, engine
from app.services.auth import ensure_role
from app.services.feature_flags import ensure_feature_flags
from app.utils import get_password_hash


def _get_user(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).one_or_none()


def seed_roles(db: Session) -> None:
    """Ensure all roles are present."""
    for role in models.UserRole:
        ensure_role(db, role)


def seed_users(db: Session) -> None:
    """Create baseline users for demos and manual testing."""
    users = [
        {"email": "admin@example.com", "password": "admin1234", "role": models.UserRole.admin},
        {"email": "teacher@example.com", "password": "teacher1234", "role": models.UserRole.teacher},
        {"email": "parent@example.com", "password": "parent1234", "role": models.UserRole.parent},
    ]

    for user in users:
        if _get_user(db, user["email"]):
            continue
        role = ensure_role(db, user["role"])
        db.add(
            models.User(
                email=user["email"],
                password_hash=get_password_hash(user["password"]),
                role=role,
            )
        )
    db.commit()


def _get_teacher(db: Session) -> models.User | None:
    return (
        db.query(models.User)
        .join(models.Role)
        .filter(models.Role.name == models.UserRole.teacher)
        .order_by(models.User.id)
        .first()
    )


def seed_students(db: Session) -> None:
    students = [
        {
            "name": "Иван Петров",
            "student_class": "5А",
            "parent_email": "parent@example.com",
            "parent_phone": "+7 999 111-22-33",
        },
        {
            "name": "Мария Смирнова",
            "student_class": "5А",
            "parent_email": "parent@example.com",
            "parent_phone": "+7 999 444-55-66",
        },
        {
            "name": "Даниил Кузнецов",
            "student_class": "6Б",
            "parent_email": "parent@example.com",
            "parent_phone": "+7 999 777-88-99",
        },
    ]

    for student in students:
        exists = (
            db.query(models.Student)
            .filter(
                models.Student.name == student["name"],
                models.Student.student_class == student["student_class"],
            )
            .one_or_none()
        )
        if exists:
            continue
        db.add(models.Student(**student, active=True))
    db.commit()


def seed_excursions(db: Session) -> None:
    teacher = _get_teacher(db)
    if not teacher:
        return

    excursions: Iterable[dict] = [
        {
            "student_class": "5А",
            "date": (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "location": "Планетарий",
            "price": 800,
            "description": "Осмотр экспозиций и мастер-класс по астрономии.",
        },
        {
            "student_class": "6Б",
            "date": (datetime.utcnow() + timedelta(days=14)).strftime("%Y-%m-%d"),
            "location": "Политехнический музей",
            "price": 1200,
            "description": "Интерактивная экскурсия по новым залам.",
        },
    ]

    for excursion in excursions:
        exists = (
            db.query(models.Excursion)
            .filter(
                models.Excursion.student_class == excursion["student_class"],
                models.Excursion.location == excursion["location"],
            )
            .one_or_none()
        )
        if exists:
            continue
        db.add(models.Excursion(**excursion, created_by=teacher.id))
    db.commit()


def seed_feature_flags(db: Session) -> None:
    settings = get_settings()
    ensure_feature_flags(db, settings.feature_flags)


def seed_all() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_roles(db)
        seed_users(db)
        seed_students(db)
        seed_excursions(db)
        seed_feature_flags(db)


if __name__ == "__main__":
    seed_all()
