# UI Testing with Codex

Find bugs, verify fixes, and automate UI tests with Codex using **Flight Search**,
a local app built with Flask.

## Run

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if needed:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
```

Start the app:

```sh
uv sync --locked
DEMO_TODAY=2030-01-15 uv run flask --app app run --debug --port 5001
```

Open **http://127.0.0.1:5001**. `DEMO_TODAY` fixes the date for reproducible
searches. Without it, the app uses the current UTC date. Stop the server with Ctrl-C.

The server returns HTTP 200 for valid searches and HTTP 422 for invalid ones.
These responses do not verify the rendered UI.

## Branches

- `main`: starting app and acceptance criteria, without tests.
- `final-result`: completed exercises with UI fixes and Playwright tests.

Switch branches with `git switch <branch>`, then run `uv sync --locked`.

## Browser tests

Install the locked development dependencies and Chromium:

```sh
uv sync --locked
uv run playwright install chromium
uv run pytest
```

The suite starts and stops its own Flask server on a free localhost port, with
`DEMO_TODAY=2030-01-15`. No separate server is needed. Each test has a fresh browser
context, an explicit CSS viewport, `en-US` locale, and UTC timezone.

To test an already-running app, start it using the command in **Run**, then use:

```sh
uv run pytest --base-url http://127.0.0.1:5001
uv run pytest tests/test_layout.py --headed
```

An external server must use the same demo date; the fixture checks its displayed
date before each test. On Linux CI, browser system libraries may also be needed:
`uv run playwright install --with-deps chromium`.

Failures retain screenshots and Playwright traces in the ignored `test-results/`
directory. Open a trace with `uv run playwright show-trace path/to/trace.zip`.
The [official pytest-Playwright reference](https://playwright.dev/python/docs/test-runners)
documents the runner options.

Coverage includes AC-01–09, required/native validation, invalid submissions and
correction, keyboard search/editing, schedule boundaries, empty results, and
phone/tablet/desktop layouts. Regression checks cover passenger loss on editing,
button overlap/alignment, dropdown-arrow inset, horizontal overflow, and clipped
date/passenger fields around 480/481 and 600/601 CSS pixels. Invalid query URLs
exercise values that native selects/date controls prevent entering normally.

### Scope and visual-review ambiguities

- The criteria do not specify an arrow inset. The suite preserves the reviewed
  **14px** custom-arrow inset as a design regression, not a new acceptance criterion.
- Native date text and calendar icons live inside browser controls. The readable-width
  check measures the fixed en-US date text plus a conservative **24px icon allowance**;
  it detects the confirmed 481px failure but is not a pixel-perfect visual oracle.
- Keep human checks for native date rendering, arrow appearance, focus-ring contrast,
  physical touch devices, and other browser engines/locales. The keyboard test avoids
  hardcoding platform-specific date-segment tab counts. This is a focused suite,
  not every combination of airports, dates, counts, and screen sizes.

[Acceptance criteria](docs/acceptance-criteria.md) · [Codex Site (slides)](https://codex-ui-testing-lab.vivianamarquez.chatgpt.site/)
