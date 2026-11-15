# Practice UI testing with Codex

Use Codex to check a UI against acceptance criteria and save the repeatable checks
as a Python regression test. This guide uses a flight-search app as the example.

The workflow produces two things: a report of what happened in the browser and a
test you can run after future changes.

## 1. Get familiar with the project

Read `AGENTS.md` and `docs/acceptance-criteria.md`. Focus on three checks:

- **AC-01:** submitting a valid search opens results.
- **AC-02:** the summary matches the submitted values.
- **AC-08:** Edit search preserves those values.

In the Python code, `search.py` validates the input, `routes.py` renders the pages,
and `tests/conftest.py` starts the app for browser tests. The templates contain the
labeled controls and result summaries.

Check existing changes, set up the environment, and run the baseline:

```sh
git status --short
uv sync --locked
uv run playwright install chromium
uv run pytest
```

The browser smoke test checks that the search page and controls are available.
The exercise adds coverage for submitting and editing a search.

## 2. Start the app

```sh
DEMO_TODAY=2030-01-15 uv run flask --app airline_demo run --port 5001
```

Open [Flight Lab](http://127.0.0.1:5001). Confirm the form shows
**Effective today: 2030-01-15**. Keep this terminal running while you practice.

## 3. Try the main journey yourself

Enter these values:

| Field | Value |
| --- | --- |
| Origin airport | Atlanta (ATL) |
| Destination airport | New York (JFK) |
| Departure date | January 22, 2030 |
| Return date | January 25, 2030 |
| Passengers | 2 |

Use Tab to move between controls and notice the focus outline. Activate
**Search flights**. On the results page:

1. Confirm there are two round-trip options.
2. Compare all five summary values with your input.
3. Inspect an option: the outbound leg should be ATL → JFK on January 22,
   and the return should be JFK → ATL on January 25.
4. Select **Edit search** and check all five form values, including 2 passengers.

Repeat with a different route or passenger count. Changing the inputs helps you
detect cases where the app might show default values instead of your choices.

## 4. Ask Codex to verify the UI

Use the [exercise prompt](exercise-prompt.md) in a separate practice session when
you are ready for Codex to verify the journey and write the test.

The browser capability is
[Computer Use in the browser](https://learn.chatgpt.com/docs/browser#browser-use).
Ask Codex to use the built-in browser, or mention `@Browser`, and provide the local
URL. It can interact with controls and inspect the rendered result.

Ask for observations against AC-01, AC-02, and AC-08. A useful report includes:

- The app URL, effective date, and submitted values.
- Expected and observed behavior for each criterion.
- Passed, failed, or blocked status, with supporting evidence.
- Screenshots or observed control values that support the findings.

Use `results-template.md` to review the report. “Everything works” is too vague:
look for specific values and actions. A screenshot may omit selected values, and
a passing test can have weak assertions. Read the evidence alongside the claim.
If a check is blocked, record the reason and what is needed to complete it.

## 5. Review the generated Python test

Ask Codex to create `tests/e2e/test_flight_search.py`. Review whether it:

- Uses the supplied `page` and `base_url` fixtures and the `browser` marker.
- Enters all five values, including a passenger count different from the default.
- Finds controls by accessible labels and actions by roles.
- Checks the exact five values in the results summary.
- Clicks Edit search and checks the exact five control values again.
- Uses Playwright assertions that wait for the expected state.
- Runs independently with the fixed demo date.

Assertions such as “the URL contains `/results`” or “the input is visible” are
useful supporting checks. They need exact value assertions to establish that
the app preserved the requested trip.

Run the generated test in another terminal:

```sh
uv run pytest tests/e2e/test_flight_search.py --headed
uv run pytest tests/e2e/test_flight_search.py --tracing on --screenshot on
uv run pytest
git diff -- tests docs
git status --short
```

Open the new test directly too: `git diff` shows tracked file changes.
Review a saved trace with `uv run playwright show-trace` followed by its path.
Manually repeat Edit search and confirm the passenger count survives.

## 6. Reuse the workflow

Keep the reviewed test and rerun it after UI changes. Extend coverage to validation
recovery and empty results as follow-up exercises.

For another application, choose a small user journey, define its acceptance
criteria, ask Codex to verify it in the browser, and review the resulting test.
