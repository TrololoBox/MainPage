"""Generate a static OpenAPI schema for sharing without running the server."""
from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.main import app


def main() -> None:
    schema = app.openapi()
    output_path = Path(__file__).resolve().parent.parent / "docs" / "openapi.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(schema, indent=2, ensure_ascii=False))
    print(f"OpenAPI schema written to {output_path}")


if __name__ == "__main__":
    main()
