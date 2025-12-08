# Observability

## Structured logging
- Backend logs are emitted as JSON through `python-json-logger`.
- Trace context (`trace_id`, `span_id`, `trace_flags`) is injected automatically when OpenTelemetry tracing is enabled.
- Configure verbosity with `LOG_LEVEL` (defaults to `INFO`).
- Service identity for logs/traces is set with `SERVICE_NAME` (defaults to `excursion-consent-api`).

## Metrics (Prometheus)
- `/metrics` is exposed by the API via `prometheus-fastapi-instrumentator` with default Prometheus format.
- Common metrics: HTTP latency/throughput, in-flight requests, and exception counters.
- Scrape example:
  ```yaml
  - job_name: excursion-consent-api
    static_configs:
      - targets: ['api:8000']
  ```

## Tracing (OpenTelemetry)
- Tracing is enabled by default; disable with `ENABLE_TRACING=false`.
- OTLP HTTP exporter endpoint is configured with `OTEL_EXPORTER_OTLP_ENDPOINT` (e.g., `http://otel-collector:4318/v1/traces`).
- Spans carry the service name from `SERVICE_NAME` and propagate through FastAPI middleware.

## Dashboards
- **API overview**: request rate, error rate, p95/p99 latency, in-flight requests, and saturation (threads/CPU). Build from Prometheus metrics and filter by `service="excursion-consent-api"`.
- **Trace waterfall**: use your APM/trace UI (e.g., Grafana Tempo/Jaeger) to visualize `/parent`, `/teacher`, `/admin` routes with span attributes for status codes.

## Alerts
- **Availability**: trigger when `rate(http_requests_total{service="excursion-consent-api",status=~"5.."}[5m]) / rate(http_requests_total{service="excursion-consent-api"}[5m]) > 0.05` for 10m.
- **Latency**: alert if `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{service="excursion-consent-api"}[5m])) by (le)) > 1` for 5m.
- **Missing traces**: alert when `sum(rate(otel_span_context_total{service="excursion-consent-api"}[10m])) == 0` indicating exporter/back-end issues.
