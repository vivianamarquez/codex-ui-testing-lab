# Test a UI with Codex

Give Codex acceptance criteria, let it use the browser, and review the evidence.
Flight Lab is the small example app: search for a round trip, check the results,
then edit the search.

## 1. Start the app

With [uv installed](https://docs.astral.sh/uv/getting-started/installation/), run:

```sh
uv sync --locked
DEMO_TODAY=2030-01-15 uv run flask --app app run --port 5001
```

Open [Flight Lab](http://127.0.0.1:5001). The fixed date keeps our practice inputs
valid. Leave the server running while you test; stop it with Ctrl-C.

## 2. Ask Codex to test it

Read the [three main acceptance criteria](docs/acceptance-criteria.md), then send:

> Use the built-in browser at http://127.0.0.1:5001 to verify AC-01, AC-02,
> and AC-08 from docs/acceptance-criteria.md. Explicitly set ATL → JFK,
> January 22–25, 2030, and 2 passengers. Submit, compare all five summary
> values, then click Edit search and check all five form values.
> Report each criterion as passed, failed, or blocked, with the observed values
> and screenshots. Leave application code and tests unchanged.

## 3. Review the evidence

Compare Codex's report with the screenshots. Are the route, dates, and passenger
count correct on both pages? Repeat Edit search yourself. A useful report tells
you what Codex actually observed and which checks it could not complete.

That's the core exercise: **criteria → browser interaction → evidence → review**.

<details>
<summary><strong>What is Codex doing, and why does it take screenshots?</strong></summary>

Codex uses **Computer Use in the browser** to open pages, click, type, and inspect
the rendered result. You can request the built-in browser by name or with
`@Browser`. [Official browser guide](https://learn.chatgpt.com/docs/browser?surface=app#browser-use).

The working loop is: observe the page, choose an action, perform it, and inspect
what changed. In this exercise, Codex reads control labels and values and captures
screenshots of the results and edited form. Screenshots help inspect appearance
and give you visible evidence to review. They are snapshots of those states;
checking the actual values connects that evidence to the acceptance criteria.

The criteria define what “correct” means. A screenshot alone does not decide
whether the application met the requirement. Your review checks the conclusion.

</details>

<details>
<summary><strong>How does this compare with the alternatives?</strong></summary>

| Approach | Who does the work? | What you get |
| --- | --- | --- |
| Manual testing | An engineer or QA tester follows the journey and records findings. | Human exploration and judgment; someone repeats the work after changes. |
| Scripted testing | An engineer writes and maintains a Playwright test. | Repeatable assertions that can run automatically. |
| Codex browser testing | You supply criteria; Codex interacts with the app and reports evidence. | An assisted browser check that a person reviews. Codex can then help write a saved test. |

Manual testing can be done by your existing team; hiring testers is one staffing
option, not a prerequisite. Codex can reduce repetitive interaction and test-writing
work. People still define requirements, review evidence, and investigate issues.
Compare time spent and defects caught on your own project to judge the benefit.

</details>

<details>
<summary><strong>How do we reuse this and scale it up?</strong></summary>

1. **Save a stable journey as a test.** The Python test created in this session is
   `tests/e2e/test_flight_search.py`. It checks the exact summary and edited values.
   After reviewing its assertions, run it after UI changes:

   ```sh
   uv run playwright install chromium
   uv run pytest tests/e2e/test_flight_search.py
   ```

   Add `--headed` to watch it. The test starts and stops its own app server.
   To use an existing fixed-date app, add `--base-url http://127.0.0.1:5001`.
   Run `uv run pytest` for the full suite.

2. **Add journeys one at a time.** Start with important flows, then validation
   and empty results. Give each test clear criteria and repeatable input data.

3. **Run saved tests on pull requests.** A continuous integration (CI) job can
   install dependencies and browsers, run the tests, and save failure evidence.
   See the [Playwright CI guide](https://playwright.dev/python/docs/ci).
   Keep screenshots and traces with:

   ```sh
   uv run pytest --tracing retain-on-failure --screenshot only-on-failure
   ```

   Files appear in `test-results/`. Open a trace with
   `uv run playwright show-trace <path-to-trace.zip>`.

4. **Expand where it matters.** Add relevant browsers, screen sizes, and independent
   parallel runs as coverage grows. Use Codex for new or changed journeys and for
   investigating failures. Have people review confusing behavior, accessibility,
   and whether the criteria still describe the product correctly.

A saved Playwright test runs its written assertions; it does not need Codex to
reason through every run. Codex browser exploration and automated regression tests
complement each other.

</details>

## Files

- `app.py` — Flask app, validation, and synthetic flights.
- `templates/` and `static/` — pages and styling.
- `docs/acceptance-criteria.md` — expected behavior.
- `tests/e2e/test_flight_search.py` — the reusable browser journey.
- Other files in `tests/` — checks for validation, rendering, and synthetic data.
