# Test a UI with Codex

Give Codex acceptance criteria, let it use the browser, and review the evidence.
The method works across application languages. Flight Lab is our example:
search for a round trip, check the results, then edit the search.

## Student exercise

1. Open Codex and sign in with your work account.
2. Open the [student guide](https://flight-lab-ui-workshop.vivianamarquez.chatgpt.site/workshop.html)
   and [hosted Flight Lab](https://flight-lab-ui-workshop.vivianamarquez.chatgpt.site).
3. Ask Codex to open Flight Lab in the built-in browser. Review any browser-access
   prompt. If the feature is blocked, ask your facilitator or workspace administrator.
4. Copy the [browser prompt](docs/browser-prompt.md) into your chat. It includes
   the three acceptance criteria and all five input values.
5. Compare the report and screenshots with the criteria. Try Edit search yourself.

The main exercise needs Codex and browser access. Python, uv and a local app server
are not prerequisites. The hosted demo uses January 15, 2030 as its fixed date.

The journey is **ATL → JFK, January 22–25, 2030, 2 passengers**:

| Criterion | What to verify |
| --- | --- |
| AC-01 | A valid search opens results. |
| AC-02 | The summary matches all five submitted values. |
| AC-08 | Edit search returns a form containing those same five values. |

Report **passed, failed or blocked**, with exact observed values and screenshots.
The core workflow is **criteria → browser interaction → evidence → human review**.

## Instructor closing demo

Use [instructor-demo/README.md](instructor-demo/README.md) to prepare the small
Python environment before class. At the end, ask Codex to **create** a Playwright
test from the verified journey, review its assertions, and run it against the
hosted URL. The instructor folder starts with no finished test.

Only the test code and its runtime are needed locally. The application stays
hosted; its implementation language does not determine the test language.
The existing [reference test](tests/e2e/test_flight_search.py) is a fallback.

## Why screenshots? What happens behind the scenes?

Codex observes the page, clicks or types, then inspects what changed. It can read
control labels and values and capture screenshots for visible evidence. Ask to
“use the built-in browser” or mention `@Browser`.

Screenshots document states; acceptance criteria define correctness. Review both
the observed values and the screenshots before relying on a passed result.
See the official [Browser use](https://learn.chatgpt.com/docs/browser?surface=app)
and [Computer Use](https://learn.chatgpt.com/docs/computer-use?surface=app) guides.

## How this compares and scales

A teammate can perform and document the journey manually. Codex assists with
repetitive browser interactions and reporting. People still define requirements,
review findings and investigate confusing behavior.

A saved Playwright test repeats its written assertions without an agent deciding
each action. Start with one stable journey, then add important validation and
empty-results checks. Run saved tests after changes and in continuous integration;
retain screenshots and traces for failures. Compare time, review effort and quality
with your manual baseline before expanding coverage.

## Maintainer reference

- [Acceptance criteria](docs/acceptance-criteria.md) include follow-up checks.
- `hosted-demo/dist/` contains the hosted app and student guide.
- `hosted-demo/.openai/hosting.json` identifies its Sites deployment.
- `instructor-demo/` is the standalone test-creation workspace.
- `app.py`, `templates/` and `static/` are the original local Flask example.

<details>
<summary>Run the original Python app and its tests locally</summary>

With uv installed:

```sh
uv sync --locked
DEMO_TODAY=2030-01-15 uv run flask --app app run --port 5001
```

Open http://127.0.0.1:5001. Stop the server with Ctrl-C when finished.

```sh
uv run playwright install chromium
uv run pytest
```

The browser test starts its own local app server. To run the reference journey
against the hosted demo instead:

```sh
uv run pytest tests/e2e/test_flight_search.py --base-url https://flight-lab-ui-workshop.vivianamarquez.chatgpt.site --headed
```

For failure evidence, add `--tracing retain-on-failure --screenshot only-on-failure`.
See the [Playwright CI guide](https://playwright.dev/python/docs/ci) for automation.

</details>
