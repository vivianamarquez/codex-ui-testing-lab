# Starter implementation verification

Performed on **2026-11-15** while building the starter. This is an implementation
check record, **not** the learner's exercise report. `results-template.md` remains
blank, and `tests/e2e/test_flight_search.py` has intentionally not been created.

## Passed

- **50 baseline cases**: validation (including missing/malformed input, same-day
  travel, today, and passenger boundaries), server rejection/recovery, populated
  edit forms, results rendering, escaped untrusted values, UTC/fixed clock behavior,
  all 12 directed routes, and the inclusive synthetic schedule boundaries.
  Command: `.venv/bin/python -m pytest -m "not browser"`.
- **51 total tests passed** with Chromium and the automatic fixed-date server:
  `.venv/bin/python -m pytest --tracing on --screenshot on`.
  The additional browser test is only the homepage smoke test.
- **Headed smoke passed**, using the running application's configurable URL:
  `.venv/bin/python -m pytest tests/e2e --headed --base-url http://127.0.0.1:5000 --tracing retain-on-failure --screenshot only-on-failure --output artifacts/headed-smoke`.
- **Clean environment installation passed**: created a second temporary Python
  3.12 virtual environment, installed only `requirements.txt`, ran `pip check`,
  and ran the full suite: **51 passed**. The already-installed Chromium runtime
  was reused. The temporary virtual environment was removed afterward.
- `python -m pip check`: no broken requirements. `git diff --check`: clean.

## Browser implementation review

Used the local app with `DEMO_TODAY=2030-01-15`. Observed the rendered interface
through browser interaction, separately from the saved smoke test:

- Selected **SFO → LAX**, **2030-02-03 → 2030-02-06**, **7 passengers** and submitted
  with the Enter key. The summary showed those five values and two options. The
  first outbound was SFO 08:00 → LAX 09:00 on February 3; its return was
  LAX 16:00 → SFO 17:00 on February 6, explicitly UTC.
- Clicked **Edit search**. Both selected airports, both input dates, and
  **7 passengers** remained in the form.
- Changed the destination to **SFO** and submitted. The rendered validation summary
  and field error said to choose a different destination; the valid dates and
  passenger count remained available.
- Corrected the origin to **JFK** and resubmitted. Observed **No flights found**,
  the accurate summary, and the edit action. No fabricated cards appeared.
- Used Tab from the passenger control; Search flights received a visible focus
  outline and could be activated with Enter.
- Reviewed desktop and mobile rendering. A one-off Python Playwright rendering
  check captured 1280px desktop and 390px mobile pages. Search, populated results,
  empty results, and validation pages had no horizontal overflow at 390px.
  The exported desktop and mobile captures were visually inspected as well.

## Local evidence

Generated files are deliberately ignored by Git and are available in this working
copy, not promised as files in a fresh checkout:

- `artifacts/implementation/desktop-search.png`
- `artifacts/implementation/desktop-results.png`
- `artifacts/implementation/mobile-search.png`
- `artifacts/implementation/mobile-results.png`
- `artifacts/implementation/mobile-empty-results.png`
- `artifacts/implementation/mobile-validation.png`
- `test-results/tests-e2e-test-smoke-py-test-search-page-is-ready-chromium/trace.zip`
- `test-results/tests-e2e-test-smoke-py-test-search-page-is-ready-chromium/test-finished-1.png`

The browser UI tool's narrow full-page exports were cropped; they were discarded
and replaced by the Playwright captures listed above. Browser navigation and
observed control values were unaffected.

## Failed / blocked / not attempted

- No failing application checks or unresolved blockers in the checks above.
- Verified on **macOS arm64, CPython 3.12.9, Chromium**. Windows/Linux installation,
  Firefox, WebKit, physical mobile devices, and a full screen-reader audit were
  not tested. Narrow desktop browser rendering is not physical-device coverage.
- Failure-retention flags were accepted and successful-run trace/screenshot output
  was verified. No deliberate application defect was inserted to force a failing run.
- This baseline does not supply a persisted browser test of the full main journey.
  The learner must still observe AC-01/02/08, write that Python test, execute it,
  inspect its assertions, and manually repeat an important interaction.

The local preview server used for implementation was stopped after verification.
Nothing was published, pushed, or committed.
