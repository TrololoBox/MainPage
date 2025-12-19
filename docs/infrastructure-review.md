# Infrastructure and Build Review

## Docker Compose
- **Base compose (`docker-compose.yml`)**: uses `postgres:15-alpine`, backend build from `backend/Dockerfile`, frontend from `frontend/Dockerfile`. No healthchecks are defined for `db`, `backend`, or `frontend`, and `depends_on` does not gate on service health, which can cause the backend to start before PostgreSQL is ready. The frontend only depends on backend container start, not readiness. Persistent volumes are defined for database and backend data but there is no explicit environment for production secrets. 【F:docker-compose.yml†L1-L44】
- **Dev/stage overlays**: `docker-compose.dev.yml` and `docker-compose.stage.yml` only set `AUTO_SEED` and `RUN_MIGRATIONS` on the backend; they do not alter images, resources, or healthchecks. No overrides tighten security (e.g., non-root, read-only FS) or reduce image size. 【F:docker-compose.dev.yml†L1-L7】【F:docker-compose.stage.yml†L1-L7】

**Gaps / recommendations**
- Add `healthcheck` definitions for PostgreSQL (e.g., `pg_isready`), backend (HTTP `/health`), and frontend (HTTP `/`), and update `depends_on` to use `condition: service_healthy` to avoid race conditions.
- Consider using slimmer base images (e.g., `python:3.11-slim`/`alpine` for backend and an nginx-alpine or `caddy` static image for frontend) and ensure Dockerfiles use multi-stage builds to minimize final image size.
- Restrict environment exposure and add explicit restart policies per environment.

## Frontend build configuration
- **Vite config**: aliases `@` to `./src` but does not specify production-oriented options such as disabling dev sourcemaps, configuring `build.rollupOptions` for code splitting/manifest generation, or setting `define` flags for dead code elimination. 【F:vite.config.ts†L1-L12】
- **TypeScript config**: strict mode is enabled and path aliases map `@/*` to `src/*`, but there are no build-specific compiler options (e.g., `sourceMap` off in prod, incremental build cache). 【F:tsconfig.json†L1-L30】

**Gaps / recommendations**
- Configure `build` in `vite.config.ts` with explicit `target`, `sourcemap` disabled for production, and Rollup manual chunks if bundle splitting needs control. Consider enabling `manifest` for server-side rendering or asset hashing.
- Add separate `tsconfig.build.json` (or use `tsconfig.json` references) with production-friendly options and exclude test directories to streamline builds.

## CI/CD workflows
- **CI workflow (`.github/workflows/ci.yml`)**: runs backend tests (`pytest`), frontend lint (`npm run lint`), frontend tests (`npm test`), and a production build (`npm run build`) on push and pull requests. No backend linting or type checks are included here. 【F:.github/workflows/ci.yml†L1-L45】
- **Lint workflow (`.github/workflows/lint.yml`)**: separate jobs for backend (Ruff + Black) and frontend (ESLint + Prettier). It optionally pulls secrets from Vault/AWS to generate a `.env` for backend linting. No backend tests/builds are run in this workflow. 【F:.github/workflows/lint.yml†L1-L118】

**Gaps / recommendations**
- Add backend static typing (e.g., `mypy`) and security scans (e.g., `pip-audit`, `npm audit`) to CI or lint workflows.
- Ensure frontend type checking (`tsc --noEmit`) runs in CI to catch compile-time issues.
- Consider caching `pip`/`npm` in CI build job for speed (currently npm cache enabled; pip cache only in lint workflow). Include artifact uploads (coverage, build logs) if needed.
