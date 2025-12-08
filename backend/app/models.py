import enum
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import relationship

from app.db import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    teacher = "teacher"
    parent = "parent"


class SignatureMode(str, enum.Enum):
    vector = "vector"
    pdf = "pdf"


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum(UserRole), unique=True, nullable=False)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    role = relationship("Role", back_populates="users")
    refresh_tokens = relationship(
        "RefreshToken", back_populates="user", cascade="all, delete-orphan"
    )


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    student_class = Column(String, nullable=False)
    parent_email = Column(String, nullable=True)
    parent_phone = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Excursion(Base):
    __tablename__ = "excursions"

    id = Column(Integer, primary_key=True, index=True)
    student_class = Column(String, nullable=False)
    date = Column(String, nullable=False)
    location = Column(String, nullable=False)
    price = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    creator = relationship("User")


class Signature(Base):
    __tablename__ = "signatures"

    id = Column(Integer, primary_key=True)
    excursion_id = Column(Integer, ForeignKey("excursions.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    mode = Column(Enum(SignatureMode), nullable=False)
    strokes = Column(JSON, nullable=True)
    pdf_path = Column(String, nullable=True)
    metadata_json = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    excursion = relationship("Excursion")
    student = relationship("Student")


class Reminder(Base):
    __tablename__ = "reminders"

    log_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    excursion_id = Column(Integer, ForeignKey("excursions.id"), nullable=False)
    type = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    result = Column(String, nullable=True)

    student = relationship("Student")
    excursion = relationship("Excursion")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="refresh_tokens")
