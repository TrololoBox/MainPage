from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.db import get_db
from app.services.feature_flags import list_feature_flags

router = APIRouter(prefix="/feature-flags", tags=["feature-flags"])


@router.get("", response_model=list[schemas.FeatureFlagOut])
def get_feature_flags(db: Session = Depends(get_db)):
    return list_feature_flags(db)
