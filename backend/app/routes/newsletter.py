from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db

router = APIRouter(prefix="/newsletter", tags=["newsletter"])


@router.post("", response_model=schemas.NewsletterOut, status_code=201)
def subscribe(payload: schemas.NewsletterCreate, db: Session = Depends(get_db)):
    existing = db.query(models.NewsletterSubscription).filter_by(email=payload.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Subscription already exists")

    subscription = models.NewsletterSubscription(email=payload.email, name=payload.name)
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription
