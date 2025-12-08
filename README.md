
# ProstoKit — React + CSS (без Tailwind)

Это чистый проект на Vite + React + TypeScript **без Tailwind**.
UI-компоненты со стилями на обычном CSS. Можно отдавать разработчику и наращивать как обычно.

## Запуск
```bash
npm install
npm run dev
```
Открой `http://localhost:5173`.

### Backend (FastAPI)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

- Все конфиги перечислены в `backend/.env.example` и валидируются при запуске.
- В CI/CD секреты можно забирать из HashiCorp Vault или AWS Secrets Manager (см. workflow в `.github/workflows/ci.yml`).

## Где править
- Главная: `src/ProstoKitHome.tsx` (контент и логика).
- Глобальные стили: `src/styles/index.css` (переменные, сетка, компоненты).
- UI: `src/components/ui/*` — простые реализованные компоненты.

## Что внутри
- Нормальная сетка/типографика/кнопки/инпуты/карточки/диалоги на CSS.
- Никаких утилит-классов. Ничего не пропадёт, как на скриншоте.

Если захочешь позже перейти на shadcn/ui или любой другой UI-kit —
можно заменить файлы в `src/components/ui/*` на свои реализации, импорты уже унифицированы.
