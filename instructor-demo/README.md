# Optional closing demo: create a test

Use the verified, fixed local Flight Lab, with its server running on port 5001.
Keep this folder empty of test code until the instructor creates the test live.

The parent repo already has pytest and Playwright. From the repo root:

```sh
uv sync --locked
uv run playwright install chromium
```

Copy the prompt from **slide 14**. Review the generated assertions against
AC-01, AC-02, and AC-08, then run:

```sh
uv run pytest instructor-demo/test_flight_search.py --base-url http://127.0.0.1:5001 --headed
```

Explain the distinction: browser exploration investigates new risks; a saved test
repeats explicit assertions. The existing `tests/e2e/test_flight_search.py` is a
prepared reference, not a newly generated test. Identify it as such if you show it.
Rehearse test creation in a copy; keep this folder ready for class.
