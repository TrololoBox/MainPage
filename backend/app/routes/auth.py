from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db
from app.services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.AuthResponse, status_code=201)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    user = auth_service.create_user(db, payload)
    tokens = auth_service.issue_tokens(db, user)
    return schemas.AuthResponse(**tokens.model_dump(), user=user)


@router.post("/login", response_model=schemas.AuthResponse)
def login(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, payload.email, payload.password)
    tokens = auth_service.issue_tokens(db, user)
    return schemas.AuthResponse(**tokens.model_dump(), user=user)


@router.post("/refresh", response_model=schemas.TokenPair)
def refresh(payload: schemas.RefreshRequest, db: Session = Depends(get_db)):
    return auth_service.refresh_tokens(db, payload.refresh_token)


@router.post("/logout")
def logout(payload: schemas.RefreshRequest, db: Session = Depends(get_db)):
    auth_service.revoke_token(db, payload.refresh_token)
    return {"detail": "Logged out"}
