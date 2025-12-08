#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DB_FILE=${DB_FILE:-"$SCRIPT_DIR/../data.db"}

if ! command -v sqlite3 >/dev/null 2>&1; then
  echo "sqlite3 is required to rollback migrations" >&2
  exit 1
fi

echo "Rolling back migrations on $DB_FILE"
for migration in $(ls "$SCRIPT_DIR"/*_down.sql | sort -r); do
  echo "- $(basename "$migration")"
  sqlite3 "$DB_FILE" < "$migration"
done
