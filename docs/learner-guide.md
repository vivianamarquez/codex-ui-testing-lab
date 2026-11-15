# Practice the workflow

The developer problem is recurring: a search UI changed, and a reviewer needs
evidence that the main journey still works. The deliverables are an observation
report and a saved Python regression test. They are separate; browser interaction
alone creates no reusable test file.

## Before asking Codex to act

Read `AGENTS.md`, the acceptance criteria, and the run commands. Inspect
`search.py`, `routes.py`, the templates, and `tests/conftest.py` until you can
explain where validation lives and how the test server starts. You need not learn
a JavaScript framework: this app has none.

Check the working tree with `git status --short` and note any existing changes.
Install requirements and Chromium, then run the baseline tests once. The browser
smoke test only confirms that a page and controls are reachable; it does not
establish that searching, summarizing, or editing works.

## Try it yourself first

Start fixed-date mode using the README command. Confirm the form says effective
today `2030-01-15`. Choose ATL → JFK, departure `2030-01-22`, return `2030-01-25`,
and **2 passengers**. Tab through the labeled controls and activate Search flights.
Compare every summary value against what you entered. Inspect one outbound and
return leg for the correct route and dates. Select Edit search and confirm all
five values, including 2 passengers, remain selected.

Then use a different route or passenger count once, so you know what a default
value accidentally replacing the submission would look like. Date controls can
use your locale's display format; stored values/results use ISO dates.

## Ask Codex to verify

In a separate practice session, paste `exercise-prompt.md`. Start with AC-01,
AC-02, and AC-08 only. Ask Codex to use actual clicks, typing, selection, and
keyboard interaction and to inspect the rendered state. Source code inspection
can explain behavior, but cannot establish that the browser journey succeeded.

Expect explicit inputs, observations for each criterion, and passed/failed/blocked
statuses. Supporting evidence could include the URL, selected form values,
observed summary values, screenshot paths, and the exact test command/output.
Evidence should identify the running app and effective date. A screenshot alone
may not show hidden select values; a test passing alone may have weak assertions.

Use `results-template.md` to review the report. “Everything works” or “the code
looks correct” without observed values is insufficient. If browser access fails,
mark browser checks blocked, record the cause, and keep HTTP results separate.
If a real issue occurs, preserve reproduction steps and evidence; do not authorize
unrequested app edits or accept weaker assertions just to obtain a green run.

## Review the generated Python test

The learner-created file should be `tests/e2e/test_flight_search.py`. Check that it:

- Uses pytest, the supplied `page` and `base_url` fixtures, and a fresh browser
  context; it can run alone without relying on the smoke test or test order.
- Explicitly enters all five agreed values. At least passenger count should differ
  from the form default. A second example with a different route is useful later.
- Locates controls with `get_by_label` and actions/headings with `get_by_role`.
  If a results value needs an anchor, use the semantic summary region and its
  labels, avoiding styling classes and positional CSS selectors.
- Asserts the results page and the exact five summary values in their visible
  context, then clicks Edit search and asserts all five control values.
- Uses Playwright `expect(...)` assertions that wait for UI state. It has no
  arbitrary sleeps, broad exception handling, or dependence on today's real date.
- Uses `@pytest.mark.browser` so `-m "not browser"` remains accurate.
- Leaves application code unchanged and is readable enough for you to maintain.

Insufficient: asserting only that the URL contains `/results`, that “Flights”
appears somewhere, that two cards exist, or that an input is visible after edit.
Those assertions can pass while the route, dates, or passenger count are wrong.
A count of options supplements exact summary checks; it does not replace them.

Run the generated file alone, then the full suite. Collect a trace if needed:

```sh
python -m pytest tests/e2e/test_flight_search.py --headed
python -m pytest tests/e2e/test_flight_search.py --tracing on --screenshot on
python -m pytest
git diff -- airline_demo tests docs
git status --short
```

`git diff` does not show the contents of untracked new files: open the generated
test directly too. Read a trace locally with `python -m playwright show-trace`
followed by its actual path. Manually repeat editing the search and confirm the
passenger count survives. Human review includes both the code and the interaction.

## Reuse and keep the demonstration bounded

Keep the reviewed test in the repository and rerun it after future UI changes.
Follow-up exercises can cover validation recovery and empty results; pair browser
constraints with server-level checks where needed. Do not expand the initial live
demonstration to every criterion or to a reservation platform.

For a later ten-minute presentation, use one minute for the problem and criteria,
three for browser verification, three for generating/running the test, two for
human review, and one for reuse. Rehearse setup beforehand. This starter is the
practice environment, not a completed presentation or a staged bug discovery.
