from datetime import datetime
from pathlib import Path

from app.core.config import get_settings

settings = get_settings()


def excursion_pdf_path(student_class: str, excursion_name: str, student_id: int) -> Path:
    year = datetime.utcnow().year
    root = Path(settings.pdf_storage_root)
    return root / str(year) / student_class / excursion_name / f"{student_id}.pdf"


def ensure_folder(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def save_pdf(content: bytes, student_class: str, excursion_name: str, student_id: int) -> str:
    path = excursion_pdf_path(student_class, excursion_name, student_id)
    ensure_folder(path)
    path.write_bytes(content)
    return str(path)
