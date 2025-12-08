import base64
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db
from app.services.pdf import render_pdf_template
from app.services.storage import save_pdf
from app.dependencies.auth import require_roles

router = APIRouter(prefix="/parent", tags=["parent"])


@router.get("/signatures/{excursion_id}/{student_id}", response_model=list[schemas.SignatureOut])
def list_signatures(
    excursion_id: int,
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        require_roles(models.UserRole.parent, models.UserRole.admin)
    ),
):
    return (
        db.query(models.Signature).filter_by(excursion_id=excursion_id, student_id=student_id).all()
    )


@router.post("/sign/{excursion_id}/{student_id}", response_model=schemas.SignatureOut)
def sign_excursion(
    excursion_id: int,
    student_id: int,
    payload: schemas.SignatureIn,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        require_roles(models.UserRole.parent, models.UserRole.admin)
    ),
):
    excursion = db.get(models.Excursion, excursion_id)
    student = db.get(models.Student, student_id)
    if not excursion or not student:
        raise HTTPException(status_code=404, detail="Excursion or student not found")
    signature_png = None
    metadata = payload.metadata_json or {}
    if payload.metadata_json and payload.metadata_json.get("signature_png_base64"):
        signature_png = base64.b64decode(payload.metadata_json["signature_png_base64"])
    pdf_bytes = render_pdf_template(student.name, excursion.__dict__, metadata, signature_png)
    pdf_path = save_pdf(
        pdf_bytes, excursion.student_class, excursion.location.replace(" ", "_"), student.id
    )
    signature = models.Signature(
        excursion_id=excursion.id,
        student_id=student.id,
        mode=payload.mode,
        strokes=payload.strokes,
        metadata_json=metadata,
        pdf_path=pdf_path,
    )
    db.add(signature)
    db.commit()
    db.refresh(signature)
    return signature
