import importlib.util
import logging
from logging.config import dictConfig
from typing import Optional, TYPE_CHECKING

from fastapi import FastAPI

from app.core.config import Settings

if TYPE_CHECKING:
    from opentelemetry.sdk.trace import TracerProvider
else:
    TracerProvider = object


def _has_package(module_name: str) -> bool:
    try:
        return importlib.util.find_spec(module_name) is not None
    except ModuleNotFoundError:
        return False


class TraceContextFilter(logging.Filter):
    def __init__(self) -> None:
        super().__init__()
        self._trace = None
        if _has_package("opentelemetry") and _has_package("opentelemetry.trace"):
            from opentelemetry import trace as ot_trace

            self._trace = ot_trace

    def filter(self, record: logging.LogRecord) -> bool:  # noqa: D401
        if not self._trace:
            record.trace_id = ""
            record.span_id = ""
            record.trace_flags = 0
            return True

        span = self._trace.get_current_span()
        span_context = span.get_span_context()
        record.trace_id = f"{span_context.trace_id:032x}" if span_context.trace_id else ""
        record.span_id = f"{span_context.span_id:016x}" if span_context.span_id else ""
        record.trace_flags = int(span_context.trace_flags)
        return True


def setup_logging(log_level: str) -> None:
    level_name = log_level.upper()
    has_jsonlogger = _has_package("pythonjsonlogger")
    formatter_config: dict[str, object] = {
        "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s %(trace_id)s %(span_id)s %(trace_flags)s",
    }
    if has_jsonlogger:
        from pythonjsonlogger import jsonlogger

        formatter_config = {"()": jsonlogger.JsonFormatter, **formatter_config}
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": formatter_config
            },
            "filters": {"tracing": {"()": TraceContextFilter}},
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                    "filters": ["tracing"],
                    "level": level_name,
                }
            },
            "root": {"handlers": ["default"], "level": level_name},
            "loggers": {
                "uvicorn": {"handlers": ["default"], "level": level_name, "propagate": False},
                "uvicorn.access": {"handlers": ["default"], "level": level_name, "propagate": False},
            },
        }
    )
    if _has_package("opentelemetry.instrumentation.logging"):
        from opentelemetry.instrumentation.logging import LoggingInstrumentor

        LoggingInstrumentor().instrument(
            set_logging_format=False, log_level=getattr(logging, level_name, logging.INFO)
        )


def setup_metrics(app: FastAPI) -> None:
    if _has_package("prometheus_fastapi_instrumentator"):
        from prometheus_fastapi_instrumentator import Instrumentator

        Instrumentator().instrument(app).expose(app, include_in_schema=False)


def setup_tracing(app: FastAPI, settings: Settings) -> Optional[TracerProvider]:
    if not settings.enable_tracing:
        return None

    if not _has_package("opentelemetry"):
        return None

    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    resource = Resource.create({"service.name": settings.service_name})
    tracer_provider = TracerProvider(resource=resource)

    if settings.otlp_endpoint:
        otlp_exporter = OTLPSpanExporter(endpoint=settings.otlp_endpoint)
        tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

    trace.set_tracer_provider(tracer_provider)
    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)

    return tracer_provider
