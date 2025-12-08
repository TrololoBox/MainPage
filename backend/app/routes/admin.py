import io
import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db
from app.utils import get_password_hash
from app.services import auth as auth_service

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/users", response_model=schemas.UserOut)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    role = auth_service.ensure_role(db, payload.role)
    user = models.User(
        email=payload.email, password_hash=get_password_hash(payload.password), role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/students/import", response_model=list[schemas.StudentOut])
def import_students(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_roles(models.UserRole.admin)),
):
    try:
        content = file.file.read()
        df = (
            pd.read_excel(io.BytesIO(content))
            if file.filename.endswith(".xlsx")
            else pd.read_csv(io.BytesIO(content))
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка чтения файла: {e}")
    students = []
    for _, row in df.iterrows():
        student = models.Student(
            name=row.get("name") or row.get("Имя"),
            student_class=str(row.get("class") or row.get("Класс")),
            parent_email=row.get("parent_email") or row.get("Email родителя"),
            parent_phone=row.get("parent_phone") or row.get("Номер телефона родителя"),
            active=True,
        )
        db.add(student)
        students.append(student)
    db.commit()
    for st in students:
        db.refresh(st)
    return students
