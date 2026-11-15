# Working in this repository

This is a local, synthetic airline-search demo for learning browser verification
and reusable **Python** Playwright tests. The journey stops at search results.
No real airline branding, purchases, accounts, external APIs, or deliberate bugs.

## Architecture and commands

- Flask factory: `airline_demo/__init__.py`; GET routes: `routes.py`.
- Pure validation: `search.py`; deterministic schedule: `fixtures.py`.
- Jinja templates and plain CSS. Standard HTML controls; no JavaScript needed.
- Python 3.12; install: `python3.12 -m venv .venv`, then
  `.venv/bin/python -m pip install -r requirements.txt` and
  `.venv/bin/python -m playwright install chromium`.
- Run: `DEMO_TODAY=2030-01-15 .venv/bin/python -m flask --app airline_demo run --port 5000`.
- Baseline: `.venv/bin/python -m pytest -m "not browser"`.
- Browser: `.venv/bin/python -m pytest tests/e2e --browser chromium`.
- Visible browser: append `--headed`.
- Evidence: append `--tracing retain-on-failure --screenshot only-on-failure`.
- The browser fixture starts/stops a local server automatically. To use an
  existing fixed-date server, append `--base-url http://127.0.0.1:5000`.

## Exercise rules

Read `docs/acceptance-criteria.md` as the source of expected behavior. Begin with
AC-01, AC-02, AC-08. See `docs/exercise-prompt.md` and `docs/learner-guide.md`.
Keep changes focused and Python-first; avoid new infrastructure or dependencies
unless necessary. Preserve unrelated work. Do not publish or push unrequested.

During the testing exercise, leave application code unchanged unless explicitly
asked to modify it. Never weaken an assertion to make it pass. Report genuine
issues with inputs, reproduction steps, expected/actual behavior, and evidence.
Identify requirement ambiguities instead of inventing a rule.

Observe rendered behavior before claiming browser verification. Source inspection,
HTTP tests, browser exploration, and executable browser tests are distinct evidence.
Report **passed, failed, and blocked** checks separately; state checks not attempted
and limitations. Do not treat a control preventing an invalid choice as evidence
that the server rejects a forged request. Never fabricate an exercise report.

Keep fixtures deterministic and use the shared effective date. Prefer accessible
roles/labels, Playwright's waiting assertions, and exact user-visible submitted
values. Avoid CSS paths, arbitrary sleeps, order dependence, and assertions that
only check a page contains generic text. The starter intentionally contains only
a browser smoke test; the learner creates `tests/e2e/test_flight_search.py` later.
