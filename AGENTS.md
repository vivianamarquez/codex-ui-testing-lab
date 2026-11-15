# UI testing with Codex

Use this small flight-search app to practice testing against acceptance criteria.

- App: `app.py`; UI: `templates/` and `static/`.
- Setup: `uv sync --locked`.
- Run: `DEMO_TODAY=2030-01-15 uv run flask --app app run --port 5001`.
- Browser runtime: `uv run playwright install chromium`.
- All tests: `uv run pytest`.
- Browser journey: `uv run pytest tests/e2e/test_flight_search.py`.
- Add `--headed` to watch, or `--tracing retain-on-failure --screenshot only-on-failure`
  to retain failure evidence. Tests start and stop their own app server.

Read `docs/acceptance-criteria.md`; focus on AC-01, AC-02, and AC-08.
Use the built-in browser for browser verification. Report passed, failed, blocked,
and unattempted checks with exact observed values and supporting screenshots.
Distinguish browser observations from HTTP checks and saved test results.

Keep changes focused and Python-first. During verification, leave application
code unchanged unless asked to modify it. Preserve unrelated work. Report ambiguous
requirements and genuine issues with reproduction steps. Keep assertions aligned
with the criteria, fixtures deterministic, and tests independent of execution order.
Use accessible labels/roles and waiting assertions. Keep all work local unless
publishing or pushing is explicitly requested.

See README.md for the exercise, browser explanation, and how to expand coverage.
