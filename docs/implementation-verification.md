# Verification record

Verified on November 15, 2026, using Python 3.12.9, uv 0.13.8, and Chromium on macOS.

## Automated checks

- `uv sync --locked`: environment installed from `uv.lock`.
- `uv run playwright install chromium`: browser runtime ready.
- `uv run pytest`: **51 passed** — 50 validation, server, and schedule cases,
  plus the browser smoke test.
- Fresh installation: copied the project into a temporary folder, ran
  `uv sync --locked`, then `uv run pytest`: **51 passed**.

The baseline covers validation boundaries, recoverable errors, search parameter
preservation, fixed-date behavior, and synthetic schedules for all supported routes.

## Browser review

The app was reviewed with `DEMO_TODAY=2030-01-15`:

- SFO → LAX, February 3–6, 2030, 7 passengers: results showed the submitted
  values and two round-trip options.
- Edit search preserved both airports, both dates, and 7 passengers.
- SFO → SFO produced a destination error and retained valid inputs.
- JFK → SFO showed “No flights found,” the search summary, and the edit action.
- Tab navigation showed a visible focus outline; Enter activated Search flights.
- Desktop and 390px mobile views were inspected for search, results, validation,
  and empty states.

Local screenshots are under `artifacts/implementation/`. These generated files
are ignored by Git. Capture new test evidence with:

```sh
uv run pytest tests/e2e --tracing on --screenshot on
```

## Coverage

Checks cover Chromium on macOS and narrow browser layouts. Additional browsers,
physical mobile devices, and screen-reader behavior are follow-up checks.

The practice exercise adds a saved browser test for the full search-and-edit journey.
