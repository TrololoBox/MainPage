# Backend (FastAPI)

Быстрый скелет API для проекта «Цифровые согласия на экскурсию».

## Запуск (dev)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Переменные окружения см. в `.env.example`. SQLite используется по умолчанию (`./data.db`).
