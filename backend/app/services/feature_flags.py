from typing import Dict, Iterable

from sqlalchemy.orm import Session

from app import models
from app.cache import invalidate_cache


def ensure_feature_flags(db: Session, defaults: Dict[str, bool]) -> None:
    existing_flags = {
        flag.name: flag for flag in db.query(models.FeatureFlag).all()
    }

    updated_or_new: list[models.FeatureFlag] = []
    for name, enabled in defaults.items():
        feature_flag = existing_flags.get(name)
        if feature_flag:
            feature_flag.enabled = enabled
            updated_or_new.append(feature_flag)
            continue
        new_flag = models.FeatureFlag(name=name, enabled=enabled)
        db.add(new_flag)
        updated_or_new.append(new_flag)

    if updated_or_new:
        db.commit()
        for flag in updated_or_new:
            db.refresh(flag)

    invalidate_cache(["feature_flags:all"])


def list_feature_flags(db: Session) -> Iterable[models.FeatureFlag]:
    return db.query(models.FeatureFlag).order_by(models.FeatureFlag.id).all()
