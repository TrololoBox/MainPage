from enum import Enum
from typing import Any

from pydantic import BaseModel


class ErrorCode(str, Enum):
    bad_request = "bad_request"
    unauthorized = "unauthorized"
    forbidden = "forbidden"
    not_found = "not_found"
    conflict = "conflict"
    validation_error = "validation_error"
    internal_error = "internal_error"


class ErrorResponse(BaseModel):
    code: ErrorCode
    message: str
    details: Any | None = None
