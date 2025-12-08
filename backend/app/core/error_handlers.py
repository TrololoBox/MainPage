import logging
from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.errors import ErrorCode

logger = logging.getLogger(__name__)

STATUS_TO_ERROR_CODE: dict[int, ErrorCode] = {
    status.HTTP_400_BAD_REQUEST: ErrorCode.bad_request,
    status.HTTP_401_UNAUTHORIZED: ErrorCode.unauthorized,
    status.HTTP_403_FORBIDDEN: ErrorCode.forbidden,
    status.HTTP_404_NOT_FOUND: ErrorCode.not_found,
    status.HTTP_409_CONFLICT: ErrorCode.conflict,
    status.HTTP_422_UNPROCESSABLE_ENTITY: ErrorCode.validation_error,
}


def _error_response(
    *,
    code: ErrorCode,
    message: str,
    status_code: int,
    details: Any | None = None,
) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"code": code, "message": message, "details": details})


def _map_status_to_code(status_code: int) -> ErrorCode:
    if status_code in STATUS_TO_ERROR_CODE:
        return STATUS_TO_ERROR_CODE[status_code]

    if status_code >= 500:
        return ErrorCode.internal_error

    return ErrorCode.bad_request


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:  # noqa: ARG001
    message = exc.detail if isinstance(exc.detail, str) else str(exc.detail)
    error_code = _map_status_to_code(exc.status_code)
    return _error_response(code=error_code, message=message, status_code=exc.status_code)


async def validation_exception_handler(
    request: Request, exc: RequestValidationError  # noqa: ARG001
) -> JSONResponse:
    return _error_response(
        code=ErrorCode.validation_error,
        message="Validation error",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        details=exc.errors(),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:  # noqa: ARG001,B902
    logger.exception("Unhandled exception", exc_info=exc)
    return _error_response(
        code=ErrorCode.internal_error,
        message="Internal server error",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
