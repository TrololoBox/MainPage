# Dependency Management Policy

This repository uses pinned dependency versions and lock files for reproducible installs on both the backend and frontend.

## Backend (Python)
- Package manager: **pip** using `backend/requirements.txt` for declared runtime dependencies.
- Lock file: `backend/requirements.lock` contains the exact pinned versions to deploy.
- Install command for production: `python -m pip install -r backend/requirements.lock`.
- When adding or upgrading dependencies, update `backend/requirements.txt` and regenerate the lock file before committing.

## Frontend (Node.js)
- Package manager: **npm** with strict (non-range) versions in `package.json` and the generated `package-lock.json` committed.
- Run `npm install` to restore dependencies from the lock file.
- Security: run `npm run audit` (uses `npm audit`) to check for vulnerabilities before releases.
- When changing dependencies, keep versions exact and refresh the lock file with `npm install --package-lock-only` if ranges change.
