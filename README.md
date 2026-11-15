# UI testing with Codex

Practice using Codex to test a UI against acceptance criteria, then turn the
verified interactions into a reusable Python regression test.

The example is Flight Lab, a local flight-search app built with Flask, Jinja,
and plain CSS. A traveler configures a round trip, checks the results, and edits
the search. The app uses synthetic flight data so each practice run is repeatable.

## The Codex feature

This workflow uses **Computer Use in the browser**. Codex can open the app,
click controls, enter values, inspect the rendered page, and take screenshots.
See [OpenAI's browser guide](https://learn.chatgpt.com/docs/browser#browser-use).

Use the built-in browser in the desktop app, or refer to it with `@Browser` in
your prompt. Codex also reads the repository and runs commands to write and
execute the Python test. Browser observations and the saved test are two outputs
you review separately.

## Setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if needed:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
```

From the repository folder:

```sh
uv sync --locked
uv run playwright install chromium
```

uv manages Python 3.12 and the project's environment. Dependencies are listed
in `pyproject.toml`; `uv.lock` records their versions.

## Start the app

```sh
DEMO_TODAY=2030-01-15 uv run flask --app airline_demo run --port 5001
```

Open [Flight Lab](http://127.0.0.1:5001). Stop the server with Ctrl-C.

`DEMO_TODAY` sets the app's date to January 15, 2030, so the examples below stay
valid whenever you practice. The form displays this date below the search controls.
Omitting the setting uses today's UTC date.

## Try a search

| Example | Origin → destination | Departure | Return | Passengers | Expected |
| --- | --- | --- | --- | --- | --- |
| Main journey | Atlanta (ATL) → New York (JFK) | 2030-01-22 | 2030-01-25 | 2 | Two round-trip options |
| Empty results | New York (JFK) → San Francisco (SFO) | 2030-01-22 | 2030-01-25 | 2 | “No flights found” |

Submit the main search, compare all five values in the summary, then select
**Edit search** and check that the form preserves them.

Synthetic flights cover the app's effective date through 180 days later.
JFK–SFO has an empty schedule in both directions. All flight times are UTC.
See [acceptance criteria](docs/acceptance-criteria.md) for the product rules.

## Run tests

```sh
# All tests
uv run pytest

# Validation and server tests
uv run pytest -m "not browser"

# Browser smoke test
uv run pytest tests/e2e

# Watch the browser test
uv run pytest tests/e2e --headed

# Keep screenshots and traces when a browser test fails
uv run pytest tests/e2e --tracing retain-on-failure --screenshot only-on-failure
```

Browser tests start and stop their own app server with the fixed demo date.
To test the app you already started:

```sh
uv run pytest tests/e2e --base-url http://127.0.0.1:5001
```

Screenshots and traces are saved under `test-results/`. Use `--tracing on` and
`--screenshot on` to keep evidence from a successful run too. Open a trace with:

```sh
uv run playwright show-trace test-results/<test-folder>/trace.zip
```

Replace `<test-folder>` with the folder created by your run. See the
[Playwright pytest guide](https://playwright.dev/python/docs/test-runners)
for more test options.

## Practice the workflow

1. Read the [learner guide](docs/learner-guide.md) and manually try the main journey.
2. Use the [exercise prompt](docs/exercise-prompt.md) to ask Codex to verify the UI.
3. Review its observations with the [results template](docs/results-template.md).
4. Ask Codex to create and run `tests/e2e/test_flight_search.py` for AC-01, AC-02,
   and AC-08. Review the assertions and repeat the edit interaction yourself.

The repository includes validation tests, server tests, and a browser smoke test.
You create the full search-and-edit browser test during the exercise.

## Repository map

| Path | Purpose |
| --- | --- |
| `airline_demo/__init__.py` | Flask setup and effective date |
| `airline_demo/search.py` | Search values and validation |
| `airline_demo/fixtures.py` | Synthetic flight schedule |
| `airline_demo/routes.py` | Form submissions and page rendering |
| `airline_demo/templates/`, `airline_demo/static/` | HTML and CSS |
| `tests/` | Baseline tests and browser setup |
| `docs/` | Acceptance criteria, practice guide, and verification record |
| `AGENTS.md` | Instructions for Codex |
