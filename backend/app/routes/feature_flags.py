from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.cache import get_cached_response, set_cached_response
from app.db import get_db
from app.services.feature_flags import list_feature_flags

router = APIRouter(prefix="/feature-flags", tags=["feature-flags"])


@router.get("", response_model=list[schemas.FeatureFlagOut])
def get_feature_flags(db: Session = Depends(get_db)):
    cache_key = "feature_flags:all"
    cached = get_cached_response(cache_key, endpoint="feature_flags")
    if cached is not None:
        return cached

    flags = list_feature_flags(db)
    serialized = [
        schemas.FeatureFlagOut.model_validate(flag, from_attributes=True).model_dump()
        for flag in flags
    ]
    set_cached_response(cache_key, serialized)
    return serialized
