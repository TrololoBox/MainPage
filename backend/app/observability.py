import logging
from logging.config import dictConfig
from typing import Optional

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import get_current_span
from prometheus_fastapi_instrumentator import Instrumentator
from pythonjsonlogger import jsonlogger

from app.core.config import Settings


class TraceContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:  # noqa: D401
        span = get_current_span()
        span_context = span.get_span_context()
        record.trace_id = f"{span_context.trace_id:032x}" if span_context.trace_id else ""
        record.span_id = f"{span_context.span_id:016x}" if span_context.span_id else ""
        record.trace_flags = int(span_context.trace_flags)
        return True


def setup_logging(log_level: str) -> None:
    level_name = log_level.upper()
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": jsonlogger.JsonFormatter,
                    "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s %(trace_id)s %(span_id)s %(trace_flags)s",
                }
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
    LoggingInstrumentor().instrument(set_logging_format=False, log_level=getattr(logging, level_name, logging.INFO))


def setup_metrics(app: FastAPI) -> None:
    Instrumentator().instrument(app).expose(app, include_in_schema=False)


def setup_tracing(app: FastAPI, settings: Settings) -> Optional[TracerProvider]:
    if not settings.enable_tracing:
        return None

    resource = Resource.create({"service.name": settings.service_name})
    tracer_provider = TracerProvider(resource=resource)

    if settings.otlp_endpoint:
        otlp_exporter = OTLPSpanExporter(endpoint=settings.otlp_endpoint)
        tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

    trace.set_tracer_provider(tracer_provider)
    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)

    return tracer_provider
