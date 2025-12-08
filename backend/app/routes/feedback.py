from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("", response_model=schemas.FeedbackOut, status_code=201)
def submit_feedback(payload: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    feedback = models.Feedback(**payload.dict())
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback
