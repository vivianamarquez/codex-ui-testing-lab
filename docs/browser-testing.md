# Browser testing

The suite starts and stops its own Flask server with `DEMO_TODAY=2030-01-15`.
Each test uses a fresh browser context, an explicit CSS viewport, `en-US` locale,
and UTC timezone.

## Run options

Watch tests in a visible browser:

```sh
uv run pytest --headed
```

Run only the layout checks:

```sh
uv run pytest tests/test_layout.py
```

To use an already-running app, start it with the README’s **Run** command, then use:

```sh
uv run pytest --base-url http://127.0.0.1:5001
```

The external app must use `DEMO_TODAY=2030-01-15`; the tests verify its displayed date.
On Linux CI, install browser system dependencies if needed:

```sh
uv run playwright install --with-deps chromium
```

## Debug failures

Screenshots and Playwright traces are saved in the ignored `test-results/` folder.
Open a trace with:

```sh
uv run playwright show-trace path/to/trace.zip
```

See the [pytest-Playwright reference](https://playwright.dev/python/docs/test-runners)
for other options.

## Coverage

- AC-01–09: search results, validation, error correction, schedule boundaries,
  empty results, and editing.
- Keyboard search/editing and phone, tablet, and desktop layouts.
- Regression checks for lost passenger counts, button alignment, dropdown-arrow
  spacing, horizontal overflow, and clipped fields near 480/481 and 600/601 CSS pixels.

Invalid query URLs exercise values that native controls prevent entering normally.

## Limitations and human review

- The **14px** dropdown-arrow inset preserves the reviewed design; it is not an
  acceptance criterion.
- Date readability checks measure en-US text plus a **24px icon allowance**.
  This detects the confirmed clipping issue but does not replace visual review.
- Review native date rendering, arrow appearance, focus-ring contrast, physical
  touch devices, and other browser engines/locales manually.
- The suite samples important scenarios; it does not cover every input and viewport
  combination. Keyboard checks avoid platform-specific date-segment tab counts.
