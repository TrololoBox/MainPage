from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db import Base, engine
from app.routes import admin, teacher, parent

Base.metadata.create_all(bind=engine)

settings = get_settings()
app = FastAPI(title="Excursion Consent API")

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
