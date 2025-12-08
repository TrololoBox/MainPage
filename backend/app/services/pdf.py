from io import BytesIO
from typing import Optional

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


def render_pdf_template(student_name: str, excursion: dict, parent_fields: dict, signature_png: Optional[bytes]) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica", 12)
    c.drawString(2 * cm, height - 2 * cm, "Согласие на экскурсию")
    c.setFont("Helvetica", 10)
    c.drawString(2 * cm, height - 3 * cm, f"Ученик: {student_name}")
    c.drawString(2 * cm, height - 4 * cm, f"Класс: {excursion.get('student_class')}")
    c.drawString(2 * cm, height - 5 * cm, f"Дата: {excursion.get('date')} | Место: {excursion.get('location')}")
    c.drawString(2 * cm, height - 6 * cm, f"Стоимость: {excursion.get('price') or '0'}")
    c.drawString(2 * cm, height - 7 * cm, f"Родитель: {parent_fields.get('parent_name', '—')} | Телефон: {parent_fields.get('parent_phone', '—')}")
    c.drawString(2 * cm, height - 8 * cm, f"Примечание: {parent_fields.get('note', '')}")
    c.rect(2 * cm, height - 12 * cm, 10 * cm, 3 * cm)
    c.drawString(2 * cm, height - 9 * cm, "Подпись родителя:")
    if signature_png:
        # Place inside rectangle
        c.drawImage(BytesIO(signature_png), 2.1 * cm, height - 11.9 * cm, width=9.8 * cm, height=2.8 * cm, preserveAspectRatio=True, mask='auto')
    c.showPage()
    c.save()
    return buffer.getvalue()
