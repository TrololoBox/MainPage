from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.cache import (
    get_cached_response,
    invalidate_cache,
    set_cached_response,
)
from app.db import get_db
from app.dependencies.auth import require_roles

router = APIRouter(prefix="/teacher", tags=["teacher"])


@router.post("/excursions", response_model=schemas.ExcursionOut)
def create_excursion(
    payload: schemas.ExcursionCreate,
    db: Session = Depends(get_db),
    current_user_id: int | None = None,
):
    creator_id = current_user_id or 1
    excursion = models.Excursion(**payload.dict(), created_by=creator_id)
    db.add(excursion)
    db.commit()
    db.refresh(excursion)
    invalidate_cache(["teacher:excursions"])
    set_cached_response(
        f"teacher:excursions:{excursion.id}",
        schemas.ExcursionOut.model_validate(excursion, from_attributes=True).model_dump(),
    )
    return excursion


@router.get("/excursions", response_model=list[schemas.ExcursionOut])
def list_excursions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        require_roles(models.UserRole.teacher, models.UserRole.admin)
    ),
):
    cache_key = "teacher:excursions"
    cached = get_cached_response(cache_key, endpoint="teacher_excursions")
    if cached is not None:
        return cached

    excursions = (
        db.query(models.Excursion).order_by(models.Excursion.created_at.desc()).all()
    )
    serialized = [
        schemas.ExcursionOut.model_validate(excursion, from_attributes=True).model_dump()
        for excursion in excursions
    ]
    set_cached_response(cache_key, serialized)
    return serialized


@router.get("/excursions/{excursion_id}", response_model=schemas.ExcursionOut)
def get_excursion(
    excursion_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        require_roles(models.UserRole.teacher, models.UserRole.admin)
    ),
):
    cache_key = f"teacher:excursions:{excursion_id}"
    cached = get_cached_response(cache_key, endpoint="teacher_excursion_detail")
    if cached is not None:
        return cached

    excursion = db.get(models.Excursion, excursion_id)
    if not excursion:
        raise HTTPException(status_code=404, detail="Excursion not found")
    serialized = schemas.ExcursionOut.model_validate(
        excursion, from_attributes=True
    ).model_dump()
    set_cached_response(cache_key, serialized)
    return serialized
