# codex-airline-ui-testing
A local airline-search demo for practicing Codex browser verification and reusable Python Playwright tests.

The recurring task: **verify a flight-search journey against acceptance criteria
in a browser, then turn the verified interactions into a reusable Python regression
test.** A passing journey is a useful outcome; this exercise contains no planted bug.

Flight Lab is a small Flask application with Jinja templates, plain CSS, standard
HTML forms, and deterministic synthetic flights. There is no JavaScript, frontend
build step, database, authentication, external inventory, or paid service. The
journey ends at results: no bookings, payments, identity collection, or accounts.

## Setup

Prerequisites: Python **3.12**, a terminal, and internet access for the initial
package/browser download. Python 3.12 is a
[supported Python series](https://devguide.python.org/versions/); this checkout was
verified with **CPython 3.12.9 on macOS arm64**. Use a current 3.12 patch release for
a new installation. A browser runtime is installed separately from its Python package.

From the repository root, on macOS/Linux:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
```

On Windows PowerShell, replace the first two commands with
`py -3.12 -m venv .venv` and `.venv\Scripts\Activate.ps1`.
If activation is disabled, invoke `.venv\Scripts\python.exe` directly.
Linux hosts missing browser system libraries can use
`python -m playwright install --with-deps chromium` (system installation may need
administrator access).

`requirements.txt` pins direct and transitive dependencies from the verified
environment. `requirements.in` records the small set of intentional direct
dependencies. Install the pinned file for rehearsals; update pins deliberately
in a clean virtual environment and rerun the checks.

## Run locally

With the virtual environment activated:

```sh
DEMO_TODAY=2030-01-15 python -m flask --app airline_demo run --port 5000
```

Open [Flight Lab locally](http://127.0.0.1:5000). Stop it with Ctrl-C.
PowerShell: set `$env:DEMO_TODAY = "2030-01-15"` first, then run the Flask command.
If port 5000 is occupied, use `--port 5001` and that URL throughout the exercise.
This is Flask's local development server, not a production deployment.

Without `DEMO_TODAY`, the app uses the **UTC calendar date**, never the machine's
local timezone. The form defaults to departure +7 days and return +10 days.
The effective date appears below the form. A malformed `DEMO_TODAY` fails clearly
at startup; it does not silently fall back to the clock.

## Deterministic rehearsal examples

Keep `DEMO_TODAY=2030-01-15` set for these examples, even after 2030. Fixed mode
intentionally ignores the real clock. The tests use this same date.

| Example | Origin → destination | Departure | Return | Passengers | Expected |
| --- | --- | --- | --- | --- | --- |
| Main practice | Atlanta (ATL) → New York (JFK) | 2030-01-22 | 2030-01-25 | 2 | Two round-trip options |
| Empty results | New York (JFK) → San Francisco (SFO) | 2030-01-22 | 2030-01-25 | 2 | Explicit no-results state |

All distinct airport pairs except JFK–SFO in either direction have two options
when **both** dates fall within effective today through today +180 days, inclusive.
Dates beyond that window are valid searches with no results. All times are explicitly
UTC; each option has an outbound and reversed return leg on the requested dates.
Passenger count is preserved but does not change synthetic availability. There
are no prices or real seat inventory. See the
[complete product rules](docs/acceptance-criteria.md).

## Run tests

```sh
# Core validation, HTTP/template behavior, and deterministic schedule
python -m pytest -m "not browser"

# Browser infrastructure smoke test (automatic local server)
python -m pytest tests/e2e --browser chromium

# Everything currently in the starter
python -m pytest

# Watch the smoke test in a visible Chromium window
python -m pytest tests/e2e --browser chromium --headed

# Save evidence only when a browser test fails
python -m pytest tests/e2e --tracing retain-on-failure --screenshot only-on-failure

# Optionally retain evidence even for successful runs
python -m pytest tests/e2e --tracing on --screenshot on
```

Artifacts go under `test-results/` (ignored by Git). Open the actual trace path
from the output with `python -m playwright show-trace test-results/<test-folder>/trace.zip`.
The options are documented by the
[Python Playwright pytest plugin](https://playwright.dev/python/docs/test-runners).

The `base_url` fixture in `tests/conftest.py` creates a fixed-date app, listens on
an available loopback port, and stops the server after browser tests. No separate
server or arbitrary readiness sleep is needed. Each browser test gets a fresh
browser context from the plugin. Use the supplied `page` fixture so the plugin
can capture failure evidence.

To use an app you already started, run:

```sh
python -m pytest tests/e2e --base-url http://127.0.0.1:5000
```

You own starting/stopping that external server. For the future fixed-date journey
test, it **must** use `DEMO_TODAY=2030-01-15`. Unit/HTTP tests always use their
own isolated fixed-date app, regardless of this URL or your shell's date setting.

## Begin practicing

1. Read [the acceptance criteria](docs/acceptance-criteria.md) and
   [learner guide](docs/learner-guide.md).
2. Start fixed-date mode and manually try the main example once.
3. Start a separate Codex practice session in this repository and paste
   [the exercise prompt](docs/exercise-prompt.md).
4. Review browser observations, the generated test, and its actual execution.
   Use [the blank results template](docs/results-template.md); repeat an important
   interaction yourself before accepting the work.

**Prepared:** application, deterministic fixtures, server tests, browser runtime
setup, browser smoke test, and learning materials.
**Your exercise:** browser verification of AC-01/02/08 and creation of
`tests/e2e/test_flight_search.py`, which does not exist in the starter.
Browser exploration does not automatically produce a saved regression test.

The implementation was separately checked while building the starter; see
[implementation verification](docs/implementation-verification.md). That is not
a prefilled learner report or a substitute for your practice session.

## Where to look

| Path | Responsibility |
| --- | --- |
| `airline_demo/__init__.py` | Flask setup and effective date |
| `airline_demo/search.py` | Typed search values and validation |
| `airline_demo/fixtures.py` | Deterministic round-trip schedule |
| `airline_demo/routes.py` | Read query parameters and render pages |
| `airline_demo/templates/`, `static/` | Accessible HTML and responsive CSS |
| `tests/` | Python baseline tests and browser infrastructure |
| `docs/`, `AGENTS.md` | Expected behavior, exercise, and Codex instructions |
