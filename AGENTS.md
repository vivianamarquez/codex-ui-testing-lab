# UI Testing with Codex

- App: `app.py`; UI: `templates/` and `static/`.
- Setup: `uv sync --locked`.
- Run: `DEMO_TODAY=2030-01-15 uv run flask --app app run --debug --port 5001`.

Use `docs/acceptance-criteria.md` for expected behavior. Keep changes focused and
preserve unrelated work. Do not weaken criteria or assertions to make checks pass.
Use accessible labels, waiting assertions, deterministic data, and independent tests.
Keep changes local unless publishing or pushing is requested.
