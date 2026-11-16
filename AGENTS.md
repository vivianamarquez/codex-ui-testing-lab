# UI testing with Codex

This repo is a local teaching app with three intentional regressions. The main
workflow is browser inspection, an annotation-led fix, a broader investigation,
focused fixes, and verification. Preserve the seeded starting state when preparing
class; rehearse fixes in a separate copy. During a live exercise, fix only issues
the instructor has authorized.

- App: `app.py`; UI: `templates/` and `static/`.
- Setup: `uv sync --locked`.
- Run: `DEMO_TODAY=2030-01-15 uv run flask --app app run --debug --port 5001`.
- Browser runtime for saved tests: `uv run playwright install chromium`.
- Tests: `uv run pytest`; use `--headed` to watch the saved browser test.
- `hosted-demo/dist/` contains published slides and a separate reference app.
- `instructor-demo/` is optional test creation; keep it free of a finished test
  until the instructor asks for one.

Read `docs/acceptance-criteria.md`. Use the built-in browser for UI verification.
In a browser investigation, observe the UI before inspecting implementation;
do not read instructor spoilers or rehearsal artifacts to predict findings.
Report passed, failed, blocked, and unattempted checks with exact observed values,
viewport dimensions, and screenshots. Distinguish browser observations from HTTP
checks and saved test results. The six-scenario prompt is in the slides and
`docs/browser-prompt.md`.

Keep changes focused. Preserve unrelated work. Never change acceptance criteria,
remove assertions, or hide overflow to make a failing check appear to pass.
Use accessible labels/roles, waiting assertions, deterministic data, and independent
tests. Keep app changes local unless publishing or pushing is explicitly requested.

See `README.md` for the workflow. `docs/instructor-walkthrough.md` contains spoilers
and preparation notes; read it only for instructor preparation, not discovery.
