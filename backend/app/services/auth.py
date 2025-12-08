from datetime import datetime, timedelta
from secrets import token_urlsafe

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.core.config import get_settings
from app.utils import create_access_token, get_password_hash, verify_password

settings = get_settings()


def ensure_role(db: Session, role_name: models.UserRole) -> models.Role:
    role = db.query(models.Role).filter(models.Role.name == role_name).one_or_none()
    if not role:
        role = models.Role(name=role_name)
        db.add(role)
        db.commit()
        db.refresh(role)
    return role


def create_user(db: Session, payload: schemas.UserCreate) -> models.User:
    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="User with this email already exists")
    role = ensure_role(db, payload.role)
    user = models.User(
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> models.User:
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return user


def _create_refresh_token(user: models.User) -> models.RefreshToken:
    expires_at = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    return models.RefreshToken(
        token=token_urlsafe(48),
        user=user,
        expires_at=expires_at,
    )


def issue_tokens(db: Session, user: models.User) -> schemas.TokenPair:
    access_token = create_access_token(str(user.id))
    refresh_token = _create_refresh_token(user)
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)
    return schemas.TokenPair(access_token=access_token, refresh_token=refresh_token.token)


def refresh_tokens(db: Session, token: str) -> schemas.TokenPair:
    stored = db.query(models.RefreshToken).filter(models.RefreshToken.token == token).first()
    if not stored or stored.revoked:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    if stored.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token expired")

    stored.revoked = True
    token_pair = issue_tokens(db, stored.user)
    db.commit()
    return token_pair


def revoke_token(db: Session, token: str) -> None:
    stored = db.query(models.RefreshToken).filter(models.RefreshToken.token == token).first()
    if not stored:
        raise HTTPException(status_code=404, detail="Refresh token not found")
    stored.revoked = True
    db.commit()


def ensure_default_roles(db: Session) -> None:
    for role in models.UserRole:
        ensure_role(db, role)
