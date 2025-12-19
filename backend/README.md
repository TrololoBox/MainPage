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

## Документация API

- В dev-окружении Swagger UI доступен по адресу `/docs`.
- Статический OpenAPI-файл можно сгенерировать командой:

```bash
ENVIRONMENT=dev PYTHONPATH=backend python backend/scripts/generate_openapi.py
```

Схема сохраняется в `backend/docs/openapi.json` и содержит примеры payload'ов.
