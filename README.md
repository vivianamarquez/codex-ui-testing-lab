# UI testing with Codex

A local flight-search app for practicing **inspect → annotate → investigate → fix → verify**.
Use Codex in the desktop app with this folder open. The same workflow applies to
UIs written in other languages.

## Run

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if needed:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
```

Then start the app:

```sh
uv sync --locked
DEMO_TODAY=2030-01-15 uv run flask --app app run --debug --port 5001
```

Open **http://127.0.0.1:5001** in Codex’s built-in browser. The date is fixed so
class inputs stay reproducible. Stop the server with Ctrl-C.

## The workshop

Open the [slides and copyable prompts](https://ui-testing-codex-lab.vivianamarquez.chatgpt.site/slides).
Start the live demo on **slide 5** with the local app already running.

1. Inspect the page and annotate a visible layout problem.
2. Ask Codex for one focused fix; inspect the diff and browser result.
3. Run the six-scenario browser investigation from slide 7.
4. Reproduce the findings yourself, then ask Codex to fix the confirmed issues.
5. Repeat the checks and review the evidence before accepting the changes.

This teaching version includes **three intentional regressions**. It is supposed
to fail some checks at the start. The [acceptance criteria](docs/acceptance-criteria.md)
describe correct behavior; do not weaken them to make the demo pass.
The [instructor walkthrough](docs/instructor-walkthrough.md) contains spoilers,
recording cues, and the expected failures.

## What to review

Codex can click, type, inspect rendered state, and capture screenshots. An
annotation ties your feedback to a specific element. Acceptance criteria define
correctness; compare the report with the actual page and inspect the code diff.
See [Browser use and annotations](https://learn.chatgpt.com/docs/browser?surface=app#browser-use).

## Tests

```sh
uv run playwright install chromium
uv run pytest
```

The existing browser test starts its own local server. Use `--headed` to watch,
or `--tracing retain-on-failure --screenshot only-on-failure` for failure evidence.
The seeded passenger bug should fail the edit-parameter server test and the
search-and-edit browser test. The other tests should pass. Layout issues also
need browser review; the current test suite is not a visual audit.

The optional closing exercise creates a new Python Playwright test in
[instructor-demo](instructor-demo/README.md). That folder intentionally has no
finished test.

## Files

- `app.py` — routes, validation, and synthetic flight data.
- `templates/` and `static/` — the UI; no frontend build step.
- `docs/acceptance-criteria.md` — expected behavior.
- `tests/` — existing checks to run before and after a fix.
- `hosted-demo/` — published slides and the earlier hosted reference app.

The live fix exercise uses localhost. Editing this checkout does not change the
public reference app. Keep app changes local for review.
