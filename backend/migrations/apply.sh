#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DB_FILE=${DB_FILE:-"$SCRIPT_DIR/../data.db"}

if ! command -v sqlite3 >/dev/null 2>&1; then
  echo "sqlite3 is required to apply migrations" >&2
  exit 1
fi

echo "Applying migrations to $DB_FILE"
for migration in "$SCRIPT_DIR"/*_up.sql; do
  echo "- $(basename "$migration")"
  sqlite3 "$DB_FILE" < "$migration"
done
