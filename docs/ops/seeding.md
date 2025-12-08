# Сидирование данных

Скрипты начального наполнения создают роли, базовые аккаунты и примеры сущностей (ученики и экскурсии) для демонстрации. Логика собрана в модуле `app.seeding` и может запускаться вручную или автоматически при старте контейнера.

## Что создаётся
- роли `admin`, `teacher`, `parent`;
- пользователи: `admin@example.com` (`admin1234`), `teacher@example.com` (`teacher1234`), `parent@example.com` (`parent1234`);
- несколько учеников с классами `5А` и `6Б`;
- две ближайшие экскурсии, привязанные к учителю.

## Ручной запуск
1. Перейдите в директорию `backend` и установите зависимости (`pip install -r requirements.txt`).
2. Подготовьте переменные окружения (можно скопировать `.env.example`).
3. Примените миграции: `alembic upgrade head`.
4. Выполните сидирование:

```bash
AUTO_SEED=1 python -m app.seeding
```

Переменная `AUTO_SEED` не обязательна для ручного запуска, но полезна для единообразия с контейнерным окружением.

## Автоматический seed для Docker
Контейнер backend запускается через скрипт `scripts/entrypoint.sh`, который умеет применять миграции и сидировать данные при установке флага `AUTO_SEED=1`.

### dev
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

### stage
```bash
docker compose -f docker-compose.yml -f docker-compose.stage.yml up --build
```

Оба override-файла включают переменную `AUTO_SEED=1` и `RUN_MIGRATIONS=1`, поэтому при старте контейнера будут выполнены миграции и сидирование.

## Переменные окружения
- `RUN_MIGRATIONS` — применять ли Alembic-миграции перед стартом (по умолчанию `1`).
- `AUTO_SEED` — выполнять ли `python -m app.seeding` перед стартом (по умолчанию `0`, включено в `dev`/`stage`).
