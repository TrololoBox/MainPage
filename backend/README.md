# Backend (FastAPI)

Быстрый скелет API для проекта «Цифровые согласия на экскурсию».

## Запуск (dev)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

- Все переменные окружения перечислены в `.env.example`.
- Конфигурация валидируется при загрузке: пустые значения и короткий `SECRET_KEY` вызывают ошибку.
- SQLite используется по умолчанию (`./data.db`), но `DATABASE_URL` можно заменить на PostgreSQL/MySQL.

## Короткая сводка API
- `POST /feedback` — принимает имя, email и сообщение, сохраняет заявку.
- `POST /newsletter` — подписка на рассылку по email (отдает 409 при повторе).
