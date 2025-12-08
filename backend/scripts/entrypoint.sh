#!/bin/sh
set -euo pipefail

cd /app

if [ "${RUN_MIGRATIONS:-1}" = "1" ]; then
  echo "[entrypoint] Running migrations..."
  alembic upgrade head
fi

if [ "${AUTO_SEED:-0}" = "1" ]; then
  echo "[entrypoint] Seeding database..."
  python -m app.seeding
fi

echo "[entrypoint] Starting API server"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
