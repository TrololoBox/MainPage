from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db import Base, engine
from app.observability import setup_logging, setup_metrics, setup_tracing
from app.routes import admin, parent, teacher

Base.metadata.create_all(bind=engine)

settings = get_settings()
setup_logging(settings.log_level)
app = FastAPI(title="Excursion Consent API")
setup_metrics(app)
tracer_provider = setup_tracing(app, settings)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router)
app.include_router(teacher.router)
app.include_router(parent.router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("shutdown")
def shutdown_tracing() -> None:
    if tracer_provider:
        tracer_provider.shutdown()
