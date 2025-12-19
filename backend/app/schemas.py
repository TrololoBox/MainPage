from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_serializer, field_validator
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

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "teacher@example.com",
                "password": "StrongPassw0rd!",
                "role": "teacher",
            }
        }
    )


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"email": "teacher@example.com", "password": "StrongPassw0rd!"}
        }
    )


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

    model_config = ConfigDict(
        json_schema_extra={"example": {"refresh_token": "<refresh_token_here>"}}
    )


class StudentCreate(BaseModel):
    name: str = Field(..., description="Full name of the student")
    student_class: str = Field(..., description="Class identifier, e.g. 5А")
    parent_email: Optional[EmailStr] = Field(
        default=None, description="Email to send reminders and signed PDFs"
    )
    parent_phone: Optional[str] = Field(
        default=None, description="Contact phone number for the parent"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Иван Иванов",
                "student_class": "5А",
                "parent_email": "parent@example.com",
                "parent_phone": "+7 999 123-45-67",
            }
        }
    )


class StudentOut(StudentCreate):
    id: int
    active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ExcursionCreate(BaseModel):
    student_class: str = Field(..., description="Target class for the excursion")
    date: str = Field(..., description="Excursion date in ISO format")
    location: str = Field(..., description="Destination name")
    price: Optional[int] = Field(
        default=None, description="Price per student in rubles (if applicable)"
    )
    description: Optional[str] = Field(
        default=None, description="Short details that will go into consent"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "student_class": "5А",
                "date": "2024-09-15",
                "location": "Третьяковская галерея",
                "price": 850,
                "description": "Экскурсия в рамках урока истории искусства",
            }
        }
    )


class ExcursionOut(ExcursionCreate):
    id: int
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class SignatureIn(BaseModel):
    mode: SignatureMode = Field(..., description="How the signature was captured")
    strokes: Optional[list] = Field(
        default=None, description="Raw signature strokes for draw mode"
    )
    metadata_json: Optional[dict] = Field(
        default=None, description="Additional metadata provided by the client"
    )
    pdf_path: Optional[str] = Field(
        default=None,
        description="Optional path for already generated PDF (usually generated server-side)",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "mode": "draw",
                "strokes": [[{"x": 10, "y": 12}, {"x": 11, "y": 15}]],
                "metadata_json": {
                    "user_agent": "Chrome",
                    "signature_png_base64": "<base64-image>",
                },
            }
        }
    )


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


class FeedbackCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    message: str = Field(..., min_length=10, max_length=1000)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Анна",
                "email": "anna@example.com",
                "message": "Очень понравилась экскурсия, спасибо за организацию!",
            }
        }
    )


class FeedbackOut(FeedbackCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class NewsletterCreate(BaseModel):
    email: EmailStr
    name: str | None = Field(default=None, min_length=2, max_length=100)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"email": "subscriber@example.com", "name": "Пётр"}
        }
    )


class NewsletterOut(NewsletterCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class FeatureFlagOut(BaseModel):
    name: str
    enabled: bool
    description: str | None = None

    class Config:
        from_attributes = True
