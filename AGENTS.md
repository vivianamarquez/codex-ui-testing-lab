# Working in this repository

This project teaches UI testing with Codex and reusable Python Playwright tests.
The example app is a local flight search using deterministic synthetic data.

## Architecture and commands

- Flask setup: `airline_demo/__init__.py`; page routes: `routes.py`.
- Validation: `search.py`; synthetic schedule: `fixtures.py`.
- UI: Jinja templates, standard HTML forms, and plain CSS.
- Python 3.12, managed by uv. Setup: `uv sync --locked`, then
  `uv run playwright install chromium`.
- Run: `DEMO_TODAY=2030-01-15 uv run flask --app airline_demo run --port 5001`.
- All tests: `uv run pytest`.
- Baseline: `uv run pytest -m "not browser"`.
- Browser: `uv run pytest tests/e2e`; add `--headed` for a visible browser.
- Evidence: add `--tracing retain-on-failure --screenshot only-on-failure`.
- Browser tests start and stop a local server automatically. To use an existing
  fixed-date server, add `--base-url http://127.0.0.1:5001`.

## Testing workflow

Use `docs/acceptance-criteria.md` as the source of expected behavior. Start with
AC-01, AC-02, and AC-08. Follow `docs/learner-guide.md` and `docs/exercise-prompt.md`.

Use Computer Use in the built-in browser to observe the UI. See the
[official browser guide](https://learn.chatgpt.com/docs/browser#browser-use).
Keep browser observations, HTTP checks, and saved regression tests distinct.
Report passed, failed, blocked, and unattempted checks with supporting evidence.

During the testing exercise, change tests and reports only; application changes
require an explicit request. Preserve assertions that reflect the requirements.
Report issues with reproduction steps, expected and actual behavior, and evidence.
Identify ambiguous requirements before choosing a product rule.

Keep changes focused, Python-first, and local. Preserve unrelated work. Use the
shared effective date and deterministic fixtures. Prefer accessible roles and
labels, exact user-visible values, and Playwright's waiting assertions. Keep tests
independent of execution order. Distinguish a UI control preventing an invalid
choice from the server rejecting an invalid request.

The exercise creates `tests/e2e/test_flight_search.py`. Create it when the learner
asks to move from browser verification to writing the regression test.
