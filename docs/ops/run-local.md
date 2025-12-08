# Локальный запуск через Docker Compose

Ниже приведены команды для сборки образов и запуска сервисов (PostgreSQL, backend и frontend) локально.

## Предварительные требования
- Docker и Docker Compose установлены локально.
- Порты `5432`, `8000` и `4173` свободны.

## Сборка образов
```bash
docker compose build
```

## Запуск сервисов
```bash
docker compose up
```
Это запустит:
- PostgreSQL на `localhost:5432` с БД `excursion` и учетными данными `excursion/excursion`.
- Backend FastAPI на `http://localhost:8000` с переменной `DATABASE_URL`, указывающей на PostgreSQL.
- Frontend, собранный Vite и обслуживаемый Nginx, на `http://localhost:4173`.

## Остановка сервисов
```bash
docker compose down
```
Добавьте флаг `-v`, чтобы удалить именованные тома (`db-data`, `backend-data`), если нужно очистить данные.
