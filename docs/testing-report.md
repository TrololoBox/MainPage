# Testing and QA Notes (2025-12-19)

## Test execution
- `npm test` failed because `jest` binary is unavailable in the current environment. An `npm install` attempt to restore dependencies was blocked by 403 responses from the npm registry, so tests could not be executed locally. 【c69309†L1-L7】【0babf3†L1-L17】

## Existing automated coverage
- **ProstoKitHome smoke test:** Ensures the landing page renders the hero tagline and pricing header, but does not cover interactive flows (CTA clicks, toggles, filters). 【F:frontend/tests/ProstoKitHome.test.tsx†L1-L11】
- **NewsletterForm tests:** Cover a happy-path submission (mocked fetch) and basic validation that disables submit when the name is too short. Error handling and retry states are not exercised. 【F:frontend/tests/NewsletterForm.test.tsx†L1-L32】

## Linting and formatting configuration
- npm scripts provide `lint`, `lint:fix`, `lint:types`, `format`, and `format:check`, alongside `test` that invokes Jest with coverage. 【F:package.json†L6-L17】
- ESLint extends the JS and TypeScript recommended sets, plus React Hooks/Refresh plugins, and ignores `dist`, `node_modules`, `backend`, and `docs`. The configuration targets `*.ts`/`*.tsx` files only. 【F:eslint.config.js†L1-L28】
- Prettier runs over TS/TSX/CSS, `index.html`, and `vite.config.ts` via npm scripts; no custom Prettier config is present, and current code style (double quotes, semicolons, JSX wrapping) aligns with default Prettier output. 【F:package.json†L13-L14】【F:src/components/NewsletterForm.tsx†L1-L105】

## Suggested additional coverage
- **FeedbackForm smoke tests (Testing Library):**
  - Validate disabled state until name/email/message constraints are met and confirm the success banner after a mocked 200 response.
  - Cover server validation errors and network failures to assert the error text rendered from the API payload and fallback messaging. 【F:src/components/FeedbackForm.tsx†L11-L129】
- **NewsletterForm negative-path tests (Testing Library):**
  - Simulate a non-OK response to ensure API-provided errors appear, and a rejected fetch to surface the network failure copy. 【F:src/components/NewsletterForm.tsx†L11-L105】
- **Pricing toggle flows in ProstoKitHome (Testing Library):**
  - Toggle monthly/yearly pricing and assert the yearly price/annual total text updates, plus CTA tracking handlers are called with the right plan metadata. 【F:src/ProstoKitHome.tsx†L340-L370】【F:src/ProstoKitHome.tsx†L760-L819】【F:src/ProstoKitHome.tsx†L828-L848】
- **Feature-flag rendering smoke tests (Testing Library):**
  - When `newsletter_form` or `feedback_form` flags are false, corresponding cards should be hidden; when true, forms should mount and accept input. 【F:src/ProstoKitHome.tsx†L340-L366】【F:src/components/NewsletterForm.tsx†L11-L105】【F:src/components/FeedbackForm.tsx†L11-L129】
- **Screenshot/regression tests (Playwright/Vitest or Loki):**
  - Capture hero + navigation layout in light/dark themes (theme preference persisted via `prostoTheme` in localStorage) and pricing grid with yearly toggle enabled, to guard against style regressions in critical entry points. 【F:src/ProstoKitHome.tsx†L340-L370】【F:src/ProstoKitHome.tsx†L760-L848】
