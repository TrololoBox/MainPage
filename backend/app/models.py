import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import relationship

from app.db import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    teacher = "teacher"


class SignatureMode(str, enum.Enum):
    vector = "vector"
    pdf = "pdf"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


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
