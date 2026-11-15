# Copy-ready exercise prompt

Paste the following in a **new practice session** in this repository:

---

Help me practice verifying a recurring flight-search journey and turning the
observations into a reusable Python regression test.

1. Read `AGENTS.md`, `docs/acceptance-criteria.md`, and the README. Inspect the
   existing test fixtures. The acceptance criteria define expected behavior.
2. Start or locate the local application. Use fixed-date mode
   `DEMO_TODAY=2030-01-15`; confirm the displayed effective date. Identify the URL
   and whether you or I own the server. Install missing Python/browser dependencies
   if needed using the README. Keep all work local.
3. Use the browser to complete the main journey with real UI interaction:
   Atlanta (ATL) → New York (JFK), departure `2030-01-22`, return `2030-01-25`,
   **2 passengers**. Use labeled controls and include keyboard interaction.
   Submit, inspect the rendered results, then select Edit search and inspect
   every preserved value. Do not substitute HTTP requests for browser evidence.
4. Report observed behavior against **AC-01, AC-02, and AC-08** using
   `docs/results-template.md` as a structure. Separate passed, failed, and blocked
   checks. Include specific observed values, supporting evidence, and limitations.
   Do not invent findings or require a bug to make the exercise valuable.
5. After exploration, create `tests/e2e/test_flight_search.py` as a separate saved
   output. Use Python Playwright and the provided pytest fixtures. Mark it
   `browser`. Prefer accessible labels/roles, assert exact submitted values in
   the summary and edited controls, and avoid CSS paths and arbitrary sleeps.
   Make it independent of test execution order and the machine's real date.
6. Run that test and report the exact command and actual result. Then run the
   existing suite for regressions. Keep failure evidence when useful. If a test
   cannot run, state why and provide the exact command for me to run.
7. Leave application code unchanged. Do not weaken assertions to make them pass.
   If you find a real issue or ambiguous requirement, explain it with reproduction
   steps and evidence instead of silently changing product behavior. If browser
   access is unavailable, mark the observation checks blocked and clearly label
   any unverified test draft; do not claim the journey was observed.
8. Summarize the files changed, the evidence, and what I should review in the
   Python test. Ask me to manually repeat Edit search and check all values before
   accepting the result. Stop only servers that you started when finished.

This is a verification exercise, not a bug-fixing exercise. Keep the scope to
AC-01/02/08 for the main journey; list any other criteria as not attempted.
Do not push or publish anything.
