from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_serializer, field_validator
from app.models import Role, SignatureMode, UserRole


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPair(Token):
    refresh_token: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True

    @field_validator("role", mode="before")
    def parse_role(cls, value: UserRole | Role):
        if isinstance(value, Role):
            return value.name
        return value

    @field_serializer("role")
    def serialize_role(self, value: UserRole | Role):
        if isinstance(value, Role):
            return value.name
        return value


class AuthResponse(TokenPair):
    user: "UserOut" = Field(..., description="Authenticated user")


class RefreshRequest(BaseModel):
    refresh_token: str


class StudentCreate(BaseModel):
    name: str
    student_class: str
    parent_email: Optional[EmailStr] = None
    parent_phone: Optional[str] = None


class StudentOut(StudentCreate):
    id: int
    active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ExcursionCreate(BaseModel):
    student_class: str
    date: str
    location: str
    price: Optional[int] = None
    description: Optional[str] = None


class ExcursionOut(ExcursionCreate):
    id: int
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class SignatureIn(BaseModel):
    mode: SignatureMode
    strokes: Optional[list] = None
    metadata_json: Optional[dict] = None
    pdf_path: Optional[str] = None


class SignatureOut(SignatureIn):
    id: int
    excursion_id: int
    student_id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class ReminderOut(BaseModel):
    log_id: int
    student_id: int
    excursion_id: int
    type: str
    timestamp: datetime
    result: str | None

    class Config:
        from_attributes = True
