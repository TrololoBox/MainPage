# Backend Security & Quality Review

## Configuration & Secrets
- `.env.example` uses placeholder secrets and a short default `SECRET_KEY`; defaults are present but not secure for production. No hardcoded real secrets were found in the repo. The example also enables migrations by default (`RUN_MIGRATIONS=1`).
- `Settings` is defined as a `dataclass` with Pydantic validators, but dataclasses do not execute these validators, so constraints like minimum `SECRET_KEY` length and non-empty `DATABASE_URL` are never enforced at runtime. Defaults such as `secret_key="change-me"` and open `FEATURE_FLAGS` parsing therefore bypass validation.

## Application Hardening
- CORS is fully open (`*` origins, all methods/headers) with credentials allowed, which is risky outside controlled environments.
- Error handling centralizes FastAPI `HTTPException` and validation errors but lacks structured logging of request context; unhandled exceptions are logged generically.
- SQL access goes through SQLAlchemy ORM; no raw SQL strings were found in routers/services, reducing SQL injection risk.

## Database Schema & Migrations
- The project ships shell/SQL migrations for SQLite only; Alembic is configured but has no version scripts. Manual SQL migrations create `roles`, `users`, and `sessions` tables that differ from current ORM models (`RefreshToken`, `FeatureFlag`, `NewsletterSubscription`, etc.), so applying migrations will not align the database with the code.
- `Base.metadata.create_all` runs on startup, which can mask migration drift by auto-creating missing tables without version control.

## Testing
- Backend tests exist for auth, error handling, feedback, and health endpoints, but running the suite currently fails before collection because `pytest-cov` dependencies cannot be installed in the constrained environment.
- Coverage for critical paths is limited to auth flows and simple endpoints; there are no tests for admin/teacher/parent routes or for database migrations.

## Recommendations
- Convert `Settings` to inherit from `BaseSettings` (or remove Pydantic validators) so validation actually runs; enforce strong defaults and length checks for `SECRET_KEY` and other fields.
- Restrict CORS in non-dev environments and avoid `allow_credentials=True` with wildcard origins.
- Align database migrations with ORM models using Alembic; remove auto-creation on startup and ensure up/down migrations cover all tables.
- Add tests for role-protected routes, database migrations, and error scenarios; consider running tests in CI with required plugins available.
